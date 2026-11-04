"""Sinh dữ liệu GIẢ LẬP để chạy thử pipeline khi chưa có token.

Không phải số liệu thật của EComposer. Báo cáo demo luôn có dòng cảnh báo.
"""
from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd

PLANS = [("Standard", 19.0), ("Pro", 39.0), ("Premium", 103.0), ("Pro Annual", 468.0)]


def make_events(now, days: int = 120, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    now = pd.Timestamp(now, tz="UTC") if pd.Timestamp(now).tzinfo is None else pd.Timestamp(now)
    rows = []
    reasons = ["It didn't work as expected", "It's too expensive", "I found a better app",
               "I don't need it anymore", "It was difficult to use", None]
    for i in range(days * 60):
        t = now - timedelta(days=days) + timedelta(minutes=float(rng.uniform(0, days * 1440)))
        shop = f"shop_{i}"
        rows.append({"type": "RELATIONSHIP_INSTALLED", "occurred_at": t, "shop_id": shop})
        paid = rng.random() < 0.12
        if paid:
            pt = t + timedelta(days=float(rng.exponential(5)))
            name, amt = PLANS[rng.integers(0, len(PLANS))]
            rows.append({"type": "SUBSCRIPTION_CHARGE_ACTIVATED", "occurred_at": pt, "shop_id": shop,
                         "plan_name": name, "amount": amt})
            if rng.random() < 0.35:
                ct = pt + timedelta(days=float(rng.exponential(40)))
                rows.append({"type": "SUBSCRIPTION_CHARGE_CANCELED", "occurred_at": ct, "shop_id": shop,
                             "plan_name": name, "amount": amt})
                if rng.random() < 0.7:
                    rows.append({"type": "RELATIONSHIP_UNINSTALLED", "occurred_at": ct + timedelta(hours=1),
                                 "shop_id": shop, "uninstall_reason": reasons[rng.integers(0, 6)]})
        elif rng.random() < 0.55:
            ut = t + timedelta(days=float(rng.exponential(3)))
            rows.append({"type": "RELATIONSHIP_UNINSTALLED", "occurred_at": ut, "shop_id": shop,
                         "uninstall_reason": reasons[rng.integers(0, 6)]})
    df = pd.DataFrame(rows)
    df = df[df["occurred_at"] < now]
    for c in ["plan_name", "amount", "uninstall_reason"]:
        if c not in df:
            df[c] = None
    return df.sort_values("occurred_at").reset_index(drop=True)
