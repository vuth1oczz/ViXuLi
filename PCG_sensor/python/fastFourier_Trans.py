import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file (giả sử dữ liệu đã ở dạng 16-bit)
data = pd.read_csv("D:\Esp-idf\Mysource\sph0645_test\data_text\data_heartSound_3rd.csv", header=None)
data.columns = ['Amplitude']

# Chuyển dữ liệu thành numpy array và ép kiểu về int16
signal = data['Amplitude'].to_numpy(dtype=np.int16)  # Ép kiểu về số nguyên 16-bit
# Tham số tín hiệu
fs = 4000  # Tần số lấy mẫu (Hz), cần thay đổi theo tín hiệu thực tế    
N = len(signal)  # Số mẫu
T = 1 / fs  # Chu kỳ lấy mẫu    

#Sử dụng windowing để làm mượt phổ tín hiệu  
windowed_signal = signal * np.hanning(len(signal))

# Thực hiện FFT
fft_values = np.abs(np.fft.fft(windowed_signal))
frequencies = np.fft.fftfreq(N, d=T)

# Biên độ (magnitude)
amplitude = 2 / N * np.abs(fft_values)  # Chuẩn hóa biên độ

# Tạo trục thời gian
time = np.linspace(0, N * T, N)

# Vẽ đồ thị
plt.figure(figsize=(12, 8))

# Đồ thị 1: Tín hiệu trong miền thời gian
plt.subplot(2, 1, 1)
plt.plot(time, signal, linewidth=0.7, color='blue')
plt.title("Miền thời gian (Time Domain)")
plt.xlabel("Thời gian (s)")
plt.ylabel("Cường độ sóng âm")
plt.grid()

# Đồ thị 2: Phổ tần số (cả âm và dương)
plt.subplot(2, 1, 2)
plt.plot(frequencies, amplitude, linewidth=0.7, color='red')
plt.title("Miền tần số (Frequency Domain)")
plt.xlabel("Tần số (Hz)")
plt.ylabel("Cuong do tan so")
plt.grid()

plt.tight_layout()
plt.show()
