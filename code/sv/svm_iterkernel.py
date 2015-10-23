import numpy as np
from sklearn import datasets, svm
from sklearn.svm import SVC, SVR
import time

def svm_iterkernel(train_data, train_labels, test_data, test_labels, op_name_dir):


	label_set=np.unique(train_labels)

	if op_name_dir != ('None' or 'none'):
		fo=open(op_name_dir,'a')

	predict_list={}
	for kernel in ['linear']: #, 'poly', 'rbf']:
		t0=time.time()
		svm = SVC(C=1., kernel=kernel, cache_size=10240)
		svm.fit(train_data, train_labels)
		prediction=svm.predict(test_data)
		predict_list[kernel]=prediction
		pred_acc_tot =(float(np.sum(prediction == test_labels)))/len(test_labels)
		print time.time() - t0, ',kernel = '+kernel, ',pred acc = '+str(round(pred_acc_tot*100))
		if op_name_dir != ('None' or 'none'):
			fo.write('time='+str(time.time() - t0)+'sec,kernel='+kernel+',pred acc='+str(round(pred_acc_tot*100))+'\n')
		for lab_unq in label_set:	
			pred_acc=(prediction == lab_unq) & (test_labels == lab_unq)
			pred_acc=float(pred_acc.sum())/(len(test_labels[test_labels == lab_unq]))
			print 'pred_'+str(lab_unq)+','+str(round(pred_acc*100))	
			if op_name_dir != ('None' or 'none'):
				fo.write('pred_'+str(lab_unq)+','+str(round(pred_acc*100))+'\n')

	if op_name_dir != ('None' or 'none'):
		fo.close()

	return predict_list

def svr_iterkernel(train_data, train_labels, test_data, test_labels, op_name_dir):


	#label_set=np.unique(train_labels)

	if op_name_dir != ('None' or 'none'):
		fo=open(op_name_dir,'a')
	score_list={}
	predict_list={}
	for kernel in ['linear']:#, 'poly', 'rbf']:
		t0=time.time()
		svr = SVR(C=1., kernel=kernel, cache_size=10240)
		svr.fit(train_data, train_labels)
		prediction=svr.predict(test_data)
		predict_list[kernel]=prediction

	return predict_list
