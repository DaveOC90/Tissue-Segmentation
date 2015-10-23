import os
import sys
import re

direc=sys.argv[1]
files=os.listdir(direc)
opname=direc.split('/')[-1]
files=[d for d in files if '.txt' in d]
fo=open(opname+'_svm_res.csv','w')
fo.write('sub,kernel,pred_type,pred_value\n')
for f in files:
    lines=[l.strip() for l in open(direc+'/'+f,'r').readlines()]
    pattern=re.search(r"\d+",f) 
    sub=pattern.group(0)
    for i,l in enumerate(lines):
        if 'pred acc' in l.strip():
            kernel=l.strip().split(',')[-2].replace('kernel=','')
            fo.write(sub+','+kernel+',total,'+l.strip().split(',')[-1].replace('pred acc=','')+'\n')
        else:
            fo.write(sub+','+kernel+','+l.split(',')[0].replace('pred_','')+','+l.split(',')[-1]+'\n')

fo.close()
