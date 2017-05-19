#!/usr/bin/env python

import os, string, shutil
from tempfile import mkdtemp
import Numeric


def dump_fdf_options(options, f):
       #
       #      Now the one-liner options
       #   The file descriptor f must exist and be opened
       #

       f.write("# ----- Options follow ---\n")
       for key in options.keys():
          f.write("%s %s\n" % (key,options[key]))


def get_efs(filename="FORCE_STRESS"):
    """
    Return energy, forces, and stress from file

    """

    f = open(filename)
    energy = float(f.readline())
    #
    #  Read stress
    #
    stress = Numeric.zeros((3,3),Numeric.Float)
    for i in range(3):
      st = f.readline().split()
      for j in range(3):
             stress[i,j] = float(st[j])
#
#   Now the atoms and forces
#
    na = int(f.readline())

    forces = Numeric.zeros((na,3),Numeric.Float)  # Note index order
    for i in range(na):
      isa, iza, x, y, z, label = f.readline().split()
      force = x, y, z
      for j in range(3):
          forces[i,j] = float(force[j])

    f.close()
    
    return energy, forces, stress
#
       
class Siesta_efs:

  def __init__(self,executable=None):

        self.executable="$HOME/bin/siesta-2.4-optim"
	if executable is not None:
           self.executable=executable

        self.redirect_output=" > OUT"

	self.options = { "MD.TypeOfRun"  : "CG",
                         "MD.NumCGSteps" : "0"   
                       }

        self.filename = "test.fdf"

  def SetOption(self,name,value):
        self.options[name]= value

    
  def run(self,atoms,out=None):

       if out is not None:
          self.redirect_output=" > " + out

       f = open(self.filename,"w")
       atoms.write_in_fdf_form(f)
       dump_fdf_options (options=self.options, f=f)
       f.close()
       os.system("cp " + self.filename + " FDF")

       #
       #      Execute
       #
       os.system(self.executable + " <  " + self.filename + self.redirect_output)

       #
       # Direct reading of the FORCE_STRESS file
       #

       energy, forces, stress = get_efs()

       Ang = 1.0 / 0.529177
       eV  = 1.0 / 13.60580

       return energy/eV , forces*Ang/eV, stress*Ang**3/eV

  def stop(self):
	print "Bye"
       



