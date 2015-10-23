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

ip_dir='/data2/jhu_atlas_tse/organized_data/hnu_1/'
op_dir='/data2/tissue_seg/working/'
sublist='/data2/tissue_seg/sublist_tseg.txt'

subs=[d.strip() for d in open(sublist, 'r')]

for sub in subs:
	for sesh in range(1,3):

		if not os.path.exists(op_dir+'/'+sub+'session_'+str(sesh)+'/'):
			os.makedirs(op_dir+'/'+sub+'session_'+str(sesh)+'/')
		
		wf_name='tseg_anat_preproc'
		
		
		preprocflow=pe.Workflow(name=wf_name)
		
		
		# Deoblique MPRAGE
		anat_deoblique = pe.Node(interface=afni.preprocess.Refit(),
		                         name='anat_deoblique')
		anat_deoblique.inputs.in_file = ip_dir+'/'+sub+'/session_'+str(sesh)+'/anat_1/anat.nii.gz'
		anat_deoblique.inputs.deoblique = True

		# Reorient MPRAGE to RPI
		anat_reorient = pe.Node(interface=afni.preprocess.Resample(),
		                            name='anat_reorient')

		anat_reorient.inputs.orientation = 'RPI'
		anat_reorient.inputs.outputtype = 'NIFTI_GZ'

		
		# Skullstrip  MPRAGE
		anat_skullstrip = pe.Node(interface=afni.preprocess.SkullStrip(),
		                                  name='anat_skullstrip')
		anat_skullstrip.inputs.args = '-o_ply'
		anat_skullstrip.inputs.outputtype = 'NIFTI_GZ'
		
		
		# Mask MPRAGE
		anat_brain_only = pe.Node(interface=afni.preprocess.Calc(),
		                        name='anat_brain_only')
		anat_brain_only.inputs.expr = 'a*step(b)'
		anat_brain_only.inputs.outputtype = 'NIFTI_GZ'
		
		
		# Calculate ANTs Warp
		calculate_ants_warp = pe.Node(interface=ants.Registration(),
		            name='calculate_ants_warp')
		

		calculate_ants_warp.inputs. \
			fixed_image = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
		calculate_ants_warp.inputs. \
			dimension = 3
		calculate_ants_warp.inputs. \
		    use_histogram_matching=[ True, True, True ]
		calculate_ants_warp.inputs. \
		    winsorize_lower_quantile = 0.01
		calculate_ants_warp.inputs. \
		    winsorize_upper_quantile = 0.99
		calculate_ants_warp.inputs. \
		    metric = ['MI','MI','CC']
		calculate_ants_warp.inputs. \
			metric_weight = [1,1,1]
		calculate_ants_warp.inputs. \
		    radius_or_number_of_bins = [32,32,4]
		calculate_ants_warp.inputs. \
		    sampling_strategy = ['Regular','Regular',None]
		calculate_ants_warp.inputs. \
		    sampling_percentage = [0.25,0.25,None]
		calculate_ants_warp.inputs. \
		    number_of_iterations = [[1000,500,250,100], \
		    [1000,500,250,100], [100,100,70,20]]
		calculate_ants_warp.inputs. \
		    convergence_threshold = [1e-8,1e-8,1e-9]
		calculate_ants_warp.inputs. \
		    convergence_window_size = [10,10,15]
		calculate_ants_warp.inputs. \
		    transforms = ['Rigid','Affine','SyN']
		calculate_ants_warp.inputs. \
		    transform_parameters = [[0.1],[0.1],[0.1,3,0]]
		calculate_ants_warp.inputs. \
		    shrink_factors = [[8,4,2,1],[8,4,2,1],[6,4,2,1]]
		calculate_ants_warp.inputs. \
		    smoothing_sigmas = [[3,2,1,0],[3,2,1,0],[3,2,1,0]]
		calculate_ants_warp.inputs. \
		    sigma_units = ['vox','vox','vox']
		calculate_ants_warp.inputs. \
			output_warped_image = True
		calculate_ants_warp.inputs. \
			output_inverse_warped_image = True
		calculate_ants_warp.inputs. \
			output_transform_prefix = 'xfm'
		calculate_ants_warp.inputs. \
			write_composite_transform = True
		calculate_ants_warp.inputs. \
			collapse_output_transforms = False
		

		
		# FAST Node
		segment=pe.Node(interface = fsl.FAST(), name='segment')
		segment.inputs.img_type = 1
		segment.inputs.segments = True
		segment.inputs.probability_maps = True
		segment.inputs.out_basename = 'segment'
		

		## Deoblique Func
		func_deoblique = pe.Node(interface=afni.preprocess.Refit(),
		                            name='func_deoblique')
		func_deoblique.inputs.deoblique = True
		func_deoblique.inputs.in_file = ip_dir+'/'+sub+'/session_'+str(sesh)+'/rest_1/rest.nii.gz'
		    
		
		## Reorient Func
		func_reorient = pe.Node(interface=afni.preprocess.Resample(),
		                               name='func_reorient')
		func_reorient.inputs.orientation = 'RPI'
		func_reorient.inputs.outputtype = 'NIFTI_GZ'
		
		
		## Mean Func    
		func_get_mean_RPI = pe.Node(interface=afni.preprocess.TStat(),
		                            name='func_get_mean_RPI')
		func_get_mean_RPI.inputs.options = '-mean'
		func_get_mean_RPI.inputs.outputtype = 'NIFTI_GZ'
		    
		
		        
		## Calculate motion parameters
		func_motion_correct = pe.Node(interface=afni.preprocess.Volreg(),
		                             name='func_motion_correct')
		func_motion_correct.inputs.args = '-Fourier -twopass'
		func_motion_correct.inputs.zpad = 4
		func_motion_correct.inputs.outputtype = 'NIFTI_GZ'
		
		    
		
		## Mean Motion
		func_get_mean_motion = func_get_mean_RPI.clone('func_get_mean_motion')
		
		    
		
		## 1D Motion File
		func_motion_correct_A = func_motion_correct.clone('func_motion_correct_A')
		func_motion_correct_A.inputs.md1d_file = 'max_displacement.1D'
		    
		
		
		## Despike
		func_despike = pe.Node(interface=afni.preprocess.Despike(),
		                             name='func_despike')
		func_despike.inputs.outputtype = 'NIFTI_GZ'
		
		
		## Linear and Quadratic Detrending
		func_detrend_lin_quad = pe.Node(interface=afni.preprocess.Detrend(),
		                             name='func_detrend_lin_quad')
		func_detrend_lin_quad.inputs.args = '-normalize -polort 2'
		func_detrend_lin_quad.inputs.outputtype = 'NIFTI_GZ'
		
		
		## Get Brain Mask
		func_get_brain_mask = pe.Node(interface=fsl.BET(),
		                                      name='func_get_brain_mask_BET')
		func_get_brain_mask.inputs.mask = True
		func_get_brain_mask.inputs.functional = True
		
		
		## Erode Mask
		erode_one_voxel = pe.Node(interface=fsl.ErodeImage(),
		                                 name='erode_one_voxel')
		
		erode_one_voxel.inputs.kernel_shape = 'box'
		erode_one_voxel.inputs.kernel_size = 1.0
		
		        
		## Get Edge    
		func_edge_detect = pe.Node(interface=afni.preprocess.Calc(),
		                            name='func_edge_detect')
		func_edge_detect.inputs.expr = 'a*b'
		func_edge_detect.inputs.outputtype = 'NIFTI_GZ'
		
		
		## Skullstrip    
		func_mean_skullstrip = pe.Node(interface=afni.preprocess.TStat(),
		                           name='func_mean_skullstrip')
		func_mean_skullstrip.inputs.options = '-mean'
		func_mean_skullstrip.inputs.outputtype = 'NIFTI_GZ'
		
		## Func to Anat
		linear_reg_func = pe.Node(interface=fsl.FLIRT(),
		                         name='linear_reg_func')
		linear_reg_func.inputs.cost = 'corratio'
		linear_reg_func.inputs.dof = 6
		linear_reg_func.inputs.interp = 'nearestneighbour'
		
		## Apply XFM
		app_xfm_lin = pe.Node(interface=fsl.ApplyXfm(),
		                         name='app_xfm_lin')
		app_xfm_lin.inputs.apply_xfm = True
		
		    
		## Func to MNI
		func_t1_to_mni = pe.Node(interface=ants.ApplyTransforms(), name='func_t1_to_mni')
		func_t1_to_mni.inputs.dimension = 4
		func_t1_to_mni.inputs.reference_image='/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
		func_t1_to_mni.inputs.invert_transform_flags = [False]
		func_t1_to_mni.inputs.interpolation = 'NearestNeighbor'
		

		
		#### ANAT
		preprocflow.connect(anat_deoblique, 'out_file',
		                    anat_reorient, 'in_file')
		preprocflow.connect(anat_reorient, 'out_file',
		                        anat_skullstrip, 'in_file')
		preprocflow.connect(anat_skullstrip, 'out_file',
		                        anat_brain_only, 'in_file_b')
		preprocflow.connect(anat_reorient, 'out_file',
		                        anat_brain_only, 'in_file_a')                               
		
		preprocflow.connect(anat_brain_only, 'out_file',
		                    calculate_ants_warp, 'moving_image')
		
		preprocflow.connect(calculate_ants_warp, 'warped_image',
		                    segment, 'in_files')
		
		#### FUNC
		preprocflow.connect(func_deoblique, 'out_file',
		                func_reorient, 'in_file')
		
		preprocflow.connect(func_reorient, 'out_file',
		                func_get_mean_RPI, 'in_file')
		
		preprocflow.connect(func_reorient, 'out_file',
		                func_motion_correct, 'in_file')
		preprocflow.connect(func_get_mean_RPI, 'out_file',
		                func_motion_correct, 'basefile')
		                    
		preprocflow.connect(func_motion_correct, 'out_file',
		                func_get_mean_motion, 'in_file')
		
		
		preprocflow.connect(func_reorient, 'out_file',
		                func_motion_correct_A, 'in_file')
		preprocflow.connect(func_get_mean_motion, 'out_file',
		                func_motion_correct_A, 'basefile')
		
		preprocflow.connect(func_motion_correct_A, 'out_file',
		                 func_despike, 'in_file')
		
		preprocflow.connect(func_despike, 'out_file',
		                 func_detrend_lin_quad, 'in_file')
		
		
		preprocflow.connect(func_detrend_lin_quad, 'out_file',
		                 func_get_brain_mask, 'in_file')
		
		preprocflow.connect(func_get_brain_mask, 'mask_file',
		                 erode_one_voxel, 'in_file')
		
		
		preprocflow.connect(func_motion_correct_A, 'out_file',
		                func_edge_detect, 'in_file_a')
		preprocflow.connect(erode_one_voxel, 'out_file',
		                func_edge_detect, 'in_file_b')
		
		
		preprocflow.connect(func_edge_detect, 'out_file',
		                linear_reg_func, 'in_file')
		preprocflow.connect(anat_brain_only, 'out_file',
		                linear_reg_func, 'reference')
		
		preprocflow.connect(func_edge_detect, 'out_file',
							app_xfm_lin, 'in_file')
		preprocflow.connect(anat_brain_only, 'out_file',
							app_xfm_lin, 'reference')
		preprocflow.connect(linear_reg_func, 'out_matrix_file',
							app_xfm_lin, 'in_matrix_file')
		
		
		
		preprocflow.connect(calculate_ants_warp, 'composite_transform',
		                    func_t1_to_mni, 'transforms')
		preprocflow.connect(app_xfm_lin, 'out_file',
		                    func_t1_to_mni, 'input_image')
		              
		
		preprocflow.base_dir=os.path.abspath(op_dir+'/'+sub+'session_'+str(sesh)+'/')
		preprocflow.run()
		
