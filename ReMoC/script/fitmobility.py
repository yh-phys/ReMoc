import os
from sys import *
from numpy import *

try:
    fin=open('MCAR','r')
except:
    print("No Input File!")
    exit()

input=fin.readlines()
fin.close()

def findin(key):
    for i in input:
        if key in i:
            try:
                para=i[i.index('=')+1:]
                return para.split()[0]
            except:
                pass
        else:
            pass

if findin("DIR"):
    dir=findin("DIR")
else:
    dir='c'

if findin("KVBM"):
    Kpt_VBM=findin("KVBM")
else:
    Kpt_VBM='0'

if findin("KCBM"):
    Kpt_CBM=findin("KCBM")
else:
    Kpt_CBM='0'

if findin("TEM"):
    T=float(findin("TEM"))
else:
    T=300

if findin("NL"):
    n=int(findin("NL"))
else:
    n=1

VBM_Me=findin("VM")
CBM_Me=findin("CM")
KEl_VBM=findin("KEV")
KEl_CBM=findin("KEC")
VBM_El=findin("VE")
CBM_El=findin("CE")
e=1.602177E-19
h=1.054573E-34
kb=1.380658E-23
m0=9.109390E-31
if None in (VBM_Me,CBM_Me,KEl_VBM,KEl_CBM,VBM_El,CBM_El):
    print("Check your input")
    exit()

try:
    os.system("fitYoungs %s"%dir)
    Ysin=open("C2d",'r')
    print('')
except:
    print("Fit Youngs error!!")
    exit()

try:
    os.system("fitWeff %s"%dir)
    Weffin=open("Weff",'r')
    print('')
except:
    print("Fit Weff error!!")
    exit()

try:
    os.system("fitMe %s %s %s %s"%(Kpt_VBM,VBM_Me,Kpt_CBM,CBM_Me))
    Mein=open("Me",'r')
    print('')
except:
    print("Fit Me error!!")
    exit()

try:
    os.system("fitEl %s %s %s %s"%(KEl_VBM,VBM_El,KEl_CBM,CBM_El))
    Elin=open("El",'r')
    print('')
except:
    print("Fit El error!!")
    exit()

C2d=float(Ysin.readlines()[1].split()[2])
Weff=float(Weffin.readline().split()[2])*1E-10
tmp=Mein.readline().split()
ISPIN=len(tmp)-1
vbmline=Mein.readline().split()
cbmline=Mein.readline().split()
Me_vbm=[]
Me_cbm=[]
for i in range(0,ISPIN):
    Me_vbm.append(float(vbmline[i+1])*m0)
    Me_cbm.append(float(cbmline[i+1])*m0)
tmp=Elin.readline()
vbmline=Elin.readline().split()
cbmline=Elin.readline().split()
El_vbm=[]
err_vbm=[]
El_cbm=[]
err_cbm=[]
for i in range(0,ISPIN):
    El_vbm.append(float(vbmline[i*3+1])*e)
    err_vbm.append(float(vbmline[i*3+3])*e)
    El_cbm.append(float(cbmline[i*3+1])*e)
    err_cbm.append(float(cbmline[i*3+3])*e)

def omega(n,m):
    return (n*pi*h)/sqrt(2*m*Weff**2*kb*T)

def F(n,m):
    if n==1:
        up=omega(1,m)
        dn=1+omega(1,m)**2
    else:
        up=sum([omega(i,m)*exp(-omega(i,m)**2) for i in range(1,n+1)])
        dn=sum([(1+omega(i,m)**2)*exp(-omega(i,m)**2) for i in range(1,n+1)])
    return up/dn

def miu(n,m,El):
    up=pi*e*(h**4)*C2d/Weff
    dn=sqrt(2)*(kb*T)**(1.5)*m**(2.5)*El**2
    return up/dn*F(n,m)*10000

Mob_vbm=[]
Mob_cbm=[]

for i in range(0,ISPIN):
    vbm_tmp=[miu(n,Me_vbm[i],(El_vbm[i]+err_vbm[i])),miu(n,Me_vbm[i],El_vbm[i]),miu(n,Me_vbm[i],(El_vbm[i]-err_vbm[i]))]
    cbm_tmp=[miu(n,Me_cbm[i],(El_cbm[i]+err_cbm[i])),miu(n,Me_cbm[i],El_cbm[i]),miu(n,Me_cbm[i],(El_cbm[i]-err_cbm[i]))]
    Mob_vbm.append(vbm_tmp)
    Mob_cbm.append(cbm_tmp)

if ISPIN==1:
    print("omega")
    print("VBM    %9.6f"%omega(n,Me_vbm[0]))
    print("CBM    %9.6f"%omega(n,Me_cbm[0]))
else:
    print("omega      up             dn")
    print("VBM    %9.6f     %9.6f"%(omega(n,Me_vbm[0]),omega(n,Me_vbm[1])))
    print("CBM    %9.6f     %9.6f"%(omega(n,Me_cbm[0]),omega(n,Me_cbm[1])))
print('')
if ISPIN==1:
    print("F")
    print("VBM    %9.6f"%F(n,Me_vbm[0]))
    print("CBM    %9.6f"%F(n,Me_cbm[0]))
else:
    print("F          up             dn")
    print("VBM    %9.6f     %9.6f"%(F(n,Me_vbm[0]),F(n,Me_vbm[1])))
    print("CBM    %9.6f     %9.6f"%(F(n,Me_cbm[0]),F(n,Me_cbm[1])))

line="_____________Mobility(cm2/V*s)______________"
print('\n'+line)
print("             MID            MIN           MAX")
if ISPIN==1:
    print(" VBM    %9.6f     %9.6f      %9.6f"%(Mob_vbm[0][1],Mob_vbm[0][0],Mob_vbm[0][2]))
    print(" CBM    %9.6f     %9.6f      %9.6f"%(Mob_cbm[0][1],Mob_cbm[0][0],Mob_cbm[0][2]))
else:
    print("VBM_up    %9.6f     %9.6f      %9.6f"%(Mob_vbm[0][1],Mob_vbm[0][0],Mob_vbm[0][2]))
    print("VBM_dn    %9.6f     %9.6f      %9.6f"%(Mob_vbm[1][1],Mob_vbm[1][0],Mob_vbm[1][2]))
    print("CBM_up    %9.6f     %9.6f      %9.6f"%(Mob_cbm[0][1],Mob_cbm[0][0],Mob_cbm[0][2]))
    print("CBM_dn    %9.6f     %9.6f      %9.6f"%(Mob_cbm[1][1],Mob_cbm[1][0],Mob_cbm[1][2]))
