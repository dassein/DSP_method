from math import pi, cos
def rectangular(signal):
    return signal

def hanning(signal):
    N = len(signal)
    signal_window = [ x * ( 0.5 - 0.5*cos(2*pi*n/(N-1)) ) for (x, n) in zip(signal, range(N))]
    return signal_window

def hamming(signal):
    N = len(signal)
    signal_window = [ x * ( 0.54 - 0.46*cos(2*pi*n/(N-1)) ) for (x, n) in zip(signal, range(N))]
    return signal_window

def blackman(signal):
    N = len(signal)
    signal_window = [ x * ( 0.42 - 0.5*cos(2*pi*n/(N-1)) + 0.08*cos(4*pi*n/(N-1)) ) for (x, n) in zip(signal, range(N))]
    return signal_window

def triangular(signal):
    N = len(signal)
    signal_window = [ x * (1-abs(2*n-N+1)/(N-1)) for (x, n) in zip(signal, range(N))]
    return signal_window

def window(signal, str_window_type="Hamming"):
    dict_func = {"Rectangular": rectangular,
                "Hanning": hanning,
                "Hamming": hamming,
                "Blackman": blackman}
    if str_window_type not in dict_func.keys():
        raise Exception("window not found")
    return dict_func[str_window_type](signal)