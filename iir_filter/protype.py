'''
define protype function of Butterworth, Chebyshev filter
'''
try:
    from iir_filter.frac import Frac
except ModuleNotFoundError:
    from frac import Frac

from math import pi, sin, sinh, asin, asinh, log, sqrt, ceil

def butterworth_protype(order):
    if not isinstance(order, int):
        raise Exception("butterworth order should be positive integer")
    if order <= 0:
        raise Exception("butterworth order should be positive integer")
    if order % 2 == 1:
        list_frac = [Frac([1], [1, 1])]
    else:
        list_frac = []
    num_pair = order >> 1
    for m in range(num_pair):
        s_m = sin(pi * (2*m+1)/(2*order))
        list_frac.append( Frac([1], [1, 2*s_m, 1]) )
    return list_frac


def chebyshev_protype(order, epsilon):
    if not isinstance(order, int):
        raise Exception("butterworth order should be positive integer")
    if order <= 0:
        raise Exception("butterworth order should be positive integer")
    A = 1 / (epsilon * 2**(order-1))
    sh = sinh( asinh( 1/epsilon ) / order )
    if order % 2 == 1:
        list_frac = [Frac([A], [1]), Frac([1], [sh, 1])]
    else:
        list_frac = [Frac([A], [1])]
    num_pair = order >> 1
    for m in range(num_pair):
        s_m = sin(pi * (2*m+1)/(2*order))
        list_frac.append( Frac([1], [sh**2 + 1 - s_m**2, 2 * sh * s_m, 1]) )
    return list_frac
    
def calc_cheby_eps2(A_p):
    return 10 ** (A_p/10) - 1

def calc_cheby_order(A_p, A_s, ratio_omega):
    eps2 = calc_cheby_eps2(A_p)
    factor = calc_cheby_eps2(A_s) / eps2
    order = log(sqrt(factor) - sqrt(factor-1)) / log(ratio_omega + sqrt(ratio_omega**2-1))
    return ceil(order)

def calc_butter_order(A_s, ratio_omega):
    factor = calc_cheby_eps2(A_s)   
    order = log(factor) / (2 * log(ratio_omega))
    return ceil(order)
#  todo: find order of filter based on requirement

if __name__ == "__main__":
    list1 = butterworth_protype(5)
    print(list1)
    list2 = chebyshev_protype(5, 0.3493) # see li-zhe tan text book chap 8, page 352
    print(list2)
    list3 = chebyshev_protype(5, 0.5088) # see li-zhe tan text book chap 8, page 352
    print(list3)

    A_s = 10
    omega_p = 1.0691e4
    omega_s = 3.8627e4 
    ratio_omega = omega_s / omega_p
    print(calc_butter_order(A_s, ratio_omega))
