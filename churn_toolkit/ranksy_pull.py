"""Kéo dữ liệu churn từ Ranksy về data/ranksy/*.json (thư mục này không commit).

Chạy:  python -m churn_toolkit.ranksy_pull --app ecomposer --since 2026-01-01

Mỗi endpoint lỗi (thiếu scope, chưa kết nối BigQuery...) được ghi lại và bỏ qua,
không làm hỏng cả lượt kéo.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .sources.ranksy import Ranksy, RanksyError

SERIES = [
    "installs", "uninstalls", "reactivations", "deactivations", "active_merchants",
    "active_subscriptions", "active_trials", "trial_conversion_rate",
    "churn_rate", "revenue_churn_rate", "churned_total", "mrr", "nrr", "revenue", "ltv",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="ecomposer", help="tên app (khớp một phần)")
    ap.add_argument("--since", default=f"{date.today().year}-01-01")
    ap.add_argument("--out", default="data/ranksy")
    ap.add_argument("--skip-lists", action="store_true", help="bỏ các danh sách dài để tiết kiệm quota")
    args = ap.parse_args()

    rk, out = Ranksy(), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    log: dict[str, str] = {}

    def save(name: str, fn):
        try:
            data = fn()
            (out / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            log[name] = f"ok ({len(data) if isinstance(data, list) else 'object'})"
        except RanksyError as e:
            log[name] = f"LỖI {e}"

    save("me", lambda: rk.get("/me"))
    app = rk.find_app(args.app)
    a = f"/apps/{app['id']}"
    save("app", lambda: rk.get(a))

    # Tổng quan do Ranksy tính sẵn (mỗi cái 1 request)
    save("churn_overview", lambda: rk.get(f"{a}/churn", months=12))
    save("uninstall_reasons_90d", lambda: rk.get(f"{a}/uninstall-reasons", days=90))
    save("revenue_overview", lambda: rk.get(f"{a}/revenue/overview", months=12))
    save("cohorts_install_month", lambda: rk.get(f"{a}/retention/cohorts", mode="install", group_by="month", periods=12))
    save("cohorts_subscription_month", lambda: rk.get(f"{a}/retention/cohorts", mode="subscription", group_by="month", periods=12))
    save("active_trials_now", lambda: rk.get(f"{a}/active-trials"))
    save("traffic_funnel", lambda: rk.get(f"{a}/traffic/funnel", start_date=args.since, end_date=today))

    # Chuỗi thời gian theo tuần và theo tháng
    for m in SERIES:
        for g in ("week", "month"):
            save(f"series_{m}_{g}", lambda m=m, g=g: rk.pages(
                f"{a}/metrics/{m}", start_date=args.since, end_date=today, granularity=g, per_page=200))
    for w in ("7d", "90d"):
        save(f"series_churn_rate_{w}_month", lambda w=w: rk.pages(
            f"{a}/metrics/churn_rate", start_date=args.since, end_date=today, granularity="month", window=w, per_page=200))

    if not args.skip_lists:
        save("churned_customers_12m", lambda: rk.pages(f"{a}/churned-customers", months=12, per_page=100))
        save("subscriptions_cancelled", lambda: rk.pages(f"{a}/subscriptions", status="cancelled", per_page=100))
        save("subscriptions_active", lambda: rk.pages(f"{a}/subscriptions", status="active", per_page=100, max_pages=60))
        for ev in ("TRIAL_STARTED", "TRIAL_CONVERTED", "TRIAL_CANCELLED", "SUBSCRIBED", "DOWNGRADED", "UPGRADED", "CHURNED"):
            save(f"events_{ev}", lambda ev=ev: rk.pages(
                f"{a}/lifecycle-events", event_type=ev, event_date_after=args.since, per_page=100, max_pages=60))
        save("reviews_all", lambda: rk.pages(f"{a}/reviews", start_date=args.since, end_date=today, sort="date", per_page=100))
        save("competitors", lambda: rk.pages(f"{a}/competitors", per_page=100))

    (out / "_pull_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in log.items():
        print(f"{k:38s} {v}")
    print(f"\nTổng số request (tính vào quota Ranksy): {rk.calls}")


if __name__ == "__main__":
    main()
