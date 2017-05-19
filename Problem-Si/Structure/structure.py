#!/usr/bin/env python
#
# The previous first line is to make this python script directly executable.
# (do not forget to give the file an executable mode!!).
#

import sys
import string
import EquationOfState

# sys is a module that stores processing command line arguments.
# string is a module that defines some constants useful for checking character 
#        classes and some useful string functions
# EquationOfState is a module implemented by 
#        John Kitchin <jkitchin@andrew.cmu.edu> to fit an energy versus volume
#        curve to different equations of states. Those might be:
#                Murnaghan
#                Birch
#                BirchMurnaghan
#                Vinet
#                PoirerTarantola
#                AntonSchmidt
#                Taylor


if len(sys.argv) <= 1:
  print 'Usage: python latcon.py <energy_vs_latticeconstant_file>'
  sys.exit()

# Read the input file where the energy versus volume data and the type of cell
# are stored.

filenameevslatcon       = sys.argv[1]

# sys.argv returns the list of command line arguments passed to a Python script.
#          sys.argv[0] is the script name.
#          If no script name was passed to the Python interpreter, 
#          argv has zero length. 

f=open(filenameevslatcon,"r")

# open() returns a file object, and is most commonly used 
#        with two arguments: "open(filename, mode)":
#            The first argument is a string containing the filename. 
#            The second argument is another string containing a few 
#                characters describing the way in which the file will be used.
#                Mode can be:
#                'r' when the file will only be read, 
#                'w' for only writing (an existing file with the 
#                           same name will be erased), 
#                'a' opens the file for appending; any data written to 
#                           the file is automatically added to the end. 
#                'r+' opens the file for both reading and writing. 
#                The mode argument is optional; ('r' by default)

# Let's start to digest the file with the information on
# the energy versus lattice constant curve.

line = f.readline()
# f.readline() reads a single line from the file;
# if f.readline() returns an empty string, the end of the file has been reached,

# Read the type of lattice
t = string.split(line)
# string.split  returns a list of the words of the string line.
typeoflattice           = t[0]

line = f.readline()

# Read the lattice constant and energy table.
# Compute the volume.
latcon   = []
volumes  = []
energies = []

while line:
  
   t = string.split(line)
# string.split  returns a list of the words of the string line.
   if not t: break
   a   = float(t[0])

   if typeoflattice == 'sc' :
      vol = a**3
   elif typeoflattice == 'bcc' :
      vol = a**3/2
   elif typeoflattice == 'fcc' :
      vol = a**3/4
   elif typeoflattice == 'diamond' :
      vol = a**3/4

   latcon.append(a)
   volumes.append(vol)
   energies.append(float(t[1]))

   line = f.readline()

f.close()
# call f.close() to close the file and free up any system resources 
# taken up by the open file. 

eos = EquationOfState.EquationOfState('Murnaghan',volumes,energies)
print eos
g = eos.GetPlot()

minvolume = eos.eos_parameters[3]

if typeoflattice == 'sc' :
   minlatcon = minvolume**(1.0/3.0)
elif typeoflattice == 'bcc' :
   minlatcon = (2.0 * minvolume)**(1.0/3.0)
elif typeoflattice == 'fcc' :
   minlatcon = (4.0 * minvolume)**(1.0/3.0)
elif typeoflattice == 'diamond' :
   minlatcon = (4.0 * minvolume)**(1.0/3.0)

print 'Theoretical lattice constant (Angstrom) '
print minlatcon

sys.exit()

