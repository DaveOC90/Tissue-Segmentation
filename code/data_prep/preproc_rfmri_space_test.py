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
op_dir='/data2/tissue_seg/working/'
sublist='/data2/tissue_seg/sublist_tseg_swu_onesub.txt'

subs=[d.strip() for d in open(sublist, 'r')]

for sub in subs:
	for sesh in range(1,3):

		wf_name='tseg_test'		
		preprocflow=pe.Workflow(name=wf_name)

		#if not os.path.exists(op_dir+'/'+sub+'session_'+str(sesh)+'/'):
		#	os.makedirs(op_dir+'/'+sub+'session_'+str(sesh)+'/')
		
		pve=[]
		prob=[]
		prob_bin=[]
		datasink=[]
		for i in range(0,3):
			#pve.append('/data2/tissue_seg/pve_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_'+str(i)+'.nii.gz')
			#prob.append('/data2/tissue_seg/prob_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_'+str(i)+'.nii.gz')

			#prob_name='prob_bin_'+str(i)
			## Mask
			prob_bin.append(pe.Node(interface=afni.preprocess.Calc(),name='BinProbMask_'+str(i)))
			prob_bin[i].inputs.in_file_a = '/data2/tissue_seg/prob_map_softlinks/'+sub+'_session_'+str(sesh)+'/segment_prob_'+str(i)+'.nii.gz'
			prob_bin[i].inputs.expr = 'ispositive(a-0.96)'
			prob_bin[i].inputs.outputtype = 'NIFTI_GZ'

			datasink.append(pe.Node(nio.DataSink(), name='sinker_'+str(i)))
			datasink[i].inputs.base_directory = op_dir+'/'+sub+'_session_'+str(sesh)+'/prob_bin_'+str(i)

			preprocflow.connect(prob_bin[i], 'out_file', datasink[i], 'output.@prob_bin_'+str(i))

		## Mask
		#prob_bin_0 = pe.Node(interface=afni.preprocess.Calc(),
		#                             name='prob_bin_0')
		#prob_bin_0.inputs.in_file_a = prob[0]
		#prob_bin_0.inputs.expr = 'ispositive(a-0.96)'
		#prob_bin_0.inputs.outputtype = 'NIFTI_GZ'
					
	
		

		preprocflow.base_dir=os.path.abspath(op_dir+'/'+sub+'_session_'+str(sesh)+'/')
		preprocflow.run()
