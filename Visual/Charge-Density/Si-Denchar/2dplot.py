#!/usr/bin/env python
#-------------------------------------------------------------
# This script plots denchar output files (systemlabel.CON.SCF,
# systemlabel.CON.DEL, systemlabel.CON.WF#) as 3D surfaces and 
# contour lines.
#
# Script by Pablo Aguado-Puente (2007)
# pablo.aguado@unican.es
#-------------------------------------------------------------


# The first line is to make this python script directly executable.
# (do not forget to give the file an executable mode!!).
#

import sys
import string
import Gnuplot
from Numeric import *

# sys is a module that stores processing command line arguments.
# string is a module that defines some constants useful for checking character 
#        classes and some useful string functions

if len(sys.argv) <= 1:
  print 'Usage: python surf.py <denchar_file>'
  sys.exit()

# Read the input file where the band structure is stored.
filename = sys.argv[1]

# sys.argv returns the list of command line arguments passed to a Python script.
#          sys.argv[0] is the script name.
#          If no script name was passed to the Python interpreter, 
#          argv has zero length. 

 
g = Gnuplot.Gnuplot(persist=1)    

order='splot "'+filename+'" using 1:2:3 with lines'

g('set parametric')
g('unset surface')
g('set view 0, 0, 1, 1')
g('set data style lines')
g('set hidden')
g('set contour base')
g('set cntrparam levels auto 10')
# g('set pm3d')
g.title(filename)
g.xlabel('x')
g.ylabel('y')

g(order)

sys.exit()

