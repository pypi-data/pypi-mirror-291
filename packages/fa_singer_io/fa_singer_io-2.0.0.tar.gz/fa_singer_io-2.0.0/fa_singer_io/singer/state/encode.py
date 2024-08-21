from .core import (
    SingerState,
)
from fa_purity import (
    FrozenTools,
)
from fa_purity.json import (
    JsonObj,
    JsonPrimitive,
    JsonValue,
)


def encode_state(state: SingerState) -> JsonObj:
    return FrozenTools.freeze(
        {
            "type": JsonValue.from_primitive(JsonPrimitive.from_str("STATE")),
            "value": JsonValue.from_json(state.value),
        }
    )
