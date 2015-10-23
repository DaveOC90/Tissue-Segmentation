def img_ts_to_four(img_name, op_name):

	import numpy as np
	import nibabel as nb
	import scipy as sp
	from extract_fourier import freq_comp
	import os
	img=nb.Nifti1Image.load(img_name)

	img_data=img.get_data()
	img_data=img_data[:,:,:,0:127]
	img_hdr=img.get_header()
	

	shape=img_data.shape

	op_arr=np.zeros((shape[0], shape[1], shape[2], 64))	

	for x in range(0,shape[0]):
		for y in range(0,shape[1]):
			for z in range(0,shape[2]):
				#print x,y,z
				op_arr[x,y,z,:], temp = freq_comp(img_data[x][y][z][0:127], 0.5, 'N')
		print '[ '+'='*(int((float(x)/shape[0])*10))+' '*(10-(int((float(x)/shape[0])*10)))+' ] '+str(int((float(x)/shape[0])*100))+'% complete'
	
	if op_name != ('none' or 'None'):
		if not os.path.isfile(op_name):
			np.save(op_name, op_arr)
	return op_arr
