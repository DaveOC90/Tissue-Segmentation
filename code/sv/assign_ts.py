import numpy as np
import sys
sys.path.insert(0, '/home2/oconner/git/useful_bits/')
from get_nifti_data import get_nifti_data

def mergevols(file_1, file_2, filetype):
	if filetype == 'nifti':
		img_data_1, img_shape_1, img_affine_1, img_header_1 = get_nifti_data(file_1)
		img_data_2, img_shape_2, img_affine_2, img_header_2 = get_nifti_data(file_2)
	elif filetype == 'numpy':
		img_data_1 = file_1
		img_data_2 = file_2
		img_shape_1=img_data_1.shape
		img_shape_2=img_data_2.shape
	else:
		sys.exit("ERROR! Filetype must be 'nifti' or 'numpy'")


	if len(img_shape_1) == 4:
		x1,y1,z1,t1=img_shape_1
	if len(img_shape_2) == 4:
		x2,y2,z2,t2=img_shape_2
	if len(img_shape_1) == 3:
		x1,y1,z1=img_shape_1
		t1=1
	if len(img_shape_2) == 3:
		x2,y2,z2=img_shape_2
		t2=1
	

	
	op_data=np.zeros([x1,y1,z1,t1+t2])
	op_data[:,:,:,:t1]=img_data_1

	if t2 == 1:
		op_data[:,:,:,t1]=img_data_2
	else:
		op_data[:,:,:,t1:]=img_data_2

	return op_data
	



def assign_ts(mat, savename):

	
	count_list=[]
	if len(mat.shape) == 4:	
		w,x,y,z=mat.shape

		new_mat=np.zeros((w*x*y,z))
		count=0
		for i in range(0,w):
			for j in range(0,x):
				for k in range(0,y):
					new_mat[count]=mat[i,j,k,:]
					count_list.append([i,j,k])
					count=count+1

	else:
		w,x,y=mat.shape

		new_mat=np.zeros((w*x*y))
		count=0
		for i in range(0,w):
			for j in range(0,x):
				for k in range(0,y):
					new_mat[count]=mat[i,j,k]
					count_list.append([i,j,k])
					count=count+1
	if savename:
		np.save(savename+'_flatmat', new_mat)
		np.save(savename+'_coords', count_list)

	return new_mat, count_list
				
