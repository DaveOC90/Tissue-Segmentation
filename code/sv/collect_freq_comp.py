sublist='/data2/tissue_seg/tissue_seg_sublist.txt'
cpac_op_dir='/data2/jhu_atlas_tse/preprocessing/output/pipeline_jhu_atlas_tse'
cpac_work_dir='/data2/jhu_atlas_tse/preprocessing/working'
ts_dir='/data2/tissue_seg'
ref_image='/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'

import os
from img_four import img_ts_to_four

op_dirs=os.listdir(cpac_op_dir)
subs=sorted([d.strip() for d in open(sublist, 'r')])

for opdir in op_dirs:
	for sub in subs:
		if sub in opdir:
			if not os.path.exists(ts_dir+'/freq_comps/'+opdir+'/'):
				os.makedirs(ts_dir+'/freq_comps/'+opdir+'/')
			if not os.path.isfile(ts_dir+'/freq_comps/'+opdir+'/bandpassed_demeaned_filtered_antswarp_freqmat.npy'):
				print opdir
				img_ts_to_four(cpac_op_dir+'/'+opdir+'/functional_mni/_scan_rest_1_rest/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0/_bandpass_freqs_0.01.0.1/bandpassed_demeaned_filtered_antswarp.nii.gz', ts_dir+'/freq_comps/'+opdir+'/')

	
