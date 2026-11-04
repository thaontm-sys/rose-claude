"""Crisp: đọc các cuộc hội thoại support gần đây.

Cách lấy token (miễn phí):
  1. Vào https://marketplace.crisp.chat -> tạo plugin (loại Private).
  2. Tab "Tokens" -> xin "Production token" với scope:
       website:conversation:sessions (read)
       website:conversation:messages (read)
  3. Cài plugin đó vào website EComposer.
  Đặt CRISP_IDENTIFIER, CRISP_KEY, CRISP_WEBSITE_ID
  (website id = 9d122c0c-3e42-43d8-b923-e6fca52afef8).
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests

BASE = "https://api.crisp.chat/v1"


def _session() -> requests.Session:
    s = requests.Session()
    s.auth = (os.environ["CRISP_IDENTIFIER"], os.environ["CRISP_KEY"])
    s.headers["X-Crisp-Tier"] = "plugin"
    return s


def fetch_conversations(days: int = 7, max_pages: int = 50) -> pd.DataFrame:
    """Trả về 1 dòng / conversation, kèm toàn bộ tin nhắn của khách ghép lại."""
    wid = os.environ["CRISP_WEBSITE_ID"]
    s = _session()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    rows = []
    for page in range(1, max_pages + 1):
        r = s.get(f"{BASE}/website/{wid}/conversations/{page}", timeout=60)
        r.raise_for_status()
        convs = r.json().get("data", [])
        if not convs:
            break
        stop = False
        for c in convs:
            updated = datetime.fromtimestamp(c["updated_at"] / 1000, timezone.utc)
            if updated < since:
                stop = True
                continue
            m = s.get(
                f"{BASE}/website/{wid}/conversation/{c['session_id']}/messages",
                timeout=60,
            )
            msgs = m.json().get("data", []) if m.ok else []
            user_text = " \n".join(
                str(x.get("content"))
                for x in msgs
                if x.get("from") == "user" and x.get("type") == "text"
            )
            rows.append(
                {
                    "session_id": c["session_id"],
                    "created_at": datetime.fromtimestamp(c["created_at"] / 1000, timezone.utc),
                    "updated_at": updated,
                    "state": c.get("state"),
                    "segments": ",".join(c.get("meta", {}).get("segments", []) or []),
                    "email": c.get("meta", {}).get("email"),
                    "text": user_text,
                }
            )
            time.sleep(0.2)
        if stop:
            break
    return pd.DataFrame(rows)
