#clone
clone Directoryname(0-initial recommended) Direction Step Number(Odd recommended)

Example:
clone 0-initial a 0.025 5
Get:
1-0.950 2-0.975 3-1.000 4-1.025 5-1.050

#fitYoungs
fitYoungs VacuumDirection
output: C2d

#fitWeff
fitWeff VacuumDirection
output: Weff

#fitMe
fitMe Kpoints(Start-End or 0 for all,0 default) VBM Kpoints CBM
output:Me

#fitEl
fitEl Kpoint_VBM VBM Kpoint_CBM CBM
output:El

#Format:
Only "(1-99)-(relative lattice constant)" directories can be taken into account. Please avoid (1-99)-XXXX for other files!!
"X-1.000" directory is necessary, meanwhile, "3-Me" sub-directory should be included
"1-CHG" and "2-band" sub-directory should be included in each directory
