import spl_lib as spl
from scipy.signal import lfilter
import numpy
import scipy.io.wavfile as wf

NUMERATOR, DENOMINATOR = spl.A_weighting(48000)

old=0
min_decibel=100
max_decibel=0


fs, signal = wf.read('audioinput.wav')
y = lfilter(NUMERATOR, DENOMINATOR, signal)
new_decibel = 20*numpy.log10(spl.rms_flat(y))
if abs(old - new_decibel) > 3:
    old = new_decibel
    print new_decibel


