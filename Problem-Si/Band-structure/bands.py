#!/usr/bin/env python
#-------------------------------------------------------------
# This script plots the band diagram reading the Siesta output
# file systemlabel.bands. If there are bands for both spin states,
# bands for each one are plotted.
#
# Script by Javier Junquera and Pablo Aguado-Puente (2007)
# javier.junquera@unican.es     pablo.aguado@unican.es
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
  print 'Usage: python dos.py <bands_file>'
  sys.exit()

# Read the input file where the band structure is stored.
filenamebands       = sys.argv[1]

# sys.argv returns the list of command line arguments passed to a Python script.
#          sys.argv[0] is the script name.
#          If no script name was passed to the Python interpreter, 
#          argv has zero length. 

f=open(filenamebands,"r")

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

# Let's read the band structure from the file.

# Read the Fermi energy
line = f.readline()
# f.readline() reads a single line from the file;

t = string.split(line)
efermi = float(t[0])
print 'Fermi energy = ', efermi, ' eV'

# Read the maximum and minimum point in the line of k-points
line = f.readline()
t = string.split(line)
xmin = float(t[0])
xmax = float(t[1])
#print xmin, xmax

# Read the maximum and minimum energy in the band structure
line = f.readline()
t = string.split(line)
energymin = float(t[0])
energymax = float(t[1])
#print energymin, energymax

# Read the number of orbitals in the unit cell, 
# the number of spin components, and
# the number of k-points used to plot the band structure
line = f.readline()
t = string.split(line)
norb    = int(t[0])
print "Number of orbitals in unit cell          =", norb
nspin   = int(t[1])
print "Number of different spin polarizations   =", nspin
nkpoint = int(t[2])
print "Number of k-points to represent the band =", nkpoint
norb=norb*nspin

# nlines is the number of lines per k point 
# containing the orbitals.
nlines = norb / 10
nrest  = norb - (nlines * 10)

xkpoint = []
# Initialize the vectors holding the bands
bands=[]
for ibands in range(0,norb):
   bands.append([])

# Read the bands
for ik in range(1, nkpoint + 1):
   for ilines in range(0, nlines):
      line = f.readline()
      t = string.split(line)
      if ilines == 0:
        xkpoint.append(float(t[0]))
        for it in range(1, len(t)):
          ibands=it-1
          bands[ibands].append(float(t[it]))
      else:
        for it in range(0,len(t)):
          ibands=ilines*10+it
          bands[ibands].append(float(t[it]))
   if nrest > 1:
      line = f.readline()
      t = string.split(line)
      for it in range(0,len(t)):
        ibands=nlines*10+it
        bands[ibands].append(float(t[it]))

# Define the limits of the plot
ymin=min(bands[0])
ymax=efermi
ymin=ymin-abs(ymax-ymin)*0.1
ymax=ymax+abs(ymax-ymin)

g = Gnuplot.Gnuplot(persist=1)
g.xlabel('')
g.ylabel('Energy (eV)')
g('set xrange ['+str(xmin)+':'+str(xmax)+']')
g('set yrange ['+str(ymin)+':'+str(ymax)+']')

line = f.readline()
t = string.split(line)
nlabels = int(t[0])

# Add ticks in the special k points
lineplot=[]
tics='set xtics ('
for ilabel in range(0, nlabels-1):
  line = f.readline()
  t = string.split(line)
  tics=tics+t[1]+' '+t[0]+', '
  lineplot.append(Gnuplot.Data([float(t[0]),float(t[0])],[ymin,ymax],with='lines -1'))

line = f.readline()
t = string.split(line)
tics=tics+t[1]+' '+t[0]+')'
lineplot.append(Gnuplot.Data([float(t[0]),float(t[0])],[ymax,ymax],with='lines -1'))
g(tics)

# Plot vertical lines in the special k-points
for iplot in range(0,nlabels):
  g.replot(lineplot[iplot])

# Plot the Fermi level
g.replot(Gnuplot.Data([xmin,xmax],[efermi,efermi],with='lines 3'))
fermi_label='set label "E_F" at '+str(xmax+abs(xmax-xmin)*.005)+','+str(efermi)
g(fermi_label)

# The maximum number of lines is 24 so maxnumbands is defined
# this might not be necessary in some systems
maxnumbands = 24-(nlabels+1)
maxnumbands = min([maxnumbands,norb])
# maxnumbands = norb

bandplot=[]
# If nspin == 2 spin bands are plotted in two colors
# else only one color is showed
for ibands in range(0,maxnumbands/nspin):
  bandplot.append(Gnuplot.Data(xkpoint,bands[ibands],
                         with='line -1'))
for ibands in range(norb/nspin,norb):
  bandplot.append(Gnuplot.Data(xkpoint,bands[ibands],
                         with='line 1'))

for iplot in range(0,maxnumbands):
  g.replot(bandplot[iplot])

f.close()
# call f.close() to close the file and free up any system resources 
# taken up by the open file. 

sys.exit()

