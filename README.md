# 🇻🇳 VNIndex Pipeline – Dự án thu thập & xử lý dữ liệu chỉ số thị trường chứng khoán Việt Nam

Dự án này giúp bạn:
- ✅ Thu thập lịch sử giá chỉ số từ [cophieu68.vn](https://www.cophieu68.vn)
- ✅ Làm sạch và chuẩn hóa dữ liệu theo format chuẩn: `ticker, date, open, high, low, close, volume`
- ✅ Lưu dữ liệu vào PostgreSQL để truy vấn dễ dàng
- ✅ Hỗ trợ các chỉ số: `VNINDEX`, `VN30`, `HNXINDEX`, `UPCOM`

---

## 🏗️ Cấu trúc dự án

vnindex-pipeline/
├── data/index/ # File dữ liệu .csv đã được làm sạch
├── scripts/index/ # Script xử lý và import vào DB
│ ├── fetch_.py # Lấy dữ liệu từng chỉ số
│ ├── clean_and_export_.py # Làm sạch dữ liệu từng chỉ số
│ ├── import_index_all_to_postgres.py
│ └── test_index_summary.py
├── requirements.txt # Thư viện cần cài
├── .env.example # Biến môi trường mẫu
└── README.md # Tài liệu hướng dẫn


---

## ⚙️ Cài đặt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
🧪 Cách sử dụng
Lấy dữ liệu lịch sử cho từng chỉ số:

python scripts/index/fetch_vnindex_cophieu68.py
Làm sạch dữ liệu:

python scripts/index/clean_and_export_vnindex.py
Import toàn bộ chỉ số vào PostgreSQL:

python scripts/index/import_index_all_to_postgres.py
Kiểm tra dữ liệu đã lưu:

python scripts/index/test_index_summary.py
🐘 Kết nối PostgreSQL
Điền thông tin DB vào file .env dựa trên .env.example.

🧠 Liên hệ
Dự án phát triển bởi nhóm VSM AI Mentor – hỗ trợ AI truy vấn dữ liệu chứng khoán Việt Nam bằng tiếng Việt.

---

### 🔐 `.env.example`

```env
# PostgreSQL config
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vsm_db
DB_USER=vsm_user
DB_PASSWORD=your_password_here
