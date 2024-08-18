import types
from typing import Sequence, overload

from . import Enum as Enum
import pyoptinterface._src.core_ext


class Env:
    def __init__(self) -> None: ...

    def putlicensecode(self, arg: Sequence[int], /) -> None: ...

class RawModel(_RawModelBase):
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: Env, /) -> None: ...

    def init(self, arg: Env, /) -> None: ...

    def write(self, arg: str, /) -> None: ...

    def add_variable(self, domain: pyoptinterface._src.core_ext.VariableDomain = VariableDomain.Continuous, lb: float = -1e+30, ub: float = 1e+30, name: str = '') -> pyoptinterface._src.core_ext.VariableIndex: ...

    def delete_variable(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> None: ...

    def delete_variables(self, arg: Sequence[pyoptinterface._src.core_ext.VariableIndex], /) -> None: ...

    def is_variable_active(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> bool: ...

    @overload
    def get_value(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    @overload
    def get_value(self, arg: pyoptinterface._src.core_ext.ScalarAffineFunction, /) -> float: ...

    @overload
    def get_value(self, arg: pyoptinterface._src.core_ext.ScalarQuadraticFunction, /) -> float: ...

    @overload
    def get_value(self, arg: pyoptinterface._src.core_ext.ExprBuilder, /) -> float: ...

    @overload
    def pprint(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> str: ...

    @overload
    def pprint(self, expr: pyoptinterface._src.core_ext.ScalarAffineFunction, precision: int = 4) -> str: ...

    @overload
    def pprint(self, expr: pyoptinterface._src.core_ext.ScalarQuadraticFunction, precision: int = 4) -> str: ...

    @overload
    def pprint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, precision: int = 4) -> str: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.ScalarAffineFunction, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.VariableIndex, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_quadratic_constraint(self, expr: pyoptinterface._src.core_ext.ScalarQuadraticFunction, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_quadratic_constraint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    def add_second_order_cone_constraint(self, variables: Sequence[pyoptinterface._src.core_ext.VariableIndex], name: str = '', rotated: bool = False) -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    def add_exp_cone_constraint(self, variables: Sequence[pyoptinterface._src.core_ext.VariableIndex], name: str = '', dual: bool = False) -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    def delete_constraint(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> None: ...

    def is_constraint_active(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> bool: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.ScalarQuadraticFunction, sense: pyoptinterface._src.core_ext.ObjectiveSense = pyoptinterface._src.core_ext.ObjectiveSense.Minimize) -> None: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.ScalarAffineFunction, sense: pyoptinterface._src.core_ext.ObjectiveSense = pyoptinterface._src.core_ext.ObjectiveSense.Minimize) -> None: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ObjectiveSense = pyoptinterface._src.core_ext.ObjectiveSense.Minimize) -> None: ...

    @overload
    def set_objective(self, expr: float, sense: pyoptinterface._src.core_ext.ObjectiveSense = pyoptinterface._src.core_ext.ObjectiveSense.Minimize) -> None: ...

    def optimize(self) -> int: ...

    def version_string(self) -> str: ...

    def get_raw_model(self) -> types.CapsuleType: ...

    def raw_parameter_type(self, arg: str, /) -> int: ...

    def set_raw_parameter_int(self, arg0: str, arg1: int, /) -> None: ...

    def set_raw_parameter_double(self, arg0: str, arg1: float, /) -> None: ...

    def set_raw_parameter_string(self, arg0: str, arg1: str, /) -> None: ...

    def get_raw_parameter_int(self, arg: str, /) -> int: ...

    def get_raw_parameter_double(self, arg: str, /) -> float: ...

    def get_raw_parameter_string(self, arg: str, /) -> str: ...

    def get_raw_information_int(self, arg: str, /) -> int: ...

    def get_raw_information_double(self, arg: str, /) -> float: ...

    def getnumvar(self) -> int: ...

    def getnumcon(self) -> int: ...

    def getprosta(self) -> int: ...

    def getsolsta(self) -> int: ...

    def getprimalobj(self) -> float: ...

    def getdualobj(self) -> float: ...

    def enable_log(self) -> None: ...

    def disable_log(self) -> None: ...

    def set_variable_name(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: str, /) -> None: ...

    def get_variable_name(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> str: ...

    def set_variable_type(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: pyoptinterface._src.core_ext.VariableDomain, /) -> None: ...

    def get_variable_type(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> pyoptinterface._src.core_ext.VariableDomain: ...

    def set_variable_lower_bound(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def set_variable_upper_bound(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def get_variable_lower_bound(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def get_variable_upper_bound(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_variable_primal(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def get_constraint_primal(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> float: ...

    def get_constraint_dual(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> float: ...

    def get_constraint_name(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> str: ...

    def set_constraint_name(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: str, /) -> None: ...

    def set_obj_sense(self, arg: pyoptinterface._src.core_ext.ObjectiveSense, /) -> None: ...

    def get_obj_sense(self) -> pyoptinterface._src.core_ext.ObjectiveSense: ...

    def get_normalized_rhs(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> float: ...

    def set_normalized_rhs(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: float, /) -> None: ...

    def get_normalized_coefficient(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_normalized_coefficient(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: pyoptinterface._src.core_ext.VariableIndex, arg2: float, /) -> None: ...

    def get_objective_coefficient(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_objective_coefficient(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

def is_library_loaded() -> bool: ...

def load_library(arg: str, /) -> bool: ...
