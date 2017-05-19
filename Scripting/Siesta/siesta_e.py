#!/usr/bin/env python

import os, string, shutil
from tempfile import mkdtemp

class Siesta:

  def __init__(self,executable=None):

        self.executable="/Users/ag/bin/siesta-xlf"
	if executable is not None:
           self.executable=executable
        self.redirect_output=" > OUT"
	self.options = {}
	self.filename = "test.fdf"

  def SetOption(self,name,value):
        self.options[name]= value

  def run(self,atoms,out=None):
       if out is not None:
          self.redirect_output=" > " + out

       f = open(self.filename,"w")
       atoms.write_in_fdf_form(f)
#
#      Now the one-liner options
#
       f.write("# ----- Options follow ---\n")
       for key in self.options.keys():
          f.write("%s %s\n" % (key,self.options[key]))

       f.close()

       os.system(self.executable + " <  " + self.filename + self.redirect_output)
       os.system(" grep FreeEng  OUT | tail -1 | awk '{print $4}' > tmp.energy")
       g = open("tmp.energy","r")
       e = g.readline()
       g.close()
       os.system("rm -f tmp.energy")

       return string.atof(e)


