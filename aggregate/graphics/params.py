from abc import abstractmethod
from dataclasses import dataclass

from typing_extensions import Protocol


# The following notation looks like dataclasses, but it is a particular
# notation allowed by PEP 544 to specify the members that implement these
# protocols. To avoid any ambiguity these do specify instance variables.

class PWidth(Protocol):
    width: float


class PHeight(Protocol):
    height: float


class PX(Protocol):
    x: float


class PY(Protocol):
    y: float


class PColor(Protocol):
    r: float
    g: float
    b: float
    a: float


@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float


# This property had to be made read only to avoid a mypy error. See:
# https://github.com/python/mypy/issues/5998
class PColorProp(Protocol):
    @abstractmethod
    @property
    def color(self) -> PColor: ...


class PPoint(PX, PY, Protocol): ...


@dataclass
class Point:
    x: float
    y: float


class PointProp(Protocol):
    @abstractmethod
    @property
    def point(self) -> PPoint: ...


class PRectangle(PPoint, PWidth, PHeight, Protocol): ...


@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float


class PRectangleProp(Protocol):
    @abstractmethod
    @property
    def rect(self) -> PRectangle: ...
