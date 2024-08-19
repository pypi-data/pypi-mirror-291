from gptlite.gpt import GPT


def test_load_gpt():
    GPT.set_tools([dummy, dummy2])

    gpt = GPT("./tests/data/gpt.yaml")
    assert gpt.trigger == "trigger_name"
    assert gpt.desc == "description"
    assert gpt.single == False
    assert gpt.prompt == "prompt line #1\nprompt line #2\n"
    assert gpt.tools == [dummy, dummy2]


from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field


class Arguments(BaseModel):
    x: int = Field(description="dummy property")


@tool
def dummy(data: Arguments) -> str:
    """dummy tool"""
    return ""


@tool
def dummy2() -> str:
    "dummy 2 tool"
    return ""
