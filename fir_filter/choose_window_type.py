'''
choose the window type based on the requirement of :
1. passband_ripple
2. stopband_attenuation
page 254 table 7.7 in Li-zhe Tan textbook 3rd version
'''

def choose_window_type(passband_ripple, stopband_attenuation):
    dict_passband_ripple = {"Rectangular": 0.7416, "Hanning": 0.0546, "Hamming": 0.0194, "Blackman": 0.0017}
    dict_stopband_attenuation = {"Rectangular": 21, "Hanning": 44, "Hamming": 53, "Blackman": 74}
    filtered_passband_ripple = set(k for k, v in dict_passband_ripple.items() if v <= passband_ripple)
    filtered_stopband_attenuation = set(k for k, v in dict_stopband_attenuation.items() if v >= stopband_attenuation)
    filtered_window_type = list( filtered_passband_ripple & filtered_stopband_attenuation )
    if not filtered_window_type: # empty list
        raise Exception("No window type meet requirements")
    order_window_type = {"Rectangular": 0, "Hanning": 1, "Hamming": 2, "Blackman": 3}
    filtered_order_window_type = list( (k, v) for k, v in order_window_type.items() if k in filtered_window_type)
    str_window_type = min(filtered_order_window_type , key=lambda x : x[-1] )[0] # sort as order
    return str_window_type



if __name__ == "__main__":
    str_window_type = choose_window_type(0.5, 10)
    print(str_window_type)