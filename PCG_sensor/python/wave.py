import matplotlib.pyplot as plt
import csv

# Khởi tạo danh sách để lưu dữ liệu
time_data = []
amplitude_data = []

# Đọc file CSV
with open('pcg_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề

    for row in reader:
        if len(row) == 2:
            try:
                time_data.append(float(row[0]))
                amplitude_data.append(int(row[1]))
            except ValueError:
                continue  # Bỏ qua dòng lỗi

# Vẽ biểu đồ tín hiệu PCG
plt.figure(figsize=(10, 4))
plt.plot(time_data, amplitude_data, color='green', linewidth=1)
plt.title("PCG Signal from INMP412")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (ADC Value)")
plt.grid(True)
plt.tight_layout()
plt.show()
