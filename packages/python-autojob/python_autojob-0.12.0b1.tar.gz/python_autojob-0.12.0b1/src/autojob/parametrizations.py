"""Represent a reference to a variable."""

from collections.abc import Callable
from collections.abc import Mapping
from functools import reduce
import logging
from typing import Annotated
from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import Field
from pydantic import GetCoreSchemaHandler
from pydantic import ValidatorFunctionWrapHandler
from pydantic_core import CoreSchema
from pydantic_core import core_schema

from autojob.utils.schemas import Unset

_T = TypeVar("_T")

logger = logging.getLogger(__name__)

AttributePath = Annotated[list[str], Field(min_length=1)]
AttributePaths = Annotated[list[AttributePath], Field(min_length=1)]


# ! Only single source VariableRefences are supported ATM
class VariableReference(Generic[_T]):
    """A reference to a variable.

    Args:
        set_path: A list of strings indicating the path to the variable
            to be set.
        get_path: A list of strings indicating the path to the variable
            to be obtained.
        get_paths: A list of lists of strings each indicating a path to
            a variable to be obtained.
        constant: A value to be used to set the variable.
        composer: A function that takes in an ``AttributePath`` and
            ``AttributePaths`` and returns a value.

    Example:
        >>> context = {
        ...     "a": {
        ...         "b": 4,
        ...     }
        ... }
        >>> ref = VariableReference(
        ...     set_path=["a"],
        ...     get_path=["a", "b"],
        ...     constant=4,
        ... )
        >>> ref.evaluate(context)
        4
    """

    def __init__(
        self,
        *,
        set_path: AttributePath,
        get_path: AttributePath | None = None,
        get_paths: AttributePaths | None = None,
        constant: Any = None,
        composer: Callable | None = None,
    ) -> None:
        """Instantiate a ``VariableReference``.

        Args:
            set_path: An ``AttributePath`` indicating the variable to set.
            get_path: An ``AttributePath`` indicating the source variable.
                Defaults to None.
            get_paths: A list of ``AttributePath`` s, each of which will be
                combined to the source variable. Defaults to None.
            constant: A constant value used to set the variable. Defaults to
                None.
            composer: A function that accepts the value of the source
                variable(s) and returns a value to be used to set the
                variable. Defaults to None.
        """
        self.set_path = set_path
        self.get_path = get_path
        self.get_paths = get_paths
        self.constant = constant
        self.composer = composer
        super().__init__()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Get a Pydantic schema."""
        set_path_schema = handler.generate_schema(AttributePath)
        get_path_schema = handler.generate_schema(AttributePath | None)
        get_paths_schema = handler.generate_schema(AttributePaths | None)
        constant_schema = handler.generate_schema(Any)
        composer_schema = handler.generate_schema(Callable | None)

        def _set_path(
            v: VariableReference[Any], handler: ValidatorFunctionWrapHandler
        ) -> VariableReference[Any]:
            v.set_path = handler(v.set_path)
            return v

        def _get_path(
            v: VariableReference[Any], handler: ValidatorFunctionWrapHandler
        ) -> VariableReference[Any]:
            v.get_path = (
                handler(v.get_path) if v.get_path is not None else v.get_path
            )
            return v

        def _get_paths(
            v: VariableReference[Any], handler: ValidatorFunctionWrapHandler
        ) -> VariableReference[Any]:
            v.get_paths = handler(v.get_paths)
            return v

        def _constant(
            v: VariableReference[Any], handler: ValidatorFunctionWrapHandler
        ) -> VariableReference[Any]:
            v.constant = handler(v.constant)
            return v

        def _composer(
            v: VariableReference[Any], handler: ValidatorFunctionWrapHandler
        ) -> VariableReference[Any]:
            v.composer = handler(v.composer)
            return v

        python_schema = core_schema.chain_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.no_info_wrap_validator_function(
                    _set_path, set_path_schema
                ),
                core_schema.no_info_wrap_validator_function(
                    _get_path, get_path_schema
                ),
                core_schema.no_info_wrap_validator_function(
                    _get_paths, get_paths_schema
                ),
                core_schema.no_info_wrap_validator_function(
                    _constant, constant_schema
                ),
                core_schema.no_info_wrap_validator_function(
                    _composer, composer_schema
                ),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=core_schema.chain_schema(
                [
                    core_schema.typed_dict_schema(
                        {
                            "set_path": core_schema.typed_dict_field(
                                set_path_schema
                            ),
                            "get_path": core_schema.typed_dict_field(
                                set_path_schema,
                                required=False,
                            ),
                            "get_paths": core_schema.typed_dict_field(
                                get_paths_schema,
                                required=False,
                            ),
                            # ! Use default JSON caster
                            "constant": core_schema.typed_dict_field(
                                constant_schema,
                                required=False,
                            ),
                            "composer": core_schema.typed_dict_field(
                                composer_schema,
                                required=False,
                            ),
                        }
                    ),
                    core_schema.no_info_before_validator_function(
                        lambda data: VariableReference(
                            set_path=data["set_path"],
                            get_path=data.get("get_path", None),
                            get_paths=data.get("get_paths", None),
                            constant=data.get("constant", None),
                            composer=data.get("composer", None),
                        ),
                        python_schema,
                    ),
                ]
            ),
            python_schema=python_schema,
        )

    def evaluate(self, context: dict[str, Any] | object) -> _T:
        """Evaluate a variable reference in the given context.

        Args:
            context: A dictionary (or object) containing values to be used to
                evaluate the ``VariableReference``.

        Raises:
            NotImplementedError: ``get_paths`` and ``composer``
            ``VariableReference`` s are not supported.

        Returns:
            The value.
        """

        # ! There should be a check upon Workflow creation for circular
        # ! references
        def _get(x, y):
            if isinstance(x, Mapping):
                return x.get(y)
            return getattr(x, y)

        if self.get_path is not None:
            value = reduce(
                lambda x, y: _get(x, y),
                self.get_path,
                context,
            )
        elif not all(x is None for x in (self.get_paths, self.composer)):
            raise NotImplementedError
        else:
            value = self.constant

        return value

    # TODO: implement for objects instead
    def set_input_value(
        self, context: dict[str, Any], shell: dict[str, Any]
    ) -> None:
        """Set the value of a key specified by the ``VariableReference``.

        This method modifies ``shell`` in place.

        Args:
            context: A dictionary containing values to be used to evaluate
                the ``VariableReference``.
            shell: A dictionary containing values to be set.
        """
        to_get = shell
        to_set = self.set_path[-1]

        for node in self.set_path[:-1]:
            if node not in to_get:
                to_get[node] = {}
            to_get = to_get[node]

        value = self.evaluate(context)

        if value == Unset:
            logger.info(f"Unsetting value: {to_set}")
            del to_get[to_set]
        else:
            logger.info(f"Setting value: {to_set} to: {value}")
            to_get[to_set] = value
