def get_nifti_data(ipfile):

	import nibabel as nib
	
	## Load Image File
	ip_img=nib.nifti1.load(ipfile)
	
	## Load Data
	img_data=ip_img.get_data()
	
	## Get Shape
	img_shape=ip_img.shape
	
	## Get Affine
	img_aff=ip_img.get_affine()
	
	## Get Header
	img_header=ip_img.get_header()
	
	return img_data, img_shape, img_aff, img_header