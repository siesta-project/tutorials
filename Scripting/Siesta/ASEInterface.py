"""
Extend the ASE classes to provide Siesta-specific functionality
"""

import ASE.Atom
import ASE.ListOfAtoms

import math
import Numeric

#-------------------
class Atom(ASE.Atom):

    """Atom object for Siesta. Includes label
       and valence ground state information
    """

    def __init__(self, symbol=None, position=(0, 0, 0),
                 Z=None, mass=None, tag=0,
                 momentum=None, velocity=None,
                 magmom=0.0, label=None, valence_gs=None):
        """Atom(symbol, position, ...) -> atom object."""
	ASE.Atom.__init__(self, symbol, position,
                 Z, mass, tag, momentum, velocity,
                 magmom)

        if label is None: 
          self.label = self.symbol
        else:
          self.label = label

        if valence_gs is None: 
          self.valence_gs = []
        else:
          self.valence_gs = valence_gs

    def GetLabel(self):
        """Get label."""
        return self.label

    def SetLabel(self,label):
        """Set label."""
        self.label = label

#---------------------------------
class Structure(ASE.ListOfAtoms):

    """ListOfAtoms object for Siesta. 
       For future expansion
    """

    def __init__(self, atoms=[], cell=None, periodic=None, angle=None):
      ASE.ListOfAtoms.__init__(self, atoms, cell, periodic, angle)

    def compute_species(self):
       """ Compute a species dictionary """     
       hybrid_number = 201
       there_are_hybrids = 0
       species = {}
       hybrids = {}
       ispec = 0
       for atom in self:
         name = atom.GetLabel()
         z = atom.GetAtomicNumber()
	 if not species.has_key(name):
           ispec = ispec + 1
           if z == 0:
             z = hybrid_number
             hybrid_number = hybrid_number + 1
             there_are_hybrids = 1
             hybrids[name] = [z,atom.valence_gs]
           species[name] = [ispec, z]
       return species

    def GetSpeciesNumbers(self):
        species = self.compute_species()
        l = []
        for atom in self:
            name = atom.GetLabel()
            spec = species[name][0]
            l.append(spec)
        return l

    def GetSpecies(self):
        species = self.compute_species()
        return species.keys()
        
    def write_in_fdf_form(self,f):

       """ Create the species and structural part in fdf form,
	   and dump it to the file provided
       """

       f.write("#\n# -- Structure \n#\n")
       hybrid_number = 201
       there_are_hybrids = 0
       species = {}
       hybrids = {}
       ispec = 0
       for atom in self:
         name = atom.GetLabel()
         z = atom.GetAtomicNumber()
	 if not species.has_key(name):
           ispec = ispec + 1
           if z == 0:
             z = hybrid_number
             hybrid_number = hybrid_number + 1
             there_are_hybrids = 1
             hybrids[name] = [z,atom.valence_gs]
           species[name] = [ispec, z]
	
       f.write("NumberOfSpecies")
       f.write("%3i\n" % len(species))
       f.write("%block ChemicalSpeciesLabel\n")
       for i in species.keys():
          ispec, z = species[i]
          f.write("%3i %3i %4s\n" % (ispec, z, i))
       f.write("%endblock ChemicalSpeciesLabel\n")

       if there_are_hybrids == 1:
         f.write("%block SyntheticAtoms\n")
         for i in species.keys():
            ispec, z = species[i]
	    if z > 200:
               zdum, valgs  = hybrids[i]
               f.write("%3i\n" % (ispec,))
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
         name = atom.GetLabel()
         spec = species[name][0]
         xyz = atom.GetCartesianPosition()
         for j in range(3):
            f.write("%15.8f" % xyz[j])
         f.write("%3i\n" % spec)
       f.write("%endblock AtomicCoordinatesAndAtomicSpecies\n")

    def write_in_cif_form(self,f):
	cell = self.GetUnitCell()
        va = cell[0,:]
        vb = cell[1,:]
        vc = cell[2,:]
        rtodeg = 180./math.pi
        ma = math.sqrt(Numeric.dot(va,va))
        mb = math.sqrt(Numeric.dot(vb,vb))
        mc = math.sqrt(Numeric.dot(vc,vc))
        alpha = rtodeg*math.acos(Numeric.dot(vb,vc)/(mb*mc))
        beta = rtodeg*math.acos(Numeric.dot(va,vc)/(ma*mc))
        gamma = rtodeg*math.acos(Numeric.dot(va,vb)/(ma*mb))

        print "data_C3D_block\n"

        print "_cell_length_a ", ma
        print "_cell_length_b ", mb
        print "_cell_length_c ", mc
        print "_cell_angle_alpha ", alpha
        print "_cell_angle_beta ", beta
        print "_cell_angle_gamma ", gamma
	#
	# We will use P1 as we do not assume any symmetry
	#

	print """
	_symmetry_space_group_name_H-M 'P 1'
	_symmetry_Int_Tables_number    '1'

        loop_
        _symmetry_equiv_pos_site_id
        _symmetry_equiv_pos_as_xyz
        1     'x, y, z'

        loop_
        _atom_site_label
        _atom_site_type_symbol
        _atom_site_fract_x
        _atom_site_fract_y
        _atom_site_fract_z
        """

	#
	#   Now the atoms
	#   First, re-scale the cell to convert to
	#   fractional coordinates

	xyzcell=[(1, 0, 0), (0, 1, 0), (0, 0, 1)]
	self.SetUnitCell(xyzcell)
	for atom in self:
           xyz = atom.position
           print atom.label, atom.symbol, xyz[0], xyz[1], xyz[2]

    def write_in_cssr_form(self,f):
	cell = self.GetUnitCell()
        va = cell[0,:]
        vb = cell[1,:]
        vc = cell[2,:]
        rtodeg = 180./math.pi
        ma = math.sqrt(Numeric.dot(va,va))
        mb = math.sqrt(Numeric.dot(vb,vb))
        mc = math.sqrt(Numeric.dot(vc,vc))
        alpha = rtodeg*math.acos(Numeric.dot(vb,vc)/(mb*mc))
        beta = rtodeg*math.acos(Numeric.dot(va,vc)/(ma*mc))
        gamma = rtodeg*math.acos(Numeric.dot(va,vb)/(ma*mb))

        f.write("   %15.4f%15.4f%15.4f\n"  % ( ma, mb, mc))
        f.write("   %15.4f%15.4f%15.4f %s\n"  \
                     % ( alpha, beta, gamma, "SPGR =1  P 1"))
        ##print alpha, beta, gamma, "SPGR =1  P  1"

        f.write(" %10i %3i %s \n" % (len(self), 0, " Insert title here"))
        f.write(" some title\n")

	#
	#   Now the atoms
	#   First, re-scale the cell to convert to
	#   fractional coordinates
        def filter_small(x):
            y = x
            if (abs(x) < 1.e-10): y = 0.0
            return y

	xyzcell=[(1, 0, 0), (0, 1, 0), (0, 0, 1)]
	self.SetUnitCell(xyzcell)
	for i in range(len(self)):
	   atom = self[i]
           xyz_raw = atom.position
           xyz = map(filter_small,xyz_raw)
           f.write(" %10i %s %12.7f%12.7f%12.7f  0 0 0 0 0 0 0 0 0.000 \n" % \
                         (i+1, atom.symbol, xyz[0], xyz[1], xyz[2]))

    def plot_rasmol(self,repeat=(1,1,1)):
        from ASE.Visualization.RasMol import RasMol
        plot = RasMol(self,repeat)

    def plot_jmol(self,repeat=(1,1,1)):
	from ASE.IO.PDB import WritePDB
        import os
        new = self.Repeat(repeat)
 	pdbfile = "tmp.pdb"
	WritePDB(pdbfile,atoms=new)
	os.system("jmol.sh " + pdbfile)


if __name__=="__main__":

  a = Atom("H",label="H_surf",position=(0.4,0.1,0.2))
  b = Atom("O",(0.,0.,0.5),label="O_bulk")
  c = Atom(Z=0,label="ON-0.50000",valence_gs=[[0,2],[1,3.5]])
  cryst = Structure([a,b,c])

  print cryst
  import sys
  specs = cryst.GetSpeciesNumbers()
  print  cryst.GetSpecies()
  cryst.write_in_fdf_form(sys.stdout)
  cryst.write_in_cif_form(sys.stdout)
  cryst.write_in_cssr_form(sys.stdout)







