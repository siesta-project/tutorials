#!/usr/bin/env python
'''
Collection of equations of state E(V) for solids

typical usage:

from ASE.Utilities.EquationOfState import *

yourlistofatoms = [a long list of ListOfAtoms from various calculations of a unit cell at different volumes]

volumes = [atoms.GetUnitCellVolume() for atoms in yourlistofatoms]
energies = [atoms.GetPotentialEnergy() for atoms in yourlistofatoms]
eos = EquationOfState('Murnaghan',volumes,energies)

print eos         # print the minimum volume, energy, bulk modulus and pressure
g = eos.GetPlot() # pop up a gnuplot window of the rawdata and fit
            
eos.SavePlot('murn.png') #save the figure as a png

print eos.GetPressure(somevolume)
print eos.GetBulkModulus(somevolume)
print eos.GetEnergy(somevolume)

#wondering where the equation came from?
print eos.GetReference()

I would encourage you to cite the papers for the equations of state used
if you publish results from this module.
        
John Kitchin <jkitchin@andrew.cmu.edu>
05/20/05
'''

import os
from Scientific.Functions.LeastSquares import *
from Scientific.Functions.Derivatives import DerivVar
from Numeric import *

class EquationOfState:
    def __init__(self,eos='Murnaghan',volumes=[],energies=[]):
        '''
        EOS is a string that gives the name of the equation of state to use
        Murnaghan
        Birch
        BirchMurnaghan
        Vinet
        PoirerTarantola
        AntonSchmidt
        Taylor

        volumes should be a list of volumes of the unit cell
        energies should be a list of corresponding energies
        '''

        self.eVA3ToGPA = 160.21773
        self.eos_string = eos
        self.eos = eval('self.%s' % eos)
        self.volumes = volumes
        self.energies = energies

        self.references = {'Murnaghan':'PRB 28, 5480 (1983)',
                           'Birch':'Intermetallic compounds: Principles and Practice, Vol I: Principles. pages 195-210',
                           'BirchMurnaghan':'PRB 70, 224107',
                           'PourierTrantola':'PRB 70, 224107',
                           'Vinet':'PRB 70, 224107',
                           'AntonSchmidt':'Intermetallics 11, 23-32 (2003)',
                           'Taylor':'You can derive this yourself'}

    def __str__(self):
        '''
        print summary of equation of state fit
        '''
        try:
            self.eos_parameters
        except:
            self.GetParameters()
        s = '%s: %s\n' % (self.eos_string,self.GetReference())
        s += 'V0(A^3)       B(Gpa)   E0 (eV)    pressure(GPa) \n'
        s +=' %1.2f        %1.2f     %1.4f       %1.2f\n' % (self.V0,
                                                             self.B,
                                                             self.E0,
                                                             self.P)
        s += 'chisq = %1.4f' % self.chisq
        return s

    def GetReference(self):
        '''returns literature reference of equation of state

        note: it is the reference where the equation came from
        not necessarily the original source
        '''
        return self.references.get(self.eos_string)
    
    def GetParameters(self):
        # first fit a parabola to the data to provide initial guesses
        # for the equation of state fitting
        # the parabola equation is E(V) = a + b*V + c*V^2
        parabola_parameters,chisq = leastSquaresFit(self.parabola,
                                                    parameters=[min(self.energies),1,1],
                                                    data=zip(self.volumes,self.energies))

        ## Here I just make sure the minimum is bracketed by the volumes
        ## this if for the solver
        minvol = min(self.volumes)
        maxvol = max(self.volumes)

        # the minimum of the parabola is at dE/dV = 0, or 2*c V +b =0
        c = parabola_parameters[2]
        b = parabola_parameters[1]
        parabola_min = -b/2/c

        if not (minvol < parabola_min and parabola_min < maxvol):
            print 'Warning the true minimum volume is not in your volumes'

        # evaluate the parabola at the minimum to estimate the groundstate energy
        E0 = self.parabola(parabola_parameters,parabola_min)
        # estimate the bulk modulus from Vo*E''.  E'' = 2*c
        B0 = 2*c*parabola_min

        if self.eos_string == 'AntonSchmidt':
            BP = -2 #see pg 451 in the reference
        else:
            # B' is usually a small number like 4
            BP = 4
        # get initial guesses from parabola fit
        initial_guess = [E0, B0, BP, parabola_min]

        # now fit the equation of state
        self.eos_parameters,self.chisq = leastSquaresFit(self.eos,
                                                         initial_guess,
                                                         data=zip(self.volumes,self.energies))

        # self.eos_parameters[3] is always the minimum volume in these EOS
        self.V0 = self.eos_parameters[3]
        self.E0 = self.GetEnergy()
        self.B = self.GetBulkModulus()
        self.P = self.GetPressure()

        return self.eos_parameters
 
    
    def parabola(self,parameters,x):
        '''
        parabola polynomial function

        this function is used to fit the data to get good guesses for
        the equation of state fits

        a 4th order polynomial fit to get good guesses for
        was not a good idea because for crappy data it is wiggly
        2nd order seems to be sufficient.'''
        a=parameters[0]
        b=parameters[1]
        c=parameters[2]

        return a + b*x + c*x**2
       

    ############### Equation of state definitions #############

    def Murnaghan(self,parameters,vol):
        'From PRB 28,5480 (1983'
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]

        E = E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1)+1) - V0*B0/(BP-1)

        return E

    def Birch(self,parameters,V):
        '''
        From Intermetallic compounds: Principles and Practice, Vol. I: Princples
        Chapter 9 pages 195-210 by M. Mehl. B. Klein, D. Papaconstantopoulos
        paper downloaded from Web

        case where n=0
        '''
        E0=parameters[0]
        B0=parameters[1]
        BP=parameters[2]
        V0=parameters[3]

        E = (E0
             + 9.0/8.0*B0*V0*((V0/V)**(2.0/3.0) - 1.0)**2
             + 9.0/16.0*B0*V0*(BP-4.)*((V0/V)**(2.0/3.0) - 1.0)**3)

        return E

    def BirchMurnaghan(self,parameters,vol):
        'BirchMurnaghan equation from PRB 70, 224107'
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]

        eta = (vol/V0)**(1./3.)
        E = E0 + 9.*B0*V0/16.*(eta**2-1)**2*(6 + BP*(eta**2-1.) - 4.*eta**2)
                                            
        return E

    def PourierTarantola(self,parameters,vol):
        'Pourier-Tarantola equation from PRB 70, 224107'
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]

        eta = (vol/V0)**(1./3.)
        squiggle = -3.*log(eta)

        E = E0 + B0*V0*squiggle**2/6.*(3. + squiggle*(BP - 2))
                                            
        return E

    def Vinet(self,parameters,vol):
        'Vinet equation from PRB 70, 224107'
        E0 = parameters[0]
        B0 = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]

        eta = (vol/V0)**(1./3.)

        E = (E0 + 2.*B0*V0/(BP-1.)**2
             * (2. - (5. +3.*BP*(eta-1.)-3.*eta)*exp(-3.*(BP-1.)*(eta-1.)/2.)))
                                            
        return E

    def Taylor(self,parameters,vol):
        'Taylor Expansion up to 3rd order'
        E0 = parameters[0]
        beta = parameters[1]
        alpha = parameters[2]
        V0 = parameters[3]

        E = E0 + beta/2.*(vol-V0)**2/V0 + alpha/6.*(vol-V0)**3/V0
                                            
        return E
    
    def AntonSchmidt(self,parameters,vol):
        '''From Intermetallics 11, 23-32 (2003)

        Einf should be E_infinity, i.e. infinite separation, but
        according to the paper it does not provide a good estimate
        of the cohesive energy. They derive this equation from an
        empirical formula for the volume dependence of pressure,

        E(vol) = E_inf + int(P dV) from V=vol to V=infinity

        but the equation breaks down at large volumes, so E_inf
        is not that meaningful

        n should be in the range of -2 according to the paper.

        I find this equation does not fit volumetric data as well
        as the other equtions do.
        '''
        Einf = parameters[0]
        B = parameters[1]
        n = parameters[2]
        V0 = parameters[3]

        E = B*V0/(n+1.) * (vol/V0)**(n+1.)*(log(vol/V0)-(1./(n+1.))) + Einf
                                            
        return E

    def jrk(self,parameters,vol):
        '''
        derived from original murnaghan paper, Proc. Nat. Acad. Sci.
        vol. 30, 244-247, 1944.

        Equation differs from the Murnaghan equation above by a constant
        term, which I do not know how the authors of that reference arrived
        at.
        
        '''
        E0 = parameters[0]
        B = parameters[1]
        BP = parameters[2]
        V0 = parameters[3]

        E = B/BP*vol*(1+(V0/vol)**(BP)/(BP-1)) + E0
        return E

    #############################################################
    def GetV0(self):
        return self.V0
    
    def GetEnergy(self,vol=None):
        'calculate the energy at a volume for the equation of state. E(V)'
        try:
            self.eos_parameters
        except:
            self.GetParameters()

        if vol is None:
            vol = self.V0
            
        return self.eos(self.eos_parameters,vol)
    
    def GetPressure(self,V=None):
        '''calculate the pressure numerically at a volume: P = -dE/dV'''
        try:
            self.eos_parameters
        except:
            self.GetParameters()

        if V is None:
            V = self.V0
            
        v = DerivVar(V,0,1) #first derivative of variable 0 (vol)

        x = self.GetEnergy(v) 
        
        return -x[1][0] * self.eVA3ToGPA

    def GetBulkModulus(self,V=None):
        '''determines bulk modulus mumerically: B = V d^2E/dV^2
        
        minimum volume is used by default '''
        try:
            self.eos_parameters
        except:
            self.GetParameters()
            
        if V is None:
            V = self.V0

        v = DerivVar(V,0,2) #second derivative of variable 0 (vol)
        x= self.GetEnergy(v) 
        return V * x[2][0][0] * self.eVA3ToGPA
        
    def GetPlot(self):
        '''
        generates a gnuplot figure of the volume, energies and fit

        '''
        try:
            self.eos_parameters
        except:
            self.GetParameters()

        xdata = arange(min(self.volumes),max(self.volumes),0.01)
        ydata = [self.eos(self.eos_parameters,x) for x in xdata]

        import Gnuplot
        g = Gnuplot.Gnuplot(persist=1)
        g.xlabel('Volume (A^3)')
        g.ylabel('Energy (eV)')
        
        rawdata = Gnuplot.Data(self.volumes,self.energies,
                               title='Raw data',
                               with='points 3 3')
        fitdata = Gnuplot.Data(xdata,ydata,
                               title='%s fit' % self.eos_string,
                               with='lines')

        # x is 1/3 between minvol and max vol
        x = min(self.volumes) + (max(self.volumes)-min(self.volumes))/3
        # for y i will divide the vertical range into 10 divisions
        erange = max(self.energies) - min(self.energies)

        s ='V0 = %1.2f A^3' % self.V0
        g('set label 1 "%s" at  %f,%f left' % (s,x,max(self.energies)-erange/10.))
        
        s ='E0 = %1.4f eV' % self.E0
        g('set label 2 "%s" at  %f,%f left' % (s,x,max(self.energies)-2.*erange/10.))
        
        s = 'B(V0) = %1.0f GPa' % self.B
        g('set label 3 "%s" at  %f,%f left' % (s,x,max(self.energies)-3*erange/10.))
        
        s = 'P(V0) = %1.2f GPa' % self.P
        g('set label 4 "%s" at  %f,%f left' % (s,x,max(self.energies)-4*erange/10.))        
        
        g.plot(rawdata,fitdata)

        self.plot = g

        return self.plot

    def SavePlot(self,file=None):
        '''
        save the plot in a graphics file determined by the extension of the file
        '''

        try:
            self.plot
        except:
            self.GetPlot()

        if file is None:
            file = '%s.png' % self.eos_string

        base,ext = os.path.splitext(file)
            
        if ext == '.png':
            dev = 'png'
        elif ext == '.tex':
            dev = 'latex'
        # pdf apparently not installed in my gnuplot
        elif ext == '.pdf':
            dev = 'pdf'
        elif ext == '.epslatex':
            dev = 'epslatex color dashed "default" 12'
        elif ext == '.eps':
            dev = 'postscript eps enhanced color'
            
        self.plot('set terminal %s' % dev)
        self.plot('set output "%s"' % file)
        self.plot.replot()
            
