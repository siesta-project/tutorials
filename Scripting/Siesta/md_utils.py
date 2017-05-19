"""
 Some utilities for MD runs
"""

import Numeric as N

kb = 8.61735e-5       #   eV/K

def ekin(v,ma):
    a = 0.0
    for i in range(len(ma)):
       a = a + ma[i] * ( v[i,0]**2 + v[i,1]**2 + v[i,2]**2 )
    return 0.5*a

def temp_from_ekin(kinetic_energy,ndf):
    return 2.0*kinetic_energy / ( ndf*kb)

def v_cm(va,ma):
  # Center of mass velocity
  mtot = N.sum(ma)
  pcm = N.zeros(3,N.Float)
  for xyz in range(3):
     pcm[xyz] = N.sum(ma[:]*va[:,xyz])
  return pcm/mtot

def init_velocities(T,ma,ndf=None):
    
  # Simple equipartition, no Maxwell-Boltzmann
  # For Maxwell-Boltzmann, use RandomArray.standard_normal()
  import RandomArray
  v = RandomArray.random((len(ma),3)) - 0.5

  # Make the C.M. static
  vcm = v_cm(v,ma)
  for xyz in range(3):
     v[:,xyz] =  v[:,xyz] - vcm[xyz]

  # Re-scale for correct kinetic energy
  kin = ekin(v,ma)
  # This will take into account the reduced no of degrees of freedom
  if ndf is None:
      ndf = 3*len(ma) - 3
  temp = temp_from_ekin(kin,ndf)
  v = v * math.sqrt(T/temp)

  return v   

