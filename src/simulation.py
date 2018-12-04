# *coding:utf-8

"""
Define Simulation class
"""

from problem import Problem
from model import Model
import solvers
import analysis
from core.error_definitions import UnexpectedValueError

class Simulation:

    """
    Simulation class definition
    """

    def __init__(self, name, description="", problem=None):

        """
        Instantiate Simulation.

        :ivar str name:
            Name for the current simulation

        :ivar str description:
            Description of the current simulation

        :ivar Problem problem:
            Problem to be studied in the current simulation
        """

        self.name = name

        self.description = description

        self.problem = problem

    def report(self, object):

        """
        Print the report output for the current object

        :param [Model, Problem] object:
            Object to be analyzed
        """

        analist = analysis.Analysis()

        if isinstance(object, Model):

            analist.modelReport(object)

        elif isinstance(object, Problem):

            analist.problemReport(object)

        else:

            raise UnexpectedValueError("[Model, Problem]")

    def setProblem(self, problem):

        """
        Set the Problem object for the current simulation
        
        :param Problem problem:
        """

        self.problem = problem

    def runSimulation(self, initial_time=0., end_time=None, linear_solver='sympy', nonlinear_solver='sympy', differential_solver='scipy', differential_algebraic_solver='scipy', problem_type=None, is_dynamic=False, compile_diff_equations=True, domain=None, time_variable_name='t', arg_names=[], args=[], number_of_time_steps=100, configuration_args={}, print_output=False, output_headers="", compilation_mechanism="numpy"):

        """
        Run the current simulation using the defined parameters
        """

        additional_conf = {'compile_diff_equations':compile_diff_equations, 
                           'domain':domain, 
                           'time_variable_name':time_variable_name,
                           'initial_time':initial_time,
                           'end_time':end_time,
                           'is_dynamic':is_dynamic, 
                           'arg_names':arg_names,
                           'linear_solver':linear_solver,
                           'nonlinear_solver':nonlinear_solver,
                           'differential_solver':differential_solver,
                           'differential_algebraic_solver':differential_algebraic_solver,
                           'args':args,
                           'number_of_time_steps':number_of_time_steps,
                           'configuration_args':configuration_args,
                           'print_output':print_output,
                           'output_headers':output_headers,
                           'compilation_mechanism':compilation_mechanism
                           }

        if problem_type == None:

            problem_type = self.problem._getProblemType()

        if problem_type == "linear":

            solver_mechanism = solvers.createSolver(self.problem, additional_conf)

        elif problem_type == "nonlinear":

            solver_mechanism = solvers.createSolver(self.problem, additional_conf)
        
        elif problem_type == "differential":

            solver_mechanism = solvers.createSolver(self.problem, additional_conf)     

        elif problem_type == "differential-algebraic":

            pass
        
        else:

            raise UnexpectedValueError("EquationBlock")

        solver_mechanism.solve(additional_conf)


