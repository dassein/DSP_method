'''
Finite Impulse Response filter type:
low_pass: freq_cutoff, freq_sample, filter_len(odd)
high_pass: freq_cutoff, freq_sample, filter_len(odd)
band_pass: [freq_cutoff_1, freq_cutoff_2], freq_sample, filter_len(odd)
band_stop: [freq_cutoff_1, freq_cutoff_2], freq_sample, filter_len(odd)

return h(n)
'''
from math import sin, pi
def low_pass(freq_cutoff, freq_sample, filter_len):
    if not filter_len % 2 == 1: # not odd
        raise Exception("filter length is not odd")
    omega_c = 2*pi * (freq_cutoff / freq_sample) # normalized cutoff frequency
    M = filter_len // 2 # N := 2*M + 1
    func = lambda n: omega_c / pi if n == 0 else sin(omega_c * n) / (pi*n)
    list_filter = [func(n) for n in range(-M, M+1)] # n = -M, ..., 0, ..., M
    return list_filter

def high_pass(freq_cutoff, freq_sample, filter_len):
    if not filter_len % 2 == 1: # not odd
        raise Exception("filter length is not odd")
    omega_c = 2*pi * (freq_cutoff / freq_sample) # normalized cutoff frequency
    M = filter_len // 2 # N := 2*M + 1
    func = lambda n: 1 - omega_c / pi if n == 0 else - sin(omega_c * n) / (pi*n)
    list_filter = [func(n) for n in range(-M, M+1)] # n = -M, ..., 0, ..., M
    return list_filter

def band_pass(list_freq_cutoff, freq_sample, filter_len):
    if not filter_len % 2 == 1: # not odd
        raise Exception("filter length is not odd")
    omega_L = 2*pi * (list_freq_cutoff[0] / freq_sample)
    omega_H = 2*pi * (list_freq_cutoff[1] / freq_sample) # normalized cutoff frequency
    M = filter_len // 2 # N := 2*M + 1
    func = lambda n: (omega_H - omega_L) / pi if n == 0 else ( sin(omega_H*n) - sin(omega_L*n) ) / (pi*n) 
    list_filter = [func(n) for n in range(-M, M+1)] # n = -M, ..., 0, ..., M
    return list_filter


def band_stop(list_freq_cutoff, freq_sample, filter_len):
    if not filter_len % 2 == 1: # not odd
        raise Exception("filter length is not odd")
    omega_L = 2*pi * (list_freq_cutoff[0] / freq_sample)
    omega_H = 2*pi * (list_freq_cutoff[1] / freq_sample) # normalized cutoff frequency
    M = filter_len // 2 # N := 2*M + 1
    func = lambda n: 1 - (omega_H - omega_L) / pi if n == 0 else - ( sin(omega_H*n) - sin(omega_L*n) ) / (pi*n) 
    list_filter = [func(n) for n in range(-M, M+1)] # n = -M, ..., 0, ..., M
    return list_filter

def print_approx(list_example, precision=4):
    print([ round(elem, precision) for elem in list_example ])

def calc_omega(freq, freq_sample):
    return 2*pi * freq / freq_sample

def fir_filter(list_freq_cutoff, freq_sample, filter_len, str_filter_type):
    dict_func = {"low_pass": low_pass,
                "high_pass": high_pass,
                "band_pass": band_pass,
                "band_stop": band_stop}
    if str_filter_type not in dict_func.keys():
        raise Exception("filter type not found")
    if len(list_freq_cutoff) == 0 or len(list_freq_cutoff) > 2:
        raise Exception("cutoff frequency number is 1 or 2")
    if len(list_freq_cutoff) == 1:
        if str_filter_type != "low_pass" and str_filter_type != "high_pass":
            raise Exception("cutoff frequency number should be 1")
        freq_cutoff = list_freq_cutoff[0] # only 1 freq_cutoff
        return dict_func[str_filter_type](freq_cutoff, freq_sample, filter_len)
    if len(list_freq_cutoff) == 2:
        if str_filter_type != "band_pass" and str_filter_type != "band_stop":
            raise Exception("cutoff frequency number should be 2")
        return dict_func[str_filter_type](list_freq_cutoff, freq_sample, filter_len)


if __name__ == "__main__":
    # list_filter = low_pass(800, 8000, 3)
    list_filter = fir_filter([800], 8000, 3, "low_pass")
    print_approx(list_filter)