import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from assign_ts import assign_ts
import nibabel as nb
from img_four import img_ts_to_four

data_import_1=img_ts_to_four('/data2/tissue_seg/resample_func/0025427_session_1/rest_3mm.nii.gz', '/data2/tissue_seg/resample_func/0025427_session_1/')
data_import_2=img_ts_to_four('/data2/tissue_seg/resample_func/0025427_session_2/rest_3mm.nii.gz', '/data2/tissue_seg/resample_func/0025427_session_2/')

#data_import=np.load('/data2/tissue_seg/freq_comps/0025427_session_1/bandpassed_demeaned_filtered_antswarp_freqmat.npy')
data_1=assign_ts(data_import_1)
data_2=assign_ts(data_import_2)

target_import_1=nb.Nifti1Image.load('/data2/tissue_seg/prob_reg_mask/0025427_session_1/mask_sum_3mm.nii.gz')
target_import_2=nb.Nifti1Image.load('/data2/tissue_seg/prob_reg_mask/0025427_session_2/mask_sum_3mm.nii.gz')

target_1=assign_ts(target_import_1.get_data())
target_2=assign_ts(target_import_2.get_data())

data_1 = data_1[target_1 != 0, :]
target_1 = target_1[target_1 != 0]


n_sample_1 = len(data_1)

np.random.seed(0)
order_1 = np.random.permutation(n_sample_1)
data_1 = data_1[order_1]
target_1 = target_1[order_1].astype(np.float)

#data_train = data[:.5 * n_sample]
#target_train = target[:.5 * n_sample]
#data_test = data[.5 * n_sample:]
#target_test = target[.5 * n_sample:]

# fit the model

clf = svm.SVC(kernel='rbf', gamma=10)
clf.fit(data_1, target_1)


data_2 = data_2[target_2 != 0, :]
target_2 = target_2[target_2 != 0]


n_sample_2 = len(data_2)

np.random.seed(0)
order_2 = np.random.permutation(n_sample_2)
data_2 = data_2[order_2]
target_2 = target_2[order_2].astype(np.float)


prediction=clf.predict(data_2)

np.save('/data2/tissue_seg/resample_func/0025427_session_1/prediction', prediction)
np.save('/data2/tissue_seg/resample_func/0025427_session_1/actual', target_2)




