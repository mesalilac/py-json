from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_json.parser import JsonData


def serialize(obj: JsonData) -> str:
    """Serialize dict or array into json."""
    raise NotImplementedError
