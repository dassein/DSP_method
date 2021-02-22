import cmath
import matplotlib.pyplot as plt
from math import log10

# import numpy
# import random

def memoize(f):
   cache = {}
   def memoizedFunction(*args):
      if args not in cache:
         cache[args] = f(*args)
      return cache[args]
   memoizedFunction.cache = cache
   return memoizedFunction

@memoize
def omega(p, q):
   return cmath.exp((2.0 * cmath.pi * 1j * q) / p)  # exp( 2pi * j * (q/p) )

def pad(inputList):
   k = 0
   while 2**k < len(inputList):
      k += 1
   return inputList + [0] * (2**k - len(inputList))

def fft(signal):  # len(signal) == 2**k
   n = len(signal)
   if n == 1:
      return signal
   else:
      Feven = fft([signal[i] for i in range(0, n, 2)])
      Fodd = fft([signal[i] for i in range(1, n, 2)])
      combined = [0] * n
      for m in range( int(n/2) ):
         combined[m] = Feven[m] + omega(n, -m) * Fodd[m]
         combined[m + int(n/2) ] = Feven[m] - omega(n, -m) * Fodd[m]
      return combined

def ifft(signal):
   timeSignal = fft([x.conjugate() for x in signal])
   return [x.conjugate()/len(signal) for x in timeSignal]

norm = lambda x: cmath.polar(x)[0]
angle = lambda x: cmath.polar(x)[1]
# delta = [1, 0, 0, 0, 0, 0, 0, 0] # unshifted delta of length 8
# deltaShift = [0, 1, 0, 0, 0, 0, 0, 0] # unshifted delta of length 8

def plot_spectrum(signal, f_s, path_fig, str_title="test"):
   length = len(signal)
   list_freq = [f_s * index / length for index in range(length//2 + 1)]
   spectrum = fft(signal)
   amp_spectrum = list( map(lambda x: 2*cmath.polar(x)[0]/length, spectrum[:length//2 + 1]) )
   amp_spectrum[0] = amp_spectrum[0] / 2
   fig = plt.figure()
   plt.subplot(2, 1, 1)
   plt.plot(list(range(length)), signal)
   plt.xlabel('Time index n')
   plt.ylabel('x(n)')
   plt.title(str_title)
   ax = plt.gca()
   ax.set_xlim([0, length-1])  # 0~1ms
   plt.grid()
   plt.subplot(2, 1, 2)
   plt.plot(list_freq, amp_spectrum)
   plt.xlabel('Frequency (Hz)')
   plt.ylabel(r'$A_k$')
   ax = plt.gca()
   ax.set_xlim([0, list_freq[-1]])  # 
   ax.set_ylim([0, None])
   plt.grid()
   plt.tight_layout()
   fig.savefig(path_fig)
   plt.show()

def plot_spectrum_dB(signal, f_s, path_fig, str_title="test"):
   try:
      from iir_filter.calc_mag_angle import dB_mag
   except ModuleNotFoundError:
      from calc_mag_angle import dB_mag
   length = len(signal)
   list_freq = [f_s * index / length for index in range(length//2 + 1)]
   spectrum = fft(signal)
   amp_spectrum = list( map(lambda x: 2*cmath.polar(x)[0]/length, spectrum[:length//2 + 1]) )
   amp_spectrum[0] = amp_spectrum[0] / 2
   amp_spectrum_dB = dB_mag(amp_spectrum)
   fig = plt.figure()
   plt.subplot(2, 1, 1)
   plt.plot(list(range(length)), signal)
   plt.xlabel('Time index n')
   plt.ylabel('x(n)')
   plt.title(str_title)
   ax = plt.gca()
   ax.set_xlim([0, length-1])  # 0~1ms
   plt.grid()
   plt.subplot(2, 1, 2)
   plt.plot(list_freq, amp_spectrum_dB)
   plt.xlabel('Frequency (Hz)')
   plt.ylabel(r'$A_k$ (dB)')
   ax = plt.gca()
   ax.set_xlim([80, 12800])  # list_freq[-1]
   ax.set_ylim([-20, None])
   ax.set_xscale('log')
   plt.grid()
   plt.tight_layout()
   fig.savefig(path_fig)
   plt.show()


if __name__ == "__main__":
    # signal = [1, 0, 0, 1, 0, 0, 0]
   signal = [ cmath.exp(2.0 * cmath.pi * 1j * i *(5/8)) for i in range(5) ]
   signal_pad = pad(signal)
   freq_spectrum = fft(signal_pad)
   import matplotlib.pyplot as plt
   norm_freq = list( map(lambda x: norm(x), freq_spectrum) )
   # plt.bar( [i for i in range(len(freq_spectrum)) ], norm_freq )
   plt.stem(norm_freq, use_line_collection=True)
   plt.show()
   plt.savefig('./output_images/chap4_1_fft1d_plt.png')
   plt.close()

   signal_recover = ifft(freq_spectrum)
   print("singnal:"), print(signal)
   print("singnal_recover:"), print(signal_recover)
   norm_signal_re = list( map(lambda x: norm(x), signal_recover) )
   plt.stem(norm_signal_re, use_line_collection=True)
   plt.show()
   plt.savefig('./output_images/chap4_1_fft1d_re_plt.png')
   plt.close()
