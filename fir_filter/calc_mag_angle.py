'''
calculate |H(e^{j Omega})| and angle( H(e^{j Omega}) ) for H(z) = sum h(n-M) z^{-n}
input:
h(n) -M, ..., 0,..., +M list of filter h(-M) ~ h(0) ~ h(M)
num_point: how many point computed in 0~pi

output:
list_amp: length num_point Amplitude
list_angle: length num_point Angle
'''

from math import cos, pi, log10
import matplotlib.pyplot as plt
def calc_mag_angle(list_filter, num_point=512): # default 1024 points in 0 ~ pi
    N = len(list_filter)
    if not N % 2 == 1:
        raise Exception("length of h(n) is not odd")
    M = N // 2
    coef_cos = [elem if i == 0 else 2 * elem for (i, elem) in enumerate(list_filter[M:])] # start from M+1 position h(0)
    cos_n = lambda omega, n: cos(n * omega)
    func_mag = lambda omega: sum( [ coef_cos[n] * cos_n( omega, n ) for n in range(M+1) ] ) 
    func_angle = lambda omega: - M * omega
    list_omega = [pi * i / num_point for i in range(num_point)]
    list_mag = list( map(func_mag, list_omega) )
    list_angle = list( map(func_angle, list_omega ) )

    def count_sign_change(list_example):
        list_num_signchange = []
        list_example_positive = []
        sign = True # True: positive; False: negative
        num_signchange = 0
        for elem in list_example:
            if sign:
                if elem < 0:
                    sign = not sign
                    num_signchange += 1
            else:
                if elem > 0:
                    sign = not sign
                    num_signchange += 1
            list_num_signchange.append(num_signchange)
            list_example_positive.append(elem) if sign else list_example_positive.append(-elem)
        return list_num_signchange, list_example_positive
    
    list_num_signchange, list_mag = count_sign_change(list_mag)
    list_angle = [angle + num_signchange * pi for (angle, num_signchange) in list(zip(list_angle, list_num_signchange))] # adjust mag, angle
    return list_mag, list_angle, list_omega

def dB_mag(list_mag):
    return [20*log10(elem) for elem in list_mag]

def rad2deg_angle(list_angle):
    return [180*elem / pi for elem in list_angle]

def plot_mag_angle(list_mag, list_angle, list_omega, path_fig="./test.png"):
    list_mag_dB = dB_mag(list_mag)
    list_angle_deg = rad2deg_angle(list_angle)
    fig = plt.figure()
    
    num_point = len(list_omega)
    list_special_index = [int(factor * num_point) for factor in [0, 0.25, 0.5, 0.75]] # 0, pi/4, pi/2, 3*pi/4
    list_special_index.append(num_point - 1) # add pi
    list_omega_special = [list_omega[index] for index in list_special_index]
    list_mag_special = [list_mag_dB[index] for index in list_special_index]
    list_angle_special = [list_angle_deg[index] for index in list_special_index]

    plt.subplot(211)
    plt.plot(list_omega, list_mag_dB)
    plt.plot(list_omega_special, list_mag_special, "ro")
    plt.xlabel("Frequency (radians)")
    plt.ylabel("Magnitude response (dB)")
    plt.title(r"$|H(e^{j\Omega})|$")
    ax = plt.gca()
    ax.set_xlim([0, pi])  # 0~1ms
    plt.grid()

    plt.subplot(212)
    plt.plot(list_omega, list_angle_deg)
    plt.plot(list_omega_special, list_angle_special, "ro")
    plt.xlabel("Frequency (radians)")
    plt.ylabel("Phase response (degrees)")
    plt.title(r"$\angle H(e^{j\Omega})$")
    ax = plt.gca()
    ax.set_xlim([0, pi])  # 0~1ms
    plt.grid()
    plt.tight_layout()
    fig.savefig(path_fig)
    plt.show()




if __name__ == "__main__":
    # list_filter = [-0.09355, -0.01558, 0.1, -0.01558, -0.09355]
    list_filter = [0.1871, 0.2, 0.1871]
    list_mag, list_angle, list_omega = calc_mag_angle(list_filter, num_point=512)    
    plot_mag_angle(list_mag, list_angle, list_omega)
