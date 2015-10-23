ipdirec='/data2/tissue_seg/svr_res/fmri_reho_csf/' #$1
opdirec='/data2/tissue_seg/svr_res/fmri_reho_csf/' #$2
reffile='/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz' #$3


for ipimg in $(ls $ipdirec/pred*.nii.gz);do
	#echo $ipimg
	opimg_pre=$opdirec${ipimg#${ipdirec}*}
	opmat=${opimg_pre%.nii*}_flirtmat.mat
	opimg=${opimg_pre%.nii*}_stdreg.nii.gz
	if [[ $opimg_pre != *stdreg* ]];then
		echo ${opimg_pre%.nii*}
		flirt -in $ipimg -ref $reffile -out $opimg -omat $opmat -cost corratio -dof 6 -interp trilinear
		#flirt -in $ipimg -ref $reffile -out $opimg -init ${opmat/err/img} -applyxfm
	fi

done
