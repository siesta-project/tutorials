#!/usr/bin/env python

"""
     This implementation uses one FIFO for each process.
     It was intended to sidestep a performance issue
     in MareNostrum, but it did not work in the end due
     to GPFS issues
"""

import os, string, sys
import Numeric

class SiestaServer:

  """ A modified version (it should be a subclass) which
    uses the SiestaAsServer features.  """

  def __init__(self,executable=None):

        import os
        if os.uname()[0] == "Darwin":
          import sys
          print "FIFOS will not work on MacOSX!!"
          sys.exit(1)
          
        self.executable="siesta"
	if executable is not None:
           self.executable=executable

        self.redirect_output=" > OUT"

#	self.options = { }
	self.options = { "MD.TypeOfRun" : "forces" ,
                         "SystemLabel"  : "siesta" }

  def SetOption(self,name,value):
        self.options[name]= value

  def launch(self,atoms,out=None):

       if out is not None:
          self.redirect_output=" > " + out

       import tempfile
       self.work = tempfile.mkdtemp(prefix="siesta.work.",dir=".")
       os.system("cp *.psf " + self.work)
       self.filename=self.work + "/" +"siesta.fdf"

       fdf = open(self.filename,"w")
       atoms.write_in_fdf_form(fdf)

#      Now the one-liner options
       fdf.write("# ----- Options follow ---\n")
       for key in self.options.keys():
          fdf.write("%s %s\n" % (key,self.options[key]))

       fdf.close()
       try:
          self.nreaders =  int(os.environ["NREADERS"])
       except:
          self.nreaders =  1

       self.fifos_name = []
       self.fifos_file = []
       self.fifos_handle = []

       print "Creating ", self.nreaders, " readers"
       for i in range(self.nreaders):
            name = "%s%5.5i" % ("siesta.coords", i)
            self.fifos_name.append(name)
            filename = self.work + "/" + name
            self.fifos_file.append(filename)
            os.mkfifo(filename)
            print "Created FIFO ", filename

       self.fifo_forces = self.work + "/siesta.forces"
       os.mkfifo(self.fifo_forces)
       
       os.system("( cd " + self.work + "; " +
                 self.executable + " < siesta.fdf " + self.redirect_output + " ) &")

       print "Launched Siesta server"

       for i in range(self.nreaders):
         handle=open(self.fifos_file[i],"w")
         self.fifos_handle.append(handle)

       self.f = self.fifos_handle[0]
       self.toserver = self.f.write     # For bulk operation

       for f in self.fifos_handle:
         f.write("wait\n")
         f.flush()


  def get_forces(self,atoms):

       for f in self.fifos_handle:
         f.write("begin_coords\n")
         f.flush()
         
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

#      print "Sent coordinates"

#      Open pipe for reading energy, stress, and forces
#      We have to wait until the server has written something
#      to it (or is going to, soon)
#
       self.fromserver = open(self.fifo_forces,"r").readline
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
       for f in self.fifos_handle:
         f.write("quit\n")
         f.flush()

if __name__=="__main__":

  from ASEInterface import *

  a = Atom("H",label="H_surf",position=(0.4,0.1,0.2))
  b = Atom("O",(0.,0.,0.5),label="O_bulk")

  cryst = Structure([a,b])

  s = SiestaServer("$HOME/bin/siesta")
  s.launch(cryst)
  s.stop()


