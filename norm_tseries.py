def norm_tseries(ip_img_data, ip_img_shape):

	import numpy as np
	
	img_t_mean=np.mean(img_data,axis=3)
	img_t_std=np.std(img_data,axis=3)
	
	for t in range(0,ip_img_shape[3]):
		op_img_data[:,:,:,x]=(ip_img_data[:,:,:,x]-img_t_mean)/img_t_std
		
	return op_series
	
	