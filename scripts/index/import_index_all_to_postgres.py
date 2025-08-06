import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "vsm_db",
    "user": "vsm_user",
    "password": "2025"
}

# Danh sách file và ticker tương ứng
INDEX_FILES = [
    ("VNINDEX", "data/index/vnindex_cleaned_ohlc.csv"),
    ("VN30", "data/index/vn30_cleaned_ohlc.csv"),
    ("HNXINDEX", "data/index/hnx_cleaned_ohlc.csv"),
    ("UPCOM", "data/index/upcom_cleaned_ohlc.csv")
]

def import_to_postgres():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(f"🔗 Đã kết nối tới: postgresql://{DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

        # Xoá toàn bộ bảng trước khi import
        cursor.execute("TRUNCATE index_ohlc_all;")
        conn.commit()
        print("🧹 Đã TRUNCATE bảng index_ohlc_all.")

        for ticker, filepath in INDEX_FILES:
            print(f"📥 Đang import {ticker} từ {filepath} ...")
            df = pd.read_csv(filepath)

            if df.empty:
                print(f"⚠️ File {filepath} trống.")
                continue

            df["ticker"] = ticker
            df = df[["ticker", "date", "open", "high", "low", "close", "volume"]]

            # Ép kiểu dữ liệu rõ ràng
            values = [
                (
                    str(row["ticker"]),
                    pd.to_datetime(row["date"]).date(),
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    int(row["volume"]),
                )
                for _, row in df.iterrows()
            ]

            insert_query = """
                INSERT INTO index_ohlc_all (ticker, date, open, high, low, close, volume)
                VALUES %s;
            """
            execute_values(cursor, insert_query, values)
            conn.commit()
            print(f"✅ Đã import {len(values)} dòng cho {ticker}.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Lỗi khi import vào PostgreSQL:", e)

if __name__ == "__main__":
    import_to_postgres()