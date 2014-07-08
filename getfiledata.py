def getfiledata(ipfile):

	import numpy as np
	import nibabel as nib
	

	## Load Image File
	ip_im=nib.nifti1.load(ipfile)
	
	## Load Data
	ip_data=ip_img.get_data()
	
	## Get Shape
	ip_shape=ip_img.shape
	
	## Get Affine
	img_aff=ip_img.get_affine()
	
	## Get Header
	img_header=ip_img.get_header()
	
	## Manipulate Image Data
	op_data=some_operation(ip_data)
		
	## Initialize Output
	op_nifti=nib.nifti1.Nifti1Image(op_data,img_aff,header=img_header)	

	## Save Output
	nib.nifti1.save(op_nifti, 'output_image.nii.gz')
				