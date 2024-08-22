"""Pydantic schema utilities."""

import json
from typing import Annotated
from typing import Any

from ase import Atoms
from ase.io.jsonio import decode
from ase.io.jsonio import encode
from pydantic import BaseModel
from pydantic import GetCoreSchemaHandler
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import PydanticUndefined
from pydantic_core import core_schema

Unset: Any = PydanticUndefined


def atoms_as_dict(s: Atoms) -> dict:
    """Represent an :class:`ase.atoms.Atoms` object as a dictionary."""
    # Uses Monty's MSONable spec
    # Normally, we would want to this to be a wrapper around
    # atoms.todict() with @module and
    # @class key-value pairs inserted. However,
    # atoms.todict()/atoms.fromdict() does not currently
    # work properly with constraints.
    return {"@module": "ase.atoms", "@class": "Atoms", "atoms_json": encode(s)}


def atoms_from_dict(d: dict) -> Atoms:
    """Instantiate an :class:`ase.atoms.Atoms` object from a dictionary."""
    # Uses Monty's MSONable spec
    # Normally, we would want to have this be a wrapper around atoms.fromdict()
    # that just ignores the @module/@class key-value pairs. However,
    # atoms.todict()/atoms.fromdict()
    # does not currently work properly with constraints.
    return decode(d["atoms_json"])


class AtomsAnnotation(BaseModel):
    """The Pydantic-compatible annotation for an `ase.atoms.Atoms` object."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """Return a pydantic_core.CoreSchema.

        The schema behaves in the following ways:

        `Atoms` instances will be parsed as `Atoms` instances without any
            changes
        Everything else will be validated according to AtomsAnnotation
        Serialization is done by atoms.as_dict()
        """

        def validate_from_dict(value: dict | None) -> Atoms | None:
            if value is None:
                return value

            try:
                return atoms_from_dict(value)
            except json.JSONDecodeError as err:
                msg = "Unable to convert 'atoms' value to Atoms object"
                raise ValueError(msg) from err

        from_dict_schema = core_schema.chain_schema(
            [
                core_schema.dict_schema(),
                core_schema.no_info_plain_validator_function(
                    validate_from_dict
                ),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_dict_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(Atoms),
                    from_dict_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: atoms_as_dict(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """Get the Pydantic JSON schema."""
        # Use the same schema that would be used for `int`
        return handler(core_schema.dict_schema())


PydanticAtoms = Annotated[Atoms, AtomsAnnotation]


def hyphenate(v: str) -> str:
    """Replace underscores with hyphens."""
    return v.replace("_", "-")


def space_capitalize(v: str) -> str:
    """Replace underscores with spaces and capitalize."""
    return v.replace("_", " ").capitalize()
