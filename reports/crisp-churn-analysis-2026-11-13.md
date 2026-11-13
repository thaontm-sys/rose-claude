# Phân tích churn từ Crisp – 13/11/2026

**Nguồn:** Crisp workspace EComposer (đọc qua kết nối MCP). Tìm theo từ khoá `refund`,
`cancel`, `uninstall`, `expensive`, `pagefly`, `gempages`, `disappeared`, `annual plan`, rồi đọc
chi tiết ~10 hội thoại tiêu biểu (chủ yếu tháng 9–11/2026).

**Giới hạn:** mỗi lần tìm Crisp trả về tối đa ~40 hội thoại, nên đây là **mẫu định tính**,
chưa phải số đếm đầy đủ. Tên khách và email đã được ẩn.

---

## Tóm tắt

Có 5 nguyên nhân rời bỏ lặp lại, xếp theo mức nghiêm trọng:

| # | Nguyên nhân | Tác động | Mức độ |
|---|---|---|---|
| 1 | **Refund & gói năm**: từ chối refund → khách leo thang → nhiều khi vẫn phải refund, nhưng đã kịp để lại review 1–2★ | Mất khách + mất review | 🔴 Cao |
| 2 | **Không chỉnh sửa được trên điện thoại/tablet** | Gỡ app ngay, review 1★ | 🔴 Cao |
| 3 | **Nhạy cảm về giá + gói Free chỉ cho 1 trang** | Gỡ app / huỷ gói | 🟠 Trung bình |
| 4 | **Lỗi làm mất nội dung / vỡ trang** (ảnh biến mất, chọn variant lỗi, publish lỗi) | Khách bỏ đi, dựng lại site bằng công cụ khác | 🟠 Trung bình |
| 5 | **Chuyển sang đối thủ** (PageFly, GemPages) | Mất khách | 🟡 Thấp–trung bình |

Ngoài ra có một vấn đề về **cách support phản hồi khi khách muốn rời đi**: vài cách xử lý hiện tại
đang biến khách *rời đi trong im lặng* thành khách *rời đi kèm review xấu*.

---

## 1. Refund & gói năm – nguồn review xấu lớn nhất

**Chính sách hiện tại** (support trích lại): không refund nếu mua nhầm, không dùng, hoặc đã gỡ app;
chỉ xét trong 7 ngày **và** khi có mất dữ liệu / gián đoạn nghiêm trọng.

Các ca gần đây:

- **Mua nhầm gói năm $468** (29/10): khách gỡ app sau vài ngày, chưa dùng → bị từ chối ngay
  trong 7 phút, kèm link chính sách.
- **Khách gói năm "không đủ tiền chi trả"** (31/10 → 12/11): bị từ chối → khách hỏi
  *"có ai khác tôi có thể nói chuyện không?"* → chuyển billing → **sau gần 2 tuần vẫn đang
  "review"**. Khách dùng tablet, không gửi được ảnh hoá đơn qua link, bị yêu cầu gửi lại nhiều lần.
- **Khách gói năm, ảnh trên landing page bị mất hơn một lần** (30/10): khách đã dựng lại toàn bộ
  site ở chỗ khác, để review **2★**. Kết quả: EComposer **vẫn refund toàn bộ**, khách hứa sửa review.
  → Đã mất cả khách lẫn tiền; nếu refund ngay từ đầu thì ít nhất giữ được review.
- **Khách 3 năm, không còn sửa được trên điện thoại** (review 1★, 11/11): bị trừ $25 sau khi ngừng
  dùng. Khi khách nêu lý do, support trả lời rằng lý do này *"không liên quan đến lỗi của app"*.
  Review nêu đích danh nhân viên: *"save yourself the aggravation and DON'T!"*
- **Gói năm không dùng 5 tháng** (24/9): support hỏi lý do rời đi **3 lần** trước khi xử lý;
  cuối cùng refund theo tỉ lệ $175.

**Kết luận:** chính sách cứng ở bước đầu không giúp giữ tiền. Khách nào làm căng thì vẫn được
refund, nhưng phải qua nhiều vòng và thường để lại review xấu trước đó.

**Đề xuất:**
1. **Refund theo tỉ lệ thời gian chưa dùng cho gói năm, làm tự động**, không cần khách chứng minh
   lỗi. Partner Dashboard đã có đủ thông tin hoá đơn, không cần bắt khách gửi ảnh chụp.
2. **Refund đầy đủ trong 7 ngày đầu của gói năm**, không hỏi lý do. Mua nhầm gói năm là ca rất phổ biến.
3. **Email nhắc 7 ngày và 3 ngày trước khi gia hạn gói năm.** Shopify không làm việc này thay app.
4. **Hỏi lý do 1 lần, sau đó xử lý ngay.** Không đặt việc trả lời lý do thành điều kiện để được refund.
5. **Không bao giờ nói lý do của khách "không phải lỗi của app"**: đó chính là lý do churn cần ghi lại.
6. **Không gửi tin quảng cáo BFCM** vào hội thoại đang có yêu cầu refund hoặc huỷ.

## 2. Không chỉnh sửa được trên điện thoại / tablet

- Khách chỉ có điện thoại: *"but i have mobile only so i should uninstall it"*. Support xác nhận
  editor không hỗ trợ mobile và gợi ý gỡ app. Khách: *"such a f\*\*\*ing app"* → gỡ.
- Khách 3 năm bỏ đi vì *"could no longer edit on mobile"* → review 1★.
- Khách làm việc qua tablet không gửi được ảnh hoá đơn qua công cụ chia sẻ ảnh của support.

**Đề xuất:** tối thiểu một **chế độ sửa nhanh trên mobile** (đổi chữ, ảnh, giá, bật/tắt section).
Trong thời gian chờ: báo rõ "cần máy tính để chỉnh sửa" **trước khi** khách nâng cấp, và không
gợi ý khách gỡ app.

## 3. Giá & giới hạn gói Free

- *"I am not using a lot of pages and find $20 monthly is expensive"* → được giảm 20%/6 tháng
  hoặc 10% gói năm.
- Lý do gỡ trong khảo sát: *"Too expensive, Not using app now"* → email đề nghị giảm giá 2 lần,
  khách không trả lời.
- Rất nhiều hội thoại xoay quanh **Free = 1 trang được publish**, và support chủ động mời nâng cấp
  trong hầu hết các hội thoại với khách Free.

**Đề xuất:**
- **Tạm dừng gói** (giữ dữ liệu, $0–5/tháng) thay vì gỡ app: hợp với nhóm "not using app now".
- Gói rẻ cho shop cần 2–3 trang (gói hiện tại tính theo tính năng, khách thì nghĩ theo số trang).
- Đo hiệu quả mã giảm giá giữ chân: bao nhiêu % khách nhận mã thực sự ở lại sau 3 tháng.

## 4. Lỗi làm mất nội dung / vỡ trang

Gặp trong mẫu: ảnh landing page biến mất (lặp lại), lỗi chọn variant trên trang live, phần tử
Pricing bị mất, publish Market Page lỗi, AI tạo trang lỗi, kết quả AI không đạt nhưng vẫn trừ credit.
Dev xử lý nhanh, nhưng **lỗi mất dữ liệu là lý do mạnh nhất khiến khách dựng lại site ở chỗ khác**.

**Đề xuất:** tự động lưu phiên bản (version history) + nút "khôi phục"; cảnh báo khi xoá ảnh trong
thư viện đang được trang khác dùng; hoàn credit AI khi khách đánh giá "không đạt".

## 5. Đối thủ

- *"im switching to pagefly since it's more comfortable for my new dev"*: dev mới quen PageFly.
- Một số shop dùng song song GemPages cho store lớn (1000+ sản phẩm) và PageFly cho thị trường riêng.
- Chiều ngược lại cũng có: khách hỏi **dịch vụ chuyển trang từ PageFly sang EComposer**. Đây là
  điểm mạnh nên quảng bá rộng hơn.

---

## Vấn đề về quy trình support (cần xử lý nội bộ)

1. **Nhãn trong Crisp như "stupid user", "stupid customer", "difficult customer".** Nên đổi tên
   ngay (ví dụ `needs-extra-guidance`). Lý do: rủi ro nếu bị lộ khi xuất dữ liệu hay chụp màn hình,
   và nhãn kiểu này ảnh hưởng cách nhân viên tiếp nhận khách.
2. **Quá tải và giới hạn AI agent:** có tin "we are overloaded now", và Hugo AI hết hạn mức nên
   phải chuyển cho người. Nên kiểm tra thời gian phản hồi lần đầu theo giờ trong ngày.
3. **Gỡ app sạch:** muốn gỡ không để lại code thì khách phải *cài lại app* rồi làm theo tài liệu.
   Nên có nút "Gỡ sạch" ngay trong app, chạy trước khi khách bấm uninstall.
4. **Tận dụng nhãn sẵn có:** Crisp đã có các nhãn `refund`, `uninstall app`, `1 star`, `bad rate`,
   `20% discount given`, `cs_upsell_success`. Nếu gắn nhãn đều tay thì có thể đếm tự động mỗi tuần.

---

## Việc nên làm trong 2 tuần tới

| Ưu tiên | Việc | Ai | Đo bằng |
|---|---|---|---|
| 1 | Refund theo tỉ lệ + refund đầy đủ trong 7 ngày cho gói năm | Billing + Lead CS | Số review 1–2★ nhắc "refund"/"charged" |
| 2 | Kịch bản phản hồi khi khách muốn rời: hỏi lý do 1 lần, không phản bác lý do | Lead CS | Tỉ lệ hội thoại refund có review xấu |
| 3 | Email nhắc gia hạn gói năm 7 ngày và 3 ngày trước | Dev/Marketing | Số yêu cầu refund gói năm |
| 4 | Đổi tên các nhãn tiêu cực trong Crisp | Lead CS | — |
| 5 | Đánh giá chế độ sửa nhanh trên mobile | Product | Số chat nhắc mobile/tablet |
| 6 | Gói "tạm dừng" thay cho gỡ app | Product | Tỉ lệ khách tạm dừng rồi quay lại |

## Bước tiếp theo về dữ liệu

- Kết hợp với **Partner API** (cài/gỡ/huỷ gói) để đo: khách có yêu cầu refund thì gỡ app nhiều
  hơn bao nhiêu, và gói năm hay gói tháng churn nhiều hơn.
- Chạy phân tích này **hằng tuần** để theo dõi xu hướng.
