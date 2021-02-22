from iir_filter.frac import Frac, convert_s2z
from iir_filter.poly import Poly, Polyz
from iir_filter.util import convert_omega_z2s, filter_subs
from iir_filter.calc_mag_angle import calc_mag_angle, plot_mag_angle_freq
from iir_filter.protype import butterworth_protype
from iir_filter.pole_place import find_polezero, zmap
from math import pi
from functools import reduce
list_omega_pass_z = [2 * pi * 100, 2 * pi * 120]
f_sample = 1000
list_omega_pass_s = [convert_omega_z2s(elem, f_sample) for elem in list_omega_pass_z]
print(list_omega_pass_s)
order = int(2 / 2)
list_H_s = butterworth_protype(order)
print(list_H_s)
list_H_subs = [filter_subs(H_s, list_omega_pass_s, str_filter_type="band_pass") for H_s in list_H_s]
print(list_H_subs)
H_subs = reduce(lambda x,y:x * y, list_H_subs)
print(H_subs)
H_z = convert_s2z(H_subs, f_sample)
print(H_z)
list_pole, list_zero = find_polezero(H_z)
print(list_pole, list_zero)
zmap(list_pole, list_zero)
list_mag, list_angle, list_omega = calc_mag_angle(H_z, num_point=512)
plot_mag_angle_freq(list_mag, list_angle, list_omega, f_sample, path_fig="../p05.png")



