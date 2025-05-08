import serial
import csv
import time

# Thiết lập serial (chỉnh lại 'COM3' và baudrate theo ESP32 của bạn)
ser = serial.Serial('COM3', 115200, timeout=1)
fs = 4000  # tần số lấy mẫu (Hz) - PCG cần tần số cao
duration = 5  # thời gian thu tín hiệu (giây)
num_samples = fs * duration

# Mở file CSV để ghi
with open('pcg_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Amplitude'])  # tiêu đề

    start_time = time.time()
    sample_count = 0

    try:
        while sample_count < num_samples:
            raw_line = ser.readline().decode('utf-8').strip()
            if raw_line:
                try:
                    value = int(raw_line)
                    if 0 <= value <= 4095:  # 12-bit ADC chuẩn
                        timestamp = time.time() - start_time
                        writer.writerow([f"{timestamp:.6f}", value])
                        sample_count += 1
                except ValueError:
                    print(f"Dữ liệu lỗi: {raw_line}")
                    continue

    except KeyboardInterrupt:
        print("\nDừng thu thập.")
    finally:
        ser.close()
        print("Đã lưu xong dữ liệu PCG vào file CSV.")
