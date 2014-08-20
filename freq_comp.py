import numpy as np
import scipy
import scipy.fftpack
import pylab

def freq_comp(signal, freq, plot_var):

	
	signal=np.squeeze(signal)

	FFT = abs(scipy.fft(signal))
	bins = scipy.fftpack.fftfreq(signal.size, freq)

	zerobin=np.where(bins==np.max(bins))
	FFT=FFT[0:zerobin[0]+1]
	bins=bins[bins >= 0]

	freq_bins_vals=[bins, FFT]

	if plot_var == 'Y':
		pylab.subplot(211)
		pylab.plot(range(0,len(signal)), signal)
		pylab.subplot(212)
		pylab.plot(bins,20*scipy.log10(FFT),'x')
		pylab.show()
		
	
	return freq_bins_vals