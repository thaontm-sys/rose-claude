"""Ranksy API (v1, chỉ đọc): churn, installs, trial conversion, MRR, review, đối thủ.

Tài liệu: https://api.ranksyapp.com  ·  Base URL: https://ranksyapp.com/api/v1

Lấy key: Ranksy > Settings > API Keys > Create key (chỉ owner của team tạo được).
Nên chọn Custom scopes chỉ-đọc: apps:read, metrics:read, reviews:read,
competitors:read, catalog:read, traffic:read.

Đặt biến môi trường RANKSY_API_KEY (GitHub Secrets hoặc máy cá nhân).
Trong phiên Claude cloud, key được proxy tự gắn vào request nên không cần biến này.
"""
from __future__ import annotations

import os
import time

import requests

BASE = "https://ranksyapp.com/api/v1"


class RanksyError(RuntimeError):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(f"{status} {code}: {message}")
        self.status, self.code = status, code


class Ranksy:
    def __init__(self, key: str | None = None):
        # Giá trị giữ chỗ chỉ để có header; proxy của phiên cloud sẽ thay bằng key thật.
        key = key or os.getenv("RANKSY_API_KEY") or "rk_live_placeholder"
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Bearer {key}", "Accept": "application/json"})
        self.calls = 0  # mỗi GET tính vào quota tháng của gói Ranksy

    def get(self, path: str, **params) -> dict:
        params = {k: v for k, v in params.items() if v is not None}
        for attempt in range(4):
            r = self.s.get(f"{BASE}{path}", params=params, timeout=60)
            self.calls += 1
            if r.status_code == 429 and r.headers.get("Retry-After") and attempt < 3:
                time.sleep(min(int(float(r.headers["Retry-After"])) + 1, 65))
                continue
            break
        if not r.ok:
            try:
                err = r.json().get("error", r.json())
            except ValueError:
                err = {}
            raise RanksyError(r.status_code, str(err.get("code", "http_error")),
                              str(err.get("message", r.text[:200])))
        return r.json()

    def pages(self, path: str, max_pages: int = 30, **params) -> list[dict]:
        """Gom mọi trang của một endpoint dạng list (page/has_more hoặc cursor)."""
        rows, page, cursor = [], 1, None
        for _ in range(max_pages):
            q = dict(params, cursor=cursor) if cursor else dict(params, page=page)
            body = self.get(path, **q)
            env = body["data"] if isinstance(body.get("data"), dict) else body
            rows.extend(env.get("data") or [])
            cursor = env.get("next_cursor")
            if not (env.get("has_more") or cursor):
                break
            page += 1
        return rows

    def find_app(self, name: str = "ecomposer") -> dict:
        apps = self.pages("/apps", per_page=200)
        hits = [a for a in apps if name.lower() in str(a.get("name", "")).lower()]
        if not hits:
            raise RanksyError(404, "app_not_found",
                              f"Không thấy app chứa '{name}'. Có: {[a.get('name') for a in apps]}")
        return hits[0]
