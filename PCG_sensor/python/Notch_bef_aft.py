import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, filtfilt

# Đọc tín hiệu gốc từ file CSV
file_path = "D:/Esp-idf/Mysource/inmp441_test/data_text/Filter_test/filter_white_noise_test_1st.csv"  # Đường dẫn tới file CSV
data = pd.read_csv(file_path, header=None)

# Lấy tín hiệu từ cột đầu tiên (giả sử dữ liệu là một cột)
signal = data[0].values

# Thông số của bộ lọc Notch
notch_freq = 50.0  # Tần số nhiễu cần lọc (50Hz)
sample_rate = 4000  # Tần số lấy mẫu

# Tính toán tần số góc w0 và alpha cho bộ lọc Notch
w0 = 2 * np.pi * notch_freq / sample_rate
alpha = np.sin(w0) / (2 * 50)  # Giả sử Q = 30 cho bộ lọc Notch

# Tạo bộ lọc Notch sử dụng scipy
b, a = iirnotch(notch_freq, 50, sample_rate)  # Tạo bộ lọc Notch với Q = 30

# Áp dụng bộ lọc Notch vào tín hiệu
filtered_signal = filtfilt(b, a, signal)

# Tính toán FFT của tín hiệu gốc và tín hiệu đã lọc
fft_signal = np.fft.fft(signal)
fft_filtered_signal = np.fft.fft(filtered_signal)

# Tính tần số và magnitude
frequencies = np.fft.fftfreq(len(signal), d=1/sample_rate)
fft_signal_magnitude = np.abs(fft_signal)
fft_filtered_signal_magnitude = np.abs(fft_filtered_signal)

# Vẽ đồ thị của tín hiệu gốc và tín hiệu đã lọc trên cùng một đồ thị
plt.figure(figsize=(10, 6))

# Đồ thị FFT của tín hiệu gốc (trước khi lọc)
plt.plot(frequencies[:len(frequencies)//2], fft_signal_magnitude[:len(frequencies)//2], color='red', label='Original Signal')

# Đồ thị FFT của tín hiệu đã lọc (sau khi lọc)
plt.plot(frequencies[:len(frequencies)//2], fft_filtered_signal_magnitude[:len(frequencies)//2], color='blue', label='Filtered Signal')

# Thiết lập tiêu đề và nhãn
plt.title("FFT Comparison of Original and Filtered Signal (Notch Filter at 50Hz)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)
plt.xlim(0, 100)  # Giới hạn tần số từ 0Hz đến 100Hz để dễ dàng nhận thấy sự thay đổi ở 50Hz
plt.show()
