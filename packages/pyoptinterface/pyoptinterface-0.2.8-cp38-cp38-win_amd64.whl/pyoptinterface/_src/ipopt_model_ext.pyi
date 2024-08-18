import enum
from typing import Sequence, overload

import pyoptinterface._src.core_ext
import pyoptinterface._src.nlcore_ext


class ApplicationReturnStatus(enum.Enum):
    Solve_Succeeded = 0

    Solved_To_Acceptable_Level = 1

    Infeasible_Problem_Detected = 2

    Search_Direction_Becomes_Too_Small = 3

    Diverging_Iterates = 4

    User_Requested_Stop = 5

    Feasible_Point_Found = 6

    Maximum_Iterations_Exceeded = -1

    Restoration_Failed = -2

    Error_In_Step_Computation = -3

    Maximum_CpuTime_Exceeded = -4

    Maximum_WallTime_Exceeded = -5

    Not_Enough_Degrees_Of_Freedom = -10

    Invalid_Problem_Definition = -11

    Invalid_Option = -12

    Invalid_Number_Detected = -13

    Unrecoverable_Exception = -100

    NonIpopt_Exception_Thrown = -101

    Insufficient_Memory = -102

    Internal_Error = -199

class RawModel:
    def __init__(self) -> None: ...

    @property
    def m_function_model(self) -> pyoptinterface._src.nlcore_ext.NonlinearFunctionModel: ...

    @property
    def m_status(self) -> ApplicationReturnStatus: ...

    def add_variable(self, lb: float = float('-inf'), ub: float = float('inf'), start: float = 0.0, name: str = '') -> pyoptinterface._src.core_ext.VariableIndex: ...

    def get_variable_lb(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def get_variable_ub(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_variable_lb(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def set_variable_ub(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def set_variable_bounds(self, variable: pyoptinterface._src.core_ext.VariableIndex, lb: float, ub: float) -> None: ...

    def get_variable_start(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> float: ...

    def set_variable_start(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: float, /) -> None: ...

    def get_variable_name(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> str: ...

    def set_variable_name(self, arg0: pyoptinterface._src.core_ext.VariableIndex, arg1: str, /) -> None: ...

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

    def add_parameter(self, value: float = 0.0) -> pyoptinterface._src.nlcore_ext.ParameterIndex: ...

    def set_parameter(self, arg0: pyoptinterface._src.nlcore_ext.ParameterIndex, arg1: float, /) -> None: ...

    def get_obj_value(self) -> float: ...

    def get_constraint_primal(self, arg: int, /) -> float: ...

    def get_constraint_dual(self, arg: int, /) -> float: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.ScalarAffineFunction, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.ScalarAffineFunction, sense: pyoptinterface._src.core_ext.ConstraintSense, lb: float, ub: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.VariableIndex, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.VariableIndex, sense: pyoptinterface._src.core_ext.ConstraintSense, lb: float, ub: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_linear_constraint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ConstraintSense, lb: float, ub: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_quadratic_constraint(self, expr: pyoptinterface._src.core_ext.ScalarQuadraticFunction, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_quadratic_constraint(self, expr: pyoptinterface._src.core_ext.ScalarQuadraticFunction, sense: pyoptinterface._src.core_ext.ConstraintSense, lb: float, ub: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_quadratic_constraint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_quadratic_constraint(self, expr: pyoptinterface._src.core_ext.ExprBuilder, sense: pyoptinterface._src.core_ext.ConstraintSense, lb: float, ub: float, name: str = '') -> pyoptinterface._src.core_ext.ConstraintIndex: ...

    @overload
    def add_objective(self, arg: pyoptinterface._src.core_ext.ExprBuilder, /) -> None: ...

    @overload
    def add_objective(self, arg: pyoptinterface._src.core_ext.ScalarQuadraticFunction, /) -> None: ...

    @overload
    def add_objective(self, arg: pyoptinterface._src.core_ext.ScalarAffineFunction, /) -> None: ...

    @overload
    def add_objective(self, arg: pyoptinterface._src.core_ext.VariableIndex, /) -> None: ...

    @overload
    def add_objective(self, arg: float, /) -> None: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.ExprBuilder, clear_nl: bool = False) -> None: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.ScalarQuadraticFunction, clear_nl: bool = False) -> None: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.ScalarAffineFunction, clear_nl: bool = False) -> None: ...

    @overload
    def set_objective(self, expr: pyoptinterface._src.core_ext.VariableIndex, clear_nl: bool = False) -> None: ...

    @overload
    def set_objective(self, expr: float, clear_nl: bool = False) -> None: ...

    @overload
    def add_nl_objective(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex]) -> None: ...

    @overload
    def add_nl_objective(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[pyoptinterface._src.nlcore_ext.ParameterIndex]) -> None: ...

    @overload
    def add_nl_objective(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[float]) -> None: ...

    def clear_nl_objective(self) -> None: ...

    @overload
    def add_empty_nl_constraint(self, dim: int, sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_empty_nl_constraint(self, dim: int, sense: pyoptinterface._src.core_ext.ConstraintSense, lb: Sequence[float], ub: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_constraint(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_constraint(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[pyoptinterface._src.nlcore_ext.ParameterIndex], sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_constraint(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[float], sense: pyoptinterface._src.core_ext.ConstraintSense, rhs: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_constraint(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], sense: pyoptinterface._src.core_ext.ConstraintSense, lb: Sequence[float], ub: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_constraint(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[pyoptinterface._src.nlcore_ext.ParameterIndex], sense: pyoptinterface._src.core_ext.ConstraintSense, lb: Sequence[float], ub: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_constraint(self, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[float], sense: pyoptinterface._src.core_ext.ConstraintSense, lb: Sequence[float], ub: Sequence[float]) -> pyoptinterface._src.nlcore_ext.NLConstraintIndex: ...

    @overload
    def add_nl_expression(self, constraint: pyoptinterface._src.nlcore_ext.NLConstraintIndex, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[pyoptinterface._src.nlcore_ext.ParameterIndex]) -> None: ...

    @overload
    def add_nl_expression(self, constraint: pyoptinterface._src.nlcore_ext.NLConstraintIndex, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex], param: Sequence[float]) -> None: ...

    @overload
    def add_nl_expression(self, constraint: pyoptinterface._src.nlcore_ext.NLConstraintIndex, f: pyoptinterface._src.nlcore_ext.FunctionIndex, var: Sequence[pyoptinterface._src.core_ext.VariableIndex]) -> None: ...

    def set_raw_option_int(self, arg0: str, arg1: int, /) -> None: ...

    def set_raw_option_double(self, arg0: str, arg1: float, /) -> None: ...

    def set_raw_option_string(self, arg0: str, arg1: str, /) -> None: ...

def is_library_loaded() -> bool: ...

def load_library(arg: str, /) -> bool: ...
