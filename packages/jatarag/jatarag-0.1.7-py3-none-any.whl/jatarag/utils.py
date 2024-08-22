from __future__ import annotations

import traceback
import pdb
import openai
import os
from typing import Generator


def set_openai_key(api_key: str | None = None):
    # check that an api key was given, and set it
    if api_key is None:
        api_key = os.environ.get('OPENAI_API_KEY', None)
    if not api_key:
        raise Exception(
            "No OpenAI API key given. Please set the OPENAI_API_KEY environment variable or pass the api_key argument to set_openai_key()")
    openai.api_key = api_key


class OpenAIUtils:
    @staticmethod
    def set_openai_key(api_key: str | None = None):
        set_openai_key(api_key)


def strip_quotes(s: str) -> str:
    """strip quotes wrapping a string, if any"""
    while len(s) > 1 and s[0] == s[-1] and s[0] in ['"', "'", '`']:
        s = s[1:-1]
    return s


# TODO: consider making more generic, e.g. pass in f=lambda s: print(s, end='', flush=True)
def print_while_streaming(gen: Generator[str, None, None], end='\n') -> Generator[str, None, None]:
    for res in gen:
        print(res, end='', flush=True)
        yield res
    print(end=end)


def pdb_excepthook(type, value, tb):
    """
    Custom exception hook to start pdb debugger at the location of the exception.

    To use:
    ```
    import sys
    from jatarag.utils import pdb_excepthook
    sys.excepthook = pdb_excepthook
    ```
    """
    # Print the exception details
    traceback.print_exception(type, value, tb)
    # Start the debugger at the point of exception
    pdb.post_mortem(tb)
