from typing import Final

from moto.stepfunctions.parser.asl.component.intrinsic.function.function import Function
from moto.stepfunctions.parser.asl.component.intrinsic.functionname.state_function_name_types import (
    StatesFunctionNameType,
)
from moto.stepfunctions.parser.asl.component.state.fail.error_decl import ErrorDecl
from moto.stepfunctions.parser.asl.eval.environment import Environment
from moto.stepfunctions.parser.asl.parse.intrinsic.intrinsic_parser import (
    IntrinsicParser,
)
from moto.stepfunctions.parser.asl.utils.json_path import JSONPathUtils

_STRING_RETURN_FUNCTIONS = {
    typ.name()
    for typ in [
        StatesFunctionNameType.Format,
        StatesFunctionNameType.JsonToString,
        StatesFunctionNameType.ArrayGetItem,
        StatesFunctionNameType.Base64Decode,
        StatesFunctionNameType.Base64Encode,
        StatesFunctionNameType.Hash,
        StatesFunctionNameType.UUID,
    ]
}


class ErrorPath(ErrorDecl): ...


class ErrorPathJsonPath(ErrorPath):
    def _eval_body(self, env: Environment) -> None:
        current_output = env.stack[-1]
        cause = JSONPathUtils.extract_json(self.value, current_output)
        env.stack.append(cause)


class ErrorPathIntrinsicFunction(ErrorPath):
    function: Final[Function]

    def __init__(self, value: str) -> None:
        super().__init__(value=value)
        self.function = IntrinsicParser.parse(value)
        if self.function.name.name not in _STRING_RETURN_FUNCTIONS:
            raise ValueError(
                f"Unsupported Intrinsic Function for ErrorPath declaration: '{self.value}'."
            )

    def _eval_body(self, env: Environment) -> None:
        self.function.eval(env=env)
