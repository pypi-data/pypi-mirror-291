from gptlite.gpt import GPT
from langchain_core.tools import tool


@tool
def dummy():
    """dummy"""
    pass


@tool
def dummy2():
    """dummy2"""
    pass


def test_load_gpt():
    gpt = GPT.from_yaml("./tests/data/gpt.yaml", [dummy, dummy2])
    assert gpt.name == "trigger_name"
    assert gpt.desc == "description"
    assert gpt.single == False
    assert gpt.prompt == "prompt line #1\nprompt line #2\n"
    assert gpt.tools == [dummy, dummy2]
