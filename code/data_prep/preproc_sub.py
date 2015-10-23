import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.ants as ants
import nipype.interfaces.afni as afni
from nipype.interfaces.ants import ApplyTransforms
from nipype.interfaces.ants import WarpImageMultiTransform
import nipype.interfaces.fsl as fsl
#from utils import seperate_warps_list
import os

ip_dir='/data2/jhu_atlas_tse/preprocessing/output/pipeline_jhu_atlas_tse'
op_dir='/data2/tissue_seg/working/detrend_despike_func2anat/'
sublist='/data2/tissue_seg/sublist_tseg.txt'

subs=[d.strip() for d in open(sublist, 'r')]

for sub in subs:
	for sesh in range(1,3):

		#if not os.path.exists(op_dir+'/'+sub+'session_'+str(sesh)+'/'):
		#	os.makedirs(op_dir+'/'+sub+'session_'+str(sesh)+'/')
		
		wf_name='tseg_anat_preproc'
		
		
		preprocflow=pe.Workflow(name=wf_name)
	
	    		
		## Despike
		func_despike = pe.Node(interface=afni.preprocess.Despike(),
		                             name='func_despike')
		func_despike.inputs.in_file=ip_dir+'/'+sub+'_session_'+str(sesh)+'/motion_correct/_scan_rest_1_rest/rest_calc_resample_volreg.nii.gz'
		func_despike.inputs.outputtype = 'NIFTI_GZ'
		
		
		## Linear and Quadratic Detrending
		func_detrend_lin_quad = pe.Node(interface=afni.preprocess.Detrend(),
		                             name='func_detrend_lin_quad')
		func_detrend_lin_quad.inputs.args = '-normalize -polort 2'
		func_detrend_lin_quad.inputs.outputtype = 'NIFTI_GZ'

		## Func to Anat
		linear_reg_func = pe.Node(interface=fsl.FLIRT(),
		                         name='linear_reg_func')
		linear_reg_func.inputs.cost = 'corratio'
		linear_reg_func.inputs.dof = 6
		linear_reg_func.inputs.interp = 'nearestneighbour'
		linear_reg_func.inputs.reference = ip_dir+'/'+sub+'_session_'+str(sesh)+'/anatomical_brain/anat_resample_calc.nii.gz'



		## Reho to Anat
		linear_reg_reho = pe.Node(interface=fsl.FLIRT(),
		                         name='linear_reg_reho')
		linear_reg_reho.inputs.cost = 'corratio'
		linear_reg_reho.inputs.dof = 6
		linear_reg_reho.inputs.interp = 'nearestneighbour'
		linear_reg_reho.inputs.in_file = ip_dir+'/'+sub+'_session_'+str(sesh)+'/reho_to_standard_smooth_zstd/_scan_rest_1_rest/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0/_bandpass_freqs_0.01.0.1/_fwhm_4/reho_to_standard_smooth_zstd.nii.gz'
		linear_reg_reho.inputs.reference = ip_dir+'/'+sub+'_session_'+str(sesh)+'/anatomical_brain/anat_resample_calc.nii.gz'

		## Vmhc to Anat
		linear_reg_vmhc = pe.Node(interface=fsl.FLIRT(),
		                         name='linear_reg_vmhc')
		linear_reg_vmhc.inputs.cost = 'corratio'
		linear_reg_vmhc.inputs.dof = 6
		linear_reg_vmhc.inputs.interp = 'nearestneighbour'
		linear_reg_vmhc.inputs.in_file = ip_dir+'/'+sub+'_session_'+str(sesh)+'/vmhc_fisher_zstd/_scan_rest_1_rest/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0/_bandpass_freqs_0.01.0.1/_fwhm_4/bandpassed_demeaned_filtered_maths_antswarp_tcorr_calc.nii.gz'
		linear_reg_vmhc.inputs.reference = ip_dir+'/'+sub+'_session_'+str(sesh)+'/anatomical_brain/anat_resample_calc.nii.gz'


		## Apply XFM
		app_xfm_lin = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin')
		app_xfm_lin.inputs.apply_xfm = True
		app_xfm_lin.inputs.reference = ip_dir+'/'+sub+'_session_'+str(sesh)+'/anatomical_brain/anat_resample_calc.nii.gz'

		## Apply XFM to Mean
		app_xfm_lin_mean = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_mean')
		app_xfm_lin_mean.inputs.apply_xfm = True
		app_xfm_lin_mean.inputs.in_file = ip_dir+'/'+sub+'_session_'+str(sesh)+'/mean_functional/_scan_rest_1_rest/rest_calc_resample_volreg_calc_tstat.nii.gz'
		app_xfm_lin_mean.inputs.reference = ip_dir+'/'+sub+'_session_'+str(sesh)+'/anatomical_brain/anat_resample_calc.nii.gz'



		preprocflow.connect(func_despike, 'out_file',
		                func_detrend_lin_quad, 'in_file')

		preprocflow.connect(func_detrend_lin_quad, 'out_file',
		                linear_reg_func, 'in_file')
		preprocflow.connect(func_detrend_lin_quad, 'out_file',
				app_xfm_lin, 'in_file')
		preprocflow.connect(linear_reg_func, 'out_matrix_file',
				app_xfm_lin, 'in_matrix_file')

		preprocflow.connect(linear_reg_func, 'out_matrix_file',
				app_xfm_lin_mean, 'in_matrix_file')


		linear_reg_vmhc.base_dir=os.path.abspath(op_dir+'/'+sub+'_session_'+str(sesh)+'/tseg_anat_preproc/')
		linear_reg_reho.base_dir=os.path.abspath(op_dir+'/'+sub+'_session_'+str(sesh)+'/tseg_anat_preproc/')
		preprocflow.base_dir=os.path.abspath(op_dir+'/'+sub+'_session_'+str(sesh)+'/')
		linear_reg_vmhc.run()
		linear_reg_reho.run()
		preprocflow.run()
		
