from __future__ import annotations

from typing import Generator, Literal
from enum import Enum
from abc import ABC, abstractmethod
from openai import OpenAI

from .utils import OpenAIUtils


class Role(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"


class Text(dict):
    def __init__(self, message: str):
        super().__init__(type="text", text=message)


class Image(dict):
    def __init__(self, web_image_base64: str, ext: str = 'png', detail='auto'):
        super().__init__(type="image_url", image_url={
            "url": f"data:image/{ext};base64,{web_image_base64}", "detail": detail})


class Message(dict):
    def __init__(self, role: Role, content: str | list[Text | Image]):
        if isinstance(content, str):
            content = [Text(content)]
        super().__init__(role=role.value, content=content)


class Agent(ABC):
    @abstractmethod
    def multishot_streaming(self, messages: list[Message], **kwargs) -> Generator[str, None, None]: ...

    def multishot_sync(self, messages: list[Message], **kwargs) -> str:
        gen = self.multishot_streaming(messages, **kwargs)
        return ''.join([*gen])

    def oneshot_streaming(self, prompt: str, query: str, **kwargs) -> Generator[str, None, None]:
        return self.multishot_streaming([
            Message(role=Role.system, content=prompt),
            Message(role=Role.user, content=query)
        ], **kwargs)

    def oneshot_sync(self, prompt: str, query: str, **kwargs) -> str:
        return self.multishot_sync([
            Message(role=Role.system, content=prompt),
            Message(role=Role.user, content=query)
        ], **kwargs)


class OpenAIAgent(Agent, OpenAIUtils):
    def __init__(self, model: Literal['gpt-4o', 'gpt-4', 'gpt-4-turbo-preview', 'gpt-4-vision-preview'], timeout=None):
        self.model = model
        self.timeout = timeout

    def multishot_streaming(self, messages: list[Message], **kwargs) -> Generator[str, None, None]:
        client = OpenAI()
        gen = client.chat.completions.create(
            model=self.model,
            messages=messages,
            timeout=self.timeout,
            stream=True,
            temperature=0.0,
            **kwargs
        )
        for chunk in gen:
            try:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
            except:
                pass
