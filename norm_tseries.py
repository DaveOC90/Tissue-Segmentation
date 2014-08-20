def norm_tseries(ip_img_data, ip_img_shape):

	import numpy as np
	
	img_t_mean=np.mean(ip_img_data,axis=3)
	img_t_std=np.std(ip_img_data,axis=3)

	op_img_data=np.zeros(ip_img_shape)
	for x in range(0,ip_img_shape[0]):
		for y in range(0,ip_img_shape[1]):
			for z in range(0,ip_img_shape[2]):
				op_img_data[x,y,z,:]=(ip_img_data[x,y,z,:]-img_t_mean[x,y,z])/img_t_std[x,y,z]
		
	return op_img_data
	
	