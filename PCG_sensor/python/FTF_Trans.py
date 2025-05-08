import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Đọc tín hiệu đã lọc từ file CSV
file_path = "D:/Esp-idf/Mysource/inmp441_test/data_text/Filter_test/filter_white_noise_test_2nd.csv"
data = pd.read_csv(file_path, header=None)

# Lấy tín hiệu từ cột đầu tiên (giả sử dữ liệu là một cột)
signal = data[0].values

# Tính toán FFT của tín hiệu
fft_signal = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), d=1/4000)  # Giả sử sample rate là 4000Hz

# Lọc phần thực và phần ảo của FFT
fft_magnitude = np.abs(fft_signal)

# Vẽ đồ thị FFT
plt.plot(frequencies[:len(frequencies)//2], fft_magnitude[:len(frequencies)//2])  # Lấy nửa đầu của tần số
plt.title("FFT of Filtered Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Bien do")
plt.grid(True)
plt.show()
