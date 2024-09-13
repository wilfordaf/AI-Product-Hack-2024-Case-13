from typing import Any, Mapping, Sequence, TypedDict


class TGenericResponse(TypedDict):
    header: Mapping[str, str]
    body: Mapping[str, Any] | Sequence[Mapping[str, Any]]
