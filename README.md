# EComposer Churn Toolkit

Bộ công cụ miễn phí để theo dõi **uninstall, churn, free-to-paid** của app EComposer và
tự gửi **báo cáo hằng ngày / hằng tuần**.

| Phần | Chi phí |
|---|---|
| Shopify Partner API (cùng nguồn dữ liệu mà Ranksy dùng) | Miễn phí |
| Crisp REST API (plugin private) | Miễn phí |
| Review Shopify App Store (EComposer + PageFly, GemPages, Shogun, Replo, Instant) | Miễn phí |
| GitHub Actions chạy theo lịch (repo private: 2.000 phút/tháng miễn phí, mỗi lần chạy ~2 phút) | Miễn phí |
| Gửi Slack / Telegram / Discord | Miễn phí |
| Tóm tắt chat bằng Claude (tuỳ chọn) | ~vài USD/tháng |

> ⚠️ Báo cáo chứa MRR và số liệu kinh doanh. **Giữ repo này ở chế độ private.**

## Báo cáo có gì

**Hằng ngày:** cài / gỡ / kích hoạt gói / huỷ gói (tách riêng "đổi gói"), so với trung bình
7 ngày trước, cảnh báo khi gỡ tăng >30%, lý do gỡ từ khảo sát Shopify, review xấu mới,
chủ đề chat support trong ngày, gợi ý hành động.

**Hằng tuần:** thêm MRR & paid churn, bảng cohort (gỡ D1/D7/D30, lên paid D14/D30),
**tương quan free-to-paid ↔ churn**, thời điểm gỡ app, so sánh chủ đề phàn nàn của
EComposer với đối thủ, đối thủ được nhắc trong chat.

Xem mẫu (dữ liệu giả lập): [reports/weekly/2026-11-04-demo.md](reports/weekly/2026-11-04-demo.md)

## Cài đặt (khoảng 20 phút)

### Bước 1 – Shopify Partner API (quan trọng nhất)

1. Vào [Partner Dashboard](https://partners.shopify.com) → **Settings** → **Partner API clients** → **Create API client**.
2. Đặt tên `churn-toolkit`, tick **Manage apps** và **View financials** → Save → copy **Access token**.
3. Lấy **Organization ID**: số trong URL `partners.shopify.com/<ORG_ID>/...`.
4. Lấy **App ID**: mở app EComposer trong Partner Dashboard, số cuối URL `.../apps/<APP_ID>`.

> Ranksy cũng lấy từ API này. Trang `ranksyapp.com/settings/api-keys` là nơi *dán* token
> Partner vào Ranksy chứ Ranksy không có API công khai để lấy dữ liệu ra. Nếu vẫn muốn dùng
> dữ liệu đã có trong Ranksy: export CSV rồi chạy `--events-csv file.csv`.

### Bước 2 – Crisp

1. [marketplace.crisp.chat](https://marketplace.crisp.chat) → tạo plugin **Private**.
2. Tab **Tokens** → xin **Production token** với scope đọc
   `website:conversation:sessions` và `website:conversation:messages`.
3. Cài plugin đó vào website EComposer.
4. Ghi lại `identifier`, `key`, và website id `9d122c0c-3e42-43d8-b923-e6fca52afef8`.

### Bước 3 – Đưa token vào GitHub (không bao giờ ghi token vào code)

Repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Bắt buộc |
|---|---|
| `SHOPIFY_PARTNER_ORG_ID`, `SHOPIFY_PARTNER_TOKEN`, `SHOPIFY_APP_ID` | Có |
| `CRISP_IDENTIFIER`, `CRISP_KEY`, `CRISP_WEBSITE_ID` | Nên có |
| `SLACK_WEBHOOK_URL` hoặc `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Tuỳ chọn |
| `ANTHROPIC_API_KEY` | Tuỳ chọn (tóm tắt chat bằng AI) |

### Bước 4 – Chạy

- Tự động: 08:17 sáng (giờ VN) mỗi ngày; báo cáo tuần sáng thứ Hai.
- Chạy tay: tab **Actions → Churn reports → Run workflow**.
- Báo cáo được lưu trong `reports/daily/` và `reports/weekly/`.

Chạy trên máy:

```bash
pip install -r requirements.txt
```

```bash
python -m churn_toolkit --period weekly --demo
```

```bash
python -m churn_toolkit --period daily --events-csv export.csv
```

## Cấu trúc

```
churn_toolkit/
  sources/partner_api.py     # event cài/gỡ/subscription
  sources/crisp.py           # hội thoại support
  sources/shopify_reviews.py # review của EComposer & đối thủ
  metrics.py                 # churn, cohort, free-to-paid, tương quan
  text_topics.py             # gắn chủ đề bằng từ khoá (+ AI tuỳ chọn)
  recommend.py               # luật sinh gợi ý (sửa ngưỡng ở đây)
  report.py                  # tạo báo cáo Markdown
docs/playbook.md             # cách phân tích + nghiên cứu thị trường + chiến thuật
```

## Lưu ý

- Mặc định lấy 120 ngày gần nhất (đổi bằng biến `LOOKBACK_DAYS`). Cohort cần ≥30 ngày dữ liệu mới có số D30.
- `RelationshipUninstalled.reason/description` là khảo sát Shopify hiển thị khi gỡ; nhiều shop bỏ trống.
- Trang review Shopify có thể đổi HTML; khi phần review trống, sửa selector trong `shopify_reviews.py`.
