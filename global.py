import os
import numpy as np
import nibabel as nb
from get_nifti_data import get_nifti_data
from norm_tseries import norm_tseries
from freq_comp import freq_comp
import scipy
import scipy.fftpack
import pylab
from scipy import pi
from sklearn import datasets

#ip_img='../test_images/M10914326_rest_2500.nii.gz'
#img_data, img_shape, img_affine, img_header=get_nifti_data(ip_img)
#norm_img_data=norm_tseries(img_data, img_shape)

#f=float(1)/2.5


#signal=norm_img_data[36,36,19,0:63]
#t = np.arange(0, f*64, f)
#signal = np.sin(2*(np.pi*t*1)) + np.cos(2*(np.pi*t*.6)) + np.random.randn(len(t))*0.3



#freq_comps=freq_comp(signal, f, 'Y')

#print freq_comps




iris = datasets.load_iris()
pylab.imshow(iris)