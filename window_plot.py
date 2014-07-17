import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.stats.distributions as dist

import nitime.algorithms as tsa
import nitime.utils as utils
from nitime.viz import winspect
from nitime.viz import plot_spectral_estimate

npts = 128

fig01 = plt.figure()

# Boxcar with zeroed out fraction
b = sig.boxcar(npts)
zfrac = 0.15
zi = int(npts * zfrac)
b[:zi] = b[-zi:] = 0
name = 'Boxcar - zero fraction=%.2f' % zfrac
winspect(b, fig01, name)

winspect(sig.hanning(npts), fig01, 'Hanning')
winspect(sig.bartlett(npts), fig01, 'Bartlett')
winspect(sig.barthann(npts), fig01, 'Modified Bartlett-Hann')

plt.show()