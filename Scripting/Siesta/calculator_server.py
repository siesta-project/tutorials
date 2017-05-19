"""A Siesta Calculator.

"""

import Numeric as num
from ASE.Calculators.Calculator import Calculator
from  Siesta.server import SiestaServer as Sserver

class SiestaCalculator(Calculator,Sserver):
    """A Siesta Server Calculator."""
    
    def __init__(self,executable=None):

	Sserver.__init__(self,executable)
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
            self.Initialize()
            self.Calculate()
        elif (atoms.GetCartesianPositions() != self.positions or
              atoms.GetUnitCell() != self.cell or
              atoms.GetBoundaryConditions() != self.bc):
            self.Calculate()

    def Initialize(self):
        atoms = self.GetListOfAtoms()
        Sserver.launch(self,atoms)
        # Ready for action!
        self.ready = True
                
    def Calculate(self):
        """Calculate everything."""
        atoms = self.GetListOfAtoms()
        self.energy, self.forces, self.stress = Sserver.get_forces(self,atoms)

        self.cell = atoms.GetUnitCell()
        self.positions = atoms.GetCartesianPositions()
        self.numbers = atoms.GetAtomicNumbers()
        self.bc = atoms.GetBoundaryConditions()

        


