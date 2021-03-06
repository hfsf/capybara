
# *coding:utf-8*
import math
import sympy as sp
#import symengine as sp
import numpy as np
from numpy import array as np_array
from collections import OrderedDict
from numba import jit

class EquationBlock:

    """
    Define EquationBlock. Act as a container for Equation objects.
    """

    def __init__(self, equations, variable_dict, parameter_dict, owner_model=None):

        """
        Instantiate EquationBlock

        :ivar list(Equations) equations:
            List containing the Equation objects for the EquationBlock. Defaults to the whole set of equations from the owner model.

        :ivar dict variable_dict:
            Dictionary containing all the Variable objects present in the EquationBlock, provided by the Problem instance that instantiate current EquationBlock.

        :ivar dict parameter_dict:
            Dictionary containing all the Parameter objects present in the EquationBlock, provided by the Problem instance that instantiate current EquationBlock.

        :ivar Model owner_model:
            Model for which the EquationBlock is defined. Defaults to None.
        """

        self.owner_model = owner_model

        self.equations = equations

        self.variable_dict = variable_dict

        self.parameter_dict = parameter_dict

        self._var_list = []

        self._param_list = []

        #self._var_dict = variable_dict

        self._equations_list = []

        self._equation_groups = OrderedDict({'linear':[], 'nonlinear':[], 'differential':[]})

        self._assignEquationGroups()

        self._fs = None

    def _assignEquationGroups(self):

        """
        Get the type of each of the equations and assign them accordingly to the ._equation_groups atribute of the current EquationBlock object.
        """

        #print("\nEquation list: %s" %(self._equations_list))

        eq_lin = [i for i in self.equations if i.type == 'linear']

        eq_nlin = [i for i in self.equations if i.type == 'nonlinear']

        eq_diff = [i for i in self.equations if i.type == 'differential']

        self._equation_groups['linear'] = eq_lin

        self._equation_groups['nonlinear'] = eq_nlin

        self._equation_groups['differential'] = eq_diff

    def _convertDifferentialEquationsToResidualForm(self):

        """
        Convert the differential equations present in the current EquationBlock (._equation_groups['differential']) to the residual form
        """

        _ = [eq_i._convertToResidualForm() for eq_i in self._equation_groups['differential'] if eq_i.equation_form!='residual']


    def _getMapForRewriteSystemAsResidual(self):

        """
        Return dictionaries mapping the differential terms and ydot nomenclature (eg:yd[0]) and variables and y nomenclature (eg:y[0]), used for residual solvers

        :return:
            Two dictionaries that map between the differential terms and variables used in the equations with the residual nomenclature (yd,y)

        :rtype dict yd_map,y_map:
        """

        diff_list = self._getDiffList()

        yd_list = ["yd[{}]".format(i) for (i,_) in enumerate(diff_list)]

        var_list = self._var_list

        y_list = ["y[{}]".format(i) for (i,_) in enumerate(var_list)]

        yd_map = {k:v for (k,v) in zip(diff_list,yd_list)}

        y_map = {k:v for (k,v) in zip(var_list,y_list)}

        return yd_map, y_map

    def _getDiffList(self):

        """
        Set the list for each of the occurences of Derivative objects that appear in the equations of the model

        :return:
            List of derivatives
        :rtype list(str) diff_list:
        """

        diff_list = []

        for eqi in self._equation_groups['differential']:

            eq = eqi._getSymbolicObject('residual','rhs')

            _ = [diff_list.append(abs(i).args[0]) for i in eq.args if 'Derivative' in sp.srepr(i)]

        return diff_list

    def _getParamList(self):

        param_name_list = list(self.parameter_dict.keys())

        return param_name_list

    def _getVarList(self):

        """
        Set the list for each of the Variable objects that appear in the equations of the model

        :return:
            List of variable names
        :rtype list(str):

        """

        var_name_list = list(self.variable_dict.keys())

        return var_name_list

    def _getEquationBlockAsFunction(self, differential_form='residual', side='rhs', compilation_mechanism="mpmath"):

        """
        Return the Equations that compose the current EquationBlock object into a monolithical function that will return an array of results.

        :param str differential_form:
            Definition of which form the equations are presented, if in a 'elementary' form (y == a*x +b) or in a 'residual' form (y - a*x - b == 0). Defaults to 'residual'

        :param str side:
            Side of which the equality of the equation in the elementary form should be examined ('lhs' for left, 'rhs' for right-hand side).

        :param str compilation_mechanism:
            Determination of which mechanism to use to compile the equations. Defaults to 'numpy'

        :return:
            Monolithic function corresponding to all the equations defined for current EquationBlock, retuning an array of results
        :rtype function:
        """

        #Check if the problem is differential or purely algebraic

        if len(self._equation_groups["differential"]) > 0:

            if differential_form == 'elementary':

                fun_ = sp.lambdify(self._var_list,
                                   np_array(self._getEquationList(differential_form,side)),
                                   [{'Min':min, 'Max':max, 'Sin':np.sin, 'Cos':np.cos}, compilation_mechanism]
                            )

                return jit(fun_)


            if differential_form == 'residual':

                yd_map, y_map = self._getMapForRewriteSystemAsResidual()

                # Add y_map dict to yd_map

                yd_map.update(y_map)

                original_eqs = self._getEquationList(differential_form, side)

                rewritten_eqs = [eq_i.subs(yd_map) for eq_i in original_eqs]

                _fun_ = sp.lambdify(["t","y","yd"],
                                   np_array(rewritten_eqs),
                                   [{'Min':min, 'Max':max, 'Sin':math.sin, 'Cos':math.cos}, compilation_mechanism]
                            )

                #Provide result as numpy.array

                fun_ = lambda t,y,yd: np_array(_fun_(t,y,yd))

                return fun_

        else:

            fun_ = sp.lambdify(self._var_list,
                               np_array(self._equations_list),
                               [{'Min': min, 'Max': max, 'Sin': np.sin, 'Cos': np.cos}, compilation_mechanism]
                               )

            fun_unpacked_ = lambda x: fun_(*x)

            return fun_unpacked_

    def _getBooleanDiffFlagsForEquations(self):

        """
        Return an boolean list of if each of the Equation objects contained in the current EquationBlock are differential

        :return:
            List of boolean flags indicating which equations are boolean
        :rtype list(bool):
        """

        return [float(i.type == 'differential') for i in self.equations]

    def _getEquationList(self, differential_form=None, side='rhs'):

        """
        Set the list of sympy expressions representing the equation.

     :param str differential_form:
            Definition of which form the equations are presented, if in a 'elementary' form (y == a*x +b) or in a 'residual' form (y - a*x - b == 0). Defaults to None, for which the declared form of the equation are used.

        :param str side:
            Side of which the equality of the equation in the elementary form should be examined ('lhs' for left, 'rhs' for right-hand side).

        :return:
            List of the sympy expressions representing each Equation object of the model

        :rtype list(sympy expresion):
        """

        #return [eq_i.equation_expression.symbolic_object for eq_i in self.equations]
        return [eq_i._getSymbolicObject(differential_form, side) for eq_i in self.equations]

    def _hasVarBeenDeclared(self, var_name, group=None):

        """
        Check if an specific var was declared in current EquationBlock, in a specific group of equations, or through the entire set of equations
        """

        has_been_declared = False

        if isinstance(var_name, list) is not True:

            var_name = [var_name]

        if group is not None:

            where_to_look = self._equation_groups[group]

        else:

            where_to_look = self._equations_list

        for eq in where_to_look:

            #print("\n======>Equation: ", eq._getSymbolicObject())

            try:

                equation_members_ = eq._getSymbolicObject().args

            except:

                equation_members_ = []

            for eq_i in equation_members_:

                #print("\n\t======>Member: ",eq_i)

                #print("\n\t\t======>Has time_var_declared? : ", [ t_i in sp.srepr(eq_i) for t_i in var_name])

                #Will not trigger for 'Derivative' terms

                if any(var_i in sp.srepr(eq_i) and 'Derivative' not in sp.srepr(eq_i) for var_i in var_name):

                    has_been_declared = True

                    break

            if has_been_declared is True:

                break

        return has_been_declared

    def __call__(self):

        """
        Overloaded method for EquationBlock object. Examines the equations atribute of the EquationBlock object and build the matrix
        """

        # Fill-up the list of Variables and Equations

        self._param_list = self._getParamList()

        self._var_list = self._getVarList()

        self._equations_list = self._getEquationList()

        self._assignEquationGroups()