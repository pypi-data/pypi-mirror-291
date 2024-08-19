from typing import Dict, List, Optional

from langchain_core.tools import BaseTool
from yaml import safe_load


class GPT:
    trigger: str
    desc: Optional[str] = None
    prompt: str
    single: Optional[bool] = False
    tools: Optional[List[BaseTool]] = []

    _TOOLS_REPO: Dict[str, BaseTool] = {}

    @staticmethod
    def set_tools(tools: List[BaseTool]):
        for tool in tools:
            GPT._TOOLS_REPO[tool.name] = tool

    def __init__(self, yaml_file: str):
        gpt = safe_load(open(yaml_file, "r"))
        assert gpt is not None, f"{yaml_file} is not a valid yaml file"
        assert (
            "trigger" in gpt
        ), f"{yaml_file} is not a valid yaml file: [gpt should have a trigger]"

        self.trigger = gpt.get("trigger", None)
        self.desc = gpt.get("desc", "")
        self.prompt = gpt.get("prompt", "You are a helpful assistant.")
        self.single = gpt.get("single", False)
        names = gpt.get("tools", None)
        self.tools = []
        for name in names:
            tool = GPT._TOOLS_REPO.get(name, None)
            if tool:
                self.tools.append(tool)
