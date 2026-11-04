"""Chạy:  python -m churn_toolkit --period daily|weekly [--demo] [--events-csv file.csv]

Nguồn nào chưa cấu hình (thiếu biến môi trường) sẽ tự bỏ qua.
"""
from __future__ import annotations

import argparse
import os
import sys
import traceback
from pathlib import Path

import pandas as pd

from . import notify, report


def _try(name, fn):
    try:
        return fn()
    except KeyError as e:
        print(f"[{name}] bỏ qua: thiếu biến môi trường {e}", file=sys.stderr)
    except Exception:  # noqa: BLE001 - một nguồn lỗi không làm hỏng cả báo cáo
        print(f"[{name}] lỗi:\n{traceback.format_exc()}", file=sys.stderr)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--period", choices=["daily", "weekly"], default="daily")
    ap.add_argument("--demo", action="store_true", help="dùng dữ liệu giả lập")
    ap.add_argument("--events-csv", help="CSV event export từ Partner Dashboard / Ranksy")
    ap.add_argument("--no-reviews", action="store_true")
    ap.add_argument("--out", default="reports")
    args = ap.parse_args()

    now = pd.Timestamp.now(tz="UTC")
    data = Path("data")
    data.mkdir(exist_ok=True)

    if args.demo:
        from .demo_data import make_events
        ev = make_events(now)
    elif args.events_csv:
        from .sources.partner_api import load_events_csv
        ev = load_events_csv(args.events_csv)
    else:
        from .sources.partner_api import fetch_events
        ev = _try("partner_api", lambda: fetch_events(days=int(os.getenv("LOOKBACK_DAYS", "120"))))
    if ev is None or ev.empty:
        sys.exit("Không có dữ liệu event. Cấu hình Partner API, dùng --events-csv, hoặc --demo.")

    reviews = chats = None
    if not args.demo and not args.no_reviews:
        from .sources import shopify_reviews
        reviews = _try("reviews", lambda: shopify_reviews.fetch_all(pages=3 if args.period == "daily" else 10))
        if reviews is not None and not reviews.empty:
            reviews.to_csv(data / "reviews_latest.csv", index=False)
    if not args.demo:
        from .sources import crisp
        chats = _try("crisp", lambda: crisp.fetch_conversations(days=1 if args.period == "daily" else 7))

    md = report.build(ev, now, args.period, reviews=reviews, chats=chats, demo=args.demo)
    out = Path(args.out) / args.period
    out.mkdir(parents=True, exist_ok=True)
    name = f"{now.date()}{'-demo' if args.demo else ''}.md"
    (out / name).write_text(md, encoding="utf-8")
    print(f"Đã ghi {out / name}")

    repo, server = os.getenv("GITHUB_REPOSITORY"), os.getenv("GITHUB_SERVER_URL", "https://github.com")
    ref = os.getenv("GITHUB_REF_NAME", "main")
    link = f"{server}/{repo}/blob/{ref}/{out / name}" if repo else None
    if not args.demo:
        notify.send(md, link)


if __name__ == "__main__":
    main()
