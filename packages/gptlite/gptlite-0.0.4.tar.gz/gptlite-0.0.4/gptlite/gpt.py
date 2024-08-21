from typing import List, Optional

from langchain_core.tools import BaseTool
from yaml import safe_load

from .llm import LLM


class GPT:
    name: str
    desc: Optional[str] = None
    prompt: str
    single: Optional[bool] = False
    tools: Optional[List[BaseTool]] = []

    def __init__(
        self,
        name: str,
        desc: Optional[str] = None,
        prompt: Optional[str] = None,
        single: Optional[bool] = None,
        tools: Optional[List[BaseTool]] = None,
    ):
        self.name = name
        self.desc = desc or ""
        self.prompt = prompt or "You are a helpful assistant."
        self.single = single or False
        self.tools = tools or None

    @staticmethod
    def from_yaml(yaml_file: str, tool_repo: Optional[List[BaseTool]] = []):
        gpt = safe_load(open(yaml_file, "r"))

        assert gpt is not None, f"{yaml_file} : not a valid yaml file"
        assert "name" in gpt, f"{yaml_file} : [gpt should have a valid name]"

        names = gpt.get("tools", [])
        tools = [tool for tool in (tool_repo or []) if tool.name in names]
        gpt["tools"] = tools

        return GPT(**gpt)

    def chat(self, llm: LLM, messages: list, **params):
        assert (
            messages is not None and len(messages) > 0
        ), "gptlite.GPT.chat() : messages should be None or empty"

        if messages[0]["role"] != "system":
            messages.insert(0, {"role": "system", "content": self.prompt})

        yield from llm.chat(tools=self.tools, messages=messages, **params)
