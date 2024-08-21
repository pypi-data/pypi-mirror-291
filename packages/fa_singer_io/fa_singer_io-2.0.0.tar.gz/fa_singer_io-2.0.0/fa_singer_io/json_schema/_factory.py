from ._inner import (
    InnerJsonSchema,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from fa_purity import (
    cast_exception,
    FrozenDict,
    FrozenList,
    Result,
    ResultE,
    Unsafe,
)
from fa_purity.json import (
    JsonObj,
    JsonPrimitive,
    JsonValue,
    Unfolder,
)
from fa_singer_io.json_schema.core import (
    JsonSchema,
)
from jsonschema import (
    Draft4Validator,
    SchemaError,
)
from typing import (
    FrozenSet,
    Type,
)


class SupportedType(Enum):
    array = "array"
    boolean = "boolean"
    integer = "integer"
    null = "null"
    number = "number"
    object = "object"
    string = "string"


_encode_type = {
    bool: SupportedType.boolean,
    int: SupportedType.integer,
    type(None): SupportedType.null,
    Decimal: SupportedType.number,
    float: SupportedType.number,
    str: SupportedType.string,
}

PrimitiveTypes = (
    Type[bool]
    | Type[int]
    | Type[None]
    | Type[Decimal]
    | Type[float]
    | Type[str]
)


@dataclass(frozen=True)
class JSchemaFactory:
    @staticmethod
    def from_json(raw: JsonObj) -> ResultE[JsonSchema]:
        raw_dict = Unfolder.to_raw(JsonValue.from_json(raw))  # type: ignore[misc]
        try:
            Draft4Validator.check_schema(raw_dict)  # type: ignore[misc]
            validator = Draft4Validator(raw_dict)  # type: ignore[misc]
            draft = InnerJsonSchema(raw, validator)
            return Result.success(JsonSchema(draft))
        except SchemaError as err:  # type: ignore[misc]
            return Result.failure(cast_exception(err))

    @classmethod
    def multi_type(
        cls, types: FrozenSet[PrimitiveTypes]
    ) -> ResultE[JsonSchema]:
        if len(types) == 0:
            return Result.failure(Exception("Must specify a type"))
        _types: FrozenList[JsonValue] = tuple(
            JsonValue.from_primitive(
                JsonPrimitive.from_str(_encode_type[t].value)
            )
            for t in types
        )
        raw = {
            "type": JsonValue.from_list(_types)
            if len(_types) > 1
            else _types[0]
        }
        return Result.success(
            cls.from_json(FrozenDict(raw))
            .alt(Unsafe.raise_exception)
            .to_union()
        )

    @classmethod
    def from_prim_type(cls, p_type: PrimitiveTypes) -> JsonSchema:
        raw = {
            "type": JsonValue.from_primitive(
                JsonPrimitive.from_str(_encode_type[p_type].value)
            )
        }
        return (
            cls.from_json(FrozenDict(raw))
            .alt(Unsafe.raise_exception)
            .to_union()
        )

    @classmethod
    def opt_prim_type(cls, p_type: PrimitiveTypes) -> JsonSchema:
        return (
            cls.multi_type(frozenset([p_type, type(None)]))
            .alt(Unsafe.raise_exception)
            .to_union()
        )

    @classmethod
    def datetime_schema(cls) -> JsonSchema:
        json = {
            "type": JsonValue.from_primitive(
                JsonPrimitive.from_str(_encode_type[str].value)
            ),
            "format": JsonValue.from_primitive(
                JsonPrimitive.from_str("date-time")
            ),
        }
        return (
            cls.from_json(FrozenDict(json))
            .alt(Unsafe.raise_exception)
            .to_union()
        )

    @classmethod
    def opt_datetime_schema(cls) -> JsonSchema:
        base = cls.opt_prim_type(str).encode()
        json = {
            "type": base["type"],
            "format": JsonValue.from_primitive(
                JsonPrimitive.from_str("date-time")
            ),
        }
        return (
            cls.from_json(FrozenDict(json))
            .alt(Unsafe.raise_exception)
            .to_union()
        )

    @staticmethod
    def obj_schema(props: FrozenDict[str, JsonSchema]) -> JsonSchema:
        _props = FrozenDict(
            {k: JsonValue.from_json(v.encode()) for k, v in props.items()}
        )
        raw = {
            "properties": JsonValue.from_json(_props),
            "required": JsonValue.from_list(
                tuple(
                    JsonValue.from_primitive(JsonPrimitive.from_str(k))
                    for k in _props.keys()
                )
            ),
        }
        return (
            JSchemaFactory.from_json(FrozenDict(raw))
            .alt(Unsafe.raise_exception)
            .to_union()
        )
