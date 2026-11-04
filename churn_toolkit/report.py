"""Tạo báo cáo Markdown hằng ngày / hằng tuần."""
from __future__ import annotations

from datetime import timedelta

import pandas as pd

from . import metrics as M
from . import text_topics as T
from .recommend import recommendations


def _delta(cur, prev):
    if prev in (0, None):
        return ""
    pct = 100 * (cur - prev) / prev
    arrow = "▲" if pct > 0 else "▼" if pct < 0 else "="
    return f" ({arrow} {abs(pct):.0f}%)"


def _table(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "_(chưa có dữ liệu)_\n"
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for row in df.itertuples(index=False):
        cells = ["" if pd.isna(v) else str(v) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def build(ev: pd.DataFrame, now, period: str = "daily", reviews: pd.DataFrame | None = None,
          chats: pd.DataFrame | None = None, demo: bool = False) -> str:
    now = pd.Timestamp(now).floor("D")
    days = 1 if period == "daily" else 7
    start, end = now - timedelta(days=days), now
    prev_start = start - timedelta(days=days * (7 if period == "daily" else 1))

    cur = M.window_summary(ev, start, end)
    prev = M.window_summary(ev, prev_start, start)
    if period == "daily":  # so với trung bình 7 ngày trước
        prev = {k: v / 7 for k, v in prev.items()}

    L = []
    title = "Báo cáo NGÀY" if period == "daily" else "Báo cáo TUẦN"
    L.append(f"# EComposer – {title}: {start.date()} → {(end - timedelta(days=1)).date()}\n")
    if demo:
        L.append("> ⚠️ **DỮ LIỆU DEMO (giả lập)** – chỉ để xem định dạng báo cáo, không phải số thật.\n")

    cmp_label = "TB 7 ngày trước" if period == "daily" else "tuần trước"
    L.append(f"## 1. Tổng quan (so với {cmp_label})\n")
    L.append("| Chỉ số | Giá trị |\n|---|---|")
    names = {
        "installs": "Lượt cài", "uninstalls": "Lượt gỡ", "net_installs": "Cài ròng",
        "paid_activations": "Kích hoạt gói trả phí", "paid_cancels_real": "Huỷ gói (thật)",
        "plan_switches": "Đổi gói", "frozen": "Bị đóng băng (shop ngừng trả Shopify)",
    }
    for k, label in names.items():
        L.append(f"| {label} | {cur[k]}{_delta(cur[k], prev[k])} |")
    ratio = cur["uninstalls"] / cur["installs"] if cur["installs"] else None
    if ratio is not None:
        L.append(f"| Gỡ / Cài | {ratio:.2f} |")
    L.append("")

    alerts = []
    if prev["uninstalls"] and cur["uninstalls"] > 1.3 * prev["uninstalls"]:
        alerts.append(f"🚨 Lượt gỡ cao hơn {cmp_label} {100 * (cur['uninstalls'] / prev['uninstalls'] - 1):.0f}%.")
    if prev["paid_cancels_real"] and cur["paid_cancels_real"] > 1.5 * prev["paid_cancels_real"]:
        alerts.append("🚨 Huỷ gói trả phí tăng mạnh.")
    if alerts:
        L.append("**Cảnh báo:** " + " ".join(alerts) + "\n")

    L.append("## 2. Lý do gỡ app (khảo sát của Shopify)\n")
    reasons = M.uninstall_reasons(ev, start, end)
    L.append("\n".join(f"- {r}: **{n}**" for r, n in reasons) or "_(không có)_")
    L.append("")

    shops = M.shop_table(ev)
    cohorts = M.cohort_table(shops, now)
    corr = M.correlation_report(shops, cohorts)
    timing = M.uninstall_timing(shops[shops["uninstall_at"] >= now - timedelta(days=30)])

    review_topics = chat_topics = None
    if period == "weekly":
        pc = M.paid_churn_rate(ev, start, end)
        L.append("## 3. Doanh thu & paid churn (ước tính từ event)\n")
        L.append(f"- Shop trả phí: {pc['paid_shops_start']} → {pc['paid_shops_end']}")
        L.append(f"- Paid churn (số shop): **{pc['paid_logo_churn_pct']}%**")
        L.append(f"- MRR: ${pc['mrr_start']:,} → ${pc['mrr_end']:,}; MRR mất: ${pc['mrr_churned']:,} "
                 f"(**{pc['gross_mrr_churn_pct']}%**)\n")

        L.append("## 4. Cohort theo tuần cài app\n")
        L.append("Đọc: mỗi dòng là nhóm shop cài trong tuần đó. Ô trống = cohort chưa đủ tuổi.\n")
        L.append(_table(cohorts.tail(10)))

        L.append("## 5. Free-to-paid ↔ churn: mối tương quan\n")
        if "uninstall_30d_pct_free" in corr:
            L.append(f"- Gỡ trong 30 ngày: shop **free {corr['uninstall_30d_pct_free']}%** vs "
                     f"shop **đã trả phí {corr.get('uninstall_30d_pct_paid')}%**")
        if "median_days_to_paid" in corr:
            L.append(f"- Trung vị số ngày từ cài → trả phí: **{corr['median_days_to_paid']}**")
        for k, v in corr.get("paid_cancel_pct_by_speed", {}).items():
            L.append(f"- Huỷ gói khi lên paid {k}: **{v}%**")
        if "cohort_corr_paid_vs_uninstall" in corr:
            r = corr["cohort_corr_paid_vs_uninstall"]
            meaning = ("tuần nào convert cao thì gỡ ít hơn" if r < -0.3 else
                       "tuần nào convert cao thì gỡ cũng cao" if r > 0.3 else "chưa thấy liên hệ rõ")
            L.append(f"- Tương quan cohort (% paid D30 vs % gỡ D30): r = **{r}** → {meaning}")
        if corr.get("by_plan"):
            L.append("\nTheo gói đầu tiên:\n")
            L.append(_table(pd.DataFrame(corr["by_plan"])))

        L.append("## 6. Thời điểm gỡ app (30 ngày qua)\n")
        L.append("\n".join(f"- {k}: {v}" for k, v in timing.items()) or "_(không có)_")
        L.append("")

    sec = 3 if period == "daily" else 7
    if reviews is not None and not reviews.empty:
        L.append(f"## {sec}. Review Shopify App Store\n")
        own = reviews[reviews["app"] == "ecomposer"]
        recent = own[own["date"] >= start.tz_localize(None) - timedelta(days=0 if period == "weekly" else 2)]
        bad = recent[recent["rating"] <= 3]
        L.append(f"- Review mới của EComposer: {len(recent)} (≤3 sao: **{len(bad)}**)")
        for _, r in bad.head(5).iterrows():
            L.append(f"  - ⭐{r['rating']} – “{str(r['text'])[:200]}”")
        review_topics = T.topic_counts(reviews[(reviews["app"] == "ecomposer") & (reviews["rating"] <= 3)])
        if period == "weekly":
            L.append("\nChủ đề trong review ≤3 sao, EComposer so với đối thủ:\n")
            bad_all = reviews[reviews["rating"] <= 3]
            tbl = (pd.concat([T.topic_counts(g).assign(app=a) for a, g in bad_all.groupby("app")])
                   .pivot_table(index="topic", columns="app", values="count", fill_value=0).astype(int)
                   if len(bad_all) else pd.DataFrame())
            L.append(_table(tbl.reset_index()) if not tbl.empty else "_(chưa có)_\n")
            good = reviews[(reviews["app"] != "ecomposer") & (reviews["rating"] == 5)]
            L.append("Đối thủ được khen về (review 5 sao):\n")
            L.append(_table(T.topic_counts(good).head(6)))
        sec += 1

    if chats is not None and not chats.empty:
        L.append(f"## {sec}. Hội thoại support (Crisp)\n")
        L.append(f"- Số hội thoại: {len(chats)}\n")
        chat_topics = T.topic_counts(chats)
        L.append(_table(chat_topics.head(8)))
        comp = T.competitor_mentions(chats["text"])
        if comp:
            L.append("Đối thủ / Shopify được nhắc trong chat: " +
                     ", ".join(f"{k} ({v})" for k, v in comp.most_common()))
        for topic in chat_topics["topic"].head(2):
            for q in T.sample_quotes(chats, topic, 2):
                L.append(f"  - [{topic}] “{q}”")
        L.append("")
        llm = T.summarize_with_llm(
            chats["text"].tolist(),
            "Bạn là chuyên viên phân tích churn cho app Shopify page builder EComposer. Từ các tin nhắn "
            "support sau, liệt kê 5 vấn đề chính có nguy cơ khiến khách gỡ app hoặc huỷ gói, mỗi vấn đề "
            "kèm số lần ước tính và 1 trích dẫn. Trả lời bằng tiếng Việt, ngắn gọn.",
        )
        if llm:
            L.append("**Tóm tắt bằng AI:**\n\n" + llm + "\n")
        sec += 1

    L.append(f"## {sec}. Gợi ý hành động\n")
    for r in recommendations(cur, cohorts, corr, timing, review_topics, chat_topics):
        L.append(f"- {r}")
    L.append("\n_Chiến lược đầy đủ & nghiên cứu đối thủ: xem docs/playbook.md_\n")
    return "\n".join(L)
