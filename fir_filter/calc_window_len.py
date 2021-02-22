'''
calculate the window length for different window type
'''
from math import ceil
def calc_window_len(str_window_type, list_transient_band, f_sample):
    dict_coef = {"Rectangular": 0.9, "Hanning": 3.1, "Hamming": 3.3, "Blackman": 5.5}
    if str_window_type not in dict_coef.keys():
        raise Exception("Unkown window type")
    coef = dict_coef[str_window_type]
    for idx, [freq_start, freq_end] in enumerate(list_transient_band):
        df = abs(freq_end - freq_start) / f_sample
        if idx == 0:
            window_len = coef / df
        else:
            window_len = coef / df if coef / df > window_len else window_len
    window_len = ceil(window_len)
    return window_len if window_len % 2 == 1 else window_len + 1  # return the closest odd number

if __name__ == "__main__":
    str_window_type = "Hamming"
    list_transient_band = [[500, 1600], [2300, 3500]]
    f_sample = 8e3
    window_len = calc_window_len(str_window_type, list_transient_band, f_sample)
    print(window_len)