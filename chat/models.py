from typing import TypedDict, Literal


class GptMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str
