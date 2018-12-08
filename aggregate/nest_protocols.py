from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from typing_extensions import Protocol


class Name(Protocol):
    first: str
    last: str


class HasWand(Protocol):
    has_wand: bool


class NameProp(Protocol):
    @abstractmethod
    @property
    def name(self) -> Name: ...


class Wizard(NameProp, HasWand, Protocol): ...


def wand_report(arg: Wizard) -> None:
    print(arg.name.first)
    print(arg.name.last)
    if arg.has_wand:
        print('This wizard has a wand.')
    else:
        print('This wizard needs to visit Ollivanders')


@dataclass
class NameExtended:
    first: str
    last: str
    middle_names: List[str]


@dataclass
class DarkWizard:
    name: NameExtended
    at_large: bool
    power_level: int
    has_wand: bool = True


carl = DarkWizard(
    name=NameExtended(
        first='Carl',
        last='Fizzlbuz',
        middle_names=['Modfife']
    ),
    power_level=2,
    at_large=True,
)



wand_report(carl)
