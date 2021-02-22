from math import tan, pi, acos, cos, sqrt
import matplotlib.pyplot as plt
try:
    from iir_filter.frac import Frac
    from iir_filter.poly import Polyz, Poly
except ModuleNotFoundError:
    from frac import Frac
    from poly import Polyz, Poly
def poleplace_band_pass(freq_center, Bandwidth, f_sample):
    r_0 = 1 - 2*pi * (0.5 * Bandwidth / f_sample) # approx formula
    theta_center = 2*pi * (freq_center / f_sample)
    theta_0 = acos(  cos(theta_center) * (r_0*r_0+1) / (2*r_0)  )
    K = abs(1 - r_0*r_0) / 2
    return Frac(K * Polyz([1, 0, -1]), Polyz([1, -2*r_0*cos(theta_0), r_0*r_0]))

def poleplace_band_stop(freq_center, Bandwidth, f_sample):
    r_0 = 1 - 2*pi * (0.5 * Bandwidth / f_sample) # approx formula
    theta_0 = 2*pi * (freq_center / f_sample)
    K = ( (1+r_0*r_0) - 2*r_0*cos(theta_0) ) / ( 2 - 2*cos(theta_0) )
    return Frac(K * Polyz([1, -2*cos(theta_0), 1]), Polyz([1, -2*r_0*cos(theta_0), r_0*r_0]))

def poleplace_low_pass(freq_cutoff, f_sample):
    omega_s = tan(pi * freq_cutoff / f_sample)
    alpha = (1 - omega_s) / (1 + omega_s)
    K = abs(1 - alpha) / 2
    return Frac(K * Polyz([1, 1]), Polyz([1, -alpha]))

def poleplace_high_pass(freq_cutoff, f_sample):
    omega_s = tan(pi * freq_cutoff / f_sample)
    alpha = (1 - omega_s) / (1 + omega_s)
    K = abs(1 + alpha) / 2
    return Frac(K * Polyz([1, -1]), Polyz([1, -alpha]))


def find_polezero(H_z):
    if not isinstance(H_z, Frac):
        raise Exception("input should be Fracton of Poly")
    coef_den = H_z.den.coeffs
    coef_num = H_z.num.coeffs
    if len(coef_den) < len(coef_num):
        raise Exception("Fraction should deg(num) <= deg(den)")
    if (not isinstance(H_z.den, Polyz) ) or (not isinstance(H_z.num, Polyz) ):
        coef_den.reverse()
        coef_num.reverse()
    else:
        coef_num = coef_num + [0] * (len(coef_den) - len(coef_num))
    def solve_root(coeffs):
        if len(coeffs) > 3:
            raise Exception("Could not find roots, deg > 2")
        if len(coeffs) == 1:
            return []
        if len(coeffs) == 2:
            if coeffs[0] == 0:
                return []
            else:
                return [ (-coeffs[1]/coeffs[0], 0) ]
        else: # deg == 2
            if coeffs[0] == 0:
                if coeffs[1] == 0:
                    return []
                else:
                    return [ (-coeffs[1]/coeffs[0], 0) ]
            else: # ax^2 + bx + c = 0 (a not 0)
                delta = coeffs[1] * coeffs[1] -  4 * coeffs[0] * coeffs[2]
                if delta == 0:
                    return [(-coeffs[1]/(2*coeffs[0]), 0)] * 2
                elif delta >  0:
                    offset = sqrt(delta)
                    return [((-coeffs[1]-offset)/(2*coeffs[0]), 0), ((-coeffs[1]+offset)/(2*coeffs[0]), 0)]
                else: # delta < 0
                    offset = sqrt(-delta)
                    return [(-coeffs[1]/(2*coeffs[0]), -offset/(2*coeffs[0])), (-coeffs[1]/(2*coeffs[0]), offset/(2*coeffs[0]))]
    
    list_pole = solve_root(coef_den)
    list_zero = solve_root(coef_num)
    return list_pole, list_zero

def zmap(list_pole, list_zero):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    circ = plt.Circle((0, 0), radius=1, edgecolor='b', linestyle='--', fill=False)
    ax.add_patch(circ)
    for re, im in list_pole:
        plt.plot(re, im, 'kx', markersize=8)
    for re, im in list_zero:
        plt.plot(re,  im, 'ro', markersize=8, mfc='none')
    real_min, real_max = -2, 2
    imag_min, imag_max = -2, 2
    for re, im in list_pole:
        if re - 0.2 < real_min:
            real_min = re - 0.2
        if re + 0.2 > real_max:
            real_max = re + 0.2
        if im - 0.2 < imag_min:
            imag_min = im - 0.2
        if im + 0.2 > imag_max:
            imag_max = im + 0.2
    ax.set_xlim([real_min, real_max])
    ax.set_ylim([imag_min, imag_max])
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.axis('equal') 
    plt.xlabel("Real")
    plt.ylabel("Imag")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    H_z = Frac(Polyz([1, -4, 12]), Polyz([1, -5, 6]))
    list_pole, list_zero = find_polezero(H_z)
    print(list_pole)
    print(list_zero)
    zmap(list_pole, list_zero)