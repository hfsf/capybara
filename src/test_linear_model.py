#test_model.py

import pytest

from .model import Model

from core.equation_operators import *
from core.template_units import *

import copy

@pytest.fixture
def mod():
    """
    Create a generic linear model
    """

    class linear_model(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.a =  self.createVariable("a", kg_s, "A", is_exposed=True, type='output')
            self.b =  self.createVariable("b", kg_s, "B")
            self.c =  self.createVariable("c", kg, "C")
            self.d =  self.createConstant("d", s**-1, "D")
            self.d.setValue(0.7)

        def DeclareEquations(self):

            expr1 = self.a() + self.b() - 1.

            expr2 = self.a() + self.c()*self.d() - 2

            expr3 = self.c()*self.d() - self.a() - self.b()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
            self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

    lin_mod = linear_model("L0","Linear model")

    lin_mod()

    return lin_mod

def test_model_properties(mod):

    assert mod.name == "L0" and \
           mod.description == "Linear model" and \
           list(mod.variables.keys()) == ["a@L0","b@L0","c@L0"] and \
           list(mod.constants.keys()) == ["d@L0"] and \
           list(mod.equations.keys()) == ["eq1@L0","eq2@L0","eq3@L0"]

def test_model_enodes(mod):

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.a and \
           mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.b and \
           mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.eq2.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]]
