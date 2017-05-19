from Siesta.ASEInterface import Atom, Structure

from  math import cos, sin, sqrt, pi
import Numeric as N

#
def Read_USPEX(filename):
    """Return "Structure" object read from USPEX CEL-file.
     """
    f = open(filename)
#
#   First read unit cell
#
    tokens = f.readline().split()
    if tokens[0] != "cell": 
      print "Format mismatch -- cell line"
      sys.exit(1)

    cell = N.zeros((3,3),N.Float)

    a, b, c, alpha, beta, gamma = map(float,tokens[1:])
    alpha, beta, gamma = map(lambda x: x*pi/180.0, (alpha,beta,gamma))
    va = N.array((a,0.0,0.0),N.Float)
    vb = N.array((b*cos(gamma), b*sin(gamma), 0.0),N.Float)
    xxx = (cos(alpha)-cos(beta)*cos(gamma)) / sin(gamma)
    vc = N.array((c*cos(beta), c*xxx, c*sqrt(sin(beta)**2 - xxx**2)),N.Float)

    cell[0,:] = va[:]
    cell[1,:] = vb[:]
    cell[2,:] = vc[:]

#
#   Now the atoms
#
    tokens = f.readline().split()
    if tokens[0] != "natom": 
      print "Format mismatch -- natom line"
      sys.exit(1)
    natoms = int(tokens[1])

    crystal = Structure([])
    import re
    p = re.compile("[A-z]+")
    for a in range(natoms):
       tokens = f.readline().split()
       tag, z , x, y, z = tokens
       m = p.match(tag)
       if m:
         symbol = m.group()
       else:
         print "Cannot match ", tag  
       crystal.append(Atom(symbol, [float(x), float(y), float(z)]))

    crystal.SetUnitCell(cell)
    crystal.SetBoundaryConditions(periodic=True)

    return crystal
#

if __name__=="__main__":

  cryst = Read_USPEX("test.cel")

  print cryst
  import sys
  specs = cryst.GetSpeciesNumbers()
  cryst.write_in_fdf_form(sys.stdout)
