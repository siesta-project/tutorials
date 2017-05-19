#!/usr/bin/env python
#
# The previous first line is to make this python script directly executable.
# (do not forget to give the file an executable mode!!).
#
#---------------------------------------------------------------------------
# This script let's you run SIESTA changing systematically 
# the value of one or more parameters.
# The script will read an input with as many lines as
# parameters one wants to scan. Each line will have this structure:
#   ParameterLabel	Minimum		Maximum		NumberSteps
#
# where ParameterLabel must be written in the SIESTA input 
# substituting the value of the SIESTA variable one wants to scan.
# The input name must be SystemLabel.in.
# The script will write a file SystemLabel.script.out with all
# the possible values of the parameters and the value of
# the Total Energy and Maximum force of each simulation. If
# one of the parameters is the MeshCutoff, it will include the
# actual value of the MeshCutoff.
#
# Usage: $ autosiesta.py SystemLabel
# or:    $ python autosiesta.py SystemLabel
#--------------------------------------------------------------------------
# Pablo Aguado Puente 2008
# pablo.aguado@unican.es
#--------------------------------------------------------------------------

import os
import sys
import string
import time

if len(sys.argv) <= 1:
  print 'Usage: python autosiesta.py SystemLabel'
  sys.exit()

label = sys.argv[1]

f_fdf = open(label+'.fdf','r')  	# Opens SIESTA input.
f_in = open(label+'.in','r')		# Opens script input.
f_out = open(label+'.script.out','w')	# Opens script output.

par = []			# It will store parameters' information.
count = []                      # Index counting runnings over each parameter.
currentPar = []                 # Current values of the parameters.

ipar = 0			# Parameter counter.
Nsiestas = 1.0			# SIESTA calls counter

# ---------------------------------------------------------------------------
# Reading the script input
#----------------------------------------------------------------------------
line = f_in.readline()
while line:
	t = string.split(line)
	if t[0][0] == '#':
		line = f_in.readline()
	else:
		par.append([])
		par[ipar].append(t[0])		# Label of the parameter
		par[ipar].append(float(t[1]))	# Min
		par[ipar].append(float(t[2]))	# Max
		par[ipar].append(int(t[3]))	# Steps
		disp = (par[ipar][2] - par[ipar][1])/par[ipar][3]
		par[ipar].append(disp)		# Displacement
		ipar = ipar + 1
		Nsiestas = Nsiestas*(float(t[3])+1)
		count.append(0)
		currentPar.append(float(t[1]))
		line = f_in.readline()
	# End if
# End while
#-------------------------------------------------------------------------

Npar = ipar				# Total number of parameters
print 'Total calls to SIESTA = '+str(Nsiestas)
siesta_call = 1
control = True
MeshCutoff = False

#-------------------------------------------------------------------------
# Writing the SIESTA input and calling SIESTA
#--------------------------------------------------
f_tmp = open(label+'.'+str(siesta_call)+'.tmp','w')	# Opens SIESTA
							# temporal input

# Reading SIESTA input (SystemLabel.fdf) and writing SIESTA temporal
# input (SystemLabel.siesta_call.tmp) with corresponding values of
# the parameters.

line = f_fdf.readline()
while line:
	t = string.split(line)
	for k in range(0, len(t)):
		for m in range(0, Npar):
			if string.lower(t[k]) == string.lower(par[m][0]):
				t[k]=str(currentPar[m])
				if string.lower(t[0]) == 'meshcutoff':
					MeshCutoff = True
					ExtraLabel = 'MeshCutoff used'
				# End if
			# End if
		# End for
	# End for
       
	# Reconstructing the line and writing in the SIESTA temporal input.
	
	line = string.join(t)
	f_tmp.write(line+'\n')
	line = f_fdf.readline()
# End while

f_tmp.close()
f_fdf.seek(0)
print 'SIESTA call number ',str(siesta_call)
os.system('./siesta < '+label+'.'+str(siesta_call)+'.tmp'+' > '+label+'.'+str(siesta_call)+'.out')

#--------------------------------------------------------------------------
# Once the SIESTA running has ended, total energy and maximum force
# are read from the SIESTA output and written in the script output.
#----------------------------------------------------

# First line of the script output is written.

f_out.write('##')
for n in range(0, Npar):
	f_out.write('%20s ' % par[n][0][1:])
if MeshCutoff:
	f_out.write('%20s ' % ExtraLabel)
f_out.write('%20s ' % 'Etot')
f_out.write('%15s ' % 'Fmax\n')

# Writing in the script output current values of the parameters.

f_out.write(' ')
for n in range(0,Npar):
	f_out.write('%20s ' % str(currentPar[n]))
f_siestaOut = open(label+'.'+str(siesta_call)+'.out','r')

# Reading SIESTA output and writing script output.

line = f_siestaOut.readline()
while line:
	t = string.split(line)
	if MeshCutoff:
		if line[0:21] == 'InitMesh: Mesh cutoff':
			f_out.write('%20s ' % t[7])
	if len(t) == 3:
		if t[2] == 'constrained':
			Fmax = t[1]
	if len(t) == 4:
		if t[1] == 'Etot':
			Etot = t[3]
	line = f_siestaOut.readline()

f_out.write('%20s ' % Etot)
f_out.write('%15s ' % Fmax)
f_out.write('\n')

f_siestaOut.close()
siesta_call = siesta_call + 1
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Here the loops over all the possible values of the parameters 
# begin.
#--------------------------------------------------------------------------

while control:
	count[0] = count[0] + 1
	currentPar[0] = currentPar[0] + par[0][4]
	
	#-------------------------------------------------------------------
	# Writing the SIESTA input and calling SIESTA.
	#-------------------------------------------------------------------
	
	f_tmp = open(label+'.'+str(siesta_call)+'.tmp','w')	# Opens SIESTA
								# temporal input
	
	# Reading SIESTA input (SystemLabel.fdf) and writing SIESTA temporal
	# input (SystemLabel.siesta_call.tmp) with corresponding values of
	# the parameters.
	
	line = f_fdf.readline()
	while line:
		t = string.split(line)
		for k in range(0, len(t)):
			for m in range(0, Npar):
				if string.lower(t[k]) == string.lower(par[m][0]):
					t[k]=str(currentPar[m])
				# End if
			# End for
		# End for
		
		# Reconstructing the line and writing in the SIESTA temporal input.

		line = string.join(t)
		f_tmp.write(line+'\n')
		line = f_fdf.readline()
	# End while
	
	f_tmp.close()
	f_fdf.seek(0)
	print 'SIESTA call number ',str(siesta_call)
	os.system('./siesta < '+label+'.'+str(siesta_call)+'.tmp'+' > '+label+'.'+str(siesta_call)+'.out')
	
	#------------------------------------------------------------------
	# Once the SIESTA running has ended, total energy and maximum force
	# are read from the SIESTA output and written in the script output.
	#-----------------------------------------------------------------

	# Writing in the script output current values of the parameters.
	
	f_out.write('  ')
	for n in range(0,Npar):
	        f_out.write('%20s ' % str(currentPar[n]))
	f_siestaOut = open(label+'.'+str(siesta_call)+'.out','r')
	
	# Reading SIESTA output and writing script output.

	line = f_siestaOut.readline()
	while line:
	        t = string.split(line)
	        if MeshCutoff:
	                if line[0:21] == 'InitMesh: Mesh cutoff':
	                        f_out.write('%20s ' % t[7])
	        if len(t) == 3:
	                if t[2] == 'constrained':
	                        Fmax = t[1]
	        if len(t) == 4:
	                if t[1] == 'Etot':
	                        Etot = t[3]
	        line = f_siestaOut.readline()
	
	f_out.write('%20s ' % Etot)
	f_out.write('%15s ' % Fmax)
	f_out.write('\n')
	
	siesta_call = siesta_call + 1
	f_siestaOut.close()
	#------------------------------------------------------------------

	for j in range(0, Npar):
		if count[j] == par[j][3]:
			if j == (Npar - 1):
				control = False
			elif count[j+1] != par[j+1][3]:
				count[j+1] = count[j+1] + 1
				count[j] = 0
				currentPar[j+1] = currentPar[j+1] + par[j+1][4]
				currentPar[j] = par[j][1]
				#----------------------------------------
			        # Writing SIESTA input and calling SIESTA
				#----------------------------------------

			        f_tmp = open(label+'.'+str(siesta_call)+'.tmp','w')
				line = f_fdf.readline()
			        while line:
		        	        t = string.split(line)
                			for k in range(0, len(t)):
			                        for m in range(0, Npar):
                        			        if string.lower(t[k]) == string.lower(par[m][0]):
                                			        t[k]=str(currentPar[m])
                                			# End if
                       				 # End for
					# End for
			                line = string.join(t)
			                f_tmp.write(line+'\n')
			                line = f_fdf.readline()
			        # End while
			        f_tmp.close()
				f_fdf.seek(0)
			        print 'SIESTA call number ',str(siesta_call)
			        os.system('./siesta < '+label+'.'+str(siesta_call)+'.tmp'+' > '+label+'.'+str(siesta_call)+'.out')
			        #---------------------------------------
			        # Once the SIESTA running has ended,
				# total energy and maximum force are
				# read from the SIESTA output and
				# written in the script output.
			        #---------------------------------------
			        f_out.write('  ')	
			        for n in range(0,Npar):
			                f_out.write('%20s ' % str(currentPar[n]))
			        f_siestaOut = open(label+'.'+str(siesta_call)+'.out','r')
			
			        line = f_siestaOut.readline()
			        while line:
			                t = string.split(line)
			                if MeshCutoff:
			                        if line[0:21] == 'InitMesh: Mesh cutoff':
			                                f_out.write('%20s ' % t[7])
			                if len(t) == 3:
			                        if t[2] == 'constrained':
			                                Fmax = t[1]
			                if len(t) == 4:
			                        if t[1] == 'Etot':
			                                Etot = t[3]
			                line = f_siestaOut.readline()
			
			        f_out.write('%20s ' % Etot)
			        f_out.write('%15s ' % Fmax)
			        f_out.write('\n')
			        siesta_call = siesta_call + 1
				f_siestaOut.close()
				#---------------------------------------
				break
			elif count[j+1] == par[j+1][3]:
				count[j] = 0
				currentPar[j] = par[j][1]
			# End if
		else:
			break
		# End if
	# End for
# End while

f_fdf.close()
f_in.close()
f_out.close()

print 'The End'

sys.exit()

