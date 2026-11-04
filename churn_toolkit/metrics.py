"""Tính chỉ số churn / uninstall / free-to-paid từ bảng event.

Bảng event cần cột: type, occurred_at (UTC), shop_id, plan_name, amount,
uninstall_reason. Xem sources/partner_api.py.

Ý tưởng chính:
- Uninstall churn: shop gỡ app.
- Paid churn: shop huỷ gói trả phí (không tính đổi gói: huỷ rồi kích hoạt
  gói khác trong vòng 2 ngày là "đổi gói", không phải churn).
- Free-to-paid: shop cài app rồi kích hoạt gói trả phí lần đầu.
- Cohort: nhóm shop theo tuần cài app, rồi theo dõi D1/D7/D30.
"""
from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd

INSTALL = "RELATIONSHIP_INSTALLED"
UNINSTALL = "RELATIONSHIP_UNINSTALLED"
ACTIVATED = "SUBSCRIPTION_CHARGE_ACTIVATED"
CANCELED = "SUBSCRIPTION_CHARGE_CANCELED"
FROZEN = "SUBSCRIPTION_CHARGE_FROZEN"
UNFROZEN = "SUBSCRIPTION_CHARGE_UNFROZEN"
PLAN_SWITCH_WINDOW = timedelta(days=2)


def _monthly(row) -> float:
    amt = row.get("amount") or 0.0
    name = str(row.get("plan_name") or "").lower()
    return amt / 12 if any(k in name for k in ("annual", "year", "yearly")) else amt


def mark_real_cancels(ev: pd.DataFrame) -> pd.DataFrame:
    """Thêm cột is_real_cancel: huỷ thật (không phải đổi gói)."""
    ev = ev.sort_values("occurred_at").copy()
    ev["is_real_cancel"] = False
    acts = ev[ev["type"] == ACTIVATED].groupby("shop_id")["occurred_at"].apply(list).to_dict()
    for idx, row in ev[ev["type"] == CANCELED].iterrows():
        times = acts.get(row["shop_id"], [])
        switched = any(abs(t - row["occurred_at"]) <= PLAN_SWITCH_WINDOW for t in times)
        ev.at[idx, "is_real_cancel"] = not switched
    return ev


def shop_table(ev: pd.DataFrame) -> pd.DataFrame:
    """1 dòng / shop: lần cài đầu, lần gỡ đầu sau đó, lần trả phí đầu, gói..."""
    ev = mark_real_cancels(ev)
    g = ev.groupby("shop_id")
    first_install = ev[ev["type"] == INSTALL].groupby("shop_id")["occurred_at"].min()
    shops = pd.DataFrame({"install_at": first_install})

    def first_after(kind, col="occurred_at", mask=None):
        sub = ev[ev["type"] == kind] if mask is None else ev[(ev["type"] == kind) & mask]
        sub = sub.join(shops["install_at"], on="shop_id")
        sub = sub[sub["occurred_at"] >= sub["install_at"]]
        return sub.sort_values("occurred_at").groupby("shop_id").first()

    un = first_after(UNINSTALL)
    shops["uninstall_at"] = un["occurred_at"]
    shops["uninstall_reason"] = un.get("uninstall_reason")
    paid = first_after(ACTIVATED)
    shops["first_paid_at"] = paid["occurred_at"]
    shops["first_plan"] = paid["plan_name"]
    shops["first_amount"] = paid["amount"]
    cancel = first_after(CANCELED, mask=ev["is_real_cancel"])
    shops["paid_cancel_at"] = cancel["occurred_at"]
    shops["reinstalls"] = g.apply(lambda d: max((d["type"] == INSTALL).sum() - 1, 0))

    shops["days_to_uninstall"] = (shops["uninstall_at"] - shops["install_at"]).dt.total_seconds() / 86400
    shops["days_to_paid"] = (shops["first_paid_at"] - shops["install_at"]).dt.total_seconds() / 86400
    shops["install_week"] = shops["install_at"].dt.tz_localize(None).dt.to_period("W").dt.start_time
    shops["is_paid"] = shops["first_paid_at"].notna()
    return shops.reset_index()


def window_summary(ev: pd.DataFrame, start, end) -> dict:
    """Đếm sự kiện trong [start, end)."""
    ev = mark_real_cancels(ev)
    w = ev[(ev["occurred_at"] >= start) & (ev["occurred_at"] < end)]
    c = w["type"].value_counts()
    return {
        "installs": int(c.get(INSTALL, 0)),
        "uninstalls": int(c.get(UNINSTALL, 0)),
        "net_installs": int(c.get(INSTALL, 0) - c.get(UNINSTALL, 0)),
        "paid_activations": int(c.get(ACTIVATED, 0)),
        "paid_cancels_real": int(w["is_real_cancel"].sum()),
        "plan_switches": int(((w["type"] == CANCELED) & ~w["is_real_cancel"]).sum()),
        "frozen": int(c.get(FROZEN, 0)),
    }


def active_paid_at(ev: pd.DataFrame, at) -> pd.DataFrame:
    """Các shop đang có gói trả phí tại thời điểm `at` (ước tính MRR)."""
    sub_types = [ACTIVATED, CANCELED, FROZEN, UNFROZEN, UNINSTALL]
    e = ev[(ev["occurred_at"] < at) & ev["type"].isin(sub_types)].sort_values("occurred_at")
    # Lấy event cuối mỗi shop; nếu cùng thời điểm, ưu tiên ACTIVATED (đổi gói)
    e = e.assign(_p=(e["type"] == ACTIVATED).astype(int)).sort_values(["occurred_at", "_p"])
    last = e.groupby("shop_id").tail(1)
    act = last[last["type"].isin([ACTIVATED, UNFROZEN])].copy()
    if not act.empty:
        # UNFROZEN không có amount -> lấy amount của lần ACTIVATED gần nhất
        last_act = ev[(ev["type"] == ACTIVATED) & (ev["occurred_at"] < at)].sort_values("occurred_at")
        last_act = last_act.groupby("shop_id").tail(1).set_index("shop_id")
        act["plan_name"] = act["shop_id"].map(last_act["plan_name"])
        act["amount"] = act["shop_id"].map(last_act["amount"])
        act["mrr"] = act.apply(_monthly, axis=1)
    return act


def paid_churn_rate(ev: pd.DataFrame, start, end) -> dict:
    base = active_paid_at(ev, start)
    endset = active_paid_at(ev, end)
    lost = set(base["shop_id"]) - set(endset["shop_id"])
    mrr_start = float(base["mrr"].sum()) if not base.empty else 0.0
    mrr_end = float(endset["mrr"].sum()) if not endset.empty else 0.0
    lost_mrr = float(base[base["shop_id"].isin(lost)]["mrr"].sum()) if lost else 0.0
    return {
        "paid_shops_start": len(base),
        "paid_shops_end": len(endset),
        "paid_logo_churn_pct": round(100 * len(lost) / len(base), 2) if len(base) else None,
        "mrr_start": round(mrr_start, 2),
        "mrr_end": round(mrr_end, 2),
        "mrr_churned": round(lost_mrr, 2),
        "gross_mrr_churn_pct": round(100 * lost_mrr / mrr_start, 2) if mrr_start else None,
    }


def cohort_table(shops: pd.DataFrame, now) -> pd.DataFrame:
    """Cohort theo tuần cài: % gỡ D1/D7/D30, % lên paid D14/D30, % paid huỷ."""
    rows = []
    now = pd.Timestamp(now).tz_convert("UTC") if pd.Timestamp(now).tzinfo else pd.Timestamp(now, tz="UTC")
    for wk, d in shops.groupby("install_week"):
        n = len(d)
        age = (now - d["install_at"].max()).days  # tuổi của shop trẻ nhất cohort

        def pct(mask, min_age):
            return round(100 * mask.sum() / n, 1) if age >= min_age else np.nan

        paid = d[d["is_paid"]]
        rows.append(
            {
                "install_week": wk.date(),
                "installs": n,
                "uninstall_d1_pct": pct(d["days_to_uninstall"] <= 1, 1),
                "uninstall_d7_pct": pct(d["days_to_uninstall"] <= 7, 7),
                "uninstall_d30_pct": pct(d["days_to_uninstall"] <= 30, 30),
                "paid_d14_pct": pct(d["days_to_paid"] <= 14, 14),
                "paid_d30_pct": pct(d["days_to_paid"] <= 30, 30),
                "paid_then_cancel_pct": round(100 * paid["paid_cancel_at"].notna().mean(), 1) if len(paid) else np.nan,
            }
        )
    return pd.DataFrame(rows)


def correlation_report(shops: pd.DataFrame, cohorts: pd.DataFrame) -> dict:
    """Mối quan hệ giữa free-to-paid và churn.

    1) Mức shop: shop trả phí có ở lại lâu hơn shop free không?
    2) Theo thời gian lên paid: lên paid nhanh (<=3 ngày) vs chậm.
    3) Theo gói: gói nào bị huỷ nhiều nhất.
    4) Mức cohort: tuần nào convert cao thì uninstall có thấp hơn không (Pearson r).
    """
    out = {}
    s = shops.copy()
    s["gone_30d"] = s["days_to_uninstall"] <= 30
    old = s[(pd.Timestamp.now(tz="UTC") - s["install_at"]).dt.days >= 30]
    if len(old):
        out["uninstall_30d_pct_free"] = round(100 * old[~old["is_paid"]]["gone_30d"].mean(), 1)
        out["uninstall_30d_pct_paid"] = round(100 * old[old["is_paid"]]["gone_30d"].mean(), 1) if old["is_paid"].any() else None

    paid = s[s["is_paid"]].copy()
    if len(paid):
        paid["speed"] = np.where(paid["days_to_paid"] <= 3, "nhanh (<=3 ngày)", "chậm (>3 ngày)")
        out["paid_cancel_pct_by_speed"] = (
            paid.groupby("speed")["paid_cancel_at"].apply(lambda x: round(100 * x.notna().mean(), 1)).to_dict()
        )
        out["median_days_to_paid"] = round(float(paid["days_to_paid"].median()), 1)
        plan = paid.groupby("first_plan").agg(
            shops=("shop_id", "count"),
            cancel_pct=("paid_cancel_at", lambda x: round(100 * x.notna().mean(), 1)),
            uninstall_pct=("uninstall_at", lambda x: round(100 * x.notna().mean(), 1)),
        )
        out["by_plan"] = plan.sort_values("shops", ascending=False).reset_index().to_dict("records")

    c = cohorts.dropna(subset=["paid_d30_pct", "uninstall_d30_pct"])
    if len(c) >= 4:
        out["cohort_corr_paid_vs_uninstall"] = round(float(c["paid_d30_pct"].corr(c["uninstall_d30_pct"])), 2)
    return out


def uninstall_timing(shops: pd.DataFrame) -> dict:
    d = shops["days_to_uninstall"].dropna()
    if d.empty:
        return {}
    bins = [-0.01, 1 / 24, 1, 7, 30, 90, 1e9]
    labels = ["<1 giờ", "1 giờ-1 ngày", "1-7 ngày", "7-30 ngày", "30-90 ngày", ">90 ngày"]
    return pd.cut(d, bins=bins, labels=labels).value_counts().reindex(labels).fillna(0).astype(int).to_dict()


def uninstall_reasons(ev: pd.DataFrame, start, end, top: int = 10) -> list[tuple[str, int]]:
    w = ev[(ev["type"] == UNINSTALL) & (ev["occurred_at"] >= start) & (ev["occurred_at"] < end)]
    r = w["uninstall_reason"].fillna("(không ghi lý do)").value_counts().head(top)
    return list(r.items())
