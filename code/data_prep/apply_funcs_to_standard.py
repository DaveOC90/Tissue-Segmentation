# inputs
# - sublist
# - working directory where warps are
# - custom directory with custom funcs

# usage: python apply_funcs_to_standard.py <sublist.txt> <working directory> <directory with custom funcs> <func name>

# I know those os.walks should really be in functions.. I was in a rush, so save your comments

import sys
import os

sublist_filepath = sys.argv[1]
working_dir = sys.argv[2]
custom_dir = sys.argv[3]
func_name = sys.argv[4]


#sublist_file = open(sublist_filepath, 'rb')
sublist = [d.strip() for d in open(sublist_filepath, 'r')]


sub_warps_dict = {}

for root, folders, files in os.walk(working_dir): #working directory

    for filename in files:
        filepath = root + "/" + filename
	#print filepath

        for sub in sublist:
            if sub in filepath:
		
                subid = sub
                
                if subid not in sub_warps_dict.keys():
                    sub_warps_dict[subid] = {}


                if "anat_mni_ants_register" in filepath:
		    
                    if "transform3Warp" in filename:
                        sub_warps_dict[subid]["3Warp"] = filepath

                    if "transform2Affine" in filename:
                        sub_warps_dict[subid]["2Affine"] = filepath

                    if "transform1Rigid" in filename:
                        sub_warps_dict[subid]["1Rigid"] = filepath

                    if "transform0Derived" in filename:
                        sub_warps_dict[subid]["0Initial"] = filepath


                if "func_to_anat_bbreg" in filepath:
                    if ".mat" in filepath:
                        sub_warps_dict[subid]["func_to_anat"] = filepath


                if "anat_brain_only" in filepath:
                    if ".nii.gz" in filepath:
                        sub_warps_dict[subid]["brain_only"] = filepath


                if "func_mean_skullstrip" in filepath:
                    if ".nii.gz" in filepath:
                        sub_warps_dict[subid]["func_mean"] = filepath




func_dict = {}

for root, folders, files in os.walk(custom_dir): #directory with custom func files

    for filename in files:

        filepath = root + "/" + filename

        for sub in sublist:
            sub=str(sub)
            if sub in filepath:
                subid = sub

                if func_name in filepath:
                    func_dict[subid] = filepath

        


def change_itk_transform_type(input_affine_file, subid):

    '''
    this function takes in the affine.txt produced by the c3d_affine_tool
    (which converted an FSL FLIRT affine.mat into the affine.txt)

    it then modifies the 'Transform Type' of this affine.txt so that it is
    compatible with the antsApplyTransforms tool and produces a new affine
    file titled 'updated_affine.txt'
    '''

    import os

    new_file_lines = []

    with open(input_affine_file) as f:

        for line in f:

            if 'Transform:' in line:

                if 'MatrixOffsetTransformBase_double_3_3' in line:

                    transform_line = 'Transform: AffineTransform_double_3_3'
                    new_file_lines.append(transform_line)

            else:

                new_file_lines.append(line)


    updated_affine_file = os.path.join(os.getcwd(), '%s_updated_affine.txt' % subid)

    outfile = open(updated_affine_file, 'wt')

    for line in new_file_lines:

        print >>outfile, line.strip('\n')

    outfile.close()


    return updated_affine_file




def func_to_standard_apply_warp(sub_files, func_dict, subid):

    import os

    anat_brain = sub_files[subid]["brain_only"]
    mean_func = sub_files[subid]["func_mean"]
    func_to_anat = sub_files[subid]["func_to_anat"]
    nonlinear = sub_files[subid]["3Warp"]
    affine = sub_files[subid]["2Affine"]
    rigid = sub_files[subid]["1Rigid"]
    initial = sub_files[subid]["0Initial"]

    input_func = func_dict[subid]

    current_dir = os.getcwd()

    os.system("c3d_affine_tool -ref %s -src %s %s -fsl2ras -oitk %s/%s_converted_mat.txt" % (anat_brain, mean_func, func_to_anat, current_dir, subid))

    c3d_output = current_dir + "/" + subid + "_converted_mat.txt"

    updated_affine = change_itk_transform_type(c3d_output, subid)
    if not os.path.exists(subid+'_func_antswarp.nii.gz'):
    	os.system("antsApplyTransforms --default-value 0 --dimensionality 3 --input %s --input-image-type 3 --interpolation Linear --output %s_func_antswarp.nii.gz --reference-image /usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz --transform %s --transform %s --transform %s --transform %s --transform %s" % (input_func, subid, nonlinear, affine, rigid, initial, updated_affine))




for subid in sublist:

    try:
	print sub_warps_dict, func_dict, subid
        func_to_standard_apply_warp(sub_warps_dict, func_dict, subid)

    except:

        print "Something went horrifically wrong with subject %s" % subid
        pass
