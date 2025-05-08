import serial
import csv
import time
from datetime import datetime

# Thiết lập cổng COM và tốc độ baudrate
COM_PORT = 'COM3'
BAUD_RATE = 115200
CSV_FILE = 'max30102_data.csv'

# Mở kết nối serial
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print(f"Đang ghi dữ liệu từ {COM_PORT}... Nhấn Ctrl+C để dừng.")

# Mở file CSV và ghi tiêu đề
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'IR', 'RED'])  # tiêu đề cột

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Ví dụ dòng: "IR:12345,RED:54321"
                try:
                    parts = line.split(',')
                    ir = int(parts[0].split(':')[1])
                    red = int(parts[1].split(':')[1])
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                    # Ghi vào CSV
                    writer.writerow([timestamp, ir, red])
                    print(f"{timestamp} - IR: {ir} | RED: {red}")
                except Exception as e:
                    print(f"Lỗi phân tích dòng: {line} -> {e}")
    except KeyboardInterrupt:
        print("\nGhi dữ liệu kết thúc.")
    finally:
        ser.close()
