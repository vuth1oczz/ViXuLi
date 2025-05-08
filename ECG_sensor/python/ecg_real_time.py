import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# 📌 1. Kết nối Serial với ESP32
ser = serial.Serial('COM3', 115200, timeout=1)  # Thay COM3 bằng cổng của bạn (Linux: /dev/ttyUSB0)
fs = 100000  # Sampling rate của ADC (Hz)
buffer_size = fs * 5  # 5 giây dữ liệu lưu trữ

# 📌 2. Khởi tạo buffer lưu tín hiệu ECG
time_buffer = deque(maxlen=buffer_size)
ecg_buffer = deque(maxlen=buffer_size)

plt.ion()  # Kích hoạt chế độ vẽ real-time
fig, ax = plt.subplots(figsize=(12, 5))
line, = ax.plot([], [], label="Real-time ECG", color="blue")

while True:
    try:
        # 📌 3. Đọc dữ liệu ADC từ Serial
        raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
        if raw_data.isdigit():
            adc_value = int(raw_data)
            voltage = adc_value * (3.3 / 4095)  # Chuyển về điện áp

            # 📌 4. Cập nhật buffer
            time_buffer.append(len(time_buffer) / fs)
            ecg_buffer.append(voltage)

            # 📌 5. Vẽ tín hiệu
            line.set_xdata(time_buffer)
            line.set_ydata(ecg_buffer)
            ax.set_xlim(max(0, len(time_buffer) / fs - 5), len(time_buffer) / fs)
            ax.set_ylim(min(ecg_buffer), max(ecg_buffer))
            plt.draw()
            plt.pause(0.01)

    except KeyboardInterrupt:
        print("\nĐã dừng nhận dữ liệu ECG.")
        break

ser.close()
