#!/usr/bin/env python

from Siesta.ASEInterface import  Atom, Structure
from Siesta.calculator_server import SiestaCalculator
from ASE.Dynamics.MDMin import MDMin

import urllib 
import os, shutil 

try:
    executable =  os.environ["SIESTA_COMMAND"]
except:
    executable = "siesta"

print "using executable: ", executable

URLbase = "http://fisica.ehu.es/ag/siesta-psffiles/"

atoms = Structure([Atom('H', (0.777,0.586,0.3),label="H_test"),
                     Atom('H', (-0.757,0.610,-0.4),magmom=1),
                     Atom('O', (0, 0, 0),magmom=1)],
                     cell=(6.0, 6.0, 6.0), periodic=1)

# create a work subdirectory
orig_dir = os.getcwd()
dir = "ase_relax_work"
if os.path.isdir(dir): # does dir exist? 
  shutil.rmtree(dir) # yes, remove old directory 
os.mkdir(dir) # make dir directory 
os.chdir(dir) # move to dir 

urllib.urlretrieve(URLbase + "H.psf", "H_test.psf") 
urllib.urlretrieve(URLbase + "H.psf", "H.psf") 
urllib.urlretrieve(URLbase + "O.psf", "O.psf") 

b = SiestaCalculator(executable=executable)
b.SetOption("DM.Tolerance","0.001")
atoms.SetCalculator(b)

energy = atoms.GetPotentialEnergy()
forces = atoms.GetCartesianForces()
stress = atoms.GetStress()

print "The energy is: ", energy
print "Forces ", forces
print "Stress ", stress

dyn = MDMin(atoms, dt=0.08, fmax=0.01)
dyn.Converge()

energy = atoms.GetPotentialEnergy()
forces = atoms.GetCartesianForces()
stress = atoms.GetStress()

print "The energy is: ", energy
print "Forces ", forces
print "Stress ", stress

b.stop()

os.chdir(orig_dir) 
