"""
Created on Mon Jul  9 11:38:27 2018

@author: lei
"""

import os
from sys import *
if(len(argv)!=5):
    print("Insufficient parameter!")
    exit()
else:
    dir=argv[1]
    latdir=argv[2]
    dis=argv[3]
    N=argv[4]
if not latdir in ('a','b','c'):
    print("error!")
    exit()

start=1-(float(N)-1)/2*float(dis)
aim=[(start+i*float(dis)) for i in range(0,int(N))]
dirname=["%i-%.3f"%(i+1,aim[i]) for i in range(0,int(N))]
for i in range(0,int(N)):
    os.system("cp -rf %s %s"%(dir,dirname[i]))
    os.chdir("./%s"%dirname[i])
    os.system("remakePOSCAR POSCAR %s %f"%(latdir,aim[i]))
#   os.system("cp -f POSCAR 1-energy/POSCAR")
    os.chdir("../")
