"""Gắn chủ đề cho review / chat support bằng từ khoá (miễn phí, không cần AI).

Muốn chính xác hơn: đặt ANTHROPIC_API_KEY để dùng thêm summarize_with_llm()
(Haiku, chi phí vài cent mỗi báo cáo). Không bắt buộc.
Sửa TOPICS để thêm từ khoá riêng của EComposer.
"""
from __future__ import annotations

import os
import re
from collections import Counter

import pandas as pd

TOPICS = {
    "Bug / lỗi hiển thị": ["bug", "broken", "break", "not working", "doesn't work", "error", "glitch",
                          "crash", "lỗi", "không hoạt động", "vỡ", "messed up", "disappeared"],
    "Tốc độ / page speed": ["slow", "speed", "lag", "loading", "pagespeed", "performance", "chậm"],
    "Giá / billing / refund": ["price", "pricing", "expensive", "charge", "charged", "refund", "billing",
                               "subscription", "cancel", "money", "đắt", "hoàn tiền", "trừ tiền"],
    "Support chậm / kém": ["no response", "didn't respond", "waiting", "slow support", "rude",
                          "poor customer service", "ignored", "không trả lời"],
    "Support tốt": ["great support", "amazing support", "helpful", "quick response", "fast support",
                    "thank", "support team"],
    "Khó dùng / learning curve": ["confusing", "hard to use", "difficult", "complicated", "learning curve",
                                  "khó dùng", "not intuitive"],
    "Xung đột theme / app khác": ["theme", "conflict", "compatible", "dawn", "horizon", "other app",
                                  "xung đột"],
    "Thiếu tính năng": ["missing", "feature request", "wish", "would be nice", "can't", "cannot",
                        "no option", "thiếu"],
    "Mobile / responsive": ["mobile", "responsive", "tablet", "điện thoại"],
    "SEO / mất dữ liệu khi gỡ": ["seo", "after uninstall", "leftover", "code left", "uninstall",
                                 "removed the app", "gỡ"],
    "AI / template": ["ai ", "template", "generate", "chatgpt"],
}

COMPETITORS = ["pagefly", "gempages", "shogun", "replo", "instant", "zipify", "layouthub",
               "foxify", "sidekick", "horizon", "theme blocks"]


def tag(text: str) -> list[str]:
    t = f" {str(text).lower()} "
    return [name for name, kws in TOPICS.items() if any(k in t for k in kws)]


def competitor_mentions(texts) -> Counter:
    c = Counter()
    for t in texts:
        low = str(t).lower()
        for name in COMPETITORS:
            if re.search(rf"\b{re.escape(name)}\b", low):
                c[name] += 1
    return c


def topic_counts(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["topic", "count"])
    c = Counter(t for x in df[text_col] for t in tag(x))
    return pd.DataFrame(c.most_common(), columns=["topic", "count"])


def sample_quotes(df: pd.DataFrame, topic: str, n: int = 3, text_col: str = "text") -> list[str]:
    hits = df[df[text_col].map(lambda x: topic in tag(x))]
    return [str(x)[:220] for x in hits[text_col].head(n)]


def summarize_with_llm(texts: list[str], question: str) -> str | None:
    """Tuỳ chọn: tóm tắt bằng Claude nếu có ANTHROPIC_API_KEY."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key or not texts:
        return None
    import requests

    joined = "\n---\n".join(t[:600] for t in texts[:150])
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
        json={
            "model": os.getenv("CLAUDE_MODEL", "claude-haiku-5-5"),
            "max_tokens": 1200,
            "messages": [{"role": "user", "content": f"{question}\n\nDữ liệu:\n{joined}"}],
        },
        timeout=120,
    )
    if not r.ok:
        return f"(Không gọi được Claude API: {r.status_code})"
    return r.json()["content"][0]["text"]
