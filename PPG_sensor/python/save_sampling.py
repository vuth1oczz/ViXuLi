

# import serial
# import numpy as np
# import matplotlib.pyplot as plt
# from collections import deque

# # Kết nối Serial với ESP32
# ser = serial.Serial('COM3', 115200, timeout=1)  # Thay đổi cổng nếu cần
# fs = 100  # Tần số lấy mẫu 100Hz - phù hợp với MAX30102
# buffer_size = fs * 10  # Lưu 10 giây dữ liệu

# # Khởi tạo buffer lưu tín hiệu PPG
# time_buffer = deque(maxlen=buffer_size)
# red_buffer = deque(maxlen=buffer_size)
# ir_buffer = deque(maxlen=buffer_size)

# # Thiết lập đồ thị real-time
# plt.ion()
# fig, (ax_red, ax_ir) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# # Đồ thị Red và IR - Sửa lỗi cú pháp ở đây
# line_red, = ax_red.plot([], [], 'r-', label="Red PPG")  # 'r-' thay vì "red"
# line_ir, = ax_ir.plot([], [], 'b-', label="IR PPG")     # 'b-' thay vì b'-'

# # Cấu hình trục
# for ax in (ax_red, ax_ir):
#     ax.set_xlim(0, 10)
#     ax.set_ylim(0, 262143)  # MAX30102 thường cho giá trị 18-bit
#     ax.grid(True)
#     ax.legend()
# ax_red.set_title("MAX30102 PPG Signal")
# ax_red.set_ylabel("Red Intensity")
# ax_ir.set_ylabel("IR Intensity")
# ax_ir.set_xlabel("Time (s)")

# # Hàm kiểm tra giá trị hợp lệ
# def is_valid_sample(red, ir):
#     return (0 <= red <= 262143) and (0 <= ir <= 262143)

# while True:
#     try:
#         # Đọc dữ liệu từ Serial
#         raw_data = ser.readline().decode('utf-8').strip()
#         if raw_data:
#             try:
#                 parts = raw_data.split(",")
#                 if len(parts) == 2:
#                     red = int(parts[0])
#                     ir = int(parts[1])

#                     # Kiểm tra dữ liệu hợp lệ
#                     if is_valid_sample(red, ir):
#                         # Cập nhật buffer
#                         current_time = len(time_buffer) / fs
#                         time_buffer.append(current_time)
#                         red_buffer.append(red)
#                         ir_buffer.append(ir)

#                         # Cập nhật đồ thị
#                         line_red.set_data(list(time_buffer), list(red_buffer))
#                         line_ir.set_data(list(time_buffer), list(ir_buffer))

#                         # Điều chỉnh giới hạn trục X
#                         if current_time > 10:
#                             ax_red.set_xlim(current_time - 10, current_time)
#                             ax_ir.set_xlim(current_time - 10, current_time)

#                         # Tự động điều chỉnh trục Y dựa trên dữ liệu gần nhất
#                         if len(red_buffer) > 10:
#                             recent_red = list(red_buffer)[-fs:]  # 1 giây gần nhất
#                             recent_ir = list(ir_buffer)[-fs:]
#                             ax_red.set_ylim(min(recent_red) * 0.95, max(recent_red) * 1.05)
#                             ax_ir.set_ylim(min(recent_ir) * 0.95, max(recent_ir) * 1.05)

#                         plt.draw()
#                         plt.pause(0.001)  # Giảm độ trễ để tăng tốc độ cập nhật

#             except ValueError:
#                 print(f"Dữ liệu không hợp lệ: {raw_data}")
#                 continue

#     except KeyboardInterrupt:
#         print("\nĐã dừng chương trình.")
#         break
#     except Exception as e:
#         print(f"Lỗi: {e}")
#         continue

# # Đóng kết nối Serial
# ser.close()
# plt.ioff()
# plt.show()

# import serial
# import numpy as np
# import matplotlib.pyplot as plt
# from collections import deque

# # Kết nối Serial với ESP32
# ser = serial.Serial('COM3', 115200, timeout=1)  # Thay đổi cổng nếu cần
# fs = 100  # Tần số lấy mẫu 100Hz - phù hợp với MAX30102
# buffer_size = fs * 10  # Lưu 10 giây dữ liệu - có thể tăng nếu cần

# # Khởi tạo buffer lưu tín hiệu PPG
# time_buffer = deque(maxlen=buffer_size)
# red_buffer = deque(maxlen=buffer_size)
# ir_buffer = deque(maxlen=buffer_size)

# # Thiết lập đồ thị real-time
# plt.ion()
# fig, (ax_red, ax_ir) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# # Đồ thị Red và IR
# line_red, = ax_red.plot([], [], 'r-', label="Red PPG")
# line_ir, = ax_ir.plot([], [], 'b-', label="IR PPG")

# # Cấu hình trục ban đầu
# for ax in (ax_red, ax_ir):
#     ax.set_xlim(0, 10)  # Giới hạn ban đầu là 10 giây
#     ax.set_ylim(0, 262143)  # MAX30102 thường cho giá trị 18-bit
#     ax.grid(True)
#     ax.legend()
# ax_red.set_title("MAX30102 PPG Signal")
# ax_red.set_ylabel("Red Intensity")
# ax_ir.set_ylabel("IR Intensity")
# ax_ir.set_xlabel("Time (s)")

# # Hàm kiểm tra giá trị hợp lệ
# def is_valid_sample(red, ir):
#     return (0 <= red <= 262143) and (0 <= ir <= 262143)

# while True:
#     try:
#         # Đọc dữ liệu từ Serial
#         raw_data = ser.readline().decode('utf-8').strip()
#         if raw_data:
#             try:
#                 parts = raw_data.split(",")
#                 if len(parts) == 2:
#                     red = int(parts[0])
#                     ir = int(parts[1])

#                     # Kiểm tra dữ liệu hợp lệ
#                     if is_valid_sample(red, ir):
#                         # Cập nhật buffer
#                         current_time = len(time_buffer) / fs
#                         time_buffer.append(current_time)
#                         red_buffer.append(red)
#                         ir_buffer.append(ir)

#                         # Cập nhật đồ thị
#                         line_red.set_data(list(time_buffer), list(red_buffer))
#                         line_ir.set_data(list(time_buffer), list(ir_buffer))

#                         # Điều chỉnh trục X để luôn hiển thị từ 0 đến thời điểm hiện tại
#                         ax_red.set_xlim(0, max(10, current_time))  # Đảm bảo hiển thị ít nhất 10 giây
#                         ax_ir.set_xlim(0, max(10, current_time))

#                         # Tự động điều chỉnh trục Y dựa trên toàn bộ dữ liệu
#                         if len(red_buffer) > 1:  # Đảm bảo có ít nhất 2 điểm để tính min/max
#                             ax_red.set_ylim(min(red_buffer) * 0.95, max(red_buffer) * 1.05)
#                             ax_ir.set_ylim(min(ir_buffer) * 0.95, max(ir_buffer) * 1.05)

#                         plt.draw()
#                         plt.pause(0.001)  # Giảm độ trễ để tăng tốc độ cập nhật

#             except ValueError:
#                 print(f"Dữ liệu không hợp lệ: {raw_data}")
#                 continue

#     except KeyboardInterrupt:
#         print("\nĐã dừng chương trình.")
#         break
#     except Exception as e:
#         print(f"Lỗi: {e}")
#         continue

# # Đóng kết nối Serial
# ser.close()
# plt.ioff()
# plt.show()

import serial
import csv
import time

# Kết nối Serial với ESP32
ser = serial.Serial('COM3', 115200, timeout=1)
fs = 100  # Tần số lấy mẫu
duration = 10  # Thời gian thu thập (giây)
num_samples = fs * duration * 100

# Tạo và mở file CSV
with open('ppg_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Red', 'IR'])  # Ghi tiêu đề cột

    start_time = time.time()
    sample_count = 0

    try:
        while sample_count < num_samples:
            raw_data = ser.readline().decode('utf-8').strip()
            if raw_data:
                try:
                    parts = raw_data.split(",")
                    if len(parts) == 2:
                        red = int(parts[0])
                        ir = int(parts[1])

                        if 0 <= red <= 262143 and 0 <= ir <= 262143:
                            current_time = time.time() - start_time
                            writer.writerow([f"{current_time:.3f}", red, ir])
                            sample_count += 1
                except ValueError:
                    print(f"Dữ liệu không hợp lệ: {raw_data}")
                    continue

    except KeyboardInterrupt:
        print("\nDừng thu thập dữ liệu.")
    finally:
        ser.close()
        print("Đã đóng cổng serial và lưu file.")
