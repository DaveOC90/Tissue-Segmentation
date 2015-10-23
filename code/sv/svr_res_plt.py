import sys
sys.path.insert(0, '/data2/acpi/qc/scripts/')
from plot_overlay_imgs import op_vs_ip
import os

res_dir='/data2/tissue_seg/svr_res/'
plots_dir='/data2/tissue_seg/svr_res/plots/'

if not os.path.exists('/data2/tissue_seg/svr_res/plots'):
    os.makedirs('/data2/tissue_seg/svr_res/plots')


for tissue_type in ['gm', 'wm', 'csf']:
	ip_imgs=[]
	ip_errs=[]
	for kernel in ['linear', 'poly', 'rbf']:
		#ip_imgs.append(res_dir+tissue_type+'_pve/group_imgs/pred_img_'+kernel+'_mean.nii.gz')
		ip_errs.append(res_dir+tissue_type+'_pve/group_imgs/pred_err_'+kernel+'_mean.nii.gz')

	
	#op_vs_ip('Group', ['Linear', 'Poly', 'RBF'],ip_imgs, plots_dir+tissue_type+'_img_means.png',['','',''])
	op_vs_ip('Group', ['Linear', 'Poly', 'RBF'],ip_errs, plots_dir+tissue_type+'_err_mean.png',['','',''])
