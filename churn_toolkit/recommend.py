"""Gợi ý hành động dựa trên số liệu (luật đơn giản, dễ sửa).

Mỗi gợi ý ghi rõ: dấu hiệu -> việc nên làm -> ai đang làm tốt việc đó.
Các ngưỡng là điểm khởi đầu; chỉnh lại sau 4-6 tuần có dữ liệu thật.
"""
from __future__ import annotations


def recommendations(daily: dict, cohorts, corr: dict, timing: dict, topics, chat_topics) -> list[str]:
    recs = []
    last = cohorts.dropna(subset=["uninstall_d1_pct"]).tail(4) if cohorts is not None and len(cohorts) else None

    if last is not None and len(last) and last["uninstall_d1_pct"].mean() > 25:
        recs.append(
            f"**Gỡ trong ngày đầu cao ({last['uninstall_d1_pct'].mean():.0f}% trung bình 4 tuần).** "
            "Thường là do merchant chưa đạt 'quick win' đầu tiên. Việc nên làm: onboarding 3 bước "
            "(chọn template → sửa 1 section → publish), tự mở template theo ngành của shop, chat chủ động "
            "trong 10 phút đầu. Kinh nghiệm từ PageFly/GemPages: cho xuất bản 1 trang miễn phí "
            "ngay trong lần dùng đầu."
        )
    total_un = sum(timing.values()) if timing else 0
    if total_un:
        fast = timing.get("<1 giờ", 0) + timing.get("1 giờ-1 ngày", 0)
        if fast / total_un > 0.4:
            recs.append(
                f"**{100 * fast / total_un:.0f}% lượt gỡ xảy ra trong 24 giờ đầu.** Hãy theo dõi riêng "
                "chỉ số 'activation' (đã publish ≥1 trang). Gửi email/Crisp trigger cho shop cài >2 giờ "
                "mà chưa publish."
            )
    if corr.get("uninstall_30d_pct_free") and corr.get("uninstall_30d_pct_paid") is not None:
        f, p = corr["uninstall_30d_pct_free"], corr["uninstall_30d_pct_paid"]
        if f - p > 15:
            recs.append(
                f"**Shop trả phí ở lại tốt hơn nhiều (gỡ 30 ngày: free {f}% vs paid {p}%).** "
                "Lên paid là 'neo' giữ chân. Thử: trial gói Pro 7-14 ngày ngay khi cài, giảm giá gói năm, "
                "paywall mềm ở tính năng có giá trị (A/B test, AI section) thay vì ở số trang."
            )
    sp = corr.get("paid_cancel_pct_by_speed", {})
    if len(sp) == 2:
        fast, slow = sp.get("nhanh (<=3 ngày)"), sp.get("chậm (>3 ngày)")
        if fast is not None and slow is not None and fast - slow > 10:
            recs.append(
                f"**Shop lên paid quá nhanh lại huỷ nhiều hơn ({fast}% vs {slow}%).** Có thể bị ép "
                "upgrade trước khi thấy giá trị, hoặc 'mua thử'. Xem lại popup upgrade, kiểm tra review "
                "nhắc 'charged', 'refund'."
            )
    plans = corr.get("by_plan") or []
    worst = sorted([p for p in plans if p["shops"] >= 20], key=lambda p: -p["cancel_pct"])[:1]
    if worst:
        w = worst[0]
        recs.append(
            f"**Gói '{w['first_plan']}' bị huỷ nhiều nhất ({w['cancel_pct']}% / {w['shops']} shop).** "
            "Phỏng vấn 5-10 shop đã huỷ gói này; thêm cancel-flow: hỏi lý do → đề nghị hạ gói/tạm "
            "dừng 1-2 tháng thay vì huỷ (Shopify cho phép đổi gói qua appSubscriptionCreate)."
        )

    def has(df, name, n=1):
        return df is not None and len(df) and (df[df["topic"] == name]["count"].sum() >= n)

    if has(topics, "Giá / billing / refund", 2) or has(chat_topics, "Giá / billing / refund", 5):
        recs.append(
            "**Phàn nàn về billing/refund lặp lại.** Ghi rõ 'huỷ bất cứ lúc nào', email nhắc 3 ngày "
            "trước khi gia hạn gói năm, quy trình refund 1 bước (không đẩy qua Shopify). Review "
            "1 sao về refund ảnh hưởng mạnh đến tỉ lệ cài mới."
        )
    if has(topics, "Bug / lỗi hiển thị", 2) or has(chat_topics, "Bug / lỗi hiển thị", 10):
        recs.append(
            "**Bug/hiển thị vỡ là chủ đề nổi bật.** Lập bảng top 5 lỗi theo số chat mỗi tuần, gắn "
            "owner kỹ thuật; thêm 'preview trên theme bản sao' trước khi publish."
        )
    if has(chat_topics, "Xung đột theme / app khác", 5):
        recs.append(
            "**Nhiều chat về theme/Horizon/xung đột.** Shopify đang đẩy Horizon + Theme Blocks + "
            "Sidekick AI, làm giảm nhu cầu page builder cơ bản. Định vị lại: EComposer = tương thích "
            "tốt nhất với Horizon, xuất section dạng theme block, và tính năng mà theme editor không có."
        )
    if not recs:
        recs.append("Chưa có tín hiệu bất thường theo các ngưỡng hiện tại. Giữ nguyên theo dõi.")
    return recs
