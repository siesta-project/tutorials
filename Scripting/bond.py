#!/usr/bin/env python

#
# bond.py : An example of Siesta scripting
#
#           Compute and plot the Energy vs. bond length curve
#           for the water molecule
#
import Gnuplot

from Siesta.ASEInterface import Atom, Structure
from Siesta.server import SiestaServer as Siesta

import math, os, shutil, urllib
import Numeric as num

try:
    executable =  os.environ["SIESTA_COMMAND"]
except:
    executable = "siesta"

print "using executable: ", executable


#
# Standard bond length (units: Angstrom)
#
d0 = math.sqrt(0.757**2 +  0.586**2)

# Range of bond lengths around the presumed minimum
bonds = num.arange(0.8*d0,1.3*d0,0.1)
energy = 0.0*bonds
theta=0.5*(180.-105.0)*math.pi/180.  # Angle with the x axis, in radians
print bonds

a = Siesta(executable="siesta")          # Initialize object
##a.SetOption("DM.UseSaveDM","T")

# create a work subdirectory
orig_dir = os.getcwd()
dir = "bond_work"
if os.path.isdir(dir): # does dir exist? 
  shutil.rmtree(dir) # yes, remove old directory 
os.mkdir(dir) # make dir directory 
os.chdir(dir) # move to dir 

URLbase = "http://fisica.ehu.es/ag/siesta-psffiles/"
urllib.urlretrieve(URLbase + "H.psf", "H.psf") 
urllib.urlretrieve(URLbase + "O.psf", "O.psf") 

# First instance to launch
d = d0
atoms = Structure(
          [Atom('H', (d*math.cos(theta),d*math.sin(theta),0.0),magmom=1),
           Atom('H', (-d*math.cos(theta),d*math.sin(theta),0.0),magmom=1),
           Atom('O', (0, 0, 0),magmom=1)], cell=(8.0, 8.0, 8.0), periodic=1)



a = Siesta(executable=executable)
a.launch(atoms)

for i in range(len(bonds)):
  d = bonds[i]
  print i, d
  atoms = Structure(
          [Atom('H', (d*math.cos(theta),d*math.sin(theta),0.0),magmom=1),
           Atom('H', (-d*math.cos(theta),d*math.sin(theta),0.0),magmom=1),
           Atom('O', (0, 0, 0),magmom=1)], cell=(8.0, 8.0, 8.0), periodic=1)

  energy[i], force, stress = a.get_forces(atoms)

#
# Plot
#
g = Gnuplot.Gnuplot(debug=1)
g.title('Energy as a function of bond-length')             # (optional)
d = Gnuplot.Data(bonds[:],energy[:],title='energy', with='lp pt 3 ps 2')
g('set grid')
g.xlabel('bond length (Ang)')
g.ylabel('Energy (eV)')
g.plot(d)
ans = raw_input('Enter f to create .png file, or Enter to quit ')
if ans == 'f':
   g.hardcopy('filename.png',terminal = 'png')
g.reset() 

os.chdir(orig_dir) 
