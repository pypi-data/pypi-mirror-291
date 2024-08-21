import json
from typing import Any, Callable, Dict, List, Literal, Optional, Union

from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_function
from openai import OpenAI
from pydantic import BaseModel

from .store import Files
from .utils import chunk as ChunkUtils

_MAX_ITER = 3


_ON_FC_DictType = Dict[
    Literal["meta", "params", "result"],
    Union[
        Callable[[dict], None], Callable[[str], None], Callable[[str], None]
    ],
]


class ToolResult(BaseModel):
    type: Literal["string", "json", "bytes"]
    data: Any  # When the type is `file`, data should be in bytes


class LLM:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        support_tools: Optional[bool] = False,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_fc: Optional[_ON_FC_DictType] = None,
    ) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.support_tools = support_tools
        self.on_chunk = on_chunk if on_chunk else ChunkUtils.to_console
        self.on_fc = on_fc if on_fc else {}
        self.on_fc["meta"] = self.on_fc.get("meta", ChunkUtils.to_null)
        self.on_fc["params"] = self.on_fc.get("params", ChunkUtils.to_null)
        self.on_fc["result"] = self.on_fc.get("result", ChunkUtils.to_null)

    def chat(
        self,
        tools: Optional[List[BaseTool]] = None,
        iter: Optional[int] = 0,
        **params,
    ):
        iter = iter or 0
        if iter > _MAX_ITER + 1:
            raise Exception("Maximum number of iterations reached")

        if self.support_tools and tools is not None:
            functions = []
            for tool in tools:
                function = convert_to_openai_function(tool)
                functions.append({"type": "function", "function": function})
            stream = self._call_llm(**params, tools=functions)
        else:
            stream = self._call_llm(**params)

        new_messages = []
        content = ""
        for type, chunk in stream:
            if type == "content":
                content += chunk
            elif type == "tool_calls":
                tool_calls = chunk
                # NOTE: "content": "" is necessary for qwen models
                message = {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": tool_calls,
                }
                new_messages.append(message)
                yield message

                results = self._exec_tool_calls(
                    tool_calls=tool_calls, tools=tools
                )
                for result in results:
                    new_messages.append(result)
                    yield result

                if new_messages[-1].get("role") != "assistant":
                    new_params = params.copy()
                    new_params["messages"] = []
                    for message in params["messages"]:
                        new_params["messages"].append(message)
                    for message in new_messages:
                        new_params["messages"].append(message)
                    summary_messages = self.chat(
                        **new_params, iter=iter + 1, tools=tools
                    )
                    for message in summary_messages:
                        new_messages.append(message)
                        yield message
                else:
                    yield new_messages[-1]

        if content != "":
            message = {"role": "assistant", "content": content}
            new_messages.append(message)
            yield message

    def _exec_tool_calls(self, tool_calls, tools):
        for tool_call in tool_calls:
            if tool_call["type"] == "function":
                function_name = tool_call["function"]["name"]
                function_args = tool_call["function"]["arguments"]
                tool = next(
                    filter(lambda tool: tool.name == function_name, tools),
                    None,
                )
                try:
                    content = ""
                    params = json.loads(function_args)

                    result = tool.run(params)

                    if result.type == "string":
                        content = result.data
                    elif result.type == "json":
                        content = json.dumps(result.data, ensure_ascii=False)
                    elif result.type == "bytes":
                        info = Files.create(
                            f"{tool.name}", result.data, "tool_call"
                        )
                        obj = {
                            "file": info.__dict__,
                            "message": f"You may access the file with `id`: {info.id}",
                        }
                        content = json.dumps(obj, ensure_ascii=False)

                    self.on_fc["result"](content)
                    yield {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": content,
                    }
                except Exception as e:
                    content = f"工具[{function_name}]调用出错，停止继续调用工具。以下是出错情况：\n{'='*10}\n{str(e)}\n{'='*10}"
                    self.on_fc["result"](str(e))
                    self.on_chunk(content)
                    yield {
                        "role": "assistant",
                        "content": content,
                    }

    def _call_llm(self, **params):
        def generator(completions):
            tool_calls = []
            if "stream" in params and params["stream"]:
                for chunk in completions:
                    choice = chunk.choices[0]
                    if choice.delta.tool_calls is not None:
                        self._append_stream_delta_tool_calls(
                            choice.delta.tool_calls, tool_calls
                        )
                        # NOTE: it is a fix for Yi-Large-FC model
                        #       other models will generate a chunk with tool_calls=None in the last message
                        if choice.finish_reason == "tool_calls":
                            yield "tool_calls", tool_calls
                            return
                    elif choice.finish_reason == "tool_calls":
                        yield "tool_calls", tool_calls
                    else:
                        if choice.delta.content is not None:
                            self.on_chunk(choice.delta.content)
                            yield "content", choice.delta.content
            else:
                choice = completions.choices[0]
                if choice.finish_reason == "tool_calls":
                    tool_calls = choice.message.tool_calls
                    converted = []
                    for tool_call in tool_calls:
                        meta = {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "name": tool_call.function.name,
                        }
                        self.on_fc["meta"](meta)
                        self.on_fc["params"](tool_call.function.arguments)
                        item = {
                            "function": {
                                "arguments": tool_call.function.arguments
                            }
                        }
                        self._tool_call_to_dict(tool_call, item)
                        converted.append(item)
                    yield "tool_calls", converted
                else:
                    self.on_chunk(choice.message.content)
                    yield "content", choice.message.content

        completions = self.client.chat.completions.create(**params)
        return generator(completions)

    def _append_stream_delta_tool_calls(self, delta_tool_calls, tool_calls):
        for i, delta_tool_call in enumerate(delta_tool_calls):
            if len(tool_calls) <= i:
                tool_calls.append({"function": {"arguments": ""}})

            if delta_tool_call.function.name is not None:
                self._tool_call_to_dict(delta_tool_call, tool_calls[i])
                fc_meta = {
                    "id": tool_calls[i]["id"],
                    "type": tool_calls[i]["type"],
                    "name": tool_calls[i]["function"]["name"],
                }
                self.on_fc["meta"](fc_meta)
            tool_calls[i]["function"][
                "arguments"
            ] += delta_tool_call.function.arguments
            self.on_fc["params"](delta_tool_call.function.arguments)

    def _tool_call_to_dict(self, tool_call, d):
        d["function"]["name"] = tool_call.function.name
        d["id"] = tool_call.id
        d["type"] = tool_call.type
