from .._utils import (
    all_keys_in,
)
from .core import (
    SingerRecord,
)
from fa_purity import (
    Result,
    ResultE,
)
from fa_purity.json import (
    JsonObj,
    JsonPrimitiveUnfolder,
    JsonUnfolder,
    Unfolder,
)
from fa_singer_io.singer.errors import (
    MissingKeys,
)
from fa_singer_io.time import (
    DateTime,
)


def build_record(raw: JsonObj) -> ResultE[SingerRecord]:
    time_extracted = JsonUnfolder.optional(
        raw,
        "time_extracted",
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str),
    ).map(lambda m: m.map(DateTime.parse))
    stream = JsonUnfolder.require(
        raw,
        "stream",
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str),
    )
    record = JsonUnfolder.require(raw, "record", Unfolder.to_json)
    return time_extracted.bind(
        lambda t: stream.bind(
            lambda s: record.map(
                lambda r: SingerRecord(s, r, t.value_or(None))
            )
        )
    )
