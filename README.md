# BIDV Home Finance – Python MVP

Ứng dụng web viết bằng Python + Streamlit.

## 1. Yêu cầu
- Python 3.10 trở lên
- Kết nối Internet để tải font và ảnh minh họa từ Unsplash (có thể thay bằng ảnh nội bộ)

## 2. Cài đặt trên Windows
Mở Command Prompt tại thư mục dự án và chạy:

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
streamlit run app.py
```

Trình duyệt thường tự mở tại `http://localhost:8501`.

Nếu lệnh `py` không hoạt động, thử `python` thay thế.

## 3. Chức năng
- Landing page responsive.
- Hai nhóm sản phẩm vay và bảng lãi suất tham khảo.
- Máy tính khoản vay: gốc đều hoặc trả góp đều, có ân hạn gốc.
- Xem 12 kỳ trả nợ đầu tiên.
- Form đăng ký tư vấn, kiểm tra dữ liệu và lưu SQLite vào `leads.db`.
- Nút gọi điện và mở Zalo theo số 0989211684.

## 4. Zalo
Liên kết đang dùng: https://zalo.me/0989211684

Liên kết này đưa khách hàng tới tài khoản/hồ sơ hoặc cuộc trò chuyện Zalo tương ứng nếu tài khoản tồn tại và Zalo hỗ trợ trên thiết bị. Website không thể tự gửi tin nhắn thay khách hàng.

## 5. Dữ liệu khách hàng
Form ghi dữ liệu vào file `leads.db` trên máy đang chạy ứng dụng. Đây chỉ là cách lưu đơn giản cho MVP. Không đưa ứng dụng lên Internet để thu thập dữ liệu thật trước khi:
- triển khai HTTPS;
- giới hạn quyền truy cập và bảo vệ file database;
- bổ sung chính sách quyền riêng tư, thông báo mục đích xử lý và thời hạn lưu dữ liệu;
- xác định cơ sở pháp lý và quy trình xử lý yêu cầu của chủ thể dữ liệu;
- cấu hình sao lưu và kiểm soát truy cập.

Không thu thập CCCD, thông tin tài khoản ngân hàng hay dữ liệu nhạy cảm qua form mẫu này.

## 6. Kiểm tra trước khi công bố
- Xác minh số điện thoại và tài khoản Zalo của chuyên viên.
- Xác minh chính sách lãi suất, tỷ lệ vay, thời hạn, ân hạn và danh sách dự án.
- Xin phép sử dụng logo, tên thương hiệu và các tài liệu nhận diện BIDV.
- Thay nội dung minh họa bằng nội dung đã được phê duyệt.

## 7. Lưu ý máy tính
Công cụ mô phỏng lãi suất cố định trong toàn kỳ; thời gian ân hạn chỉ trả lãi, phần gốc chia đều hoặc tính trả góp đều trong thời gian còn lại. Kết quả không phải lịch trả nợ do ngân hàng phê duyệt.
