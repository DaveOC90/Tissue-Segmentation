masks=sorted(glob.glob('/data2/tissue_seg/prob_map_softlinks/'+sub+'_session_1/*_mask.nii.gz'))
data_dict={}
label_dict={}
coord_dict={}
for i,mask in enumerate(masks):
    ts=time.time()
    direc='/'.join(mask.split('/')[:-1])
    filename=mask.split('/')[-1]
    data = data_1
    #if not os.path.exists(direc+'/'+filename.split('.')[0]+'_flatmat.npy'):
    labels = nb.Nifti1Image.load(mask).get_data()
    labels, coords = assign_ts(labels, direc+'/'+filename.split('.')[0])
    #else:
    #    labels=np.load(direc+'/'+filename.split('.')[0]+'_flatmat.npy')
    #    coords=np.load(direc+'/'+filename.split('.')[0]+'_coords.npy')
    coords=np.array(coords)
    zeros = labels == 0.0
    labels = labels[zeros == False]
    data = data[zeros == False]
    coords = coords[zeros == False]
    #n_sample = len(labels)
    #if n_sample > 500:
    #    subset = round(n_sample*0.2)
    #else:
    #    subset=n_sample
    #data=data[0:subset]
    #coords=coords[0:subset]
    #labels=labels[0:subset]
    label_dict[mask.split('/')[-1]] = labels*(i+1)
    data_dict[mask.split('/')[-1]] = data
    coord_dict[mask.split('/')[-1]] = coords
