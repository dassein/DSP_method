from iir_filter.calc_mag_angle import plot_mag_angle_freq, calc_mag_angle
# from fir_filter.calc_mag_angle import calc_mag_angle
from fir_filter.window import window
from fir_filter.fir_filter import fir_filter, print_approx
from iir_filter.poly import Poly, Polyz

list_f_cutoff = [800, 1000]
f_sample = 4000
filter_len = 5

list_filter = fir_filter(list_f_cutoff, f_sample, filter_len, str_filter_type="band_pass")
print_approx(list_filter, precision=5)

# Hamming window function.
str_window_type = "Hamming"
path_fig = "../p03_hamm.png"
list_filter_window = window(list_filter, str_window_type=str_window_type)
print_approx(list_filter_window, precision=6)
list_mag, list_angle, list_omega = calc_mag_angle(Polyz(list_filter_window))
plot_mag_angle_freq(list_mag, list_angle, list_omega, f_sample, path_fig=path_fig)