from .core import (
    SingerSchema,
)
from fa_purity import (
    FrozenTools,
    Maybe,
)
from fa_purity.json import (
    JsonObj,
    JsonValueFactory,
)
from fa_purity.json._core.value import (
    RawUnfoldedJsonValue,
)
from typing import (
    Dict,
)


def encode_schema(schema: SingerSchema) -> JsonObj:
    bookmark_properties = (
        Maybe.from_optional(schema.bookmark_properties)
        .map(
            lambda s: FrozenTools.freeze(
                [JsonValueFactory.from_unfolded(item) for item in s]
            )
        )
        .to_result()
        .to_union()
    )
    raw_json: Dict[str, RawUnfoldedJsonValue] = {
        "type": "SCHEMA",
        "stream": schema.stream,
        "schema": schema.schema.encode(),
        "key_properties": FrozenTools.freeze(
            [
                JsonValueFactory.from_unfolded(item)
                for item in schema.key_properties
            ]
        ),
    }
    if bookmark_properties is not None:
        raw_json["bookmark_properties"] = bookmark_properties
    return FrozenTools.freeze(raw_json).map(
        lambda k: k, JsonValueFactory.from_unfolded
    )
