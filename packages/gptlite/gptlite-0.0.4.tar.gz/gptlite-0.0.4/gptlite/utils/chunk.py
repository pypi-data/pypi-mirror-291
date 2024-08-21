from typing import Union


def to_console(chunk: Union[str, dict]) -> None:
    if isinstance(chunk, dict):
        print(chunk)
    else:
        print(chunk, end="", flush=True)


def to_file(chunk: Union[str, dict]) -> None:
    pass


def to_null(chunk: Union[str, dict]) -> None:
    pass
