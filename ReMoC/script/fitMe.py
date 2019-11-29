import os
from numpy import *
from sys import *

if(len(argv)!=5):
    print("Variate error!")
    exit()
else:
    Kpt_VBM=argv[1]
    VBM=int(argv[2])
    Kpt_CBM=argv[3]
    CBM=int(argv[4])

tmp=[i.rstrip() for i in os.popen("ls").readlines()]
list=[]
for i in tmp:
    if '-' in i:
        num=i[:i.find('-')]
        try:
            num=int(num)
            if num in range(1,100):
                list.append(i)
                tmp=float(i[i.find('-')+1:])
                if (tmp-1.0)<1E-5:
                    mid=i
        except:
            pass
mid=list.index(mid)
os.chdir("./%s/3-Me"%list[mid])

ISPIN=os.popen("grep ISPIN OUTCAR").readlines()[0].rstrip()
ISPIN=int(ISPIN.split()[2])
tmp=os.popen("grep NBANDS OUTCAR").readlines()[0].rstrip()
Nk=int(tmp.split()[3])
Nb=int(tmp.split()[-1])

if '-' not in Kpt_VBM:
    Kstart_VBM=1
    Kend_VBM=Nk
else:
    Kstart_VBM=int(Kpt_VBM[:Kpt_VBM.index('-')])
    Kend_VBM=int(Kpt_VBM[Kpt_VBM.index('-')+1:])

if '-' not in Kpt_CBM:
    Kstart_CBM=1
    Kend_CBM=Nk
else:
    Kstart_CBM=int(Kpt_CBM[:Kpt_CBM.index('-')])
    Kend_CBM=int(Kpt_CBM[Kpt_CBM.index('-')+1:])

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

def getE(KNo,BNo,No):
    line=(Nb+2)*(KNo-1)+BNo+8
    Ek=float(os.popen("awk 'NR==%i{print $%i}' EIGENVAL"%(line,No+1)).readlines()[0].rstrip())
    return Ek

latt=[]
for i in range(3,6):
    latt_a=float(os.popen("awk 'NR==%i{print $1}' CONTCAR"%i).readlines()[0].rstrip())
    latt_b=float(os.popen("awk 'NR==%i{print $2}' CONTCAR"%i).readlines()[0].rstrip())
    latt_c=float(os.popen("awk 'NR==%i{print $3}' CONTCAR"%i).readlines()[0].rstrip())
    latt.append(mat([latt_a,latt_b,latt_c]))
Volumn=cross(latt[0],latt[1])*latt[2].T
Rlatt_a=(2*pi*cross(latt[1],latt[2])/Volumn).tolist()[0]
Rlatt_b=(2*pi*cross(latt[2],latt[0])/Volumn).tolist()[0]
Rlatt_c=(2*pi*cross(latt[0],latt[1])/Volumn).tolist()[0]
Rlatt=mat([Rlatt_a,Rlatt_b,Rlatt_c])

def getk(KNo):
    line=(Nb+2)*(KNo-1)+8
    Kpos=os.popen("awk 'NR==%i{print $0}' EIGENVAL"%line).readlines()[0].rstrip().split()
    Kpos=[float(i) for i in Kpos[0:3]]
    Kdis=(mat(Kpos)*Rlatt).tolist()[0]
    return Kdis

Evbm=[]
Ecbm=[]
DisK=[]

for i in range(1,Nk+1):
    DisK.append(getk(i))
    if ISPIN==2:
        Evbm.append([getE(i,VBM,1),getE(i,VBM,2)])
        Ecbm.append([getE(i,CBM,1),getE(i,CBM,2)])
    else:
        Evbm.append([getE(i,VBM,1)])
        Ecbm.append([getE(i,CBM,1)])

guessvbm=[]
guesscbm=[]
errorvbm=[]
errorcbm=[]

Klist_VBM=DisK[Kstart_VBM-1:Kend_VBM]
Klist_VBM=[[i[j]-Klist_VBM[0][j] for j in range(0,3)]for i in Klist_VBM]
dataK_VBM=[sqrt(sum([j**2 for j in i])) for i in Klist_VBM]
Klist_CBM=DisK[Kstart_CBM-1:Kend_CBM]
Klist_CBM=[[i[j]-Klist_CBM[0][j] for j in range(0,3)]for i in Klist_CBM]
dataK_CBM=[sqrt(sum([j**2 for j in i])) for i in Klist_CBM]
if (Kend_VBM-Kstart_VBM)>(Kend_CBM-Kstart_CBM):
    lnmin=Kend_CBM-Kstart_CBM+1
    lnmax=Kend_VBM-Kstart_VBM+1
    lean='CBM'
elif (Kend_VBM-Kstart_VBM)<(Kend_CBM-Kstart_CBM):
    lnmin=Kend_VBM-Kstart_VBM+1
    lnmax=Kend_CBM-Kstart_CBM+1
    lean='VBM'
else:
    lnmin=Kend_CBM-Kstart_CBM+1
    lnmax=Kend_VBM-Kstart_VBM+1
    lean=None
dataline=['' for j in range(0,lnmax)]
for i in range(0,ISPIN):
    datavbm=[Evbm[j][i] for j in range(Kstart_VBM-1,Kend_VBM)]
    datacbm=[Ecbm[j][i] for j in range(Kstart_CBM-1,Kend_CBM)]
    for k in range(0,lnmin):
        dataline[k] += "%9.6f       %9.6f       %9.6f       %9.6f       "%(dataK_VBM[k],datavbm[k],dataK_CBM[k],datacbm[k])
    if lean=='VBM':
        for l in range(lnmin,lnmax):
            dataline[l] += "                                %9.6f       %9.6f       "%(dataK_CBM[l],datacbm[l])
    elif lean=='CBM':
        for l in range(lnmin,lnmax):
            dataline[l] += "%9.6f       %9.6f                                       "%(dataK_VBM[l],datavbm[l])
    gvbm=fit_LS(dataK_VBM,datavbm,2)
    gcbm=fit_LS(dataK_CBM,datacbm,2)
    guessvbm.append(gvbm[0][2])
    guesscbm.append(gcbm[0][2])
    errorvbm.append(gvbm[1][2])
    errorcbm.append(gcbm[1][2])

Me_vbm=[abs(3.81/i) for i in guessvbm]
Me_cbm=[abs(3.81/i) for i in guesscbm]

os.chdir("../../")

line1=["Me(m0)        Fit","Me(m0)        UP           DN"]
line1=line1[ISPIN-1]
line2="  VBM"
line3="  CBM"
for i in range(0,ISPIN):
    line2 += "    %9.6f"%Me_vbm[i]
    line3 += "    %9.6f"%Me_cbm[i]
print(line1+'\n'+line2+'\n'+line3)

fout=open('Me','w')
fout.write(line1+'\n'+line2+'\n'+line3)
fout.close()

fileline=["   dis            vbm           dis          cbm","   dis            vbm_up            dis           cbm_up            dis           vbm_dn            dis           cbm_dn"]
fileline=fileline[ISPIN-1]
fileout=open("data_Me",'w')
fileout.write(fileline+'\n')
for i in dataline:
    fileout.write(i+'\n')
fileline=["para             Fit","para              UP                      DN"]
fileline=fileline[ISPIN-1]
fileout.write('\n'+fileline+'\n')
if ISPIN==1:
    fileout.write("VBM      %9.6f+%9.6f\n"%(guessvbm[0],errorvbm[0]))
    fileout.write("CBM      %9.6f+%9.6f\n"%(guesscbm[0],errorcbm[0]))
else:
    fileout.write("VBM      %9.6f+%9.6f      %9.6f+%9.6f\n"%(guessvbm[0],errorvbm[0],guessvbm[1],errorvbm[1]))
    fileout.write("CBM      %9.6f+%9.6f      %9.6f+%9.6f\n"%(guesscbm[0],errorcbm[0],guesscbm[1],errorcbm[1]))
fileout.close()
