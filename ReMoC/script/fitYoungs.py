"""
Created on Mon Jul  9 11:38:27 2018

@author: lei
"""

import os
from sys import *
from numpy import *
if(len(argv)==1):
    direction='c'
else:
    direction=argv[1]
def fit_LS(data,Y,rank):
    X=[]
    tmp=[]
    for i in range(0,len(data)):
        for j in range(0,rank+1):
            tmp.append(data[i]**j)
        X.append(tmp)
        tmp=[]
    X=mat(X)
    Y=mat(Y).T
    guess=(X.T*X).I*X.T*Y
    guess=guess.T.tolist()[0]
    return guess

tmp=[i.rstrip() for i in os.popen("ls").readlines()]
list=[]
latt=[]
Etot=[]
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
for i in list:
    try:
        line=os.popen("tail -n1 ./%s/OS* "%i).readlines()[0].rstrip()
        energy=line.split()[4]
        Etot.append(float(energy))
    except:
        print("error!Check your OSZICAR!")
        exit()
tmp=os.popen("grep vol %s/OUTCAR|tail -n1"%list[mid]).readlines()[0].rstrip()
vol=float(tmp.split()[4])
if(direction=='a'):
    direction=3
elif(direction=='b'):
    direction=4
else:
    direction=5
height=float(os.popen("awk 'NR==%i{print $%i}' %s/CONTCAR"%(direction,direction-2,list[mid])).readlines()[0].rstrip())
Area=vol/height
E0=Etot[mid]
Etot=[2*(i-E0)/Area for i in Etot]
latt=[i-1 for i in latt]
guess=fit_LS(latt,Etot,2)
tmp=guess[2]*16.0217662
output=open('C2d','w')
string1="C2d = %.6f eV/A2"%guess[2]
string2="C2d = %.6f J/m2"%tmp
print(string1+'\n'+string2)
output.write(string1+'\n'+string2)
#print("Etot= %.6f L2 + %.6f L + %.6f"%(guess[2],guess[1],guess[0]))
