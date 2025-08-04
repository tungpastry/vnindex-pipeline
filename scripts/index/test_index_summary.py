import psycopg2

# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "vsm_db",
    "user": "vsm_user",
    "password": "2025"
}

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"🔗 Đã kết nối tới: postgresql://{DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")
        return conn
    except Exception as e:
        print("❌ Lỗi kết nối PostgreSQL:", e)
        return None

def test_count_per_ticker(cursor):
    print("\n📊 Tổng số dòng theo từng chỉ số:")
    try:
        cursor.execute("""
            SELECT ticker, COUNT(*) AS row_count
            FROM index_ohlc_all
            GROUP BY ticker
            ORDER BY ticker;
        """)
        results = cursor.fetchall()
        for ticker, count in results:
            print(f"  • {ticker}: {count} dòng")
    except Exception as e:
        print("❌ Lỗi khi đếm số dòng:", e)

def test_latest_date_per_ticker(cursor):
    print("\n📅 Ngày gần nhất có dữ liệu theo từng chỉ số:")
    try:
        cursor.execute("""
            SELECT ticker, MAX(date) as latest_date
            FROM index_ohlc_all
            GROUP BY ticker
            ORDER BY ticker;
        """)
        results = cursor.fetchall()
        for ticker, latest_date in results:
            print(f"  • {ticker}: {latest_date}")
    except Exception as e:
        print("❌ Lỗi khi truy vấn ngày gần nhất:", e)

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        test_count_per_ticker(cursor)
        test_latest_date_per_ticker(cursor)
        cursor.close()
        conn.close()
