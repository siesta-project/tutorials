"""
Extend the ASE classes to provide Siesta-specific functionality
This version uses species objects
"""

import ASE.Atom 
from  ASE.Atom  import _dummy_list_of_atoms
import ASE.ListOfAtoms

from ASE.ChemicalElements.symbol import symbols
from ASE.ChemicalElements.mass import masses
from ASE.ChemicalElements import numbers, Element

import os, shutil

#  Hybrid_Symbol = "X"     # Consider making this a module variable
#-------------------
class Species:

    """Species object for Siesta. Includes label
       and valence ground state information
    """

    def __init__(self, symbol=None,
                 Z=None, mass=None,
                 label=None, valence_gs=None):
        """Species({symbol|Z} [,label] [,valence_gs] ...) -> species object."""

        self.ghost = False
                    
        if Z is None: 
          if symbol is None: raise RuntimeError, "Need symbol"
          self.Z = numbers[symbol]
          self.symbol = symbol
        else:    # Need to specify Z also
          if Z == 0: raise ValueError, "Cannot set Z=0 in Species init"
	  self.symbol = symbols[Z]
          if symbol is None:
              pass
          else:
              if symbol != self.symbol: raise RuntimeError, "mismatched symbol"
          self.Z = Z

        if label is None:
            self.label = self.symbol
        else:
            self.label = label
            
        if valence_gs is None: 
          self.valence_gs = []
        else:
          self.valence_gs = valence_gs
          for n in valence_gs[0]:
              if n <= 0: raise RuntimeError, "n quantum number must be > 0"

        if mass is None:
            self.mass = masses[self.Z]
        else:
            self.mass = mass

    def __str__(self):
        print "Species " + self.label

    def GetAtomicNumber(self):
        """Get the atomic number."""
        return self.Z

    def GetChemicalSymbol(self):
        """Get the chemical symbol."""
        return self.symbol

    def GetMass(self):
        """Get mass."""
        return self.mass

    def GetLabel(self):
        """Get label."""
        return self.label

    def SetLabel(self,label):
        """Set label."""
        self.label = label

    def GetGhostCharacter(self):
        """Is it a ghost species?"""
        return self.ghost

    def SetGhostCharacter(self,value):
        """Set flag to determine whether is a ghost species or not"""
        self.ghost = value

    def GenerateBasis(self,optionstr,psfile):
        """ Generates basis set (actually, .ion file)"""
        # create a work subdirectory
        dir = ",basis"
        if os.path.isdir(dir): # does dir exist? 
         shutil.rmtree(dir) # yes, remove old directory 
        os.mkdir(dir) # make dir directory 
        os.chdir(dir) # move to dir
        f = open("input.fdf","w")
        f.write("NumberOfSpecies 1\n")
        f.write("%block ChemicalSpeciesLabel\n")
        if self.ghost:
          f.write("%3i %5i %s\n" % (1, -self.Z, self.label))
	else:
          f.write("%3i %5i %s\n" % (1,  self.Z, self.label))
        f.write("%endblock ChemicalSpeciesLabel\n")

        if optionstr is not None: f.write(optionstr+ "\n")
        f.close()
        
        os.system("cp ../" + psfile + " ./" + self.label + ".psf")
        os.system("gen-basis < input.fdf > OUT")
        os.system("cp " + self.label +".ion ..")
        os.chdir("..")

class Hybrid(Species):

    """Hybrid object for Siesta. Must include label
       and valence ground state information
    """

    def __init__(self, label, valence_gs, mass=None):
      """Hybrid(label,valence_gs [,mass]) -> hybrid object."""

      self.ghost = False
      self.label = label
      self.mass = mass
      self.Z = 200
      self.symbol ="X"
      self.valence_gs = valence_gs

      for n in valence_gs[0]:
         if n <= 0: raise RuntimeError, "n quantum number must be > 0"
      total_charge = 0.0
      occup_list = valence_gs[1]
      for i in range(len(occup_list)):
         total_charge = total_charge + occup_list[i]
      self.Znuc = total_charge

    def __str__(self):
        print "Hybrid species " + self.label

    def GetValenceGS(self):
        """Get the valence ground state config"""
        return self.valence_gs

    
#-----------------------------------------------------------------

class Atom(ASE.Atom):

    """Atom object for Siesta. Includes label, 
       and maybe other attributes such as
          valence ground state information
          ghost character
    """

    def __init__(self, species, position=(0, 0, 0),
                 tag=0,
                 momentum=None, velocity=None,
                 magmom=0.0):
    
        """Atom(symbol, position, ...) -> atom object."""

        self.species = species
	self.label = species.GetLabel()
        self.symbol = species.GetChemicalSymbol()
        self.Z = species.GetAtomicNumber()
        self.mass = species.GetMass()

	# This section lifted from the init method of ASE/Atom.py::Atom
        #---
        self.loa = _dummy_list_of_atoms
        self.SetCartesianPosition(position)
        self.SetMagneticMoment(magmom)
        self.SetTag(tag)

        if momentum is None:
            if velocity is None:
                self.SetCartesianMomentum((0, 0, 0))
            else:
                self.SetCartesianVelocity(velocity)
        else:
            if velocity is not None:
                raise ValueError, "You can't set both momentum and velocity!"
            self.SetCartesianMomentum(momentum)
        #---
        
    def __repr__(self):
        return "Atom('%s', %s)" % (self.label, tuple(self.position))

    def __cmp__(self, other):
        #raise RuntimeError, "attempt to compare Siesta atoms"
        return cmp(self.species, other.species)

    def Copy(self):
        """ Return an exact copy of this atom"""
        return Atom(species=self.species, position=self.position, 
                    tag=self.tag, momentum=self.momentum, magmom=self.magmom)
      
    def Transmutate(self,new_species):
        """ Return a copy of this atom transmutated into a different species"""
        return Atom(species=new_species, position=self.position, 
                    tag=self.tag, momentum=self.momentum, magmom=self.magmom)
      
    def GetLabel(self):
        """Get label."""
        return self.label

    def GetSpecies(self):
        """Get species."""
        return self.species


#---------------------------------
class Structure(ASE.ListOfAtoms):

    """ListOfAtoms object for Siesta. 
       Includes support for species handling and structure fdf generation
    """
    
    def SetMasses(self):
       raise RuntimeError, "SetMasses not implemented for Siesta Structure"
    def SetAtomicNumbers(self):
       raise RuntimeError, "SetMasses not implemented for Siesta Structure"
    def SetMasses(self):
       raise RuntimeError, "SetMasses not implemented for Siesta Structure"


    def GetListOfSpecies(self):
       label2specindex = {}
       spec = {}
       ispec = 0
       for atom in self:
         name = atom.GetLabel()
	 if not label2specindex.has_key(name):
           ispec = ispec + 1
           label2specindex[name] = ispec
           spec[ispec] = atom.GetSpecies()
       return spec, label2specindex

    def write_in_fdf_form(self,f):

       """ Create the species and structural part in fdf form,
	   and dump it to the file provided
       """

       f.write("#\n# -- Structure \n#\n")

       speclist, label2specindex = self.GetListOfSpecies()

       f.write("NumberOfSpecies %3i\n" % len(speclist))
       f.write("%block ChemicalSpeciesLabel\n")
       hyb_index = 200
       there_are_hybrids = 0
       for i in speclist.keys():    # Could sort by index...
          species = speclist[i]
          label = species.GetLabel()
          z = species.GetAtomicNumber()
          is_ghost =  species.GetGhostCharacter()
          if z == 200:
                 there_are_hybrids = 1
                 hyb_index = hyb_index + 1
                 z = hyb_index
          if is_ghost: z = -z
          f.write("%3i %5i %4s\n" % (i, z, label))
       f.write("%endblock ChemicalSpeciesLabel\n")

       if there_are_hybrids == 1:
         f.write("%block SyntheticAtoms\n")
         for i in speclist.keys():
          species = speclist[i]
          z = species.GetAtomicNumber()
          if z == 200:
               valgs  = species.GetValenceGS()
               f.write("%3i\n" % (i,))
               for j in valgs[0]:
                 f.write("%3i" % j )
               f.write("\n")
               for j in valgs[1]:
                 f.write("%12.8f" % j )
               f.write("\n")
         f.write("%endblock SyntheticAtoms\n")


       # see if we have periodic  boundary conditions
       bc = self.GetBoundaryConditions()
       if (bc[0] or bc[1] or bc[2]):
         ucell = self.GetUnitCell()
         f.write("LatticeConstant 1.0 Ang\n")
         f.write("%block LatticeVectors\n")
	 for i in range(3):
           for j in range(3):
             f.write("%15.8f" % ucell[i,j])
           f.write("\n")
         f.write("%endblock LatticeVectors\n")

       f.write("NumberOfAtoms")
       f.write("%5i\n" % len(self))
       f.write("AtomicCoordinatesFormat Ang\n")
       f.write("%block AtomicCoordinatesAndAtomicSpecies\n")

       for atom in self:
         label = atom.GetLabel()
         spec = label2specindex[label]
         xyz = atom.GetCartesianPosition()
         for j in range(3):
            f.write("%15.8f" % xyz[j])
         f.write("%3i\n" % spec)
       f.write("%endblock AtomicCoordinatesAndAtomicSpecies\n")

if __name__=="__main__":

  print """  Examples:

  H = Species("H",label="H_surf")
  O = Species("O",label="O_bulk")
  ON = Species(Z=0,label="ON-0.50000",valence_gs=[[2,2],[1.0,3.5]], mass=4.6)

  a = Atom(H,position=(0.4,0.1,0.2))
  b = Atom(O,(0.,0.,0.5))
  c = Atom(ON)
  cryst = Structure([a,b,c])
  """

  H = Species("H",label="H_surf")
  O = Species("O",label="O_bulk")
  O_ghost = Species("O",label="O_ghost")
  O_ghost.SetGhostCharacter(True)
  ON = Hybrid(label="ON-0.50000",valence_gs=[[2,2],[1.0,3.5]], mass=4.6)

  basis_options =  """
       PAO.BasisSize DZP
       PAO.EnergyShift 0.001 Ry
       PAO.SoftDefault T
     """
##  O.GenerateBasis(basis_options,"O.psf")
  
  a = Atom(H,position=(0.4,0.1,0.2))
  b = Atom(O,(0.,0.,0.5))
  c = Atom(ON)
  d = Atom(O_ghost, (-1.0,0.3,0.6))
  cryst = Structure([a,b,c,d])

  cryst.GetListOfSpecies()
  
  print cryst
  import sys
  cryst.write_in_fdf_form(sys.stdout)







