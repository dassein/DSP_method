import numpy as np
import cmath

def pad(inputList):
   k = 0
   while 2**k < len(inputList):
      k += 1
   return np.concatenate(( inputList, [0] * (2**k - len(inputList)) ))


def cooley_tukey_dit_fft(x, inverse=False):
    """
    1. This transform is based on Cooley-Tukey decimation-in-time radix-2 algorithm.
    2. Require the input x's length to be the power-of-2. In order to compute the FFT of the input x.
    """
    # Returns the integer whose value is the reverse of the lowest 'bits' bits of the integer 'x'.
    def bit_reversal_permutation(_x, bits):
        y = 0
        for i in range(bits):
            y = (y << 1) | (_x & 1)
            _x >>= 1
        return y

    N = x.shape[0]
    levels = N.bit_length()-1   # levels = log2(n)
    if 2 ** levels != N:
        raise ValueError("Length is not a power of 2")
    coef = (2j if inverse else -2j) * np.pi / N
    W_exp = np.exp(np.arange(N//2) * coef)
    # Copy with bit-reversed permutation
    x = [x[bit_reversal_permutation(i, levels)] for i in range(N)]
    # Radix-2 decimation-in-time FFT
    size = 2
    while size <= N:
        half_size = size // 2
        table_step = N // size
        for i in range(0, N, size):
            k = 0
            for j in range(i, i + half_size):
                temp = x[j + half_size] * W_exp[k]
                x[j + half_size] = x[j] - temp
                x[j] += temp
                k += table_step
        size *= 2
    return np.asarray(x)

def cooley_tukey_dit_ifft(signal):
    timeSignal = np.conjugate(signal)
    return np.conjugate( cooley_tukey_dit_fft(timeSignal) ) / len(signal)

norm = lambda x: np.absolute(x)
angle = lambda x: np.angle(x)

if __name__ == "__main__":
    # signal = [1, 0, 0, 1, 0, 0, 0]
    signal = np.array([ cmath.exp(2.0 * cmath.pi * 1j * i *(5/8)) for i in range(5) ])
    signal_pad = pad(signal)
    freq_spectrum = cooley_tukey_dit_fft(signal_pad)
    import matplotlib.pyplot as plt
    norm_freq = norm(freq_spectrum)
    # plt.bar( [i for i in range(len(freq_spectrum)) ], norm_freq )
    plt.stem(norm_freq, use_line_collection=True)
    plt.show()
    plt.savefig('./output_images/chap4_1_fft1d_2rd_plt.jpg')
    plt.close()

    signal_recover = cooley_tukey_dit_ifft(freq_spectrum)
    print("singnal:"), print(signal)
    print("singnal_recover:"), print(signal_recover)
    norm_signal_re = norm(signal_recover) 
    plt.stem(norm_signal_re, use_line_collection=True)
    plt.show()
    plt.savefig('./output_images/chap4_1_fft1d_2rd_re_plt.jpg')
    plt.close()