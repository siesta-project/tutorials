#!/usr/bin/env python
#-------------------------------------------------------------
# This script plots the projected density of states
#
# Script by Javier Junquera (2007)
# javier.junquera@unican.es
#-------------------------------------------------------------


# The first line is to make this python script directly executable.
# (do not forget to give the file an executable mode!!).
#

import sys
import string
import Gnuplot

# sys is a module that stores processing command line arguments.
# string is a module that defines some constants useful for checking character 
#        classes and some useful string functions

if len(sys.argv) <= 1:
  print 'Usage: python dos.py <dos_file>'
  sys.exit()

# Read the input file where the energy versus volume data and the type of cell
# are stored.

filenamedos       = sys.argv[1]

# sys.argv returns the list of command line arguments passed to a Python script.
#          sys.argv[0] is the script name.
#          If no script name was passed to the Python interpreter, 
#          argv has zero length. 

f=open(filenamedos,"r")

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

# Let's read the DOS file.
# the energy versus lattice constant curve.

line = f.readline()
# f.readline() reads a single line from the file;

# Read the density of states
energies = []
dosup    = []
dosdown  = []

while line:
  
   t = string.split(line)
# string.split  returns a list of the words of the string line.

   energies.append(float(t[0]))
   dosup.append(float(t[1]))
   dosdown.append(float(t[2]))

   line = f.readline()

f.close()
# call f.close() to close the file and free up any system resources 
# taken up by the open file. 

g = Gnuplot.Gnuplot(persist=1)
g.xlabel('Energy (eV)')
g.ylabel('Total DOS (1/eV)')

dataup = Gnuplot.Data(energies,dosup,
                      title='Density Of States for Spin Up',
                      with='lines')

if max(dosdown) == 0 : 
   g.plot(dataup)
else:
   datadown = Gnuplot.Data(energies,dosdown,
                      title='Density Of States for Spin Down',
                      with='lines')
   g.plot(dataup,datadown)


sys.exit()

