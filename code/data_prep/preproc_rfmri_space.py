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
sublist='/data2/tissue_seg/sublist_tseg_swu.txt'

subs=[d.strip() for d in open(sublist, 'r')]

for sub in subs:
	for sesh in range(1,3):

		#if not os.path.exists(op_dir+'/'+sub+'session_'+str(sesh)+'/'):
		#	os.makedirs(op_dir+'/'+sub+'session_'+str(sesh)+'/')

		pve_0='/data2/tissue_seg/pve_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_0.nii.gz'
		pve_1='/data2/tissue_seg/pve_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_1.nii.gz'
		pve_2='/data2/tissue_seg/pve_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_2.nii.gz'
		prob_0='/data2/tissue_seg/prob_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_0.nii.gz'
		prob_1='/data2/tissue_seg/prob_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_1.nii.gz'
		prob_2='/data2/tissue_seg/prob_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_2.nii.gz'
		
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
	

		## Linear and Quadratic Detrending Mean Func
		func_mean = pe.Node(interface=fsl.maths.MeanImage(),
		                             name='func_mean')
		func_mean.inputs.output_type = 'NIFTI_GZ'
		func_mean.inputs.in_file=ip_dir+'/'+sub+'_session_'+str(sesh)+'/motion_correct/_scan_rest_1_rest/rest_calc_resample_volreg.nii.gz'

		## Anatomical to Rest
		linear_reg_anat = pe.Node(interface=fsl.FLIRT(),
		                         name='linear_reg_anat')
		linear_reg_anat.inputs.cost = 'corratio'
		linear_reg_anat.inputs.dof = 6
		linear_reg_anat.inputs.interp = 'trilinear'
		linear_reg_anat.inputs.in_file = ip_dir+'/'+sub+'_session_'+str(sesh)+'/anatomical_brain/anat_resample_calc.nii.gz'
		linear_reg_anat.inputs.out_file = '/data2/tissue_seg/working/detrend_despike_func2anat/'+sub+'_session_'+str(sesh)+'/tseg_anat_preproc/linear_reg_anat/anat_flirt.nii.gz'


		## CSF TP to Rest
		## Apply XFM
		app_xfm_lin_csf_prob = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_csf_prob')
		app_xfm_lin_csf_prob.inputs.apply_xfm = True
		app_xfm_lin_csf_prob.inputs.in_file = prob_0

		## GM TP to Rest
		## Apply XFM
		app_xfm_lin_gm_prob = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_gm_prob')
		app_xfm_lin_gm_prob.inputs.apply_xfm = True
		app_xfm_lin_gm_prob.inputs.in_file = prob_1

		## WM TP to Rest
		## Apply XFM
		app_xfm_lin_wm_prob = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_wm_prob')
		app_xfm_lin_wm_prob.inputs.apply_xfm = True
		app_xfm_lin_wm_prob.inputs.in_file = prob_2


		## CSF PVE to Rest
		## Apply XFM
		app_xfm_lin_csf_pve = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_csf_pve')
		app_xfm_lin_csf_pve.inputs.apply_xfm = True
		app_xfm_lin_csf_pve.inputs.in_file = pve_0

		## GM PVE to Rest
		## Apply XFM
		app_xfm_lin_gm_pve = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_gm_pve')
		app_xfm_lin_gm_pve.inputs.apply_xfm = True
		app_xfm_lin_gm_pve.inputs.in_file = pve_1

		## WM PVE to Rest
		## Apply XFM
		app_xfm_lin_wm_pve = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin_wm_pve')
		app_xfm_lin_wm_pve.inputs.apply_xfm = True
		app_xfm_lin_wm_pve.inputs.in_file = pve_2

		datasink = pe.Node(nio.DataSink(), name='sinker')
		datasink.inputs.base_directory = '/data2/tissue_seg/working/detrend_despike_func2anat/'+sub+'_session_'+str(sesh)+'/tseg_anat_preproc/linear_reg_anat'

		## CSF Mask
		csf_prob_bin = pe.Node(interface=afni.preprocess.Calc(),
		                             name='csf_prob_bin')
		csf_prob_bin.inputs.in_file_a = prob_0
		csf_prob_bin.inputs.expr = 'ispositive(a-0.96)'
		csf_prob_bin.inputs.outputtype = 'NIFTI_GZ'

		## GM Mask
		gm_prob_bin = pe.Node(interface=afni.preprocess.Calc(),
		                             name='gm_prob_bin')
		gm_prob_bin.inputs.in_file_a = prob_1
		gm_prob_bin.inputs.expr = 'ispositive(a-0.7)'
		gm_prob_bin.inputs.outputtype = 'NIFTI_GZ'

		## WM Mask
		wm_prob_bin = pe.Node(interface=afni.preprocess.Calc(),
		                             name='wm_prob_bin')
		wm_prob_bin.inputs.in_file_a = prob_2
		wm_prob_bin.inputs.expr = 'ispositive(a-0.96)'
		wm_prob_bin.inputs.outputtype = 'NIFTI_GZ'

		## CSF Mask to Rest
		## Apply XFM
		app_xfm_csf_prob_bin = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_csf_prob_bin')
		app_xfm_csf_prob_bin.inputs.apply_xfm = True

		## GM Mask to Rest
		## Apply XFM
		app_xfm_gm_prob_bin = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_gm_prob_bin')
		app_xfm_gm_prob_bin.inputs.apply_xfm = True

		## WM Mask to Rest
		## Apply XFM
		app_xfm_wm_prob_bin = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_wm_prob_bin')
		app_xfm_wm_prob_bin.inputs.apply_xfm = True

		## Reho to Rest
		app_xfm_reho = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_reho')
		app_xfm_reho.inputs.apply_xfm = True
		app_xfm_reho.inputs.in_file = ip_dir+'/'+sub+'_session_'+str(sesh)+'/reho_to_standard_smooth_zstd/_scan_rest_1_rest/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0/_bandpass_freqs_0.01.0.1/_fwhm_7/reho_to_standard_smooth_zstd.nii.gz'

		## VMHC to Rest
		app_xfm_vmhc = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_vmhc')
		app_xfm_vmhc.inputs.apply_xfm = True
		app_xfm_vmhc.inputs.in_file = ip_dir+'/'+sub+'_session_'+str(sesh)+'/vmhc_fisher_zstd/_scan_rest_1_rest/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm0.global0.motion1.quadratic1.gm0.compcor1.csf0/_bandpass_freqs_0.01.0.1/_fwhm_7/bandpassed_demeaned_filtered_maths_antswarp_tcorr_calc.nii.gz'

		## Func OP
		preprocflow.connect(func_despike, 'out_file',
		                func_detrend_lin_quad, 'in_file')

		#preprocflow.connect(func_detrend_lin_quad, 'out_file',
		#               func_mean, 'in_file')

		## Register Anat to Mean Motion Corrected Func
		preprocflow.connect(func_mean, 'out_file',
		                linear_reg_anat, 'reference')
		
		## Sunk Registered Anat
		preprocflow.connect(linear_reg_anat, 'out_file',
		                datasink, 'output.@linear_reg_anat')
		
		## Send Anat affines to Prob Map Reg
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_lin_csf_prob, 'in_matrix_file')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_lin_gm_prob, 'in_matrix_file')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_lin_wm_prob, 'in_matrix_file')

		## Send Anat Affines to PVE Map Reg
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_lin_csf_pve, 'in_matrix_file')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_lin_gm_pve, 'in_matrix_file')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_lin_wm_pve, 'in_matrix_file')

		## Send Anat Affines to Binarized Prob Map Reg
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_csf_prob_bin, 'in_matrix_file')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_gm_prob_bin, 'in_matrix_file')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_wm_prob_bin, 'in_matrix_file')

		## Send Mean Func to Prob Map Reg as Ref
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_lin_csf_prob, 'reference')
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_lin_gm_prob, 'reference')
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_lin_wm_prob, 'reference')

		## Send Mean Func to PVE Map Reg as Ref
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_lin_csf_pve, 'reference')
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_lin_gm_pve, 'reference')
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_lin_wm_pve, 'reference')

		## Send Mean Func to Prob Map Binarized Reg as Ref
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_csf_prob_bin, 'reference')
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_gm_prob_bin, 'reference')
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_wm_prob_bin, 'reference')

		## Send Binarized Maps to Reg
		preprocflow.connect(csf_prob_bin, 'out_file',
		                app_xfm_csf_prob_bin, 'in_file')
		preprocflow.connect(gm_prob_bin, 'out_file',
		                app_xfm_gm_prob_bin, 'in_file')
		preprocflow.connect(wm_prob_bin, 'out_file',
		                app_xfm_wm_prob_bin, 'in_file')

		## VMHC Reg
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_vmhc, 'reference')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_vmhc, 'in_matrix_file')

		## ReHo Reg
		preprocflow.connect(func_mean, 'out_file',
		                app_xfm_reho, 'reference')
		preprocflow.connect(linear_reg_anat, 'out_matrix_file',
		                app_xfm_reho, 'in_matrix_file')

		# Sink Preproc Flow
		preprocflow.base_dir=os.path.abspath(op_dir+'/'+sub+'_session_'+str(sesh)+'/')
		preprocflow.run()
		
