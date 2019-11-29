"""
Created on Mon Jul  9 11:38:27 2018

@author: lei
"""

from sys import *
import os
if(len(argv)!=4):
    print("error!")
    exit()
else:
    file=argv[1]
    dir=argv[2]
    per=float(argv[3])

if(dir=='a'):
    line=3
elif(dir=='b'):
    line=4
elif(dir=='c'):
    line=5
else:
    print("error!")
    exit()

lat=os.popen("awk 'NR==%i{print $0}' %s"%(line,file)).readlines()[0].rstrip()
lat_x=lat.split()[0]
lat_y=lat.split()[1]
lat_z=lat.split()[2]
pos=lat_x.find('.')
l=len(lat_x)-pos-1
new_x=per*float(lat_x)
new_y=per*float(lat_y)
new_z=per*float(lat_z)
os.system("sed -i %ic'    %.*f    %.*f    %.*f' %s"%(line,l,new_x,l,new_y,l,new_z,file))
