# Playbook: phân tích & giảm churn cho EComposer

## 1. Đánh giá churn thế nào cho đúng

"Churn cao" thường là 4 con số khác nhau bị gộp làm một. Tách ra:

| Chỉ số | Công thức | Ý nghĩa |
|---|---|---|
| **Uninstall rate D1 / D7 / D30** | shop gỡ trong N ngày / shop cài trong cohort | Chất lượng onboarding & mức độ đúng kỳ vọng |
| **Free-to-paid (D14, D30)** | shop kích hoạt gói trả phí lần đầu trong N ngày / shop cài | Giá trị đủ rõ để trả tiền chưa |
| **Paid logo churn (tháng)** | shop đang trả phí đầu kỳ mà cuối kỳ không còn / shop trả phí đầu kỳ | Giữ chân khách trả tiền |
| **Gross MRR churn** | MRR mất do huỷ & hạ gói / MRR đầu kỳ | Tác động doanh thu |

Ba lỗi hay gặp:

1. **Tính "đổi gói" là churn.** Khi shop đổi gói, Shopify sinh ra `CANCELED` gói cũ và `ACTIVATED`
   gói mới. Toolkit coi huỷ + kích hoạt trong vòng 2 ngày là đổi gói.
2. **Trộn shop free và shop trả phí.** Phần lớn lượt gỡ thường là shop free trong vài ngày đầu.
   Đây là vấn đề onboarding, khác với khách trả tiền bỏ đi.
3. **Nhìn tổng thay vì cohort.** Lượt gỡ tăng có thể chỉ vì lượt cài tuần trước tăng
   (ví dụ chạy ads). Luôn xem bảng cohort.

### Cách đọc mối tương quan free-to-paid ↔ churn (mục 5 báo cáo tuần)

- **Gỡ 30 ngày: free vs paid.** Nếu chênh lệch lớn → đưa shop lên paid (trial, ưu đãi gói năm)
  là đòn bẩy giữ chân mạnh nhất.
- **Huỷ gói theo tốc độ lên paid.** Nếu shop lên paid trong ≤3 ngày lại huỷ nhiều hơn → đang
  ép upgrade trước khi khách thấy giá trị (hoặc có hiểu lầm về billing).
- **Theo gói.** Gói có tỉ lệ huỷ cao nhất là nơi nên phỏng vấn khách trước tiên.
- **r của cohort.** r âm (< -0,3): tuần nào convert tốt thì gỡ ít. Đây là tương quan, chưa phải
  nhân quả; muốn chắc cần A/B test (ví dụ: 50% shop mới được trial Pro 14 ngày).

### Phân rã nguyên nhân (dùng cùng báo cáo)

```
Shop gỡ app
├── < 24 giờ  → không tìm thấy giá trị / khó dùng / cài nhầm   → onboarding, template
├── 1–7 ngày  → thử xong, không publish được / vỡ theme        → support chủ động, QA
├── 7–30 ngày → hết nhu cầu (làm xong 1 landing page)           → lý do để quay lại hằng tháng
└── > 30 ngày → đổi đối thủ, giá, bug lặp lại, Shopify tự làm được → định vị, roadmap
```

Ghép với: lý do gỡ (khảo sát Shopify), chủ đề chat Crisp 7 ngày trước khi gỡ, review ≤3 sao.

## 2. Bối cảnh thị trường (tháng 11/2026)

**Đối thủ và định vị** (theo các bài so sánh 2026; nhiều bài do chính các vendor viết, cần kiểm tra lại giá):

| App | Định vị | Giá tham khảo |
|---|---|---|
| EComposer | Rẻ nhất trong nhóm có gói trả phí, có gói free | Standard $25/tháng ($19 năm), Pro $49, Premium $129 |
| PageFly | "Value pick", editor & support trưởng thành | Free 1 trang; từ $24/tháng |
| GemPages | Tập trung CRO, kho template lớn | Free 1 trang; Build ~$29/tháng |
| Replo | Cao cấp, cho đội dev/agency | Từ ~$99–119/tháng |
| Shogun | Lâu đời, nhiều khách enterprise | Từ ~$39/tháng, không có free |

**Rủi ro lớn nhất từ chính Shopify:**

- **Theme Horizon + Theme Blocks**: merchant kéo thả block lồng nhau (tới 8 cấp) mà không cần app.
- **Sidekick / AI tạo block và AI store builder**: tạo section từ mô tả bằng chữ ngay trong theme editor.
- **Canvas** (công bố 2026): bề mặt thiết kế mới với Sidekick; chưa thay theme editor.
- Từ 1/10/2026, app không còn tạo/cập nhật storefront script tag.

→ Nhu cầu "tạo landing page cơ bản" đang bị Shopify ăn dần. Shop free dùng EComposer để làm
1 trang rồi gỡ sẽ ngày càng nhiều. Giá trị cần nhấn mạnh: những gì theme editor **không** làm được
(A/B test, CRO template theo ngành, funnel, analytics, tốc độ, hỗ trợ con người).

**Review của EComposer** (4,9★, ~3.450 review): phần lớn khen support và editor dễ dùng; nhóm
phàn nàn lặp lại là **bug làm vỡ trang**, **support không phản hồi tiếp**, và **tranh chấp refund
gói năm** (bị đẩy qua lại giữa EComposer và Shopify).

## 3. Chiến thuật giảm uninstall & tăng free-to-paid

Ưu tiên theo mức tác động / công sức:

### Tuần 1–2 (rẻ, nhanh)

1. **Định nghĩa "activation" = đã publish ≥1 trang trong 24h.** Theo dõi tỉ lệ này mỗi ngày.
   Nhiều nghiên cứu ngành cho rằng phần lớn churn của app Shopify được quyết định trong tuần đầu,
   và ngày đầu có tỉ lệ gỡ cao nhất.
2. **Crisp trigger:** shop cài >2 giờ chưa publish → tin nhắn chủ động kèm video 60 giây +
   đề nghị "chúng tôi dựng giúp trang đầu tiên miễn phí" (EComposer đã mạnh về support, dùng nó
   làm vũ khí onboarding).
3. **Quy trình huỷ/refund minh bạch:** email nhắc 3 ngày trước khi gia hạn gói năm; refund do
   EComposer xử lý, không đẩy khách sang Shopify. Mỗi review 1★ về refund làm giảm lượt cài mới.
4. **Cancel flow:** trước khi huỷ gói → hỏi lý do → đề nghị hạ gói / tạm dừng 1–2 tháng / giảm giá
   1 tháng. Lưu lý do vào Crisp segment để báo cáo đọc được.

### Tháng 1–2

5. **Onboarding theo ngành:** hỏi 1 câu khi cài (thời trang / làm đẹp / đồ điện tử...) → mở sẵn
   template phù hợp. Mục tiêu: "quick win" trong lần dùng đầu.
6. **Trial gói Pro 7–14 ngày (A/B test 50/50)** cho shop mới, đo bằng cohort: free-to-paid D30 và gỡ D30.
7. **Paywall ở tính năng giá trị cao** (A/B test, AI section, analytics) thay vì giới hạn số trang
   quá sớm. GemPages/PageFly đều cho publish 1 trang miễn phí để khách thấy giá trị trước.
8. **Uninstall hygiene:** gỡ app không để lại code thừa / không làm vỡ theme. Hướng dẫn rõ trong
   app. Khách gỡ "sạch" sẽ dễ quay lại hơn và ít để lại review xấu.

### Quý tới

9. **Định vị theo Horizon:** "page builder tương thích tốt nhất với Horizon/Theme Blocks", xuất
   section thành theme block, bổ sung cho Sidekick thay vì cạnh tranh trực diện.
10. **Lý do quay lại hằng tháng:** template theo mùa (BFCM, Tết...), báo cáo CRO hằng tháng gửi
    vào email, A/B test gợi ý tự động. Đây là cách biến khách "làm 1 trang rồi đi" thành khách dài hạn.
11. **Win-back:** shop đã gỡ 30/60 ngày → email ưu đãi + "có gì mới". Partner API cho biết shop
    nào đã cài lại (`reinstalls` trong bảng shop).

## 4. Học từ đối thủ & SaaS khác (theo dõi hằng tuần)

- Bảng "Chủ đề trong review ≤3 sao, EComposer vs đối thủ": chủ đề nào EComposer bị phàn nàn nhiều
  hơn hẳn đối thủ là điểm yếu tương đối.
- "Đối thủ được khen về": điều khách đánh giá cao ở đối thủ → ý tưởng sản phẩm.
- "Đối thủ được nhắc trong chat": khách so sánh với ai → chuẩn bị battlecard cho support.
- Kênh theo dõi miễn phí: Shopify Changelog (shopify.dev/changelog), Shopify Editions (2 lần/năm),
  r/shopify, r/shopifyDev, Shopify Community, blog đối thủ.

## Nguồn

- [Review EComposer trên Shopify App Store](https://apps.shopify.com/ecomposer/reviews?page=1)
- [Ranksy: kết nối Partner API](https://docs.ranksyapp.com/hc/docs/articles/1774679931-connect-partner-api)
- [Shopify Partner API – AppEventTypes](https://shopify.dev/docs/api/partner/latest/enums/AppEventTypes)
- [Shopify Partner API – SubscriptionChargeCanceled](https://shopify.dev/docs/api/partner/latest/objects/SubscriptionChargeCanceled.md)
- [Shopify Partners blog: App onboarding](https://www.shopify.com/partners/blog/app-onboarding)
- [Shopify Community: lý do merchant gỡ app](https://community.shopify.com/t/whats-the-biggest-reason-merchants-uninstall-a-shopify-app/660762)
- [Taylor Sicard: onboarding benchmarks](https://taylorsicard.com/blog/shopify-app-onboarding-benchmarks) (số liệu tham khảo, chưa kiểm chứng)
- [Spur-IT: chỉ số doanh thu app Shopify](https://spur-i-t.com/blog/shopify-app-store-guide-to-revenue-app-metrics/)
- [So sánh page builder 2026 – Craftshift](https://craftshift.com/best-shopify-page-builder-apps-2026/)
- [Replo alternatives – Fudge](https://www.fudge.ai/blog/replo-alternatives/)
- [Shopify Horizon themes 2026 – GemPages](https://gempages.net/blogs/shopify/top-shopify-horizon-themes)
- [Shopify Horizon guide – ecommerce-platforms](https://ecommerce-platforms.com/articles/shopify-horizon-themes)
- [Shopify Summer '25 Edition](https://www.shopify.com/news/summer-25-edition-merchant)
- [TechCrunch: Shopify AI store builder](https://techcrunch.com/2025/05/21/shopify-launches-an-ai-powered-store-builder-as-part-of-its-latest-update)
