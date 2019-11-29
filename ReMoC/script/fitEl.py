"""
Created on Mon Jul  9 11:38:27 2018

@author: lei
"""

import os
from numpy import *
from sys import *

if(len(argv)!=5):
    print("Variate error!")
    exit()
else:
    Kpoint_VBM=int(argv[1])
    VBM=int(argv[2])
    Kpoint_CBM=int(argv[3])
    CBM=int(argv[4])

tmp=[i.rstrip() for i in os.popen("ls").readlines()]
list=[]
latt=[]
for i in tmp:
    if '-' in i:
        num=i[:i.find('-')]
        try:
            num=int(num)
            if num in range(1,100):
                list.append(i)
                tmp=float(i[i.find('-')+1:])
                latt.append(tmp)
                if (tmp-1.0)<1E-5:
                    mid=i
        except:
            pass
mid=list.index(mid)
os.chdir("./%s/2-band"%list[mid])
ISPIN=os.popen("grep ISPIN OUTCAR").readlines()[0].rstrip()
ISPIN=int(ISPIN.split()[2])
tmp=os.popen("grep NBANDS OUTCAR").readlines()[0].rstrip()
Nk=int(tmp.split()[3])
Nb=int(tmp.split()[-1])
os.chdir("../../")

def getE(KNo,BNo,No):
    line=(Nb+2)*(KNo-1)+BNo+8
    Ek=float(os.popen("awk 'NR==%i{print $%i}' EIGENVAL"%(line,No+1)).readlines()[0].rstrip())
    return Ek

Evac=[]
Evbm=[]
Ecbm=[]

for dir in list:
    os.chdir("./%s"%dir)
    tmp=os.popen("grep ' 1s ' 1-CHG/OUTCAR | head -n1").readlines()[0].rstrip()
    Evac=float(tmp.split()[2])
    os.chdir("./2-band")
    if ISPIN==2:
        Evbm.append([getE(Kpoint_VBM,VBM,1)-Evac,getE(Kpoint_VBM,VBM,2)-Evac])
        Ecbm.append([getE(Kpoint_CBM,CBM,1)-Evac,getE(Kpoint_CBM,CBM,2)-Evac])
    else:
        Evbm.append([getE(Kpoint_VBM,VBM,1)-Evac])
        Ecbm.append([getE(Kpoint_CBM,CBM,1)-Evac])
    os.chdir("../../")

latt=[i-1 for i in latt]

def fit_LS(data,Y,rank):
    if len(data) <= rank+1:
        print("Insufficient data")
        return
    X=[]
    tmp=[]
    for i in range(0,len(data)):
        for j in range(0,rank+1):
            tmp.append(data[i]**j)
        X.append(tmp)
        tmp=[]
    X=mat(X)
    Y=mat(Y).T
    C=(X.T*X).I    
    guess=C*X.T*Y
    error=(Y-X*guess).T.tolist()[0]
    stde=sqrt(sum([i**2 for i in error])/(len(data)-rank-1))
    trans=[C[i,i] for i in range(0,rank+1)]
    trans_error=[stde*sqrt(i) for i in trans]
    guess=guess.T.tolist()[0]    
    return [guess,trans_error]

guessvbm=[]
guesscbm=[]
errorvbm=[]
errorcbm=[]
dataline=['' for i in range(0,len(list))]

for i in range(0,ISPIN):
    datavbm=[Evbm[j][i] for j in range(0,len(list))]
    datacbm=[Ecbm[j][i] for j in range(0,len(list))]
    datavbm=[j-datavbm[mid] for j in datavbm]
    datacbm=[j-datacbm[mid] for j in datacbm]
    for k in range(0,len(list)):
        dataline[k] += "%9.6f       %9.6f       %9.6f       "%(latt[k],datavbm[k],datacbm[k])
    gvbm=fit_LS(latt,datavbm,1)
    gcbm=fit_LS(latt,datacbm,1)
    guessvbm.append(abs(gvbm[0][1]))
    guesscbm.append(abs(gcbm[0][1]))
    errorvbm.append(gvbm[1][1])
    errorcbm.append(gcbm[1][1])

line1=["El(eV)             Fit","El(eV)             UP                       DN"]
line1=line1[ISPIN-1]
line2="  VBM"
line3="  CBM"
for i in range(0,ISPIN):
    line2 += "    %9.6f + %9.6f"%(guessvbm[i],errorvbm[i])
    line3 += "    %9.6f + %9.6f"%(guesscbm[i],errorcbm[i])
print(line1+'\n'+line2+'\n'+line3)

fout=open('El','w')
fout.write(line1+'\n'+line2+'\n'+line3)

fileline=["  latt            vbm            cbm","  latt            vbm_up           cbm_up            latt           vbm_dn          cbm_dn"]
fileline=fileline[ISPIN-1]
fileout=open("data_El",'w')
fileout.write(fileline+'\n')
for i in dataline:
    fileout.write(i+'\n')
fileout.close()
