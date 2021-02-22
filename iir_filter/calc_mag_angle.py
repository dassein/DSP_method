'''
calculate |H(e^{j Omega})| and angle( H(e^{j Omega}) ) for H(z) = sum h(n-M) z^{-n}
input:
h(n) -M, ..., 0,..., +M list of filter h(-M) ~ h(0) ~ h(M)
num_point: how many point computed in 0~pi

output:
list_amp: length num_point Amplitude
list_angle: length num_point Angle
'''
try:
    from iir_filter.poly import Poly, Polyz
    from iir_filter.frac import Frac
except ModuleNotFoundError:
    from poly import Poly, Polyz
    from frac import Frac
from math import sin, cos, pi, log10, atan, sqrt
import matplotlib.pyplot as plt
def calc_mag_angle(H, num_point=512): # default 1024 points in 0 ~ pi
    def spectrum_poly(poly, list_omega):
        if not isinstance(poly, Poly):
            raise Exception("input should be poly")
        list_coef = poly.coeffs
        if isinstance(poly, Polyz):
            cos_n = lambda omega, n: cos(n * omega)
            sin_n = lambda omega, n: sin(n * omega)
            func_re = lambda omega: sum( [ coef * cos_n( omega, n ) for n, coef in enumerate(list_coef) ] ) 
            func_im = lambda omega: - sum( [ coef * sin_n( omega, n ) for n, coef in enumerate(list_coef) ] )
        else: # H(s) must subs before use: s' = j omega = fs * j Omega = fs * s
            # example: H_subs = H_s.subs(Frac([0, f_sample], [1]))
            func_re = lambda omega: sum( [ coef * ( - omega**2 )**(n >> 1) for n, coef in enumerate(list_coef) if n % 2 == 0 ] )
            func_im = lambda omega: omega * sum( [ coef * ( - omega**2 )**(n >> 1) for n, coef in enumerate(list_coef) if n % 2 == 1 ] )
        list_re = list( map(func_re, list_omega) )
        list_im = list( map(func_im, list_omega) )
        return list_re, list_im
    def atan_special(real, imag):
        if real != 0:
            if real > 0:
                return atan(imag / real)
            else:
                if imag >= 0:
                    return pi + atan(imag / real) # [0, pi]
                else:
                    return -pi + atan(imag / real) # (-pi, 0)
        elif imag > 0:
            return pi / 2
        elif imag == 0:
            return None
        else:
            return -pi / 2
    
    def adjust_angle(list_angle):
        list_ind_zero = [ind for ind, elem in enumerate(list_angle) if elem == None]
        if len(list_ind_zero) == 0:
            return list_angle
        elif len(list_ind_zero) == len(list_angle):
            raise Exception("dB_mag input cannot be all zeros")
        else:
            for ind in list_ind_zero:
                if ind == 0:
                    list_angle[ind] = list_angle[ind+1]
                elif ind == len(list_angle)-1:
                    list_angle[ind] = list_angle[ind-1]
                else:
                    list_angle[ind] = (list_angle[ind-1] + list_angle[ind+1]) / 2
            return list_angle
    
    list_omega = [pi * i / num_point for i in range(num_point)]
    if isinstance(H, Poly):
        list_re, list_im = spectrum_poly(H, list_omega)
    elif isinstance(H, Frac):
        list_re_num, list_im_num = spectrum_poly(H.num, list_omega)
        list_re_den, list_im_den = spectrum_poly(H.den, list_omega)
        list_re = [(a1*a2 + b1*b2) / (a2*a2 + b2*b2) for a1, b1, a2, b2 in list(zip(list_re_num, list_im_num, list_re_den, list_im_den))]
        list_im = [(-a1*b2 + a2*b1) / (a2*a2 + b2*b2) for a1, b1, a2, b2 in list(zip(list_re_num, list_im_num, list_re_den, list_im_den))]
    else:
        raise Exception("input type for calc_mag_angle should be Poly or Frac")
    list_mag = [sqrt(real*real + imag*imag) for real, imag in list(zip(list_re, list_im))]
    list_angle = [atan_special(real, imag) for real, imag in list(zip(list_re, list_im)) ]
    list_angle = adjust_angle(list_angle)

    def unwrap(list_angle):
        list_angle_prev = [list_angle[0]] + list_angle[:-1]
        list_num_2pi = []
        num_2pi = 0
        for elem, elem_prev in list(zip(list_angle, list_angle_prev)):
            if abs(elem - elem_prev) > 0.95 * (2 * pi):
                num_2pi += round( (elem_prev - elem) / (2*pi) )
            elif (elem - elem_prev) > -1.05 * pi and (elem - elem_prev) < -0.95 * pi:
                num_2pi += 1
            list_num_2pi.append(num_2pi)
        return list_num_2pi
        
    list_num_2pi = unwrap(list_angle)
    list_angle = [angle + num_2pi * (2 * pi) for (angle, num_2pi) in list(zip(list_angle, list_num_2pi))] # adjust mag, angle
    return list_mag, list_angle, list_omega

def dB_mag(list_mag):
    list_mag_dB = [20*log10(elem) if elem != 0 else None for elem in list_mag]
    list_ind_zero = [ind for ind, elem in enumerate(list_mag_dB) if elem == None]
    if len(list_ind_zero) == 0:
        return list_mag_dB
    elif len(list_ind_zero) == len(list_mag_dB):
        raise Exception("dB_mag input cannot be all zeros")
    else:
        for ind in list_ind_zero:
            if ind == 0:
                list_mag_dB[ind] = list_mag_dB[ind+1]
            elif ind == len(list_mag_dB)-1:
                list_mag_dB[ind] = list_mag_dB[ind-1]
            else:
                list_mag_dB[ind] = (list_mag_dB[ind-1] + list_mag_dB[ind+1]) / 2
        return list_mag_dB



def rad2deg_angle(list_angle):
    return [180*elem / pi for elem in list_angle]

def plot_mag_angle(list_mag, list_angle, list_omega, path_fig="./test.png"):
    list_mag_dB = dB_mag(list_mag)
    list_angle_deg = rad2deg_angle(list_angle)
    fig = plt.figure()
    
    num_point = len(list_omega)
    list_special_index = [int(factor * num_point) for factor in [0, 0.25, 0.5, 0.75]] # 0, pi/4, pi/2, 3*pi/4
    list_special_index.append(num_point - 1) # add pi
    list_freq_special = [list_omega[index] for index in list_special_index]
    list_mag_special = [list_mag_dB[index] for index in list_special_index]
    list_angle_special = [list_angle_deg[index] for index in list_special_index]

    plt.subplot(211)
    plt.plot(list_omega, list_mag_dB)
    plt.plot(list_freq_special, list_mag_special, "ro")
    plt.xlabel("Frequency (radians)")
    plt.ylabel("Magnitude response (dB)")
    plt.title(r"$|H(e^{j\Omega})|$")
    ax = plt.gca()
    ax.set_xlim([0, pi])  # 0~1ms
    plt.grid()

    plt.subplot(212)
    plt.plot(list_omega, list_angle_deg)
    plt.plot(list_freq_special, list_angle_special, "ro")
    plt.xlabel("Frequency (radians)")
    plt.ylabel("Phase response (degrees)")
    plt.title(r"$\angle H(e^{j\Omega})$")
    ax = plt.gca()
    ax.set_xlim([0, pi])  # 0~1ms
    plt.grid()
    plt.tight_layout()
    fig.savefig(path_fig)
    plt.show()

def plot_mag_angle_freq(list_mag, list_angle, list_omega, f_sample, path_fig="./test.png"):
    list_freq = [f_sample * (omega / (2 * pi)) for omega in list_omega]
    list_mag_dB = dB_mag(list_mag)
    list_angle_deg = rad2deg_angle(list_angle)
    fig = plt.figure()

    num_point = len(list_freq)
    list_special_index = [int(factor * num_point) for factor in [0, 0.25, 0.5, 0.75]] # 0, pi/4, pi/2, 3*pi/4
    list_special_index.append(num_point - 1) # add pi
    list_freq_special = [list_freq[index] for index in list_special_index]
    list_mag_special = [list_mag_dB[index] for index in list_special_index]
    list_angle_special = [list_angle_deg[index] for index in list_special_index]

    plt.subplot(211)
    plt.plot(list_freq, list_mag_dB)
    plt.plot(list_freq_special, list_mag_special, "ro")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude response (dB)")
    plt.title(r"$|H(e^{j\Omega})|$")
    ax = plt.gca()
    ax.set_xlim([0, f_sample/2])  # 0~1ms
    plt.grid()

    plt.subplot(212)
    plt.plot(list_freq, list_angle_deg)
    plt.plot(list_freq_special, list_angle_special, "ro")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase response (degrees)")
    plt.title(r"$\angle H(e^{j\Omega})$")
    ax = plt.gca()
    ax.set_xlim([0, f_sample/2])  # 0~1ms
    plt.grid()
    plt.tight_layout()
    fig.savefig(path_fig)
    plt.show()

def plot_mag_freq_multiple(list2D_mag, list2D_omega, f_sample, path_fig="./test.png"):
    fig = plt.figure()
    for ind in range( len(list2D_omega) ):
        list_freq = [f_sample * (omega / (2 * pi)) for omega in list2D_omega[ind]]
        list_mag_dB = dB_mag(list2D_mag[ind])
        plt.plot(list_freq, list_mag_dB)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude response (dB)")
    plt.title(r"$|H(e^{j\Omega})|$")
    ax = plt.gca()
    # ax.set_xlim([0, f_sample/2])  # 0~1ms
    ax.set_xlim([80, 12800])  # 7 bands
    ax.set_ylim([-100, None])
    ax.set_xscale('log')
    plt.grid()
    plt.tight_layout()
    fig.savefig(path_fig)
    plt.show()


def plot_Hs_Hz(H_s, H_z, f_sample, num_point=512, path_fig="./test.png"):
    H_subs = H_s.subs(Frac([0, f_sample], [1]))
    list_mag_s, list_angle_s, list_omega_s = calc_mag_angle(H_subs, num_point=num_point)
    list_mag_z, list_angle_z, list_omega_z = calc_mag_angle(H_z, num_point=num_point)    
    list_freq_s = [elem * f_sample/(2*pi) for elem in list_omega_s]
    list_freq_z = [elem * f_sample/(2*pi) for elem in list_omega_z]
    factor = list_mag_s[0] / list_mag_z[0]
    list_mag_scaled_z = [elem * factor for elem in list_mag_z]
    list_angle_deg_s = rad2deg_angle(list_angle_s)
    list_angle_deg_z = rad2deg_angle(list_angle_z)
    fig = plt.figure()

    plt.subplot(311)
    plt.plot(list_freq_s, list_mag_s, label=r"$|H(f)|$")
    plt.plot(list_freq_z, list_mag_z, 'r', label=r"$|H(e^{j2\pi fT})|$")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Mag. responses")
    # plt.title(r"$|H(f)|$, $|H(e^{j2\pi fT})|$")
    ax = plt.gca()
    ax.legend()
    ax.set_xlim([0, f_sample/2])  # 0~1ms
    plt.grid()

    plt.subplot(312)
    plt.plot(list_freq_s, list_mag_s, label=r"$|H(f)|$")
    plt.plot(list_freq_z, list_mag_scaled_z, 'r', label=r"Scaled $|H(e^{j2\pi fT})|$")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Scaled Mag. responses")
    # plt.title(r"$|H(f)|$, Scaled $|H(e^{j2\pi fT})|$")
    ax = plt.gca()
    ax.legend()
    ax.set_xlim([0, f_sample/2])  # 0~1ms
    plt.grid()

    plt.subplot(313)
    plt.plot(list_freq_s, list_angle_deg_s, label=r"$\angle H(f)$")
    plt.plot(list_freq_z, list_angle_deg_z, 'r', label=r"$\angle H(e^{j2\pi fT})$")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phases (deg.)")
    # plt.title(r"$\angle H(f)$, $\angle H(e^{j2\pi fT})$")
    ax = plt.gca()
    ax.legend()
    ax.set_xlim([0, f_sample/2])  # 0~1ms
    plt.grid()
    plt.tight_layout()
    fig.savefig(path_fig)
    plt.show()


if __name__ == "__main__":
    list_filter = [-0.09355, -0.01558, 0.1, -0.01558, -0.09355]
    # list_filter = [0.1871, 0.2, 0.1871]
    H = Polyz(list_filter)
    list_mag, list_angle, list_omega = calc_mag_angle(H, num_point=512)    
    plot_mag_angle(list_mag, list_angle, list_omega)

    H2 = Frac(Polyz([0.1327, -0.2654, 0.1327]), Polyz([1, 0.7996, 0.3618]))
    list_mag, list_angle, list_omega = calc_mag_angle(H2, num_point=512)    
    plot_mag_angle(list_mag, list_angle, list_omega)

    H2 = Frac(Polyz([0.0730, 0, -0.0730]), Polyz([1, 0.7117, 0.8541]))
    list_mag, list_angle, list_omega = calc_mag_angle(H2, num_point=512)    
    plot_mag_angle(list_mag, list_angle, list_omega)
    plot_mag_angle_freq(list_mag, list_angle, list_omega, f_sample=8e3)
