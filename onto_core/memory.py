from __future__ import annotations
from pathlib import Path
import json
import time
from typing import Any, Dict, List

DATA_DIR = Path(__file__).parent / "data"
MEMORY_FILE = DATA_DIR / "memory.json"

def _ensure_store() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text(json.dumps({"users": {}}, ensure_ascii=False, indent=2), encoding="utf-8")

def _load() -> Dict[str, Any]:
    _ensure_store()
    return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))

def _save(store: Dict[str, Any]) -> None:
    _ensure_store()
    MEMORY_FILE.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")

def append_message(user_id: str, role: str, content: str) -> None:
    store = _load()
    users = store.setdefault("users", {})
    u = users.setdefault(user_id, {"history": []})
    u["history"].append({"ts": int(time.time()), "role": role, "content": content})
    u["history"] = u["history"][-80:]  # garde un peu plus
    _save(store)

def get_recent_history(user_id: str, max_items: int = 12) -> List[Dict[str, str]]:
    store = _load()
    u = store.get("users", {}).get(user_id)
    if not u:
        return []
    hist = u.get("history", [])[-max_items:]
    return [{"role": m["role"], "content": m["content"]} for m in hist if "role" in m and "content" in m]
