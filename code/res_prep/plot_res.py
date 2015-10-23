import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def plot_barchart(ipcsv):

	data=pd.read_csv(ipcsv)
	unq=np.unique(data.kernel)
	index=np.arange(len(unq))
	
	plt.close()
	fig,ax =plt.subplots()
	bar_width=0.1
	error_config = {'ecolor': '0.3'}
	
	rects1 = plt.bar(index, [data.csf[data.kernel == 'linear'].mean(), data.csf[data.kernel == 'poly'].mean(), data.csf[data.kernel == 'rbf'].mean()],bar_width, yerr=[data.csf[data.kernel == 'linear'].std(), data.csf[data.kernel == 'poly'].std(), data.csf[data.kernel == 'rbf'].std()], error_kw=error_config, color='b', label='CSF')
	#rects2 = plt.bar(index+bar_width, [data.gm[data.kernel == 'linear'].mean(), data.gm[data.kernel == 'poly'].mean(), data.gm[data.kernel == 'rbf'].mean()], bar_width, yerr=[data.gm[data.kernel == 'linear'].std(), data.gm[data.kernel == 'poly'].std(), data.gm[data.kernel == 'rbf'].std()],error_kw=error_config, color='r', label='GM')
	#rects3 = plt.bar(index+(2*bar_width), [data.wm[data.kernel == 'linear'].mean(), data.wm[data.kernel == 'poly'].mean(), data.wm[data.kernel == 'rbf'].mean()], bar_width,yerr=[data.wm[data.kernel == 'linear'].std(), data.wm[data.kernel == 'poly'].std(), data.wm[data.kernel == 'rbf'].std()],error_kw=error_config, color='g', label='WM')

	#plt.xticks(index, ('Linear', 'Polynomial', 'RBF'))
	plt.xticks(index, ('Linear'))
	plt.legend()
	plt.show()
