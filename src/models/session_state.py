"""Mutable session context, passed to every command.

Uniform command signature: run(state, args). Dataclass fields (not dict keys)
keep state changes reviewable. Data-only: no methods, no extra services; every
field has one owner and one reason to exist.
"""

from dataclasses import dataclass

from openai import OpenAI


@dataclass
class SessionState:
    model: str
    client: OpenAI
    tools: dict
    messages: list
