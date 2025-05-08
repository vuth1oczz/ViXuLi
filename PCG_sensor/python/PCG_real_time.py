import serial
import matplotlib.pyplot as plt
from collections import deque

# Kết nối Serial với ESP32
ser = serial.Serial('COM3', 115200, timeout=1)  # Thay đổi cổng nếu cần
fs = 4000  # Tần số lấy mẫu 1000Hz - phù hợp với tín hiệu âm thanh PCG
buffer_size = fs * 10  # Lưu 10 giây dữ liệu - có thể tăng nếu cần

# Khởi tạo buffer lưu tín hiệu PCG thô
time_buffer = deque(maxlen=buffer_size)
raw_buffer = deque(maxlen=buffer_size)

# Thiết lập đồ thị real-time
plt.ion()
fig, ax = plt.subplots(figsize=(12, 6))

# Đồ thị tín hiệu âm thanh thô
line_raw, = ax.plot([], [], 'b-', label="Raw PCG Signal")

# Cấu hình trục ban đầu
ax.set_xlim(0, 10)  # Giới hạn ban đầu là 10 giây
ax.set_ylim(-32768, 32767)  # Giả sử INMP441 cho giá trị 16-bit signed
ax.grid(True)
ax.legend()
ax.set_title("Real-Time Raw PCG Signal from INMP441")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Raw Amplitude")

while True:
    try:
        # Đọc dữ liệu thô từ Serial
        raw_data = ser.readline().decode('utf-8').strip()
        if raw_data:
            try:
                # Chuyển dữ liệu thô thành số nguyên (không xử lý thêm)
                raw_value = int(raw_data)

                # Cập nhật buffer với dữ liệu thô
                current_time = len(time_buffer) / fs
                time_buffer.append(current_time)
                raw_buffer.append(raw_value)

                # Cập nhật đồ thị với dữ liệu thô
                line_raw.set_data(list(time_buffer), list(raw_buffer))

                # Điều chỉnh trục X để luôn hiển thị từ 0 đến thời điểm hiện tại
                ax.set_xlim(0, max(10, current_time))  # Đảm bảo hiển thị ít nhất 10 giây

                # Tự động điều chỉnh trục Y dựa trên dữ liệu thô
                if len(raw_buffer) > 1:  # Đảm bảo có ít nhất 2 điểm để tính min/max
                    ax.set_ylim(min(raw_buffer) * 1.05, max(raw_buffer) * 1.05)

                plt.draw()
                plt.pause(0.001)  # Giảm độ trễ để tăng tốc độ cập nhật

            except ValueError:
                print(f"Dữ liệu thô không hợp lệ: {raw_data}")
                continue

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
        break
    except Exception as e:
        print(f"Lỗi: {e}")
        continue

# Đóng kết nối Serial
ser.close()
plt.ioff()
plt.show()