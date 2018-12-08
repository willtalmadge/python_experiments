"""
This approach accomplishes the same goal of not requiring stuff in the middle
to know about the end points. What's the disadvantage vs. the structural
approach?

The problem comes if I want to use a subset of a request.
"""
from typing import NamedTuple


class Name(NamedTuple):
    first: str
    last: str


class Address(NamedTuple):
    street: str
    state: str
    zip: str


class User(NamedTuple):
    name: Name
    address: Address


def is_in_california(zip: str) -> bool:
    return zip.startswith('902')


def is_user_john_in_california(first: str, zip: str) -> bool:
    return (
            first.lower() == 'john'
            and is_in_california(zip)
    )


my_address = Address(
    '100 green street',
    'CA',
    '90210'
)
my_user = User(
    Name('John', 'Smith'),
    my_address
)
print(is_in_california(my_address.zip))
print(is_in_california(my_user.address.zip))
print(is_user_john_in_california(my_user.name.first, my_user.address.zip))
