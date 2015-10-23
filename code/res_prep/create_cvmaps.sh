ipdirec='/data2/tissue_seg/svr_res/gm_pve'
opdirec=$ipdirec/group_imgs/
mask_3mm=/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain_mask.nii.gz

mkdir -p $opdirec

for kernel in linear poly rbf;do
	
	fslmerge -t $opdirec/pred_img_${kernel}_merge.nii.gz $ipdirec/pred_img_${kernel}_*stdreg*.nii.gz
	fslmerge -t $opdirec/pred_err_${kernel}_merge.nii.gz $ipdirec/pred_err_${kernel}_*stdreg*.nii.gz

	fslmaths $opdirec/pred_img_${kernel}_merge.nii.gz -abs $opdirec/pred_img_${kernel}_merge_abs.nii.gz
	fslmaths $opdirec/pred_err_${kernel}_merge.nii.gz -abs $opdirec/pred_err_${kernel}_merge_abs.nii.gz
	
	fslmaths $opdirec/pred_img_${kernel}_merge_abs.nii.gz -Tmean $opdirec/pred_img_${kernel}_mean.nii.gz
	fslmaths $opdirec/pred_err_${kernel}_merge_abs.nii.gz -Tmean $opdirec/pred_err_${kernel}_mean.nii.gz

	fslmaths $opdirec/pred_img_${kernel}_merge_abs.nii.gz -Tstd $opdirec/pred_img_${kernel}_std.nii.gz
	fslmaths $opdirec/pred_err_${kernel}_merge_abs.nii.gz -Tstd $opdirec/pred_err_${kernel}_std.nii.gz

	fslmaths $opdirec/pred_img_${kernel}_std.nii.gz -div $opdirec/pred_img_${kernel}_mean.nii.gz $opdirec/pred_img_${kernel}_cv.nii.gz
	fslmaths $opdirec/pred_err_${kernel}_std.nii.gz -div $opdirec/pred_err_${kernel}_mean.nii.gz $opdirec/pred_err_${kernel}_cv.nii.gz

	fslmaths $opdirec/pred_img_${kernel}_cv.nii.gz -mul $mask_3mm $opdirec/pred_img_${kernel}_cv_mask.nii.gz
	fslmaths $opdirec/pred_err_${kernel}_cv.nii.gz -mul $mask_3mm $opdirec/pred_err_${kernel}_cv_mask.nii.gz

done
