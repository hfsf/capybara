# *coding:utf-8*

"""
Define Problem class. Unite several Model classes through Connections, forming one single Equation block. Used by Simulation class to perform the calculations.
"""

from core.error_definitions import ExposedVariableError
from core.equation_block import EquationBlock
from collections import OrderedDict
import numpy as np

class Problem(object):

    """
    Problem class definitions. Unite several Model objects into one single equation block for solving.
    """

    def __init__(self, name, description=""):

        """
        Instantiate Problem.

        :ivar str name:
            Name for the current problem

        :ivar str description:
            Description of the current problem
        """

        self.name = name

        self.description = description

        self.models = OrderedDict({})

        self.connections = OrderedDict({})

        self._equation_list = None

        self.equation_block = None

    def _buildEquationBlock(self):

        """
        Return the EquationBlock object for the models defined for the current problem.
        """

        #eqs_ = [ list(model_i.equations.values()) for model_i in self.models.values() ]

        #self._equation_list = (np.array(eqs_).ravel()).tolist()

        #================== OPTIMIZE THIS CODE SNIPPET ===================

        self._equation_list = []

        for model_i in list(self.models.values()):

            for eq_i in list(model_i.equations.values()):

                self._equation_list.append(eq_i)

        #=================================================================

        self.equation_block = EquationBlock(equations=self._equation_list)

    def createConnection(self, model_1, model_2, output_var, input_var, expr=None):

        """
        Connect two Models creating a Connection for both models, linking the ouput variable of the former to the input variable of the later.
        """

        if output_var in model_1.exposed_vars['output'] and \
           input_var  in model_2.exposed_vars['input']:

           # Creating connection equation in the second Model object

           conn = model_2._createConnection("","", output_var, input_var, \
                                            model_1, expr)

           self.connections[output_var.name+"@"+model_1.name+" ---> "+input_var.name+"@"+model_2.name] = conn

           return conn

        else:

            raise ExposedVariableError(model_1.exposed_vars['output'], model_2.exposed_vars['input'], output_var, input_var) 

    def addModels(self, model_list):

        """
        Add models to current problem

        :param [Model, list(Model)] mod_list:
            Model to be added to the current Problem.
        """
        
        if isinstance(model_list,list):

            # A list of models were supplied

            self.models = OrderedDict( (modx.name,modx) for modx in model_list )

        else:

            # A single model was supplied

            self.models[model_list.name] = model_list

    def resolve(self):

        """
        Resolve current Problem object, builing its EquationBlock object and resolving it
        """ 
    
        self._buildEquationBlock()

        self.equation_block()
