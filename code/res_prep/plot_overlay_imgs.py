import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import matplotlib as mpl
import nibabel as nib
import numpy as np
import os
from sklearn import preprocessing
from skimage import filters
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator

def img_segmentation(background_image, overlay, bgname, olname, subid,imagetype):
	##Load Image and Template
	bkgd_img=nib.nifti1.load(background_image)
	ol_img=nib.nifti1.load(overlay)


	## Load Data and Ensure it is in Numpy Format
	bkgd_data=bkgd_img.get_data()
	bkgd_data=np.array(bkgd_data)
	ol_data=ol_img.get_data()
	ol_data=np.array(ol_data)
	ol_data_masked=np.ma.masked_where(ol_data <  1, ol_data)
	ol_data_masked_max=np.max(ol_data_masked)
	## Get Matrix Dims
	bkgd_shape=bkgd_img.shape	
	ol_shape=ol_img.shape

	## Get Overlap and Difference
	bool_data1=bkgd_data > (np.max(bkgd_data)*0.1)
	binar_data1=bool_data1.astype(int)

	bool_data2=ol_data > (np.max(ol_data)*0.1)
	binar_data2=bool_data2.astype(int)


	in_bkgd_only=np.zeros([bkgd_shape[0],bkgd_shape[1],bkgd_shape[2]])
	in_ol_only=np.zeros([bkgd_shape[0],bkgd_shape[1],bkgd_shape[2]])
	in_both=np.zeros([bkgd_shape[0],bkgd_shape[1],bkgd_shape[2]])
	
	for x in range(0,bkgd_shape[0]):
		for y in range(0,bkgd_shape[1]):
			for z in range(0,bkgd_shape[2]):
				if bool_data1[x,y,z] == 1 and bool_data2[x,y,z] ==1:
					in_both[x,y,z]=1
				if bool_data1[x,y,z] == 1 and bool_data2[x,y,z] ==0:
					in_bkgd_only[x,y,z]=1
				if bool_data1[x,y,z] == 0 and bool_data2[x,y,z] ==1:
					in_ol_only[x,y,z]=1

	in_both=np.ma.masked_where(in_both <  1, in_both)
	in_bkgd_only=np.ma.masked_where(in_bkgd_only <  1, in_bkgd_only)
	in_ol_only=np.ma.masked_where(in_ol_only <  1, in_ol_only)

	## Create Aspect Ratios ### Put in Voxels
	#Axial
	img_aspect_axial_bkgd=float(bkgd_shape[0])/float(bkgd_shape[1])
	img_aspect_axial_bkgd=round(img_aspect_axial_bkgd*100)

	#Coronal
	img_aspect_cor_bkgd=float(bkgd_shape[0])/float(bkgd_shape[2])
	img_aspect_cor_bkgd=round(img_aspect_cor_bkgd*100)

	#Saggital
	img_aspect_sag_bkgd=float(bkgd_shape[1])/float(bkgd_shape[2])
	img_aspect_sag_bkgd=round(img_aspect_sag_bkgd*100)

	##Create Axial Slice of Background, Overlay, and Segemented Images
	## Original Images
	#Axial
	axial_mid_bkgd_index=round(bkgd_shape[2]/2)
	axial_bkgd_slice=bkgd_data[:,:,axial_mid_bkgd_index]	
	axial_bkgd_slice=np.rot90(axial_bkgd_slice)
	

	axial_mid_ol_index=round(ol_shape[2]/2)	
	axial_ol_slice=ol_data[:,:,axial_mid_ol_index]
	axial_ol_slice=np.rot90(axial_ol_slice)

	axial_in_both=in_both[:,:,axial_mid_bkgd_index]
	axial_in_both=np.rot90(axial_in_both)
	

	axial_in_bkgd_only=in_bkgd_only[:,:,axial_mid_bkgd_index]
	axial_in_bkgd_only=np.rot90(axial_in_bkgd_only)
	

	axial_in_ol_only=in_ol_only[:,:,axial_mid_bkgd_index]
	axial_in_ol_only=np.rot90(axial_in_ol_only)
	

	#Coronal
	cor_mid_bkgd_index=round(bkgd_shape[1]/2)
	cor_bkgd_slice=bkgd_data[:,cor_mid_bkgd_index,:]
	cor_bkgd_slice=np.rot90(cor_bkgd_slice)

	cor_mid_ol_index=round(ol_shape[1]/2)
	cor_ol_slice=ol_data[:,cor_mid_ol_index,:]
	cor_ol_slice=np.rot90(cor_ol_slice)

	cor_in_both=in_both[:,cor_mid_ol_index,:]
	cor_in_both=np.rot90(cor_in_both)

	cor_in_bkgd_only=in_bkgd_only[:,cor_mid_ol_index,:]
	cor_in_bkgd_only=np.rot90(cor_in_bkgd_only)

	cor_in_ol_only=in_ol_only[:,cor_mid_ol_index,:]
	cor_in_ol_only=np.rot90(cor_in_ol_only)
	
	#Saggital
	sag_mid_bkgd_index=round(bkgd_shape[0]/2)
	sag_bkgd_slice=bkgd_data[sag_mid_bkgd_index,:,:]
	sag_bkgd_slice=np.rot90(sag_bkgd_slice)

	sag_mid_ol_index=round(ol_shape[0]/2)
	sag_ol_slice=ol_data[sag_mid_ol_index,:,:]
	sag_ol_slice=np.rot90(sag_ol_slice)

	sag_in_both=in_both[sag_mid_ol_index,:,:]
	sag_in_both=np.rot90(sag_in_both)

	sag_in_bkgd_only=in_bkgd_only[sag_mid_ol_index,:,:]
	sag_in_bkgd_only=np.rot90(sag_in_bkgd_only)

	sag_in_ol_only=in_ol_only[sag_mid_ol_index,:,:]
	sag_in_ol_only=np.rot90(sag_in_ol_only)
	
	

	#plt.close('All')
	
	fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(ncols=3, nrows=3, figsize=(16,16))
	plt.suptitle(subid+' File Comparison Segmentation \n Blue =Both, Green = B/G only, Red = O/L only', fontsize=20)	
	
	my_cmap1 = plt.cm.winter#YlOrRd
	my_cmap2 = plt.cm.summer
	my_cmap3 = plt.cm.autumn#YlOrRd

	alpha_val=.8

	titlearray=['Axial', 'Coronal', 'Saggital']
	
	ax1.imshow(axial_in_both, alpha=1, interpolation='none', cmap=my_cmap1)
	ax1.imshow(axial_in_bkgd_only, alpha=alpha_val, interpolation='none', cmap=my_cmap2)
	ax1.imshow(axial_in_ol_only, alpha=alpha_val, interpolation='none', cmap=my_cmap3)
	ax1.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax1.set_title('Overlay '+titlearray[0])

	ax2.imshow(cor_in_both, alpha=1, interpolation='none', cmap=my_cmap1)
	ax2.imshow(cor_in_bkgd_only, alpha=alpha_val, interpolation='none',cmap=my_cmap2)
	ax2.imshow(cor_in_ol_only, alpha=alpha_val, interpolation='none', cmap=my_cmap3)
	ax2.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax2.set_title('Overlay '+titlearray[1])
		
	ax3.imshow(sag_in_both, alpha=1, interpolation='none', cmap=my_cmap1)
	ax3.imshow(sag_in_bkgd_only, alpha=alpha_val, interpolation='none', cmap=my_cmap2)
	ax3.imshow(sag_in_ol_only, alpha=alpha_val, interpolation='none', cmap=my_cmap3)
	ax3.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax3.set_title('Overlay '+titlearray[2])

	ax4.imshow(axial_bkgd_slice, interpolation='nearest', cmap=plt.cm.gray)
	ax4.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax4.set_title(bgname+' '+titlearray[0])

	ax5.imshow(cor_bkgd_slice, interpolation='nearest', cmap=plt.cm.gray)
	ax5.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax5.set_title(bgname+' '+titlearray[1])
		
	ax6.imshow(sag_bkgd_slice, interpolation='nearest', cmap=plt.cm.gray)
	ax6.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax6.set_title(bgname+' '+titlearray[2])

	ax7.imshow(axial_ol_slice, interpolation='nearest', cmap=plt.cm.gray)
	ax7.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax7.set_title(olname+' '+titlearray[0])

	ax8.imshow(cor_ol_slice, interpolation='nearest', cmap=plt.cm.gray)
	ax8.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax8.set_title(olname+' '+titlearray[1])
		
	ax9.imshow(sag_ol_slice, interpolation='nearest', cmap=plt.cm.gray)
	ax9.set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
	ax9.set_title(olname+' '+titlearray[2])

	#ax10=fig.add_axes([0.92,0.1,0.02,0.8])
	#ax10.imshow(([0,1,2],[0,1,2],[0,1,2]))

	#cb=mpl.colorbar.ColorbarBase(ax10,cmap=my_cmap, norm=mpl.colors.Normalize			(vmin=0,vmax=ol_data_masked_max),orientation='vertical')

	#colorbar()

	#plt.suptitle(foldname, fontsize=20)
	plt.tight_layout()
	plt.autoscale()
	plt.savefig('./op_images/rest_645/'+imagetype+'_'+subid)
	#plt.show()


def pull_midslices(path):

		##Load Image
		load_img=nib.nifti1.load(path)

		## Extract Data
		img_data=load_img.get_data()
		
		## Get Matrix Dims
		img_shape=load_img.shape
		mean_img_shape=img_shape/np.mean(img_shape)
		## Get Img Voxel Size
		img_vox=load_img.get_header().get_zooms()
		mean_img_vox=img_vox/np.mean(img_vox)	
		
		#print img_vox, mean_img_vox		
	
		if len(img_shape) == 4:
			img_data=img_data[:,:,:,0]
	
		## Create Aspect Ratios ### Put in Voxels
		#Axial
		img_aspect_axial=float(mean_img_vox[1])/float(mean_img_vox[0])
		#img_aspect_axial=round(img_aspect_axial*100)

		#Coronal
		img_aspect_cor=float(mean_img_vox[2])/float(mean_img_vox[0])
		#img_aspect_cor=round(img_aspect_cor*100)

		#Saggital
		img_aspect_sag=float(mean_img_vox[2])/float(mean_img_vox[1])
		#img_aspect_sag=round(img_aspect_sag*100)

		##Create Slices of Images
		#Axial
		axial_mid_index=round(img_shape[2]/2)
		axial_slice=img_data[:,:,axial_mid_index]	
		axial_slice=np.rot90(axial_slice)
	
		#Coronal
		cor_mid_index=round(img_shape[1]/2)
		cor_slice=img_data[:,cor_mid_index,:]
		cor_slice=np.rot90(cor_slice)
	
		#Saggital
		sag_mid_index=round(img_shape[0]/2)
		sag_slice=img_data[sag_mid_index,:,:]
		sag_slice=np.rot90(sag_slice)

		return axial_slice, cor_slice, sag_slice, img_aspect_axial, img_aspect_cor, img_aspect_sag
	



def op_vs_ip(subid, image_types, imagepaths, op_direc, overlays):
	
	
	img_data_group=[]
	img_shape_group=[]
	ol_data_group=[]
	ol_shape_group=[]
	for i, path in enumerate(imagepaths):	

		axial_slice, cor_slice, sag_slice, img_aspect_axial, img_aspect_cor, img_aspect_sag = pull_midslices(path)
		if os.path.isfile(overlays[i]):
			axial_slice_ol, cor_slice_ol, sag_slice_ol, img_aspect_axial_ol, img_aspect_cor_ol, img_aspect_sag_ol = pull_midslices(overlays[i])
			ol_data_group.append([axial_slice_ol, cor_slice_ol, sag_slice_ol])
			ol_shape_group.append([img_aspect_axial_ol, img_aspect_cor_ol, img_aspect_sag_ol])
		else:
			ol_data_group.append(['null','null','null'])
			ol_shape_group.append(['null','null','null'])
		## Append to Matrices
		img_data_group.append([axial_slice, cor_slice, sag_slice])
		img_shape_group.append([img_aspect_axial,img_aspect_cor,img_aspect_sag])
		


	my_cmap=plt.cm.gray


	fig, axarr = plt.subplots(ncols=np.shape(img_shape_group)[1], nrows=np.shape(img_shape_group)[0], figsize=(np.shape(img_shape_group)[0]*5,np.shape(img_shape_group)[1]*5))
	plt.suptitle(subid+' File Comparison', fontsize=20)	
	
	titlearray=['Axial', 'Coronal', 'Saggital']
	
	for x in range(0,np.shape(img_shape_group)[0]):
		for y in range(0,np.shape(img_shape_group)[1]):
			im = axarr[x, y].imshow(img_data_group[x][y], cmap=my_cmap, aspect=img_shape_group[x][y])
			axarr[x, y].set_xlabel('(Right) Radiological Convention (Left)', fontsize=10)
			axarr[x, y].set_title(image_types[x]+' '+titlearray[y])
			#divider = make_axes_locatable(axarr[x, y])
			#cax_ = divider.append_axes("right", size="5%", pad=0.05)
			#cbar = plt.colorbar(im, cax=cax_, ticks=MultipleLocator(round(np.max(img_data_group[x][y])/5, 1)))
			axarr[x, y].xaxis.set_visible(False)
			axarr[x, y].yaxis.set_visible(False)




			if os.path.isfile(overlays[x]):
				if x == 1:
					thresh=0.25
				if x == 2:
					thresh=0.4
				sl=np.array(ol_data_group[x][y]).astype(np.float64)
				sl=filters.sobel(sl)
				sl=preprocessing.binarize(sl, np.max(sl)*thresh)
				sl[sl < 1] = 'Nan'
				axarr[x, y].imshow(sl, cmap='autumn', aspect=ol_shape_group[x][y])

	#plt.show()
	plt.tight_layout()
	plt.autoscale()
	plt.savefig(op_direc)


