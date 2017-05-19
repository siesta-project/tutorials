#!/usr/bin/env python

import os, string, sys
import Numeric

class SiestaServer:

  """ A modified version (it should be a subclass) which
    uses the NEW in/out (no pipes) SiestaAsServer features.  """

  def __init__(self,executable=None):

        self.executable="siesta"
	if executable is not None:
           self.executable=executable
           
	self.filename="FDF"

#	self.options = { }
	self.options = { "MD.TypeOfRun" : "forces" ,
                         "SystemLabel"  : "siesta" }

  def SetOption(self,name,value):
        self.options[name]= value

  def launch(self,atoms):

       self.parent_dir = os.getcwd()
       import tempfile
       self.work = tempfile.mkdtemp(prefix="siesta.work.",dir=".")
       os.chdir(self.work)
       fdf = open(self.filename,"w")
       atoms.write_in_fdf_form(fdf)

#      Now the one-liner options
       fdf.write("# ----- Options follow ---\n")
       for key in self.options.keys():
          fdf.write("%s %s\n" % (key,self.options[key]))

       fdf.close()
       os.system("cp ../*.psf .")
       
       import popen2
       self.child = popen2.Popen3(self.executable)    
       print "Launched Siesta server. PID: ", self.child.pid, " . Working dir: ", self.work
       print "Siesta executable: ", self.executable
       self.f = self.child.tochild
       self.toserver = self.f.write
       self.fromserver = self.child.fromchild.readline
       self.toserver("wait\n")   

       os.chdir(self.parent_dir)
       print "Now returned to ", os.getcwd()
       
       
  def get_forces(self,atoms):
       self.toserver("begin_coords\n")
       self.toserver("Ang\n")
       self.toserver("eV\n")

       ucell = atoms.GetUnitCell()
       for i in range(3):
          for j in range(3):
             self.toserver("%15.8f" % ucell[i,j])
          self.toserver("\n")

       self.toserver("%d\n" % len(atoms))

       for atom in atoms:
         xyz = atom.GetCartesianPosition()
         for i in range(3):
           self.toserver("%15.8f " % xyz[i])
         self.toserver("\n")
       self.toserver("end_coords\n")
       self.f.flush()
       print "Sent coordinates"

#      Open pipe for reading energy, stress, and forces
#

       msg = self.fromserver().split()
       if  msg[0] != "begin_forces" : 
             print "Not begin_forces"
             sys.exit(1)
       energy = float(self.fromserver().split()[0])

       stress = Numeric.zeros((3,3),Numeric.Float)
       for i in range(3):
         st = self.fromserver().split()
         for j in range(3):
           stress[i,j] = float(st[j])

       na = int(self.fromserver().split()[0])
       if na != len(atoms): 
           print "number of atoms", na
           sys.exit(1)
       forces = Numeric.zeros((na,3),Numeric.Float)  # Note index order
       for i in range(na):
         force = self.fromserver().split()
         for j in range(3):
           forces[i,j] = float(force[j])

       msg = self.fromserver().split()
       if  msg[0] != "end_forces" :
             print "Not end_forces"
             sys.exit(1)

       return (energy, forces, stress)

  def stop(self):
       self.toserver("quit\n")
       self.child.tochild.close()
       self.child.wait()
       print "".join(self.child.fromchild.readlines())              
       status = self.child.fromchild.close()
       if status is not None:
          print " Child status: ", status
    
if __name__=="__main__":

  from ASEInterface import *

  a = Atom("H",label="H_surf",position=(0.4,0.1,0.2))
  b = Atom("O",(0.,0.,0.5),label="O_bulk")

  cryst = Structure([a,b])

  s = SiestaServer("$HOME/bin/siesta-server")
  s.launch(cryst)
  s.stop()


