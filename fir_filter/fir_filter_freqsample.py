'''
Finite Impulse Response filter type:
Using frequency sampling method

1. generate spectrum H_k := | H(e^{j k * 2*pi/N}) | here N = 2 M + 1 odd number
*  To reduce this ripple effect, the modified specification with a smooth transition band H_k = 0.5
2. compute h(n) for n=0~M (equiv 0~N-1) based on H_k
'''
from math import cos, pi
def calc_spectrum(list_freq_cutoff, freq_sample, filter_len, str_filter_type):
    # define exceptions
    if not filter_len % 2 == 1: # not odd
        raise Exception("filter length is not odd")
    list_filter_type = ["low_pass", "high_pass", "band_pass", "band_stop"]
    if str_filter_type not in list_filter_type:
        raise Exception("filter type not found")
    if len(list_freq_cutoff) == 0 or len(list_freq_cutoff) > 2:
        raise Exception("cutoff frequency number is 1 or 2")
    if len(list_freq_cutoff) == 1 \
        and (str_filter_type != "low_pass") and (str_filter_type != "high_pass"):
            raise Exception("cutoff frequency number should be 1")
    if len(list_freq_cutoff) == 2 \
        and (str_filter_type != "band_pass") and (str_filter_type != "band_stop"):
            raise Exception("cutoff frequency number should be 2")
    # calculation
    M = filter_len // 2 # N = 2 * M + 1
    freq_resolution = freq_sample / (filter_len-1) # f_s / (2 * M) freq resolution
    index_cutoff = [round(freq_cutoff / freq_resolution) for freq_cutoff in list_freq_cutoff]
    if len(list_freq_cutoff) == 1:
        freq_cutoff = list_freq_cutoff[0]        
        list_spectrum = [1 if k * freq_resolution <= freq_cutoff else 0 for k in range(M+1)] # H_0 ~ H_M
        if abs(freq_cutoff / freq_resolution - index_cutoff[0]) < 0.25:
            list_spectrum[index_cutoff[0]] = 0.5
        if str_filter_type == "low_pass":
            return list_spectrum
        else: # "high_pass"
            return [1-elem for elem in list_spectrum]
    else: # len(list_freq_cutoff) == 2
        list_spectrum = [1 if (k * freq_resolution >= list_freq_cutoff[0]) \
                         and (k * freq_resolution <= list_freq_cutoff[1]) else 0 \
                        for k in range(M+1)] # H_0 ~ H_M
        if abs(list_freq_cutoff[0] / freq_resolution - index_cutoff[0]) < 0.25:
            list_spectrum[index_cutoff[0]] = 0.5
        if abs(list_freq_cutoff[1] / freq_resolution - index_cutoff[1]) < 0.25:
            list_spectrum[index_cutoff[1]] = 0.5
        if str_filter_type == "band_pass":
            return list_spectrum
        else: # "band_stop"
            return [1-elem for elem in list_spectrum]

def calc_list_filter_freqsample(list_spectrum):
    M = len(list_spectrum) - 1
    N = 2 * M + 1 # odd number
    coef_cos = [elem if i == 0 else 2 * elem for (i, elem) in enumerate(list_spectrum)] # H_k (k=0); 2 * H_k (k=1~M)
    cos_n = lambda k, n: cos(k * n * 2*pi / N)
    func_filter = lambda n: sum( [ coef_cos[k] * cos_n( k, n ) for k in range(M+1) ] ) / N
    list_filter = [func_filter(n) for n in range(-M, M+1)]
    return list_filter


def fir_filter_freqsample(list_freq_cutoff, freq_sample, filter_len, str_filter_type):
    list_spectrum = calc_spectrum(list_freq_cutoff, freq_sample, filter_len, str_filter_type)
    list_filter = calc_list_filter_freqsample(list_spectrum)
    return list_filter



if __name__ == "__main__":
    list_spectrum = calc_spectrum([1000, 3000], 8000, 25, str_filter_type="band_pass")
    print(list_spectrum)
    # list_spectrum = calc_spectrum([2000], 8000, 25, str_filter_type="low_pass")
    # print(list_spectrum)
    list_filter = fir_filter_freqsample([1000, 3000], 8000, 25, str_filter_type="band_pass")
    print([ round(elem, 6) for elem in list_filter ]) # page 280 test
