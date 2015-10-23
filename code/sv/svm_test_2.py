import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from assign_ts import assign_ts
import nibabel as nb
from img_four import img_ts_to_four
import time
import sys
import shutil 
import os
from sklearn.svm import SVC


rest_1 = sys.argv[1] #'/data2/tissue_seg/resample_func/0025428_session_1/rest_3mm.nii.gz'
rest_2 = sys.argv[2] #'/data2/tissue_seg/working/2mm_reg/0025428_func_antswarp.nii.gz'
mask_1 = sys.argv[3] #'/data2/tissue_seg/prob_reg_mask/0025428_session_1/mask_sum_3mm.nii.gz'
mask_2 = sys.argv[4] #'/data2/tissue_seg/prob_reg_mask/0025428_session_2/mask_sum.nii.gz' 
reho_1 = sys.argv[5] #'/data2/tissue_seg/reho_resample/0025428_session_1/reho_z_std_3mm.nii.gz'
reho_2 = sys.argv[6] #'/data2/jhu_atlas_tse/preprocessing/output/pipeline_jhu_atlas_tse/0025428_session_2/reho_to_standard_smooth_zstd/_scan_rest_1_rest/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0/_bandpass_freqs_0.01.0.1/_fwhm_4/reho_to_standard_smooth_zstd.nii.gz'
sub = sys.argv[7]

## Reho
reho_img_1=nb.Nifti1Image.load(reho_1)
reho_data_1=reho_img_1.get_data()

reho_img_2=nb.Nifti1Image.load(reho_2)
reho_data_2=reho_img_2.get_data()

## Generate 4D Freq Component Arrays
data_import_1=img_ts_to_four(rest_1, 'none')
data_import_2=img_ts_to_four(rest_2, 'none')

## Append Reho
x1,y1,z1,t1=data_import_1.shape
zeros1=np.zeros([x1,y1,z1,t1+2])
zeros1[:,:,:,:t1]=data_import_1
zeros1[:,:,:,t1+1]=reho_data_1


x2,y2,z2,t2=data_import_2.shape
zeros2=np.zeros([x2,y2,z2,t2+2])
zeros2[:,:,:,:t2]=data_import_2
zeros2[:,:,:,t2+1]=reho_data_2

data_import_1=(data_import_1 - np.mean(data_import_1))/np.std(data_import_1)
data_import_2=(data_import_2 - np.mean(data_import_2))/np.std(data_import_2)

## Make 2D freq Component Arrays
data_1, data_coords_1=assign_ts(data_import_1)
data_2, data_coords_2=assign_ts(data_import_2)


data_coords_2=np.array(data_coords_2)

## Load 3D Label Array
target_import_1=nb.Nifti1Image.load(mask_1)
target_import_2=nb.Nifti1Image.load(mask_2)

## Make 1D Label Array
target_1, target_coords_1=assign_ts(target_import_1.get_data())
target_2, target_coords_2=assign_ts(target_import_2.get_data())

sesh_1=np.zeros(len(data_1))
sesh_2=np.zeros(len(data_2))

sesh_1[sesh_1 == 0] = 1
sesh_2[sesh_2 == 0] = 2

zeros_1 = target_1 == 0
zeros_2 = target_2 == 0

data_1 = data_1[zeros_1 == False, :]
target_1 = target_1[zeros_1 == False]

data_2 = data_2[zeros_2 == False, :]
data_coords_2=data_coords_2[zeros_2 == False]
target_2 = target_2[zeros_2 == False]



n_sample_1 = len(data_1)
np.random.seed(0)
order_1 = np.random.permutation(n_sample_1)

data_1 = data_1[order_1]
target_1 = target_1[order_1].astype(np.float)
sesh_1=sesh_1[order_1]


#n_sample_2 = len(data_2)
#np.random.seed(0)
#order_2 = np.random.permutation(n_sample_2)

#data_2 = data_2[order_2]
#target_2 = target_2[order_2].astype(np.float)
#sesh_2=sesh_2[order_2]

subset_1=round(n_sample_1*(0.025))
#subset_2=round(n_sample_2*(0.025))

data_1 = data_1[0:subset_1]
target_1 = target_1[0:subset_1]
sesh_1=sesh_1[0:subset_1]

#data_2 = data_2[0:subset_2]
#target_2 = target_2[0:subset_2]
#sesh_2=sesh_2[0:subset_2]

data=np.concatenate([data_1,data_2], axis=0)
target=np.concatenate([target_1,target_2], axis=0)
sesh_data=np.concatenate([sesh_1,sesh_2], axis=0)

#zeros = target == 0

#data = data[zeros == False, :]
#sesh_data=sesh_data[zeros == False]
#target = target[zeros == False]


categories=[1,2,3]



# A support vector classifier
mni_2mm=nb.nifti1.load('/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz')
mni_2mm_header=mni_2mm.get_header()
mni_2mm_affine=mni_2mm.get_affine()
mni_2mm_data=mni_2mm.get_data()

if os.path.exists(sub+'_svm_pred_2mm_reho.txt'):
	os.remove(sub+'_svm_pred_2mm_reho.txt')

fo=open(sub+'_svm_pred_2mm_reho.txt','a')
for kernel in ['linear', 'poly', 'rbf']:
	t0=time.time()
	svm = SVC(C=1., kernel=kernel, cache_size=10240)
	svm.fit(data_1, target_1)
	prediction=svm.predict(data_2)
	pred_acc=(float(np.sum(prediction == target_2)))/len(target_2)
	pred_acc_gm=(prediction == 2) & (target_2 == 2)
	pred_acc_gm=float(pred_acc_gm.sum())/(len(target_2[target_2 == 2]))
	pred_acc_wm=(prediction == 3) & (target_2 == 3)
	pred_acc_wm=float(pred_acc_wm.sum())/(len(target_2[target_2 == 3]))
	pred_acc_csf=(prediction == 1) & (target_2 == 1)
	pred_acc_csf=float(pred_acc_csf.sum())/(len(target_2[target_2 == 1]))
	
	print time.time() - t0, ',kernel = '+kernel, ',pred acc = '+str(round(pred_acc*100))
	print 'pred gm = '+str(round(pred_acc_gm*100))
	print 'pred wm = '+str(round(pred_acc_wm*100))
	print 'pred csf = '+str(round(pred_acc_csf*100))

	
	fo.write('time='+str(time.time() - t0)+'sec,kernel='+kernel+',pred acc='+str(round(pred_acc*100))+'\n')
	fo.write('pred gm = '+str(round(pred_acc_gm*100))+'\n')
	fo.write('pred wm = '+str(round(pred_acc_wm*100))+'\n')
	fo.write('pred csf = '+str(round(pred_acc_csf*100))+'\n')
	

	#np.save('test_labels_'+kernel, target_2)
	#np.save('test_prediction_'+kernel, prediction)
	#np.save('test_coordinates_'+kernel, data_coords_2)

	op_img_data=np.zeros(mni_2mm_data.shape)
	for i, coords in enumerate(data_coords_2):
		op_img_data[coords[0], coords[1], coords[2]]=prediction[i]

	op_img=nb.Nifti1Image(op_img_data, mni_2mm_affine, mni_2mm_header)
	nb.nifti1.save(op_img, '/data2/tissue_seg/svm_res/reho/2mm_img/test_pred_img_'+kernel+'_'+sub+'_reho.nii.gz')
fo.close()
