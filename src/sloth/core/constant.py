"""
Define constant class.
"""

from .quantity import Quantity
from .unit import null_dimension
from .error_definitions import UnexpectedValueError, DimensionalCoherenceError



def convert_to_constant(num):
    """
    Convert one float argument to Constant, returning the converted object.

    :param float num:
        Float number to be converted to Constant

    :return:
        Float number converted to a Constant object
    :rtype: object
    """

    return Constant(name=str(num), units = null_dimension, value = float(num) )


class Constant(Quantity):
    """
    Constant class definition, that holds capabilities for:

    * Constant definition, including its units for posterior dimensional coherence analysis

    * Constant operations using overloaded mathematical operators,
    making possible an almost-writing-syntax (eg: a() + b() )
    """

    def __init__(self, name, units , description="", value=0, latex_text="", is_specified=False, owner_model_name=""):

        super().__init__(name, units, description, value, latex_text, owner_model_name)

        """
        Initial definition.

        :param str name:
        Name for the current constant

        :param Unit units:
        Definition of dimensional unit of current constant

        :param str description:
        Description for the present constant. Defauls to ""

        """

        self.name = name

        self.units = units

        self.description = description

        self.is_specified = is_specified

    def setValue(self, quantity_value, quantity_unit=None):

        """
        Method for value specification of Parameter object. Overloaded from base class Quantity.

        :param [float, Quantity] quantity_value:
            Value to the current Parameter object

        :param Unit quantity_unit:
            Unit object for the parameter. Defaults to currennt units
        """

        if isinstance(quantity_value, self.__class__):


            if quantity_unit == None and  quantity_value.units._check_dimensional_coherence(self.units) == True:

                self.value = quantity_value.value

                self.is_specified = True

            else:

                raise DimensionalCoherenceError(self.units,quantity_value.units)

        elif isinstance(quantity_value, float) or isinstance(quantity_value, int) and quantity_unit==None:

            self.value = quantity_value

            self.is_specified = True


        elif isinstance(quantity_value, float) or isinstance(quantity_value, int) and quantity_unit!=None and quantity_unit._check_dimensional_coherence(self.units):

            self.value = quantity_value

            self.is_specified = True

        else:

            raise UnexpectedValueError("(Quantity, float, int)")