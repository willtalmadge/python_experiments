from typing_extensions import Protocol


class First(Protocol):
    def first(self) -> str: ...


class Last(Protocol):
    def last(self) -> str: ...


class Name(First, Last, Protocol): ...


class Street(Protocol):
    def street(self) -> str: ...


class State(Protocol):
    def state(self) -> str: ...


class Zip(Protocol):
    def zip(self) -> str: ...


class Address(Street, State, Zip, Protocol): ...


class AddressProp(Protocol):
    def address(self) -> Address: ...


class User(Name, Address, Protocol): ...


def is_in_california(data: Zip) -> bool:
    return data.zip().startswith('902')


class Spec(First, Zip, Protocol): ...


def is_user_john_in_california(data: Spec) -> bool:
    return (
            data.first().lower() == 'john'
            and is_in_california(data)
    )


class MyName:
    def first(self) -> str:
        return 'John'

    def last(self) -> str:
        return 'Smith'


class MyAddress:
    def street(self) -> str:
        return '100 green street'

    def state(self) -> str:
        return 'CA'

    def zip(self) -> str:
        return '90210'


class MyUser(MyName, MyAddress): ...



print(is_in_california(MyUser()))
print(is_in_california(MyAddress()))
print(is_user_john_in_california(MyUser()))
