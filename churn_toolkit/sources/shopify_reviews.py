"""Thu thập review công khai trên Shopify App Store (EComposer + đối thủ).

Không cần token. Chạy chậm (1 trang / 2 giây) để lịch sự với Shopify.
Nếu Shopify đổi HTML, chỉ cần sửa các selector trong _parse().
"""
from __future__ import annotations

import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

APPS = {
    "ecomposer": "EComposer",
    "pagefly": "PageFly",
    "gempages": "GemPages",
    "shogun": "Shogun",
    "replo": "Replo",
    "instant": "Instant",
}

UA = {"User-Agent": "Mozilla/5.0 (churn-toolkit; review research)"}


def _parse(html: str, app: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for card in soup.select("[data-review-content-id]"):
        rating_el = card.select_one("[aria-label*='out of 5']")
        rating = None
        if rating_el:
            m = re.search(r"(\d)\s*out of 5", rating_el["aria-label"])
            rating = int(m.group(1)) if m else None
        text_el = card.select_one("[data-truncate-content-copy]") or card.select_one("p")
        date_el = card.find(string=re.compile(r"\b(January|February|March|April|May|June|July|"
                                              r"August|September|October|November|December)\s+\d{1,2},\s+\d{4}"))
        # Tên shop và quốc gia nằm ở cột bên cạnh; lấy thô nếu có
        meta = [t.get_text(" ", strip=True) for t in card.select("span, div") if t.get_text(strip=True)]
        usage = next((x for x in meta if "using the app" in x), None)
        out.append(
            {
                "app": app,
                "review_id": card["data-review-content-id"],
                "rating": rating,
                "date": date_el.strip() if date_el else None,
                "usage_time": usage,
                "text": text_el.get_text(" ", strip=True) if text_el else "",
            }
        )
    return out


def fetch_reviews(app: str = "ecomposer", pages: int = 5, ratings: str | None = None) -> pd.DataFrame:
    """ratings: ví dụ "1,2,3" để chỉ lấy review xấu (thường chứa lý do churn)."""
    rows = []
    for p in range(1, pages + 1):
        params = {"page": p, "sort_by": "newest"}
        if ratings:
            params["ratings[]"] = ratings.split(",")
        r = requests.get(f"https://apps.shopify.com/{app}/reviews", params=params, headers=UA, timeout=60)
        if r.status_code != 200:
            break
        batch = _parse(r.text, app)
        if not batch:
            break
        rows.extend(batch)
        time.sleep(2)
    df = pd.DataFrame(rows)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%B %d, %Y")
    return df


def fetch_all(pages: int = 3) -> pd.DataFrame:
    frames = [fetch_reviews(slug, pages) for slug in APPS]
    frames += [fetch_reviews(slug, pages, ratings="1,2,3") for slug in APPS]
    df = pd.concat([f for f in frames if not f.empty], ignore_index=True) if frames else pd.DataFrame()
    return df.drop_duplicates("review_id") if not df.empty else df
