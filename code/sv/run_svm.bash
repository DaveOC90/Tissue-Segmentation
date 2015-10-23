#! /bin/bash
sublist='/data2/tissue_seg/sublist_tseg_swu.txt'

for sub in `cat $sublist`;do
#for sub in 0025427;do

echo $sub

python svr_pipeline.py /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_1/tseg_anat_preproc/func_detrend_lin_quad/rest_calc_resample_volreg_despike_detrend.nii.gz /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_2/tseg_anat_preproc/func_detrend_lin_quad/rest_calc_resample_volreg_despike_detrend.nii.gz None /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_2/tseg_anat_preproc/app_xfm_lin_csf_pve/segment_prob_0_flirt.nii.gz /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_1/tseg_anat_preproc/app_xfm_reho/reho_to_standard_smooth_zstd_flirt.nii.gz /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_2/tseg_anat_preproc/app_xfm_reho/reho_to_standard_smooth_zstd_flirt.nii.gz /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_1/tseg_anat_preproc/app_xfm_vmhc/bandpassed_demeaned_filtered_maths_antswarp_tcorr_calc_flirt.nii.gz /data2/tissue_seg/working/detrend_despike_func2anat/${sub}_session_2/tseg_anat_preproc/app_xfm_vmhc/bandpassed_demeaned_filtered_maths_antswarp_tcorr_calc_flirt.nii.gz $sub

done



