from collections.abc import Sequence
import enum
import types
from typing import overload

from . import Enum as Enum
import pyoptinterface._src.core_ext


class HighsSolution:
    @property
    def status(self) -> HighsSolutionStatus: ...

    @property
    def model_status(self) -> int: ...

    @property
    def primal_solution_status(self) -> int: ...

    @property
    def dual_solution_status(self) -> int: ...

    @property
    def has_primal_ray(self) -> bool: ...

    @property
    def has_dual_ray(self) -> bool: ...

class HighsSolutionStatus(enum.Enum):
    OPTIMIZE_NOT_CALLED = 0

    OPTIMIZE_OK = 1

    OPTIMIZE_ERROR = 2

class RawModel(_RawModelBase):
    def __init__(self) -> None: ...

    @property
    def m_n_variables(self) -> int: ...

    @property
    def m_n_constraints(self) -> int: ...

    def init(self) -> None: ...

    def write(self, arg: str, /) -> None: ...

    @property
    def solution(self) -> HighsSolution: ...

    def add_variable(self, domain: pyoptinterface._src.core_ext.VariableDomain = VariableDomain.Continuous, lb: float = float('-inf'), ub: float = float('inf'), name: str = '') -> pyoptinterface._src.core_ext.VariableIndex: ...

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

    def optimize(self) -> None: ...

    def version_string(self) -> str: ...

    def get_raw_model(self) -> types.CapsuleType: ...

    def getruntime(self) -> float: ...

    def getnumrow(self) -> int: ...

    def getnumcol(self) -> int: ...

    def raw_option_type(self, arg: str, /) -> int: ...

    def set_raw_option_bool(self, arg0: str, arg1: bool, /) -> None: ...

    def set_raw_option_int(self, arg0: str, arg1: int, /) -> None: ...

    def set_raw_option_double(self, arg0: str, arg1: float, /) -> None: ...

    def set_raw_option_string(self, arg0: str, arg1: str, /) -> None: ...

    def get_raw_option_bool(self, arg: str, /) -> bool: ...

    def get_raw_option_int(self, arg: str, /) -> int: ...

    def get_raw_option_double(self, arg: str, /) -> float: ...

    def get_raw_option_string(self, arg: str, /) -> str: ...

    def raw_info_type(self, arg: str, /) -> int: ...

    def get_raw_info_int(self, arg: str, /) -> int: ...

    def get_raw_info_int64(self, arg: str, /) -> int: ...

    def get_raw_info_double(self, arg: str, /) -> float: ...

    def set_variable_name(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: str, /) -> None: ...

    def get_variable_name(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> str: ...

    def set_variable_type(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: pyoptinterface._src.core_ext.VariableDomain, /) -> None: ...

    def get_variable_type(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> pyoptinterface._src.core_ext.VariableDomain: ...

    def set_variable_lower_bound(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def set_variable_upper_bound(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def get_variable_lower_bound(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def get_variable_upper_bound(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def get_constraint_primal(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> float: ...

    def get_constraint_dual(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> float: ...

    def get_constraint_name(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> str: ...

    def set_constraint_name(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: str, /) -> None: ...

    def set_obj_sense(self, arg: pyoptinterface._src.core_ext.ObjectiveSense, /) -> None: ...

    def get_obj_sense(self) -> pyoptinterface._src.core_ext.ObjectiveSense: ...

    def get_obj_value(self) -> float: ...

    def set_primal_start(self, arg0: Sequence[pyoptinterface._src.core_ext.VariableIndex], arg1: Sequence[float], /) -> None: ...

    def get_normalized_rhs(self, arg: pyoptinterface._src.core_ext.ConstraintIndex, /) -> float: ...

    def set_normalized_rhs(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: float, /) -> None: ...

    def get_normalized_coefficient(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_normalized_coefficient(self, arg0: pyoptinterface._src.core_ext.ConstraintIndex, arg1: pyoptinterface._src.core_ext.VariableIndex, arg2: float, /) -> None: ...

    def get_objective_coefficient(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_objective_coefficient(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

def is_library_loaded() -> bool: ...

def load_library(arg: str, /) -> bool: ...
