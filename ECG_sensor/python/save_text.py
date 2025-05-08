import serial
import csv
import time

# Cấu hình Serial - chỉnh lại 'COM3' nếu cần
ser = serial.Serial('COM3', 115200, timeout=1)

fs = 100000           # Tần số lấy mẫu cao (100kHz)
duration = 5          # Thời gian thu (giây)
num_samples = fs * duration  # Tổng số mẫu

# Mở file CSV để ghi
with open('ecg_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Amplitude'])

    start_time = time.time()
    count = 0

    try:
        while count < num_samples:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    value = int(line)
                    if 0 <= value <= 4095:  # Nếu ADC 12-bit
                        timestamp = time.time() - start_time
                        writer.writerow([f"{timestamp:.8f}", value])
                        count += 1
                except ValueError:
                    continue
    except KeyboardInterrupt:
        print("\nDừng thu thập.")
    finally:
        ser.close()
        print("✅ Đã lưu xong tín hiệu ECG vào ecg_data.csv.")
