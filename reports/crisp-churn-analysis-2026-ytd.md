# Phân tích churn từ Crisp: 1/1/2026 – 13/11/2026

**Nguồn:** Crisp workspace EComposer, đọc qua kết nối MCP ngày 13/11/2026.
**Dữ liệu từng ca:** `reports/data/crisp-churn-cases-2026.csv` (đã bỏ tên, email, tên shop; giữ mã hội thoại Crisp để team tra lại).

---

## 1. Tóm tắt

1. **Hơn một nửa số ca rời bỏ đi kèm tranh chấp hoá đơn** (17/31 ca). Kiểu phổ biến nhất (11 ca): khách huỷ, hạ gói hoặc gỡ app vài ngày *sau* khi chu kỳ mới bắt đầu, vẫn bị tính đủ tháng, rồi bị từ chối refund. Đây là điểm ma sát lớn nhất và lặp lại đều từ tháng 1 đến tháng 11.
2. **Lý do rời bỏ hàng đầu là tiền, không phải sản phẩm.** 8/31 ca nói thẳng "không đủ tiền" hoặc "đắt"; 7/31 ca là shop đóng, tạm dừng, hoặc người cài app đã nghỉ. Hai nhóm này cộng lại gần một nửa.
3. **Lỗi làm mất nội dung và AI lỗi ở lần dùng đầu** là lý do sản phẩm rõ nhất (4 ca). Hai trong bốn ca gỡ app ngay trong ngày gặp lỗi.
4. **Trong 3 review thấp sao tìm thấy, 2 review nói thẳng nguyên nhân là cách xử lý refund**, và cả hai đều của khách đã dùng app 3 năm. Review còn lại do lỗi mất ảnh.
5. **Email hỏi lý do sau khi gỡ app gần như không ai trả lời.** Trong khoảng 30 email gửi tháng 10 mà tôi thấy, không có ca nào có phản hồi.
6. **Đối thủ chảy cả hai chiều.** Có khách sang PageFly, nhưng cũng có khách bỏ gói GemPages €158/tháng để sang EComposer vì khả năng dựng trang bằng AI. Crisp chưa cho thấy Horizon/Sidekick là lý do rời bỏ, nhưng nhóm này thường bỏ đi mà không nhắn support.

> **Đọc các con số thế nào:** đây là mẫu 31 ca được tìm bằng từ khoá và đọc toàn văn, không phải thống kê toàn bộ. Tỉ lệ cho biết *vấn đề nào lặp lại*, không cho biết *tỉ lệ churn thật*. Xem mục 2.

---

## 2. Phạm vi, phương pháp và giới hạn

**Cách làm**

- Chạy 33 lượt tìm kiếm trong Crisp với các từ khoá: `refund`, `refunded`, `cancel`, `cancellation`, `downgrade`, `uninstall`, `uninstalled`, `expensive`, `disappointed`, `useless`, `scam`, `switching`, `pagefly`, `gempages`, `shogun`, `horizon`, `remboursement`, cùng một số cụm khác.
- Lọc lấy hội thoại của EComposer có hoạt động trong năm 2026. Workspace này còn nhận thư của Fontify, EcomRise, Stockify, Lookbook và khá nhiều thư rác; các phần đó bị loại.
- Đọc toàn văn **41 hội thoại**, chọn rải theo tháng. Trong đó **31 ca** có sự kiện rời bỏ rõ ràng (gỡ app, huỷ gói, hạ gói, hoặc xin refund vì nghỉ dùng). 10 hội thoại còn lại là khách đang cân nhắc, câu hỏi trước khi mua, review tốt, hoặc thư rác.

**Giới hạn cần biết**

| Giới hạn | Ảnh hưởng |
|---|---|
| Mỗi lượt tìm Crisp chỉ trả về ~40 kết quả mới nhất, không lọc được theo ngày | Mẫu **lệch về tháng 9–11** (12/31 ca rơi vào tháng 10). Không dùng bảng theo tháng để kết luận churn tăng hay giảm. Tháng 3 không có ca nào trong mẫu, nhiều khả năng do tìm không tới chứ không phải không có. |
| Tìm bằng từ khoá refund/cancel | Mẫu **lệch về tranh chấp hoá đơn** và về khách trả phí. Khách Free gỡ app thường không nhắn support. |
| Tìm theo nhãn (segment) của Crisp không hoạt động qua kết nối này | Không đếm được theo các nhãn sẵn có như `refund`, `uninstalled`, `1 star`. |
| Thư thông báo review của Shopify có về Crisp, nhưng không lọc được theo số sao | Chỉ bắt được 3 review thấp sao. Muốn đủ cần đọc trực tiếp trang review. |
| Crisp không có dữ liệu cài/gỡ/doanh thu | Không tính được tỉ lệ churn, free-to-paid hay MRR. Cần Partner API. |

---

## 3. Bức tranh chung từ 31 ca

### 3.1 Lý do rời bỏ chính

| Lý do chính | Số ca | Tỉ lệ |
|---|---|---|
| Giá / tài chính ("không đủ tiền", "đắt") | 8 | 26% |
| Không còn nhu cầu: shop đóng, tạm dừng, đổi người phụ trách | 7 | 23% |
| Không rõ (khách không nói) | 6 | 19% |
| Lỗi, mất dữ liệu, AI lỗi | 4 | 13% |
| Sang đối thủ / đang thử app khác | 2 | 6% |
| Không sửa được trên điện thoại | 2 | 6% |
| Tích hợp app bên thứ ba | 1 | 3% |
| Mua nhầm gói năm | 1 | 3% |

### 3.2 Tranh chấp hoá đơn đi kèm

| Kiểu tranh chấp | Số ca |
|---|---|
| Bị tính chu kỳ mới sau khi (hoặc ngay trước khi) huỷ, hạ gói, gỡ app | 11 |
| Liên quan gói năm (mua nhầm, tự gia hạn, không đủ tiền, lỗi sản phẩm) | 4 |
| Khác (app không chạy, huỷ 5 ngày sau khi trả) | 2 |
| **Tổng có tranh chấp** | **17 / 31 (55%)** |

### 3.3 Kết quả của 17 yêu cầu refund

| Kết quả | Số ca |
|---|---|
| Từ chối | 6 |
| Từ chối lúc đầu, mở lại sau khi có review 1★ | 1 |
| Hoàn toàn bộ | 3 |
| Hoàn một phần theo thời gian chưa dùng | 2 |
| Đang chờ (13+ ngày) | 1 |
| Không hoàn; khách tự tìm câu trả lời ở Shopify | 1 |
| Không rõ kết cục | 3 |

Cả 3 ca hoàn toàn bộ đều xảy ra **sau khi khách leo thang**: một ca nhắn suốt 6 ngày và doạ review xấu, một ca gửi liên tiếp nhiều thư gay gắt trong 1 ngày, một ca đã đăng review 2★.

---

## 4. Phân tích từng nhóm nguyên nhân

### 4.1 Chu kỳ tính phí và refund: vấn đề xuyên suốt cả năm

**Cơ chế.** Shopify tính phí app vào *đầu* mỗi chu kỳ 30 ngày. Chu kỳ của app lại khác ngày với hoá đơn Shopify của shop. Khách thấy khoản phí xuất hiện sau khi họ đã huỷ và kết luận là bị tính sai.

**Các ca theo tháng:**

| Tháng | Tình huống | Kết quả |
|---|---|---|
| 1 | Gỡ app 20/12, chu kỳ mới bắt đầu 10/12. Khách không đủ tiền. Chờ 6 ngày, nhắn nhiều lần: *"I find it funny how any other reply is instant. But billing is mysteriously not taken into high priority"* | Hoàn toàn bộ |
| 2 | Tạm dừng shop, hạ gói trước ngày hoá đơn Shopify nhưng vẫn bị tính $19. Support yêu cầu ảnh chụp hoá đơn 4 lần. | Khách tự hỏi Shopify và tự hiểu ra |
| 4 | Nói đã gỡ app nhưng bị tính tháng 1 và tháng 2; hồ sơ ghi huỷ ngày 11/3 | Từ chối ("chỉ xét trong 7 ngày") |
| 4–5 | Hạ gói 23/4 (giờ Anh), hệ thống ghi 24/4. Bị tính £14.50, được hoàn £3.82. Khách mất 12 ngày để hiểu vì sao. | Hoàn một phần |
| 6–8 | Khách 26 tháng, *"My finances are very limited"*. Hạ gói 12/6. Support bảo **thanh toán hoá đơn xong rồi báo lại để xem xét**. Sáu tuần sau khách gửi hoá đơn đã trả. | Từ chối |
| 6–9 | Đóng shop, gỡ app 4 ngày sau khi chu kỳ mới bắt đầu. *"vous devez me rembourser… voleur"*, doạ khiếu nại. | Từ chối |
| 7 | *"I can't afford to pay that especially I didn't use it anymore"*. Xin gặp cấp trên. | Từ chối ít nhất 4 lần |
| 7 | Khách 3 năm. Được hẹn chờ rồi bị từ chối. | Từ chối → review từ 5★ xuống 3★ |
| 7 | Gỡ app đúng ngày chu kỳ mới bắt đầu; hoá đơn chưa thanh toán; Shopify nói nhà phát triển có thể xin cấp credit | Không rõ |
| 11 | Khách 3 năm, bị tính $25 sau khi ngừng dùng | Từ chối → review 1★ |
| 11 | Đóng shop, nhận thêm hoá đơn sau khi gỡ. Shopify bảo hỏi EComposer, EComposer bảo hỏi Shopify. | Không rõ |

**Ba điều làm tình hình tệ hơn:**

1. **Hẹn rồi từ chối.** Hai ca được bảo "chờ hoá đơn thanh toán xong rồi gửi lại", sau đó bị từ chối theo chính sách. Review 3★ viết: *"all they had to initially tell me was, it was past refund policy"*. Từ chối ngay từ đầu còn ít gây hại hơn.
2. **Bắt khách chứng minh.** Nhiều ca phải gửi ảnh chụp hoá đơn nhiều lần, trong khi thông tin này có trong Partner Dashboard.
3. **Định hướng nội bộ là tìm căn cứ để từ chối.** Trong một ca tháng 7, ghi chú nội bộ nhắc nhân viên rằng mục tiêu là hỏi rõ hoá đơn để xem có từ chối được không, và không nên trả lời như thể chắc chắn sẽ hoàn. Với khoản $19, cách tiếp cận này tốn nhiều giờ support và đổi lại là rủi ro review xấu.

**Gói năm (4 ca, đều trong tháng 9–11):** mua nhầm $468 và bị từ chối trong 7 phút; người cài app đã nghỉ việc, gói tự gia hạn dù không dùng từ 2025 (được hoàn $175 sau khi bị hỏi lý do 3 lần); không đủ tiền (mở từ 31/10, đến 12/11 vẫn đang xem xét); ảnh bị mất nhiều lần (hoàn toàn bộ sau review 2★).

### 4.2 Giá và tài chính (8 ca)

Phần lớn không chê app. Họ nói về hoàn cảnh của mình:

- *"Just need you to stop billing me please as I can't afford it!"* (tháng 1)
- *"It's very difficult time for my business right now, I will need this money."* (tháng 6)
- *"the payments are overwhelming me and i have other things to focus on"* (tháng 10)
- *"unfortunately I cannot afford it"* (tháng 11)

Hai chi tiết về cách trình bày giá:

- Một khách thấy chỗ ghi $19, chỗ ghi $25 và cho là sai lệch ($19 là giá theo tháng của gói năm).
- Cùng khách đó: *"i don't think it's fair that the free plan have one page available, i wasn't even able to see if it was applicable for my needs before upgrading"*.

Ở những ca có ghi chú phân tích tự động trong Crisp, shop rời bỏ thường có doanh thu thấp (từ $0 đến khoảng $1.000/tháng). Với họ $19–25/tháng là khoản đáng kể. Đề nghị giảm 20% trong 6 tháng ít có tác dụng với người đang nói "không đủ tiền".

### 4.3 Không còn nhu cầu, shop đóng, đổi người phụ trách (7 ca)

- **Shop đóng hoặc tạm dừng (3 ca).** Không giữ được, nhưng cả 3 đều thành tranh chấp hoá đơn.
- **Đã gỡ và không dùng nữa nhưng vẫn bị tính phí (1 ca).**
- **Người tiếp quản không biết app làm gì (3 ca).**
  - *"I want to cancel this service as I don't even know what it's doing. However, no one can tell me if the store will crash if I do."* (tháng 8)
  - *"My developer installed this app, not me… I am going to get this app uninstalled and let them worry about it."* (tháng 10)
  - *"The app was originally installed by a former colleague."* (tháng 9)
- Ở ca tháng 8, support trả lời rằng nếu huỷ thì các trang đang chạy sẽ bị xoá khỏi shop. Đúng về kỹ thuật, nhưng khách chỉ nhận được lời cảnh báo mà không được cho thấy app đang mang lại gì.

### 4.4 Lỗi, mất dữ liệu, AI lỗi (4 ca rời bỏ, cộng nhiều tín hiệu rủi ro)

| Tháng | Chuyện gì xảy ra | Thời gian đến lúc gỡ |
|---|---|---|
| 4 | AI tạo trang không chạy. *"the app never worked and I was never able to use it"* | Vài ngày |
| 5 | Shop doanh thu ~$5.200/tháng, mua AI credit, AI lỗi do mất kết nối server. *"I use another page builder I was just trying to try this one out"* | **30 phút** |
| 7 | Gói Pro, shop 9 ngày tuổi. *"everything deleted!!!! why you have not auto save???"* | **Trong 1,5 giờ** |
| 10 | Gói năm. Ảnh trên trang đang chạy bị mất nhiều lần. Khách dựng lại site ở chỗ khác. | 2 tháng |

Tín hiệu rủi ro ở khách chưa rời đi:

- Tháng 1: *"The first home page generated by the AI was terrible… If I discard something because it gave out something useless why would I buy tokens?"*
- Tháng 3: mất trang chưa lưu, hết token sau 1–2 lần thử. Khách đề nghị có **lịch sử và nút hoàn tác**.
- Tháng 5: nâng lên Pro để dùng tính năng đa thị trường vì support giải thích chưa đúng (support đã nhận lỗi); sau đó gặp lỗi nút Buy Now. *"OMG! Does that app ever work for you??"*

AI vừa là lý do khách đến (xem 4.6), vừa là nơi khách bỏ đi nhanh nhất khi nó lỗi ở lần dùng đầu.

### 4.5 Không sửa được trên điện thoại (2 ca)

- Tháng 9, shop mới, gói Free: *"i have mobile only so i should uninstall it"*. Support xác nhận editor không hỗ trợ mobile và gợi ý gỡ.
- Tháng 11, khách 3 năm: *"I stopped using EComposer because I could no longer edit on mobile."* Từ "no longer" cho thấy trước đây khách làm được. Nên kiểm tra xem có thay đổi nào của editor trong năm 2026 làm mất khả năng này không.

### 4.6 Đối thủ: chảy cả hai chiều

**Rời đi**

- Tháng 2: *"im switching to pagefly since it's more comfortable for my new dev"*.
- Tháng 5: khách đang dùng page builder khác, thử EComposer, AI lỗi, gỡ sau 30 phút.
- Tháng 10: một khách gói Standard gỡ app; theo email của support thì khách đang thử app khác.

**Đến với EComposer**

- Tháng 1: *"left a 158€ subscription Gempages for you… really appreciate the fact that we can empower AI to build great pages"*. Khách này tự dựng quy trình tạo file `.ecom` bằng AI và đề nghị EComposer công bố tài liệu để làm việc đó chính thức. Khách chỉ vướng tương thích với Kaching Bundles; đến tháng 10 thì hạ gói.
- Tháng 3: shop Shopify Plus 9 ngôn ngữ đang dùng PageFly, hỏi về đa ngôn ngữ và giá.
- Tháng 9: chủ nhiều shop đang dùng GemPages (1.000+ sản phẩm), thử EComposer cho shop mới.
- Tháng 10: khách hỏi dịch vụ chuyển 5 trang từ PageFly sang.
- Tháng 11: review 5★: *"I've had a lot more success with eComposer over using the traditional shopify theme editor"*.

**Shopify Horizon / Sidekick.** Các hội thoại nhắc Horizon trong 2026 đều là câu hỏi cách dùng (ví dụ section không hiện trong theme editor với Horizon 4.1.1), chưa có ca nào nói bỏ EComposer để dùng theme editor. Điều này không chứng minh là không có: người chuyển sang công cụ gốc của Shopify không có lý do gì để nhắn support.

### 4.7 Tích hợp bên thứ ba và gỡ app không sạch

- **Kaching Bundles** (tháng 1): lỗi điều hướng sang checkout. Support kết luận lỗi thuộc về app kia và đề nghị khách tự liên hệ. Khách này đang định giới thiệu EComposer cho một nhóm 1.000 merchant.
- **Gỡ app còn sót code** (tháng 7): khách gỡ app, code còn trong theme. Mất 3 ngày, phải cài lại app, nút Reset bị lỗi, hướng dẫn thiếu bước. *"les 2 autres applications auxquelles j'ai fait exactement la même requête ont tout réglé super rapidement."*

---

## 5. Theo vòng đời khách hàng

| Giai đoạn | Số ca xác định được | Lý do điển hình | Tốc độ rời đi |
|---|---|---|---|
| **Mới (< 1 tháng)** | 6 | AI lỗi, mất nội dung, không sửa được trên mobile, mua nhầm gói năm | Trong ngày đến vài ngày |
| **Giữa (2–12 tháng)** | 6 | Tài chính, shop đóng, tương thích app khác | Hạ gói trước, gỡ sau |
| **Lâu năm (> 2 năm)** | 3 | Tài chính, mất khả năng sửa trên mobile | Rời đi kèm tranh chấp hoá đơn và review thấp sao |
| Không rõ thâm niên (gồm 1 ca trên 1 năm) | 16 | | |

Hai nhận xét:

- **Khách mới rời đi vì sản phẩm, khách cũ rời đi vì tiền và vì cách được đối xử lúc ra đi.**
- Khách lâu năm kỳ vọng được châm chước: *"I have been a good client for many years"*, *"Mind you, I've been loyal this app for over 3 years."* Áp cùng một chính sách cứng cho khách 3 năm và khách 3 ngày là nguyên nhân trực tiếp của 2 trong 3 review thấp sao.

---

## 6. Tín hiệu về free-to-paid

Crisp không đo được tỉ lệ chuyển đổi, nhưng cho thấy vài điểm nghẽn:

1. **Gói Free 1 trang không đủ để đánh giá.** Câu hỏi về giới hạn này xuất hiện rất nhiều, và có khách nói thẳng là không thử được trước khi nâng cấp.
2. **Dùng thử 7 ngày phải nhờ support bật tay.** Ca tháng 2: khách đồng ý dùng thử lúc 14:26, đến 22:50 mới được bật. Khi hết hạn, khách nhận một email rồi quay về Free; không có bước nào hỏi họ đã làm được gì.
3. **Mời nâng cấp rất dày.** Tin nhắn "tôi thấy shop bạn đang ở gói Free…" xuất hiện trong phần lớn hội thoại với khách Free. Ghi chú phân tích tự động còn khuyến nghị nâng cấp cho cả shop 2 ngày tuổi, doanh thu $0, 14 lượt truy cập. *Giả thuyết cần kiểm chứng bằng Partner API:* shop bị đẩy lên paid quá sớm sẽ huỷ nhiều hơn.
4. **Phản đối về giá khi cân nhắc nâng cấp:** *"i am not using a lot of pages and find 20$ monthly is expensive"* (shop doanh thu ~$27.000/tháng). Khách nghĩ theo số trang, bảng giá tính theo gói tính năng.
5. **AI credit là cửa vào paid nhưng dễ vỡ.** Hết token sau 1–2 lần thử, kết quả kém vẫn bị trừ. Support hoàn token khi được hỏi, nhưng khách phải hỏi.

---

## 7. Quy trình support

**Điểm mạnh.** Review 5★ trong năm nhắc tên từng nhân viên; lỗi kỹ thuật thường được dev xử lý trong ngày; có dịch vụ chuyển trang từ đối thủ.

**Điểm cần sửa:**

| # | Vấn đề | Bằng chứng |
|---|---|---|
| 1 | Hẹn refund rồi từ chối | 2 ca (tháng 6–8, tháng 7), một ca thành review 3★ |
| 2 | Yêu cầu ảnh chụp hoá đơn nhiều lần | Tháng 2, 7, 9, 10, 11 |
| 3 | Thời gian xử lý refund dài | 6 ngày, 12 ngày, 13+ ngày chưa xong, 6 tuần |
| 4 | Khách bị kẹt với bot | *"J'aimerais arrêter de parler à un bot"* (tháng 10); *"Give me a real person"* (tháng 9). Tháng 10, khách hỏi "gỡ app thì trang của tôi ra sao", bot trả lời về gỡ branding. |
| 5 | AI agent hết hạn mức | Ghi chú "Hugo AI usage limit reached" ngày 21/5 ở 2 hội thoại, khách bị chuyển sang người giữa chừng |
| 6 | Email hỏi lý do sau khi gỡ/hạ gói không có phản hồi | ~30 email (21 sau gỡ app, 9 sau hạ gói) gửi theo đợt các ngày 2, 6, 7, 9, 15, 19/10; không thấy ca nào trả lời |
| 7 | Tin quảng cáo BFCM tự động gửi vào hội thoại của khách đang muốn rời | Tháng 10: một khách trả lời tin BFCM bằng *"hi pls cancel my subscription"* |
| 8 | Giải thích tính năng chưa đúng dẫn đến nâng cấp không cần thiết | Tháng 5 (đa thị trường). Support đã nhận lỗi. |
| 9 | Nhãn Crisp có từ ngữ xúc phạm khách | Đã nêu ở báo cáo trước |

---

## 8. Danh sách ca theo tháng

Mẫu lệch về các tháng gần đây; bảng này để tra cứu, không dùng để so sánh giữa các tháng.

| Tháng | Số ca | Tóm tắt |
|---|---|---|
| 1 | 1 | Không đủ tiền, bị tính phí sau khi gỡ |
| 2 | 2 | Tạm dừng shop; chuyển sang PageFly |
| 3 | 0 | (không tìm tới) |
| 4 | 3 | Bị tính sau khi gỡ; AI không chạy; tranh cãi ngày hạ gói |
| 5 | 1 | AI lỗi lần đầu, gỡ sau 30 phút |
| 6 | 3 | Tài chính (khách 26 tháng); đóng shop; chê đắt |
| 7 | 4 | Không đủ tiền; review 3★ vì refund; mất nội dung do không autosave; gỡ app còn sót code |
| 8 | 1 | Chủ mới không biết app làm gì |
| 9 | 2 | Gói năm tự gia hạn; chỉ có điện thoại |
| 10 | 12 | 4 ca gói năm; 3 ca hạ gói; 3 ca gỡ không rõ lý do; đang thử app khác; dev cài hộ |
| 11 | 2 | Review 1★ (mobile + refund); đóng shop |

---

## 9. Khuyến nghị

### Làm ngay (2–4 tuần)

| # | Việc | Giải quyết | Đo bằng |
|---|---|---|---|
| 1 | **Chính sách refund mới:** tự động hoàn theo ngày chưa dùng khi khách huỷ giữa chu kỳ; hoàn đủ nếu huỷ trong 3 ngày đầu chu kỳ; hoàn đủ gói năm trong 7 ngày đầu | 11 ca chu kỳ + 4 ca gói năm | Số hội thoại refund; số review nhắc "charged"/"refund" |
| 2 | **Nhờ dev kiểm tra tham số `prorate` của `appSubscriptionCancel`** (Shopify Admin API). Nếu dùng được, khi khách bấm hạ gói trong app Shopify sẽ tự cấp credit phần chưa dùng, không cần support can thiệp. | Phần lớn 11 ca chu kỳ | Số ticket billing |
| 3 | **Hiển thị trong app:** ngày gia hạn tiếp theo, số tiền, và câu "nếu huỷ hôm nay bạn dùng được đến ngày X" | Hiểu nhầm về chu kỳ | Số câu hỏi "why was I charged" |
| 4 | **Email nhắc trước khi gia hạn:** gói năm 7 và 3 ngày trước; gói tháng 3 ngày trước nếu shop không mở app 30 ngày qua | Ca "không dùng nhưng vẫn bị tính" | Tỉ lệ refund gói năm |
| 5 | **Quy tắc trả lời refund:** trả lời dứt khoát trong 1 ngày làm việc; không hẹn "chờ rồi tính"; tự tra hoá đơn; không hỏi lý do quá 1 lần | Ca hẹn rồi từ chối | Thời gian xử lý trung vị |
| 6 | **Ngoại lệ cho khách ≥ 12 tháng:** Lead CS được quyền hoàn 1 chu kỳ không cần duyệt | 2 review thấp sao từ khách 3 năm | Review ≤ 3★ từ khách lâu năm |
| 7 | **Tắt tin quảng cáo tự động** cho hội thoại có yêu cầu refund/huỷ trong 30 ngày | Mục 7.7 | — |

### Trong quý (sản phẩm)

| # | Việc | Giải quyết |
|---|---|---|
| 8 | **Autosave và lịch sử phiên bản** trong editor | Ca mất toàn bộ nội dung; đề nghị undo/history; ảnh bị mất |
| 9 | **AI builder:** tự hoàn credit khi lỗi server hoặc khi khách đánh giá "không đạt"; cho lần tạo đầu tiên miễn phí; cảnh báo số credit trước khi chạy | 2 ca gỡ trong ngày đầu, 2 ca rủi ro |
| 10 | **Tuỳ chọn tạm dừng gói** (giữ trang, $0–5/tháng, tối đa 3 tháng) thay cho huỷ | Nhóm tài chính và shop tạm dừng (10+ ca) |
| 11 | **Màn hình khảo sát khi hạ gói hoặc huỷ ngay trong app**, kèm đề nghị phù hợp từng lý do (tạm dừng, hạ gói, giảm giá, đặt lịch hỗ trợ) | Thay cho email không ai trả lời |
| 12 | **Nút "Gỡ sạch"** chạy được trước khi uninstall, không cần cài lại | Ca tháng 7 |
| 13 | **Trang "App này đang làm gì cho shop bạn"**: số trang đang chạy, lượt xem, đơn hàng qua trang EComposer. Gửi email tóm tắt hằng tháng. | Nhóm chủ mới tiếp quản, và mọi khách đang cân nhắc giá |
| 14 | **Sửa nhanh trên mobile** (chữ, ảnh, giá, bật/tắt section); kiểm tra xem 2026 có thay đổi nào làm mất khả năng sửa trên mobile | 2 ca, trong đó 1 review 1★ |
| 15 | **Dùng thử tự bật** không cần support; hỏi lại vào ngày 5 | Mục 6.2 |

### Cơ hội tăng trưởng

| # | Việc | Căn cứ |
|---|---|---|
| 16 | **Công bố tài liệu định dạng `.ecom` và hướng dẫn dựng trang bằng AI bên ngoài** (Claude, ChatGPT) | Khách tháng 1 bỏ GemPages vì điều này và sẵn sàng giới thiệu cho 1.000 merchant |
| 17 | **Đưa dịch vụ chuyển trang từ PageFly/GemPages lên trang chủ và trang giá** | Có khách chủ động hỏi; hiện chỉ biết khi nhắn support |
| 18 | **Danh sách ưu tiên tương thích app** (Kaching Bundles trước), có người chịu trách nhiệm phía EComposer thay vì chuyển khách sang app kia | Ca tháng 1 |

---

## 10. Những gì Crisp không trả lời được

| Câu hỏi | Cần nguồn nào |
|---|---|
| Tỉ lệ gỡ app D1/D7/D30, free-to-paid, paid churn, MRR mất | **Partner API** (bộ công cụ trong repo đã sẵn sàng, cần token) |
| 31 ca này chiếm bao nhiêu phần trăm tổng số gỡ/huỷ | Partner API |
| Shop lên paid quá sớm có huỷ nhiều hơn không | Partner API (mục "tốc độ lên paid" trong báo cáo tuần) |
| Khách Free gỡ app vì sao | Khảo sát gỡ app của Shopify (Partner API) + màn hình khảo sát trong app |
| Toàn bộ review ≤ 3★ trong năm | Trang review Shopify (cần mở quyền truy cập `apps.shopify.com`) |
| Số ca theo từng nhãn Crisp | Gắn nhãn chuẩn (ví dụ `churn:price`, `churn:billing-cycle`, `churn:bug`, `churn:mobile`, `churn:competitor`) rồi xuất từ Crisp |

**Đề xuất bước tiếp theo:** (1) cấp token Partner API để ghép 31 ca này với dữ liệu cài/gỡ thật; (2) thống nhất bộ nhãn `churn:*` trong Crisp để từ tháng sau đếm được đầy đủ thay vì lấy mẫu; (3) chạy lại phân tích này hằng tháng.
