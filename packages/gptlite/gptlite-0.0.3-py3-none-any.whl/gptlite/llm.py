import json
from typing import Any, Callable, Dict, List, Literal, Optional, Union

from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_function
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionToolParam,
)  # CompletionCreateParams,

_ON_FC_DictType = Dict[
    Literal["meta", "params", "result"],
    Union[
        Callable[[dict], None], Callable[[str], None], Callable[[str], None]
    ],
]


class LLM:
    def __init__(
        self,
        api_key,
        base_url: Optional[str] = None,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_fc: Optional[_ON_FC_DictType] = None,
    ) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.on_chunk = on_chunk if on_chunk else self._do_nothing
        self.on_fc = on_fc if on_fc else {}
        self.on_fc["meta"] = self.on_fc.get("meta", self._do_nothing)
        self.on_fc["params"] = self.on_fc.get("params", self._do_nothing)
        self.on_fc["result"] = self.on_fc.get("result", self._do_nothing)

    def chat(self, tools: Optional[list[BaseTool]] = None, **params):
        tools_json: List[ChatCompletionToolParam] = []
        for tool in tools or []:
            function: Any = convert_to_openai_function(tool)
            json = ChatCompletionToolParam(type="function", function=function)
            tools_json.append(json)
        stream = self._call_llm(**params, tools=tools_json)

        new_messages = []
        content = ""
        for type, chunk in stream:
            if type == "content":
                content += chunk
            elif type == "tool_calls":
                tool_calls = chunk
                message = {"role": "assistant", "tool_calls": tool_calls}
                new_messages.append(message)
                yield message

                results = self._exec_tool_calls(
                    tool_calls=tool_calls, tools=tools
                )
                for result in results:
                    new_messages.append(result)
                    yield result

                new_params = params.copy()
                new_params["messages"] = []
                for message in params["messages"]:
                    new_params["messages"].append(message)
                for message in new_messages:
                    new_params["messages"].append(message)
                summary_messages = self.chat(**new_params, tools=tools)
                for message in summary_messages:
                    new_messages.append(message)
                    yield message

        if content != "":
            message = {"role": "assistant", "content": content}
            new_messages.append(message)
            yield message

    def _exec_tool_calls(self, tool_calls, tools):
        for tool_call in tool_calls:
            if tool_call.type == "function":
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments
                tool = next(
                    filter(lambda tool: tool.name == function_name, tools),
                    None,
                )
                try:
                    params = json.loads(function_args)
                    result = tool.run(params)
                    # TODO: add support for multiple result types: string, file, json
                    content = json.dumps(result)
                    self.on_fc["result"](content)
                    yield {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": content,
                    }
                except Exception as e:
                    self.on_fc["result"](str(e))
                    yield {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(e),
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
                    for tool_call in tool_calls:
                        meta = {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "name": tool_call.function.name,
                        }
                        self.on_fc["meta"](meta)
                        self.on_fc["params"](tool_call.function.arguments)
                    yield "tool_calls", tool_calls
                else:
                    self.on_chunk(choice.message.content)
                    yield "content", choice.message.content

        completions = self.client.chat.completions.create(**params)
        return generator(completions)

    def _append_stream_delta_tool_calls(self, delta_tool_calls, tool_calls):
        for i, delta_tool_call in enumerate(delta_tool_calls):
            if len(tool_calls) <= i:
                tool_calls.append(delta_tool_call)
            if delta_tool_call.function.name is not None:
                tool_calls[i].function.name = delta_tool_call.function.name
                tool_calls[i].id = delta_tool_call.id
                tool_calls[i].type = delta_tool_call.type
                fc_meta = {
                    "id": tool_calls[i].id,
                    "type": tool_calls[i].type,
                    "name": tool_calls[i].function.name,
                }
                self.on_fc["meta"](fc_meta)
            tool_calls[
                i
            ].function.arguments += delta_tool_call.function.arguments
            self.on_fc["params"](delta_tool_call.function.arguments)

    def _do_nothing(self, _: str):
        pass
