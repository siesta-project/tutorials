#
import math
import Numeric as N

from read_struct import *

def struct_file_to_object(fname,species_names):
  """
     Accepts a file name and a list of species labels,
     and reads the information if a ".STRUCT_OUT" file
     from Siesta to create a Structure object
     The units of the Siesta file are Angs.
  """

  species_map = { }
  for i in range(len(species_names)):
    species_map [str(i+1)] = species_names[i]

  print species_map
  a=ReadStruct(fname, species_map)

  return a

def set_velocities_from_XV(fname,crystal):
  """ Updates the velocities in Structure object a
      with information from a XV file
  """

  # Unit handling: Siesta XV file uses v units
  # based on femtosecond for time and bohr for length
  # To convert to simulation units (eV,amu,Ang), we
  # need this

  time_factor = 10.1806    # unit of time in femtoseconds
  femto_second = 1.0 / time_factor
  bohr = 0.52918
  siesta_v_unit = bohr/femto_second
  
  print "Reading velocities from file ", fname
  print "Using siesta_v_unit (bohr/femtosecond): ", siesta_v_unit

  f = open(fname,"r")
  #
  #   First read unit cell velocity
  #

  vcell = []
  for i in range(3):
    vector = f.readline()
    x, y, z, vx, vy, vz = vector.split()
    vcell.append([ float(vx), float(vy), float(vz) ])
    
  #
  #   Now the atoms
  #
  #   Assume unbroken lines
  
  natoms = int(f.readline())
  if natoms != len(crystal):
    print "Number of atoms mismatch"
    sys.exit(1)

  #   ... and extract the information for each atom in turn
  #
  va = N.zeros((natoms,3),N.Float)
    
  for i in range(natoms):
    line = f.readline()
    l = line.split()
    # This is needed due to some brain damage in list handling
    #  species, z, x, y, z, vx, vy, vz
    z = int(l[1])
    vx = float(l[5])
    vy = float(l[6])
    vz = float(l[7])

    ##print "vx, vy, vz in file: ", vx, vy, vz

    if z != crystal[i].GetAtomicNumber():
      print "Z mismatch ", z, crystal[i].GetAtomicNumber()
      sys.exit(1)
      
    va[i,0] = vx
    va[i,1] = vy
    va[i,2] = vz

  crystal.SetCartesianVelocities(va*siesta_v_unit)
  f.close()
          
  return crystal

def set_xv_from_LOG(fname,crystal,get_thermostat=False):
  """ Updates the positions and velocities in Structure object a
      with information from a section of LOG file
      The user should have prepared this section, starting
      with the --MDstep record, and followed by the --MDixv lines
      If get_thermostat is True, the values of s and vs are returned
      as a tuple (s,vs) in the attribute "thermostat" of the crystal structure.
      Otherwise (1.0, 0.0) is returned.
  """

  # Units handling: The LOG file uses simulation units
  
  print "Reading x and v from LOG file snippet in ", fname

  f = open(fname,"r")

  #   Assume unbroken lines
  
  tokens = f.readline().split()
  natoms = int(tokens[2])
  if natoms != len(crystal):
    print "Number of atoms mismatch"
    sys.exit(1)

  #   ... and extract the information for each atom in turn
  #
  xa = N.zeros((natoms,3),N.Float)
  va = N.zeros((natoms,3),N.Float)
    
  for i in range(natoms):
    line = f.readline()
    l = line.split()
    # This is needed due to some brain damage in list handling
    #  prefix, ia, y, z, vx, vy, vz
    ia = int(l[1])
    x = float(l[2])
    y = float(l[3])
    z = float(l[4])
    vx = float(l[5])
    vy = float(l[6])
    vz = float(l[7])

    ##print "vx, vy, vz in file: ", vx, vy, vz

    if ia != i+1:
      print "Atom number  mismatch ", i+1, ia
      sys.exit(1)
      
    va[i,0] = vx
    va[i,1] = vy
    va[i,2] = vz
    xa[i,0] = x
    xa[i,1] = y
    xa[i,2] = z

  crystal.SetCartesianPositions(xa)
  crystal.SetCartesianVelocities(va)

  f.close()

  if get_thermostat:
    tokens = f.readline().split()
    if tokens[0] != "--MDthermostat" :
      print "Cannot find thermostat information in LOG file "
      sys.exit(1)
      
    s = float(tokens[1])
    vs = float(tokens[2])
    crystal.thermostat = (s,vs)
  else:
    crystal.thermostat = (1.0,0.0)

  return crystal
    





