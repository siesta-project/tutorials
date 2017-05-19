"""A Siesta Calculator.

"""

import Numeric as num
from ASE.Calculators.Calculator import Calculator
from  siesta_efs import Siesta_efs

class SiestaCalculator(Calculator,Siesta_efs):
    """A Siesta Server Calculator."""
    
    def __init__(self,executable=None):

	Siesta_efs.__init__(self,executable)
        self.ready = False

    def GetPotentialEnergy(self):
        """Return the energy for the current state of the ListOfAtoms."""
        self.UpdateEnergyAndForces()
        return self.energy 

    def GetCartesianForces(self):
        """Return the forces for the current state of the ListOfAtoms."""
        self.UpdateEnergyAndForces()
        return self.forces 
      
    def GetStress(self):
        """Return the stress for the current state of the ListOfAtoms."""
        self.UpdateEnergyAndForces()
        return self.stress

    def UpdateEnergyAndForces(self):
        atoms = self.GetListOfAtoms()
        if not self.ready:
            self.Initialize()
            self.Calculate()
	elif  atoms.GetAtomicNumbers() != self.numbers:
            self.Calculate()
        elif (atoms.GetCartesianPositions() != self.positions or
              atoms.GetUnitCell() != self.cell or
              atoms.GetBoundaryConditions() != self.bc):
            self.Calculate()

    def Initialize(self):
        self.cell = None
        self.positions = None
        self.numbers = None
        self.bc = None

        # Ready for action!
        self.ready = True
                
    def Calculate(self):
        """Calculate everything."""
        atoms = self.GetListOfAtoms()
        self.energy, self.forces, self.stress = Siesta_efs.run(self,atoms)

        self.cell = atoms.GetUnitCell()
        self.positions = atoms.GetCartesianPositions()
        self.numbers = atoms.GetAtomicNumbers()
        self.bc = atoms.GetBoundaryConditions()

        


