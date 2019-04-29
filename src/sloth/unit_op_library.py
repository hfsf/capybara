# unit_op_library.py

"""
Define Models of some unit operations to be used in the model declaration
"""

from . import model
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *

class MaterialStream(model.Model):

    """
    Model for a simple material stream (homogeneous)

    *INPUTS: -
    *OUTPUTS: (Parameters are directly referenced)
    *PARAMETERS: mdot, ndot, P, H, T

    *REQUIRES: PropertyPackage
    """

    def __init__(self, name, description="Material stream", property_package=None):

        super().__init__(name, description, property_package)

        self.mdot = self.createParameter("mdot", kg/s, "Mass flux for stream")
        self.ndot = self.createParameter("ndot", mol/s, "Molar flux for stream")
        self.P = self.createParameter("P", Pa, "Pressure for stream")
        self.H = self.createParameter("H", J/mol, "Molar enthalpy for stream")
        self.T = self.createParameter("T", K, "Temperature for stream")

        #self.mdot_out = self.createVariable("mdot_out",kg/s, "Mass flux from stream", is_exposed=True, type="output")
        #self.ndot_out = self.createVariable("ndot_out",mol/s, "Molar flux from stream",is_exposed=True, type="output")
        #self.P_out = self.createVariable("P_out", Pa, "Pressure from stream",is_exposed=True, type="output")
        #self.H_out = self.createVariable("H_out", J/mol, "Molar enthalpy from stream",is_exposed=True, type="output")
        #self.T_out = self.createVariable("T_out", K, "Temperature from stream",is_exposed=True, type="output")

        self.ignore_equation_warning = True
        self.ignore_variable_warning = True

    def DeclareParameters(self):

        #try to set values if the property_package was defined
        if self.property_package is not None:

            if self.mdot.is_specified is True and self.ndot.is_specified is not True:

                self.ndot.setValue( self.mdot.value/(self.property_package["*"].MW*1e-3) )

            if self.mdot.is_specified is not True and self.ndot.is_specified is True:

                self.mdot.setValue( self.ndot.value*self.property_package["*"].MW*1e-3 )

        #Recalculate property_package if T and P where provided

        if self.T.is_specified is True and self.P.is_specified is False:

            self.property_package.calculate(T=self.T.value)

        if self.T.is_specified is False and self.P.is_specified is True:

            self.property_package.calculate(P=self.P.value)

        if self.T.is_specified is True and self.P.is_specified is True:

            self.property_package.calculate(T=self.T.value, P=self.P.value)

    '''
    def DeclareEquations(self):

        #Create equations for output of streams using parameter values

        self.createEquation("mass_flux", self.mdot_out.description, self.mdot_out() - self.mdot() )
        self.createEquation("molar_flux", self.ndot_out.description, self.ndot_out() - self.ndot() )
        self.createEquation("pressure_output", self.P_out.description, self.P_out() - self.P() )
        self.createEquation("enthalpy_output", self.H_out.description, self.H_out() - self.H())
        self.createEquation("temperature_output", self.T_out.description, self.T_out() - self.T())
    '''

class MultiphasicMaterialStream(model.Model):


    """
    Model for a biphasic material stream

    *INPUTS: -
    *OUTPUTS: (Parameters are directly referenced)
    *PARAMETERS: mdot, ndot, P, H, T, x_<phase1_name>, x_<phase2_name>, w_<phase1_name>, w_<phase2_name>, ..., x_<phaseN_name>, w_<phaseN_name>

    *REQUIRES: PropertyPackage[phase1, phase2, ... phaseN]
    """

    def __init__(self, name, description="Biphasic material stream", property_package=None):

        super().__init__(name, description, property_package)

        self.mdot = self.createParameter("mdot", kg/s, "Mass flux for stream")
        self.ndot = self.createParameter("ndot", mol/s, "Molar flux for stream")
        self.P = self.createParameter("P", Pa, "Pressure for stream")
        self.H = self.createParameter("H", J/mol, "Molar enthalpy for stream")
        self.T = self.createParameter("T", K, "Temperature for stream")

        for phase_i in self.property_package.phase_names:

            exec("self.x_{} = self.createParameter('x_{}',dimless,'Molar fraction for {} phase')".format(phase_i, phase_i, phase_i))
            exec("self.w_{} = self.createParameter('w_{}',dimless,'Mass fraction for {} phase')".format(phase_i, phase_i, phase_i))

            #exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))
            #exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))

        '''
        self.mdot_out = self.createVariable("mdot_out",kg/s, "Mass flux from stream", is_exposed=True, type="output")
        self.ndot_out = self.createVariable("ndot_out",mol/s, "Molar flux from stream",is_exposed=True, type="output")
        self.P_out = self.createVariable("P_out", Pa, "Pressure from stream",is_exposed=True, type="output")
        self.H_out = self.createVariable("H_out", J/mol, "Molar enthalpy from stream",is_exposed=True, type="output")
        self.T_out = self.createVariable("T_out", K, "Temperature from stream",is_exposed=True, type="output")

        for phase_i in self.property_package.phase_names:

            exec("self.createEquation('','Molar fraction for {} phase', self.x_{}_out()-self.x_{}())".format(phase_i, phase_i, phase_i, phase_i))
            exec("self.createEquation('','Mass fraction for {} phase', self.w_{}_out()-self.w_{}())".format(phase_i, phase_i, phase_i, phase_i))
        '''

        self.ignore_equation_warning = True
        self.ignore_variable_warning = True

    def DeclareParameters(self):

        #try to set values if the property_package was defined
        if self.property_package is not None:

            if self.mdot.is_specified is True and self.ndot.is_specified is False:

                self.ndot.setValue( self.mdot.value/(self.property_package["*"].MW*1e-3) )

            if self.mdot.is_specified is False and self.ndot.is_specified is True:

                self.mdot.setValue( self.ndot.value*self.property_package["*"].MW*1e-3 )

        #Recalculate property_package if T and P where provided

        if self.T.is_specified is True and self.P.is_specified is False:

            self.property_package.calculate(T=self.T.value)

        if self.T.is_specified is False and self.P.is_specified is True:

            self.property_package.calculate(P=self.P.value)

        if self.T.is_specified is True and self.P.is_specified is True:

            self.property_package.calculate(T=self.T.value, P=self.P.value)

    '''
    def DeclareEquations(self):

        #Create equations for output of streams using parameter values

        self.createEquation("mass_flux", self.mdot_out.description, self.mdot_out() - self.mdot() )
        self.createEquation("molar_flux", self.ndot_out.description, self.ndot_out() - self.ndot() )
        self.createEquation("pressure_output", self.P_out.description, self.P_out() - self.P() )
        self.createEquation("enthalpy_output", self.H_out.description, self.H_out() - self.H())
        self.createEquation("temperature_output", self.T_out.description, self.T_out() - self.T())
    '''

class Mixer(model.Model):
    """
    Model for a mixer of material streams

    If homogeneous (property_package = None or property_package has 1 phase):

    *INPUTS: ndot_in, mdot_in, H_in, P_in, T_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out, T_out
    *PARAMETERS: -

    *REQUIRES: -

    If multiphasic (property_package has 2+ phases):

    *INPUTS: ndot_in, mdot_in, H_in, P_in,  x_<phase1>_in, w_<phase1>_in, ..., x_<phaseN-1>_in, w_<phaseN-1>_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out,  x_<phase1>_out, w_<phase1>_out, ..., x_<phaseN>_out, w_<phaseN>_out
    *PARAMETERS: -

    *REQUIRES: -
    """

    def __init__(self, name, description="Mixer model", property_package=None):

        super().__init__(name, description, property_package)

        if self.property_package is not None:

            if len(self.property_package.phase_names) > 1:

                for phase_i in self.property_package.phase_names:

                    exec("self.x_{}_in = self.createVariable('x_{}_in',dimless,'Molar fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                    exec("self.w_{}_in = self.createVariable('w_{}_in',dimless,'Mass fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                    exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                    exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass consevation", _mass_conservation)

        if self.property_package.number_of_phases >=2:

            _sum_molar_frac_in = -1.
            _sum_mass_frac_in = -1.
            _sum_molar_frac_out = -1.
            _sum_mass_frac_out = -1.

            for phase_i in self.property_package.phase_names:

                _sum_molar_frac_in += eval("self.x_{}_in()".format(phase_i))
                _sum_mass_frac_in += eval("self.w_{}_in()".format(phase_i))
                _sum_molar_frac_out += eval("self.x_{}_out()".format(phase_i))
                _sum_mass_frac_out += eval("self.w_{}_out()".format(phase_i))

            self.createEquation("molar_frac_sum_in", "Molar fraction summation for input", _sum_molar_frac_in)
            self.createEquation("mass_frac_sum_in", "Mass fraction summation for input", _sum_mass_frac_in)
            self.createEquation("molar_frac_sum_out", "Molar fraction summation for output", _sum_molar_frac_out)
            self.createEquation("mass_frac_sum_out", "Mass fraction summation for output", _sum_mass_frac_out)

        #---- Multiphasic balances ----

        if self.property_package is not None:

            if len(self.property_package.phase_names) > 1:

                for phase_i in self.property_package.phase_names[:-1]:

                    #Create molar conservation for each component

                    exec("_molar_conservation_i = self.x_{}_out() - self.x_{}_in()".format(phase_i, phase_i))

                    exec("self.createEquation('molar_conservation_for_{}', 'Molar conservation for {} phase', _molar_conservation_i)".format(phase_i, phase_i))

                    #Create mass conservation for each component

                    exec("_mass_conservation_i = self.w_{}_out() - self.w_{}_in()".format(phase_i, phase_i))

                    exec("self.createEquation('mass_conservation_for_{}', 'Mass conservation for {} phase', _mass_conservation_i)".format(phase_i, phase_i))

        #------------------------------------


        self.T_in = self.createVariable("T_in", K, "Temperature for the input stream", latex_text="{T}_{in}", is_exposed=True, type='input')
        self.T_out = self.createVariable("T_out", K, "Temperature for the output stream", latex_text="{T}_{out}", is_exposed=True, type='output')

        _temperature_balance = self.T_out() - self.T_in()

        self.createEquation("thermal_equilibrium", "Thermal equilibrium", _temperature_balance)

        self.P_in = self.createVariable("P_in", Pa, "p_in", latex_text="{P}_{in}", is_exposed=True, type='input')
        self.P_out = self.createVariable("P_out", Pa, "p_out", latex_text="{P}_{out}", is_exposed=True, type='output')

        _mechanical_equilibrium = self.P_out() - self.P_in()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

        self.H_in =  self.createVariable("H_in", J/mol, "molar enthalpy for output stream", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out =  self.createVariable("H_out", J/mol, "molar enthalpy for output stream", latex_text="H_{out}", is_exposed=True, type='output')

        _energy_balance = self.ndot_out()*self.H_out() - self.ndot_in()*self.H_in()

        self.createEquation("energy_balance","Energy balance", _energy_balance)

class Splitter(Mixer):

    """
    Model for a splitter (separation in multiple streams from one initial one) of material streams
    """

    def __init__(self, name, description="Tee model", property_package=None):

        super().__init__(name, description, property_package)

class Tank(model.Model):


    def __init__(self, name, description="Tank", property_package=None, orientation='vertical'):

        """
        Defines a generic tank

        *INPUTS: ndot_in, mdot_in, h_in, P_in
        *OUTPUTS: mdot_out, mdot_out, h_out, P_out
        *PARAMETERS: area_sec, Q

        *REQUIRES: PropertyPackage
        """

        super().__init__(name, description, property_package)

        self.orientation = orientation

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("self.x_{}_in = self.createVariable('x_{}_in',dimless,'Molar fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_in = self.createVariable('w_{}_in',dimless,'Mass fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))

        self.t = self.createVariable("t",s,"time",latex_text="t")

        self.time_domain = Domain("time_domain", s, self.t, "time domain")

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        self.N = self.createVariable("N", mol, "molar holdup", latex_text="N")
        self.N.distributeOnDomain(self.time_domain)

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        self.M = self.createVariable("M", kg, "mass holdup", latex_text="M")
        self.M.distributeOnDomain(self.time_domain)

        self.H_in  = self.createVariable("H_in", J/mol, "molar enthalpy input", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "molar enthalpy output", latex_text="H_{out}", is_exposed=True, type='output')
        self.E = self.createVariable("E", J, "Internal energy", latex_text="E")

        self.Q = self.createParameter("Q", J, "Heat rate", latex_text="Q", value=0.)

        self.E.distributeOnDomain(self.time_domain)

        self.level = self.createVariable("level", m, "liquid level", latex_text="L")
        self.area_sec = self.createParameter("area_sec", m**2, "squared section area", latex_text="{A}_{sec}")

        self.level.distributeOnDomain(self.time_domain)

        self.P_In = self.createVariable("P_In", Pa, "p_in")
        self.P_Out = self.createVariable("P_Out", Pa, "p_out")


    def DeclareEquations(self):

        _molar_conservation = self.N.Diff(self.t) == self. self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        _mass_conservation = self.M.Diff(self.t) ==  self. self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        _energy_balance = self.E.Diff(self.t) == self.n_dot_in()*self.H_in() - self.n_dot_out()*self.H_out() + self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        _level_balance = self.level.Diff(self.t) == (1./(self.property_package["*"].rho*self.area_sec()))*(self.mdot_in()-self.mdot_out())

        self.createEquation("_level_balance", "Liquid level balance", _level_balance)

        _mechanical_equilibrium = self.P_In() - self.P_Out()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)


class Fermenter(Tank):

    def __init__(self, name, description="Fermenter", property_package=None):

        super().__init__(name, description, property_package)

class Valve(model.Model):
    """
    Model for a valve of material streams

    If homogeneous (property_package = None or property_package has 1 phase):

    *INPUTS: ndot_in, mdot_in, H_in, P_in, T_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out, T_out, Qdot_out
    *PARAMETERS: Delta_P, perc_open

    *REQUIRES: -

    If multiphasic (property_package has 2+ phases):

    *INPUTS: ndot_in, mdot_in, H_in, P_in,  T_in, x_<phase1>_in, w_<phase1>_in, ..., x_<phaseN>_in, w_<phaseN>_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out,  T_out, x_<phase1>_out, w_<phase1>_out, ..., x_<phaseN>_out, w_<phaseN>_out
    *PARAMETERS: -

    *REQUIRES: -
    """

    def __init__(self, name, description="Valve", property_package=None):

        super().__init__(name, description, property_package)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        self.Qdot_out = self.createVariable("Qdot_out", (m**3)/s, "volumetric output flux", latex_text="\\dot{Q}_{out}", is_exposed=True, type='output')

        self.H_in = self.createVariable("H_in", J/mol, "input molar enthalpy", latex_text="{H}_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "output molar enthalpy", latex_text="{H}_{out}", is_exposed=True, type='output')

        self.P_in = self.createVariable("P_in", Pa, "input pressure", latex_text="{P}_{in}", is_exposed=True, type='input')
        self.P_out = self.createVariable("P_out", Pa, "output pressure", latex_text="{P}_{out}", is_exposed=True, type='output')

        self.T_in = self.createVariable("T_in", K, "input stream temperature", latex_text="{T}_{in}", is_exposed=True, type='input')
        self.T_out = self.createVariable("T_out", K, "output stream temperature", latex_text="{T}_{out}", is_exposed=True, type='output')

        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")
        self.perc_open = self.createParameter("perc_open", dimless, "percentage of opening", latex_text="{\\%}_{open}")

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("self.x_{}_in = self.createVariable('x_{}_in',dimless,'Molar fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_in = self.createVariable('w_{}_in',dimless,'Mass fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))


    def DeclareEquations(self):


        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        _isoenthalpy = self.H_in()*self.ndot_in() - self.H_out()*self.ndot_out()

        self.createEquation("isoenthalpy", "isoenthalpy", _isoenthalpy)

        _mechanical_equilibrium = self.P_out() - self.P_in() + self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

        _energy_balance = self.T_out() - self.T_in()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        mix_rho = self.createParameter("mix_rho",kg/(m**3),"Density for the mixture of components")

        if self.property_package.number_of_phases>=2:

            mix_rho_ = 0.

            for phase_i in self.property_package.phase_names:

                mix_rho_ += eval("self.w_{}_out()*self.property_package['{}'].rho".format(phase_i, phase_i))

            mix_rho.setValue(mix_rho_)

        else:

            mix_rho.setValue(self.property_package["*"].rho)

        _volumetric_flux = self.Qdot_out() - self.perc_open()*(self.mdot_out()/mix_rho())

        self.createEquation("vol_flux_balance", "Volumetric flux balance", _volumetric_flux)

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("_molar_conservation_i = self.x_{}_out() - self.x_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('molar_fraction_conservation_for_{}', 'Molar conservation for {} phase', _molar_conservation_i)".format(phase_i, phase_i))

                #Create mass conservation for each component

                exec("_mass_conservation_i = self.w_{}_out() - self.w_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('mass_fraction_conservation_for_{}', 'Mass conservation for {} phase', _mass_conservation_i)".format(phase_i, phase_i))

class SimplePump(model.Model):

    """
    Model for a simple pump

    If homogeneous (property_package = None or property_package has 1 phase):

    *INPUTS: ndot_in, mdot_in, H_in, P_in, T_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out, T_out
    *PARAMETERS: Delta_P

    *REQUIRES: -

    If multiphasic (property_package has 2+ phases):

    *INPUTS: ndot_in, mdot_in, H_in, P_in,  T_in, x_<phase1>_in, w_<phase1>_in, ..., x_<phaseN>_in, w_<phaseN>_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out,  T_out, x_<phase1>_out, w_<phase1>_out, ..., x_<phaseN>_out, w_<phaseN>_out
    *PARAMETERS: Delta_P

    *REQUIRES: -
    """

    def __init__(self, name, description="SimplePump", property_package=None):

        super().__init__(name, description, property_package)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        self.H_in = self.createVariable("H_in", J/mol, "input molar enthalpy", latex_text="{H}_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "output molar enthalpy", latex_text="{H}_{out}", is_exposed=True, type='output')

        self.P_in = self.createVariable("P_in", Pa, "input pressure", latex_text="{P}_{in}", is_exposed=True, type='input')
        self.P_out = self.createVariable("P_out", Pa, "output pressure", latex_text="{P}_{out}", is_exposed=True, type='output')

        self.T_in = self.createVariable("T_in", K, "input stream temperature", latex_text="{T}_{in}", is_exposed=True, type='input')
        self.T_out = self.createVariable("T_out", K, "output stream temperature", latex_text="{T}_{out}", is_exposed=True, type='output')

        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("self.x_{}_in = self.createVariable('x_{}_in',dimless,'Molar fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_in = self.createVariable('w_{}_in',dimless,'Mass fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))


    def DeclareEquations(self):

        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        _isoenthalpy = self.H_in()*self.ndot_in() - self.H_out()*self.ndot_out()

        self.createEquation("isoenthalpy", "isoenthalpy", _isoenthalpy)

        _mechanical_equilibrium = self.P_out() - self.P_in() - self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

        _energy_balance = self.T_out() - self.T_in()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("_molar_conservation_i = self.x_{}_out() - self.x_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('molar_fraction_conservation_for_{}', 'Molar conservation for {} phase', _molar_conservation_i)".format(phase_i, phase_i))

                #Create mass conservation for each component

                exec("_mass_conservation_i = self.w_{}_out() - self.w_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('mass_fraction_conservation_for_{}', 'Mass conservation for {} phase', _mass_conservation_i)".format(phase_i, phase_i))

class Heater(model.Model):

    def __init__(self, name, description="Heater", property_package=None):

        """
        Defines a generic heater

        *INPUTS: ndot_in, mdot_in, H_in, P_in, T_in
        *OUTPUTS: mdot_out, mdot_out, H_out, P_out, T_out
        *PARAMETERS:  Q, Delta_P

        *REQUIRES: PropertyPackage

        If multiphasic (property_package has 2+ phases):

        *INPUTS: ndot_in, mdot_in, H_in, P_in,  T_in, x_<phase1>_in, w_<phase1>_in, ..., x_<phaseN>_in, w_<phaseN>_in
        *OUTPUTS: mdot_out, mdot_out, H_out, P_out,  T_out, x_<phase1>_out, w_<phase1>_out, ..., x_<phaseN>_out, w_<phaseN>_out
        *PARAMETERS: Q, Delta_P

        *REQUIRES: -
        """

        super().__init__(name, description, property_package)

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("self.x_{}_in = self.createVariable('x_{}_in',dimless,'Molar fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_in = self.createVariable('w_{}_in',dimless,'Mass fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        self.P_in = self.createVariable("P_in", Pa, "pressure from input", latex_text="P_{in}", is_exposed=True, type="input")
        self.P_out = self.createVariable("P_out", Pa, "pressure from output", latex_text="P_{out}", is_exposed=True, type="output")

        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")

        self.H_in  = self.createVariable("H_in", J/mol, "molar enthalpy input", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "molar enthalpy output", latex_text="H_{out}", is_exposed=True, type='output')

        self.Q = self.createParameter("Q", J/s, "Heat rate", latex_text="Q")

        self.T_in  = self.createVariable("T_in", K, "temperature from input", latex_text="T_{in}", is_exposed=True, type='input')
        self.T_out = self.createVariable("T_out", K, "temperature from output", latex_text="T_{out}", is_exposed=True, type='output')

        self.cp_mix = self.createParameter("cp_mix",J/(kg*K),"Mass specific capacity for the mixture of components")

        if self.property_package.number_of_phases>=2:

            cp_mix_ = 0.

            for phase_i in self.property_package.phase_names:

                cp_mix_ += eval("self.w_{}_out()*self.property_package['{}'].Cp".format(phase_i, phase_i))

            self.cp_mix.setValue(mix_rho_)

        else:

            self.cp_mix.setValue(self.property_package["*"].Cp)

        #Assume heat rate (Q) for heating is positive

    def DeclareEquations(self):

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("_molar_conservation_i = self.x_{}_out() - self.x_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('molar_fraction_conservation_for_{}', 'Molar conservation for {} phase', _molar_conservation_i)".format(phase_i, phase_i))

                #Create mass conservation for each component

                exec("_mass_conservation_i = self.w_{}_out() - self.w_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('mass_fraction_conservation_for_{}', 'Mass conservation for {} phase', _mass_conservation_i)".format(phase_i, phase_i))

        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        _mechanical_equilibrium = self.P_out() - self.P_in() + self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

        _energy_balance = self.ndot_out()*self.H_out() - self.ndot_in()*self.H_in() - self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        _temperature_balance = self.T_out() - self.T_in() - (self.Q()/(self.mdot_out()*self.cp_mix()))

        self.createEquation("temperature_balance", "Temperature balance", _temperature_balance)

class Cooler(Heater):

    def __init__(self, name, description="Cooler", property_package=None):

        """
        Defines a generic cooler

        *INPUTS: ndot_in, mdot_in, H_in, P_in, T_in
        *OUTPUTS: mdot_out, mdot_out, H_out, P_out, T_out
        *PARAMETERS:  Q, Delta_P

        *REQUIRES: PropertyPackage

        If multiphasic (property_package has 2+ phases):

        *INPUTS: ndot_in, mdot_in, H_in, P_in,  T_in, x_<phase1>_in, w_<phase1>_in, ..., x_<phaseN>_in, w_<phaseN>_in
        *OUTPUTS: mdot_out, mdot_out, H_out, P_out,  T_out, x_<phase1>_out, w_<phase1>_out, ..., x_<phaseN>_out, w_<phaseN>_out
        *PARAMETERS: Q, Delta_P

        *REQUIRES: -
        """

        super().__init__(name, description, property_package)

class DynamicFlash(model.Model):

    def __init__(self, name, description="DynamicFlash", property_package=None, orientation='vertical'):

        """
        Flash model
        """
        super().__init__(name, description, property_package)

        self.orientation = orientation

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("self.x_{}_in = self.createVariable('x_{}_in',dimless,'Molar fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_in = self.createVariable('w_{}_in',dimless,'Mass fraction for {} phase in the input', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.x_{}_out = self.createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i,phase_i, phase_i))
                exec("self.w_{}_out = self.createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output', is_exposed='True', type='output')".format(phase_i, phase_i, phase_i))


        self.t = self.createVariable("t",s,"time",latex_text="t")

        self.time_domain = Domain("time_domain", s, self.t, "time domain")

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')
        self.N = self.createVariable("N", mol, "molar holdup", latex_text="N", is_exposed=True, type="output")

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')
        self.M = self.createVariable("M", kg, "mass holdup", latex_text="M", is_exposed=True, type='output')

        self.P_in = self.createVariable("P_in", Pa, "pressure from input", latex_text="P_{in}", is_exposed=True, type="input")
        self.P_out = self.createVariable("P_out", Pa, "pressure from output", latex_text="P_{out}", is_exposed=True, type="output")

        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")

        self.H_in  = self.createVariable("H_in", J/mol, "molar enthalpy input", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "molar enthalpy output", latex_text="H_{out}", is_exposed=True, type='output')
        self.E = self.createVariable("E", J, "energy holdup", latex_text="E", is_exposed=True, type='output')

        self.Q = self.createParameter("Q", J/s, "Heat rate", latex_text="Q")

        self.T_in  = self.createVariable("T_in", K, "temperature from input", latex_text="T_{in}", is_exposed=True, type='input')
        self.T_out = self.createVariable("T_out", K, "temperature from output", latex_text="T_{out}", is_exposed=True, type='output')

        self.cp_mix = self.createParameter("cp_mix",J/(kg*K),"Mass specific capacity for the mixture of components")

        if self.property_package.number_of_phases>=2:

            cp_mix_ = 0.

            for phase_i in self.property_package.phase_names:

                cp_mix_ += eval("self.w_{}_out()*self.property_package['{}'].Cp".format(phase_i, phase_i))

            self.cp_mix.setValue(mix_rho_)

        else:

            self.cp_mix.setValue(self.property_package["*"].Cp)

    def DeclareEquations(self):

        if self.property_package.number_of_phases>=2:

            for phase_i in self.property_package.phase_names:

                exec("_molar_conservation_i = self.x_{}_out() - self.x_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('molar_fraction_conservation_for_{}', 'Molar conservation for {} phase', _molar_conservation_i)".format(phase_i, phase_i))

                #Create mass conservation for each component

                exec("_mass_conservation_i = self.w_{}_out() - self.w_{}_in()".format(phase_i, phase_i))

                exec("self.createEquation('mass_fraction_conservation_for_{}', 'Mass conservation for {} phase', _mass_conservation_i)".format(phase_i, phase_i))

        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        _mechanical_equilibrium = self.P_out() - self.P_in() + self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

        _energy_balance = self.ndot_out()*self.H_out() - self.ndot_in()*self.H_in() - self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        _temperature_balance = self.T_out() - self.T_in() - (self.Q()/(self.mdot_out()*self.cp_mix()))

        self.createEquation("temperature_balance", "Temperature balance", _temperature_balance)

class Centrifuge:

    pass

class CentrifugalPump:

    pass

class HeatExchanger:

    pass

class DistillationColumn:

    pass