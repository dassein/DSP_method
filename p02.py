from iir_filter.pole_place import find_polezero, zmap
from iir_filter.frac import Frac, convert_s2z
from iir_filter.poly import Poly, Polyz
from iir_filter.calc_mag_angle import calc_mag_angle, plot_mag_angle_freq, dB_mag
from math import sqrt, cos, pi
f_sample = 8000
H_z = Frac(Polyz([0.2]), Polyz([1, 0, 0.8]))
list_pole, list_zero = find_polezero(H_z)
print(list_pole, list_zero)
zmap(list_pole, list_zero)
list_mag, list_angle, list_omega = calc_mag_angle(H_z, num_point=4096)
plot_mag_angle_freq(list_mag, list_angle, list_omega, f_sample, path_fig="../p02_mag.png")
func_mag = lambda omega: 0.2 / sqrt(1.64 + 1.6 * cos(2 * omega))
list_omega = [2*pi * (f/f_sample) for f in [0, 1000, 2000, 3000, 4000] ]
list_mag = list(map(func_mag, list_omega))
list_mag_dB = dB_mag(list_mag)
print(list_mag)
print(list_mag_dB)