"""
Created on Mon Jul  9 11:38:27 2018

@author: lei
"""

import os
from numpy import *
from sys import *

if(len(argv)!=2):
    print("Please input direction!")
    exit()
else:
    direction=argv[1]

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
if(mid==0):
    other=mid+1
else:
    other=mid-1
plength=0
gridp=0
def readCHGCAR(filename):
    global gridp
    carin=open(filename,'r')
    tmp=carin.readline() #system_name
    tmp=carin.readline() #size
    tmp=carin.readline()
    tmp=carin.readline()
    tmp=carin.readline() #lattice
    tmp=carin.readline() #atom type
    tmp=carin.readline()
    atnum=[int(i) for i in tmp.split()]
    N=sum(atnum) #total
    tmp=carin.readline() #Direct
    for i in range(0,N):
        tmp=carin.readline() #position
    tmp=carin.readline() #empty
    tmp=carin.readline()
    gridnum=[int(i) for i in tmp.split()]
    data=[[[0 for i in range(0,gridnum[2]+1)]for j in range(0,gridnum[1]+1)]for k in range(0,gridnum[0]+1)]
    pos=[1,1,1]
    def nextnum(pos,num):
        data[pos[0]][pos[1]][pos[2]]=num
        if pos[0]==gridnum[0]:
            if pos[1]==gridnum[1]:
                pos[0]=1
                pos[1]=1
                pos[2]+=1
            else:
                pos[0]=1
                pos[1]+=1
        else:
            pos[0]+=1
        return pos
    tmp=carin.readline()
    while pos[2]<=gridnum[2]:
        line=[float(i) for i in tmp.split()]
        n=len(line)
        for i in range(0,n):
            pos=nextnum(pos,line[i])
        tmp=carin.readline()
    def sumx(x):
        sum=0
        for j in range(1,gridnum[1]+1):
            for k in range(1,gridnum[2]+1):
                sum+=data[x][j][k]
        return sum
    def sumy(y):
        sum=0
        for i in range(1,gridnum[0]+1):
            for k in range(1,gridnum[2]+1):
                sum+=data[i][y][k]
        return sum
    def sumz(z):
        sum=0
        for i in range(1,gridnum[0]+1):
            for j in range(1,gridnum[1]+1):
                sum+=data[i][j][z]
        return sum
    def sum_all(dir):
        global gridp
        sum=0
        Ptotal=[]
        if(dir=='a'):
            Ptotal=[sumx(i) for i in range(1,gridnum[0]+1)]
            gridp=gridnum[0]
        elif(dir=='b'):
            Ptotal=[sumy(j) for j in range(1,gridnum[1]+1)]
            gridp=gridnum[1]
        else:
            Ptotal=[sumz(k) for k in range(1,gridnum[2]+1)]
            gridp=gridnum[2]
        return Ptotal
    Ptotal=sum_all(direction)
    etotal=sum(Ptotal)
    Ptotal=[i/etotal for i in Ptotal]
    return Ptotal
os.chdir("./%s/1-CHG"%list[mid])
P0=readCHGCAR('CHGCAR')
os.chdir("../")
if(direction=='a'):
    line=3
elif(direction=='b'):
    line=4
else:
    line=5
height=float(os.popen("awk 'NR==%i{print $%i}' ./CONTCAR"%(line,line-2)).readlines()[0].rstrip())
plength=height/gridp
os.chdir("../%s/1-CHG"%list[other])
P1=readCHGCAR('CHGCAR')
PP=[P0[i]*P1[i] for i in range(0,len(P0))]
PPtot=sum(PP)
Weff=plength/PPtot
string="Weff = %.10f A"%Weff
os.chdir("../../")
output=open('Weff','w')
output.write(string)
print(string)
