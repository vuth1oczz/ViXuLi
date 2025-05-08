import matplotlib.pyplot as plt
import csv

# Đọc dữ liệu từ file CSV
time_data = []
red_data = []
ir_data = []

with open('ppg_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề
    for row in reader:
        if len(row) == 3:
            try:
                time_data.append(float(row[0]))
                red_data.append(int(row[1]))
                ir_data.append(int(row[2]))
            except ValueError:
                continue  # Bỏ qua dòng lỗi

# Vẽ tín hiệu
plt.figure(figsize=(10, 6))

# Red PPG
plt.plot(time_data, red_data, label='Red PPG', color='red')

# IR PPG
plt.plot(time_data, ir_data, label='IR PPG', color='blue')

plt.title("PPG Signal from MAX30102")
plt.xlabel("Time (s)")
plt.ylabel("Intensity")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
