from dataclasses import dataclass
from typing import TextIO
from .parser import JsonData


@dataclass
class Json:
    @staticmethod
    def loads(s: str) -> JsonData:
        raise NotImplementedError

    @staticmethod
    def load(fp: TextIO) -> JsonData:
        raise NotImplementedError

    def dump(obj: JsonData, fp: TextIO) -> None:
        raise NotImplementedError

    def dumps(obj: JsonData) -> str:
        raise NotImplementedError
