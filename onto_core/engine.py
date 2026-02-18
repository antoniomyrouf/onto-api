# onto_core/engine.py
from __future__ import annotations
import os
import hashlib
from typing import Optional, List, Dict

from openai import OpenAI
from .prompts import ONTO_SYSTEM_PROMPT
from .memory import get_recent_history, append_message

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def prompt_hash() -> str:
    return hashlib.sha256(ONTO_SYSTEM_PROMPT.encode("utf-8")).hexdigest()[:12]

def is_pro(access_key: Optional[str]) -> bool:
    pro_key = os.getenv("ONTO_PRO_KEY", "")
    return bool(pro_key) and bool(access_key) and access_key == pro_key

def onto_reply(user_text: str, user_id: str = "public", pro_key: Optional[str] = None) -> str:
    # conformité test
    if user_text == "PING":
        return "PONG-ONTO-OK"

    messages: List[Dict[str, str]] = []
    # mémoire uniquement si pro
    if is_pro(pro_key):
        messages.extend(get_recent_history(user_id))

    # Ajoute message user
    messages.append({"role": "user", "content": user_text})

    resp = client.responses.create(
        model="gpt-4.1",
        instructions=ONTO_SYSTEM_PROMPT,
        input=messages,
    )

    out = resp.output_text

    # Écrit mémoire si pro
    if is_pro(pro_key):
        append_message(user_id, "user", user_text)
        append_message(user_id, "assistant", out)

    return out
