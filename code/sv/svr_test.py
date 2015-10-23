import numpy as np
from assign_ts import *
import nibabel as nb
from img_four import img_ts_to_four
import time
import sys
import shutil 
import os
from svm_iterkernel import svm_iterkernel, svr_iterkernel
from get_nifti_data import get_nifti_data
import glob


tooo=time.time()
rest_1 = '/data2/tissue_seg/working/detrend_despike_func2anat/0025427_session_1/tseg_anat_preproc/func_detrend_lin_quad/rest_calc_resample_volreg_despike_detrend.nii.gz'
rest_2 = '/data2/tissue_seg/working/detrend_despike_func2anat/0025427_session_2/tseg_anat_preproc/func_detrend_lin_quad/rest_calc_resample_volreg_despike_detrend.nii.gz' 
mask_2 = '/data2/tissue_seg/prob_map_thresh/0025427_session_2/mask_sum.nii.gz'
sub = '0025427'


trash, op_img_shape, op_img_affine, op_img_header = get_nifti_data(rest_2)


## Make 2D freq Component Arrays
direc_1='/'.join(rest_1.split('/')[:-1])
filename_1=rest_1.split('/')[-1]
direc_2='/'.join(rest_2.split('/')[:-1])
filename_2=rest_2.split('/')[-1]



data_1=np.load(direc_1+'/'+filename_1.split('.')[0]+'_flatmat.npy')
data_coords_1=np.load(direc_1+'/'+filename_1+'_coords.npy')

data_2=np.load(direc_2+'/'+filename_2.split('.')[0]+'_flatmat.npy')
data_coords_2=np.load(direc_2+'/'+filename_2+'_coords.npy')

## Convert to numpy
data_coords_2=np.array(data_coords_2)

## Load 3D Label Array
#target_import_1=nb.Nifti1Image.load(mask_1)
target_import_2=nb.Nifti1Image.load(mask_2)

## Make 1D Label Array
#target_1, target_coords_1=assign_ts(target_import_1.get_data())
target_2, target_coords_2=assign_ts(target_import_2.get_data(), '')

masks=sorted(glob.glob('../prob_map_thresh/'+sub+'_session_1/*_mask.nii.gz'))
data_dict={}
label_dict={}
coord_dict={}
for i,mask in enumerate(masks):
    ts=time.time()
    direc='/'.join(mask.split('/')[:-1])
    filename=mask.split('/')[-1]
    data = data_1
    if not os.path.exists(direc+'/'+filename.split('.')[0]+'_flatmat.npy'):
        labels = nb.Nifti1Image.load(mask).get_data()
        labels, coords = assign_ts(labels, direc+'/'+filename.split('.')[0])
    else:
        labels=np.load(direc+'/'+filename.split('.')[0]+'_flatmat.npy')
        coords=np.load(direc+'/'+filename.split('.')[0]+'_coords.npy')
    coords=np.array(coords)
    zeros = labels == 0
    labels = labels[zeros == False]
    data = data[zeros == False]
    coords = coords[zeros == False]
    n_sample = len(labels)
    subset = round(n_sample*0.5)
    data=data[0:subset]
    coords=coords[0:subset]
    labels=labels[0:subset]
    label_dict[mask.split('/')[-1]] = labels*(i+1)
    data_dict[mask.split('/')[-1]] = data
    coord_dict[mask.split('/')[-1]] = coords


data_1=np.concatenate(data_dict.values(), 0)
target_1=np.concatenate(label_dict.values(), 0)
coord_1=np.concatenate(coord_dict.values(), 0)
n_sample_1 = len(target_1)
np.random.seed(0)
order_1 = np.random.permutation(n_sample_1)

data_1=data_1[order_1]
target_1=target_1[order_1]
coord_1=coord_1[order_1]


print len(data_1), len(target_1), len(coord_1)
    
## Create Session Markers
#sesh_1=np.zeros(len(data_1))
#sesh_2=np.zeros(len(data_2))

#sesh_1[sesh_1 == 0] = 1
#sesh_2[sesh_2 == 0] = 2

## Remove Data with no Label
#zeros_1 = target_1 == 0
zeros_2 = target_2 == 0

#data_1 = data_1[zeros_1 == False, :]
#target_1 = target_1[zeros_1 == False]

data_2 = data_2[zeros_2 == False, :]
data_coords_2=data_coords_2[zeros_2 == False]
target_2 = target_2[zeros_2 == False]


## Randomize Training Set
#n_sample_1 = len(data_1)
#np.random.seed(0)
#order_1 = np.random.permutation(n_sample_1)

#data_1 = data_1[order_1]
#target_1 = target_1[order_1].astype(np.float)
#sesh_1=sesh_1[order_1]

## Retain X% of Training Set
#subset_1=round(n_sample_1*(0.025))

#data_1 = data_1[0:subset_1]
#target_1 = target_1[0:subset_1]
#sesh_1=sesh_1[0:subset_1]


## Get Prediction Output Format
op_ex_data, op_ex_shape, op_ex_affine, op_ex_header=get_nifti_data('/data2/jhu_atlas_tse/preprocessing/output/pipeline_jhu_atlas_tse/0025428_session_1/anatomical_brain/anat_resample_calc.nii.gz')


##Calculate Predictions for 3 kernels

if os.path.exists('/data2/tissue_seg/svc_res/test_pred_img_'+sub+'_svc_pred.txt'):
    os.remove('/data2/tissue_seg/svc_res/test_pred_img_'+sub+'_svc_pred.txt')

print "Pre SVM", time.time() - tooo

predictions, scores=svr_iterkernel(data_1, target_1, data_2, target_2, '/data2/tissue_seg/svc_res/test_pred_img_'+sub+'_svm_pred.txt')


#predictions=svm_iterkernel(data_1, target_1, data_2, target_2, 'None')

## Create Predicted Images

for prediction in predictions:
    op_img_data=np.zeros(op_img_shape)
    for i, coords in enumerate(data_coords_2):
        op_img_data[coords[0], coords[1], coords[2]]=predictions[prediction][i]

    op_img=nb.Nifti1Image(op_img_data, op_img_affine, op_img_header)
    nb.nifti1.save(op_img, '/data2/tissue_seg/svc_res/test_pred_img_'+prediction+'_'+sub+'.nii.gz')
