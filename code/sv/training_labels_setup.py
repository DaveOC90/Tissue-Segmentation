import numpy as np
import nibabel as nb
import glob


imgs=glob.glob('../prob_map_thresh/0025428_session_1/*_mask*')
data_dict={}
coords_dict={}
for img in imgs:
    ## Load Data
    data_dict[img.split('/')[-1]]=nb.Nifti1Image.load(img).get_data()
    ## Get 
    coords_dict[img.split('/')[-1]]=np.asarray(np.where(data_dict[img.split('/')[-1]] == 1))
    zeros = data_dict[img.split('/')[-1]] == 0

    #data_dict[img.split('/')[-1]] = data_dict[img.split('/')[-1]][zeros == False, :]
    #coords_dict[img.split('/')[-1]] = coords_dict[img.split('/')[-1]][zeros == False]


"""
## Randomize Training Set
n_sample_1 = len(data_1)
np.random.seed(0)
order_1 = np.random.permutation(n_sample_1)

data_1 = data_1[order_1]
target_1 = target_1[order_1].astype(np.float)
#sesh_1=sesh_1[order_1]

## Retain X% of Training Set
subset_1=round(n_sample_1*(0.025))

data_1 = data_1[0:subset_1]
target_1 = target_1[0:subset_1]
"""
