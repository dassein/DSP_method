'''
1. convert omega_s <=> omega_z
2. know omega_z_mid, bandwidth_z => find omega_s_low, omega_s_high
3. s domain subs: low pass, high_pass, band_pass, band_stop
4. calc ratio_omega to find out order of prototype filter: Butterworth, Chebyshev
'''
try:
    from iir_filter.poly import Poly, Polyz
    from iir_filter.frac import Frac
except ModuleNotFoundError:
    from poly import Poly, Polyz
    from frac import Frac

from math import tan, atan, pi
def convert_omega_s2z(omega_s, f_sample):
    omega_z = (2*f_sample) * atan(omega_s / (2*f_sample))
    return omega_z 

def convert_omega_z2s(omega_z, f_sample):
    omega_s = (2*f_sample) * tan(omega_z / (2*f_sample))
    return omega_s

def filter_subs(list_frac, list_omega_pass, str_filter_type):
    list_filter_type = ["low_pass", "high_pass", "band_pass", "band_stop"]
    if str_filter_type not in list_filter_type:
        raise Exception("filter type not found")
    if len(list_omega_pass) == 0 or len(list_omega_pass) > 2:
        raise Exception("omega_pass number is 1 or 2")
    if len(list_omega_pass) == 1 \
        and (str_filter_type != "low_pass") and (str_filter_type != "high_pass"):
            raise Exception("omega_pass number should be 1")
    if len(list_omega_pass) == 2 \
        and (str_filter_type != "band_pass") and (str_filter_type != "band_stop"):
            raise Exception("omega_pass number should be 2")
    # substitution
    list_frac_subs = []
    if len(list_omega_pass) == 1:
        if str_filter_type == "low_pass":
            frac_subs = Frac([0, 1], [list_omega_pass[0]])
            
        else:
            frac_subs = Frac([list_omega_pass[0]], [0, 1])
    else: # len(list_omega_pass) == 2:
        W = abs(list_omega_pass[1] - list_omega_pass[0])
        sq_omega_0 = list_omega_pass[1] * list_omega_pass[0]
        if str_filter_type == "band_pass":
            frac_subs = Frac([sq_omega_0, 0, 1], [0, W])           
        else: # str_filter_type == "band_stop":
            frac_subs = Frac([0, W], [sq_omega_0, 0, 1])
    if isinstance(list_frac, Frac): # single Frac
        return list_frac.subs(frac_subs)
    for frac in list_frac:          # lsit of Frac
        list_frac_subs.append( frac.subs(frac_subs) )
    return list_frac_subs

def calc_omega_pass(list_omega_pass_z, f_sample, str_filter_type):
    if any(elem < 0 or elem/(2*pi) > f_sample/2 for elem in list_omega_pass_z):
        raise Exception("omega_pass in z domain should be within 0 ~ f_s/2")
    if str_filter_type not in ["low_pass", "high_pass", "band_pass", "band_stop"]:
        raise Exception("filter type not found")
    if len(list_omega_pass_z) == 1: # low_pass and high_pass
        return [convert_omega_z2s(list_omega_pass_z[0], f_sample)]
    else: # len(list_omega_pass) == 2:
        omega_0_z = (list_omega_pass_z[1] + list_omega_pass_z[0]) / 2
        omega_0_s = convert_omega_z2s(omega_0_z, f_sample)
        if str_filter_type == "band_pass":
            if omega_0_z / (2*pi) > f_sample / 4:
                omega_pass_high = convert_omega_z2s(list_omega_pass_z[1], f_sample)
                omega_pass_low = omega_0_s * omega_0_s / omega_pass_high
            else:
                omega_pass_low = convert_omega_z2s(list_omega_pass_z[0], f_sample)
                omega_pass_high = omega_0_s * omega_0_s / omega_pass_low
        else: # str_filter_type == "band_stop":
            if omega_0_z / (2*pi) > f_sample / 4:
                omega_pass_low = convert_omega_z2s(list_omega_pass_z[0], f_sample)
                omega_pass_high = omega_0_s * omega_0_s / omega_pass_low               
            else:
                omega_pass_high = convert_omega_z2s(list_omega_pass_z[1], f_sample)
                omega_pass_low = omega_0_s * omega_0_s / omega_pass_high
        return [omega_pass_low, omega_pass_high]

def calc_omega_stop(list_omega_stop_z, f_sample, str_filter_type):
    if any(elem < 0 or elem > f_sample/2 for elem in list_omega_stop_z):
        raise Exception("omega_stop in z domain should be within 0 ~ f_s/2")
    if str_filter_type not in ["low_pass", "high_pass", "band_pass", "band_stop"]:
        raise Exception("filter type not found")
    if len(list_omega_stop_z) == 1: # low_pass and high_pass
        return [convert_omega_z2s(list_omega_stop_z[0], f_sample)]
    else: # len(list_omega_pass) == 2:
        omega_0_z = (list_omega_stop_z[1] + list_omega_stop_z[0]) / 2
        omega_0_s = convert_omega_z2s(omega_0_z, f_sample)
        if str_filter_type == "band_pass":
            if omega_0_z / (2*pi) <= f_sample / 4:
                omega_stop_high = convert_omega_z2s(list_omega_stop_z[1], f_sample)
                omega_stop_low = omega_0_s * omega_0_s / omega_stop_high
            else:
                omega_stop_low = convert_omega_z2s(list_omega_stop_z[0], f_sample)
                omega_stop_high = omega_0_s * omega_0_s / omega_stop_low
        else: # str_filter_type == "band_stop":
            if omega_0_z / (2*pi) <= f_sample / 4:
                omega_stop_low = convert_omega_z2s(list_omega_stop_z[0], f_sample)
                omega_stop_high = omega_0_s * omega_0_s / omega_stop_low               
            else:
                omega_stop_high = convert_omega_z2s(list_omega_stop_z[1], f_sample)
                omega_stop_low = omega_0_s * omega_0_s / omega_stop_high
        return [omega_stop_low, omega_stop_high]



if __name__ == "__main__":
    f_sample = 8e3
    omega_z = 1.5e3 * 2 * pi
    omega_s = convert_omega_z2s(omega_z, f_sample)
    list_frac_subs = filter_subs([Frac([1], [1, 1])], [omega_s], str_filter_type="low_pass")
    print(list_frac_subs)
    try:
        from iir_filter.frac import convert_s2z
    except ModuleNotFoundError:
        from frac import convert_s2z
    list_frac_z = [convert_s2z(frac, f_sample) for frac in list_frac_subs ]
    print(list_frac_z)
    