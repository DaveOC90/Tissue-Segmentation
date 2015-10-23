import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from assign_ts import assign_ts
import nibabel as nb
from img_four import img_ts_to_four
import time
import sys

rest_1 = sys.argv[1]
rest_2 = sys.argv[2]
mask_1 = sys.argv[3]
mask_2 = sys.argv[4]

## Generate 4D Freq Component Arrays
data_import_1=img_ts_to_four(rest_1, 'none')
data_import_2=img_ts_to_four(rest_2, 'none')

data_import_1=(data_import_1 - np.mean(data_import_1))/np.std(data_import_1)
data_import_2=(data_import_2 - np.mean(data_import_2))/np.std(data_import_2)

## Make 2D freq Component Arrays
data_1, data_coords_1=assign_ts(data_import_1)
data_2, data_coords_2=assign_ts(data_import_2)

## Load 3D Label Array
target_import_1=nb.Nifti1Image.load(mask_1)
target_import_2=nb.Nifti1Image.load(mask_2)

## Make 1D Label Array
target_1, target_coords_1=assign_ts(target_import_1.get_data())
target_2, target_coords_2=assign_ts(target_import_2.get_data())

sesh_1=np.zeros(len(data_1))
sesh_2=np.zeros(len(data_2))

sesh_1[sesh_1 == 0] = 1
sesh_2[sesh_2 == 0] = 2

zeros_1 = target_1 == 0
zeros_2 = target_2 == 0

data_1 = data_1[zeros_1 == False, :]
target_1 = target_1[zeros_1 == False]

data_2 = data_2[zeros_2 == False, :]
target_2 = target_2[zeros_2 == False]



n_sample_1 = len(data_1)
np.random.seed(0)
order_1 = np.random.permutation(n_sample_1)

data_1 = data_1[order_1]
target_1 = target_1[order_1].astype(np.float)
sesh_1=sesh_1[order_1]


n_sample_2 = len(data_2)
np.random.seed(0)
order_2 = np.random.permutation(n_sample_2)

data_2 = data_2[order_2]
target_2 = target_2[order_2].astype(np.float)
sesh_2=sesh_2[order_2]

subset_1=round(n_sample_1*(0.05))
subset_2=round(n_sample_2*(0.05))

data_1 = data_1[0:subset_1]
target_1 = target_1[0:subset_1]
sesh_1=sesh_1[0:subset_1]

data_2 = data_2[0:subset_2]
target_2 = target_2[0:subset_2]
sesh_2=sesh_2[0:subset_2]




data=np.concatenate([data_1,data_2], axis=0)
target=np.concatenate([target_1,target_2], axis=0)
sesh_data=np.concatenate([sesh_1,sesh_2], axis=0)

#zeros = target == 0

#data = data[zeros == False, :]
#sesh_data=sesh_data[zeros == False]
#target = target[zeros == False]


categories=[1,2,3]

#n_sample = len(data)

#np.random.seed(0)
#order = np.random.permutation(n_sample)
#data = data[order]
#target = target[order].astype(np.float)
### Classifiers definition

# A support vector classifier
from sklearn.svm import SVC
svm_lin = SVC(C=1., kernel="linear", cache_size=10240)
svm_poly = SVC(C=1., kernel="poly", cache_size=10240)
svm_rbf = SVC(C=1., kernel="rbf", cache_size=10240)


from sklearn.grid_search import GridSearchCV
# GridSearchCV is slow, but note that it takes an 'n_jobs' parameter that
# can significantly speed up the fitting process on computers with
# multiple cores
svm_cv_lin = GridSearchCV(SVC(C=1., kernel="linear", cache_size=10240),
                      #param_grid={'C': [.1, .5, 1., 5., 10., 50., 100.]},
		      param_grid={'C': [.1, .5, 1.]},
                      scoring='f1')
svm_cv_poly = GridSearchCV(SVC(C=1., kernel="poly", cache_size=10240),
                      param_grid={'C': [.1, .5, 1.]},
                      scoring='f1')
svm_cv_rbf = GridSearchCV(SVC(C=1., kernel="rbf", cache_size=10240),
                      param_grid={'C': [.1, .5, 1.]},
                      scoring='f1')

# The logistic regression
#from sklearn.linear_model import LogisticRegression, RidgeClassifier, \
#    RidgeClassifierCV
#logistic = LogisticRegression(C=1., penalty="l1")
#logistic_50 = LogisticRegression(C=50., penalty="l1")
#logistic_l2 = LogisticRegression(C=1., penalty="l2")

#logistic_cv = GridSearchCV(LogisticRegression(C=1., penalty="l1"),
#                           param_grid={'C': [.1, .5, 1., 5., 10., 50., 100.]},
#                           scoring='f1')
#logistic_l2_cv = GridSearchCV(LogisticRegression(C=1., penalty="l1"),
#                              param_grid={'C': [.1, .5, 1., 5., 10., 50., 100.]},
#                              scoring='f1')

#ridge = RidgeClassifier()
#ridge_cv = RidgeClassifierCV()


# Make a data splitting object for cross validation
from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score
cv = LeaveOneLabelOut(sesh_data)

classifiers = {'SVC Lin': svm_lin,
               'SVC Poly': svm_poly,
               'SVC RBF': svm_rbf,
               'SVC Lin CV': svm_cv_lin,
               'SVC Poly CV': svm_cv_poly,
               'SVC RBF CV': svm_cv_rbf}
#               'log l1': logistic,
#               'log l1 50': logistic_50,
#               'log l1 cv': logistic_cv,
#               'log l2': logistic_l2,
#               'log l2 cv': logistic_l2_cv,
#               'ridge': ridge,
#               'ridge cv': ridge_cv}

classifiers_scores = {}

for classifier_name, classifier in sorted(classifiers.items()):
    classifiers_scores[classifier_name] = {}
    print 70 * '_'

    for category in categories:
        classification_target = target == category
        t0 = time.time()
        classifiers_scores[classifier_name][category] = cross_val_score(
            classifier,
            data,
            classification_target,
            cv=10, scoring="f1")

        print "%10s: %14s -- scores: %1.2f +- %1.2f, time %.2fs" % (
            classifier_name, category,
            classifiers_scores[classifier_name][category].mean(),
            classifiers_scores[classifier_name][category].std(),
            time.time() - t0)
	fo1=open('/data2/tissue_seg/group_results.txt', 'a')
	fo1.write("%10s: %14s -- scores: %1.2f +- %1.2f, time %.2fs\n" % (
            classifier_name, category,
            classifiers_scores[classifier_name][category].mean(),
            classifiers_scores[classifier_name][category].std(),
            time.time() - t0))
	fo1.close()
	fo2=open('/data2/tissue_seg/'+rest_1.split('/')[-2]+'svmres.txt', 'a')
	fo2.write(str(classifier_name)+','+str(category)+','+str(classifiers_scores[classifier_name][category].mean())+','+str(classifiers_scores[classifier_name][category].std())+'\n')
	fo2.close()
