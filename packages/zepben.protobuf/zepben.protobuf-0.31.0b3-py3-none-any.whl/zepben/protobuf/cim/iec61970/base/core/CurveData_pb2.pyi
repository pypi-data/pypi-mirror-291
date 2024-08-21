from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CurveData(_message.Message):
    __slots__ = ["xvalue", "y1value", "y2value", "y3value"]
    XVALUE_FIELD_NUMBER: _ClassVar[int]
    Y1VALUE_FIELD_NUMBER: _ClassVar[int]
    Y2VALUE_FIELD_NUMBER: _ClassVar[int]
    Y3VALUE_FIELD_NUMBER: _ClassVar[int]
    xvalue: float
    y1value: float
    y2value: float
    y3value: float
    def __init__(self, xvalue: _Optional[float] = ..., y1value: _Optional[float] = ..., y2value: _Optional[float] = ..., y3value: _Optional[float] = ...) -> None: ...
