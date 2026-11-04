"""Gửi báo cáo qua Slack / Telegram / Discord (tuỳ chọn, đều miễn phí)."""
from __future__ import annotations

import os

import requests


def send(markdown: str, link: str | None = None) -> None:
    head = markdown[:3500] + ("\n…" if len(markdown) > 3500 else "")
    if link:
        head += f"\n\nBản đầy đủ: {link}"
    if url := os.getenv("SLACK_WEBHOOK_URL"):
        requests.post(url, json={"text": head}, timeout=30)
    if url := os.getenv("DISCORD_WEBHOOK_URL"):
        requests.post(url, json={"content": head[:1900]}, timeout=30)
    tok, chat = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if tok and chat:
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",
                      json={"chat_id": chat, "text": head}, timeout=30)
