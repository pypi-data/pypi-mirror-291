from fa_purity import (
    Cmd,
)
from fa_purity.json import (
    JsonObj,
    JsonUnfolder,
)
from fa_singer_io.singer import (
    SingerMessage,
)
from fa_singer_io.singer.record.core import (
    SingerRecord,
)
from fa_singer_io.singer.record.encode import (
    encode_record,
)
from fa_singer_io.singer.schema.core import (
    SingerSchema,
)
from fa_singer_io.singer.schema.encode import (
    encode_schema,
)
from fa_singer_io.singer.state.encode import (
    encode_state,
)
from typing import (
    IO,
)


def encode(singer: SingerMessage) -> JsonObj:
    return singer.map(encode_record, encode_schema, encode_state)


def emit(target: IO[str], singer: SingerMessage) -> Cmd[None]:
    def _action() -> None:
        target.write(JsonUnfolder.dumps(encode(singer)))
        target.write("\n")

    return Cmd.wrap_impure(_action)
