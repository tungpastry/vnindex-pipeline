import pandas as pd

def clean_data_vn30_csv(csv_path):
    df_raw = pd.read_csv(csv_path)

    # Đặt lại tên cột (dựa trên cophieu68)
    df_raw.columns = [
        "Ngày", "Giá khớp", "Khối lượng", "Giá mở cửa",
        "Giá cao nhất", "Giá thấp nhất",
        "NN mua", "NN bán", "Giá trị NN"
    ]

    # Loại bỏ dòng trùng tên cột (khi parse HTML)
    df_raw = df_raw[df_raw["Ngày"] != "Ngày"]

    # Chuyển định dạng ngày
    df_raw["date"] = pd.to_datetime(df_raw["Ngày"], format="%d/%m/%Y")

    # Hàm chuyển đổi số có dấu phân cách
    def to_numeric(col):
        return (
            df_raw[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(".", "", regex=False)
            .replace("-", "0")
            .replace("", "0")
            .astype(float)
        )

    # Tạo DataFrame chuẩn hóa
    df = pd.DataFrame()
    df["ticker"] = "VN30"
    df["date"] = df_raw["date"]
    df["open"] = to_numeric("Giá mở cửa")
    df["high"] = to_numeric("Giá cao nhất")
    df["low"] = to_numeric("Giá thấp nhất")
    df["close"] = to_numeric("Giá khớp")
    df["volume"] = to_numeric("Khối lượng")

    # Sắp xếp theo ngày
    df = df.sort_values(by="date").reset_index(drop=True)
    return df

if __name__ == "__main__":
    input_csv = "vn30_raw_42pages.csv"
    output_csv = "vn30_cleaned_ohlc.csv"

    df_cleaned = clean_data_vn30_csv(input_csv)
    df_cleaned.to_csv(output_csv, index=False)

    print(f"✅ Đã xử lý và lưu file: {output_csv}")
    print(f"📊 Số dòng: {len(df_cleaned)}")