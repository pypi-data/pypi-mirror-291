# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
#### Maybe and Either Monads

Functional data types to use in lieu of exceptions.
"""

from __future__ import annotations

__all__ = [ 'MB', 'XOR', 'mb_to_xor', 'xor_to_mb' ]

from typing import Callable, cast, Final, Generic, Iterator, Never, TypeVar
from .nada import Nada, nada

T = TypeVar('T')
S = TypeVar('S')
L = TypeVar('L')
R = TypeVar('R')

class MB(Generic[T]):
    """
    #### Maybe Monad

    Class representing a potentially missing value.

    * where `MB(value)` contains a possible value of type `~T`
    * `MB( )` semantically represent a non-existent or missing value
    * implementation wise `MB( )` contains an inaccessible sentinel value
    * immutable, a MB does not change after being created
    * immutable semantics, map and flatMap produce new instances
    * two MB values only return equal if both ...

    """
    __slots__ = '_value',

    def __init__(self, value: T|Nada=nada) -> None:
        self._value = value

    def __bool__(self) -> bool:
        return not self._value is nada

    def __iter__(self) -> Iterator[T]:
        if self:
            yield cast(T, self._value)

    def __repr__(self) -> str:
        if self:
            return 'MB(' + repr(self._value) + ')'
        else:
            return 'MB()'

    def __len__(self) -> int:
        return (1 if self else 0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._value is other._value:
            return True
        return self._value == other._value

    def get(self, alt: T|Nada=nada) -> T|Never:
        """
        ##### Get an alternate value for the non-existent value.

        * if given, return an alternate value of type ~T
        * otherwise, raises `ValueError`
        * will happily return `None` or `()` as sentinel values
        """
        if self._value is not nada:
            return cast(T, self._value)
        else:
            if alt is not nada:
                return cast(T, alt)
            else:
                raise ValueError('Alternate return type not provided.')

    def map(self, f: Callable[[T], S]) -> MB[S]:
        """
        #### Map over the `MB`

        Map MB function f over the 0 or 1 elements of this data structure.
        """
        return (MB(f(cast(T, self._value))) if self else MB())

    def flatmap(self, f: Callable[[T], MB[S]]) -> MB[S]:
        """Map MB with function f and flatten."""
        return (f(cast(T, self._value)) if self else MB())

class XOR(Generic[L, R]):
    """
    #### Either Monad

    Class that can semantically contains either a "left" value or "right" value,
    but not both.

    * implements a left biased Either Monad
    * `XOR(left, right)` produces a "left" and default potential "right" value
    * `XOR(left)` produces a "left" value
    * `XOR(right=right)` produces a "right" value
    * in a Boolean context, returns True if a "left", False if a "right"
    * immutable, an XOR does not change after being created
    * immutable semantics, map & flatMap return new instances
    * raises ValueError if both "left" and "right" values are not given
    * raises ValueError if both if a potential "right" value is not given

    """
    __slots__ = '_left', '_right'

    def __init__(self
            , left: L|Nada=nada
            , right: R|Nada=nada):

        if left == nada == right:
            raise ValueError('XOR: neither left nor right values provided')
        self._left, self._right = left, right

    def __bool__(self) -> bool:
        """Predicate to determine if the XOR contains a "left" or a "right".

        * true if the XOR is a "left"
        * false if the XOR is a "right"
        """
        return self._left is not nada

    def __iter__(self) -> Iterator[L]:
        """Yields its value if the XOR is a "left"."""
        if self._left is not nada:
            yield cast(L, self._left)

    def __repr__(self) -> str:
        return 'XOR(' + repr(self._left) + ', ' + repr(self._right) + ')'

    def __str__(self) -> str:
        if self:
            return '< ' + str(self._left) + ' | >'
        else:
            return '< | ' + str(self._right) + ' >'

    def __len__(self) -> int:
        """Semantically, an XOR always contains just one value."""
        return 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self and other:
            if self._left is other._left:
                return True
            return self._left == other._left
        elif not self and not other:
            if self._right is other._right:
                return True
            return self._right == other._right
        else:
            return False

    def get(self, alt: L|Nada=nada) -> L:
        """
        ##### Get value if a Left.

        * if the XOR is a left, return its value
        * otherwise, return alt if it is provided
        * raises `ValueError` if alternate value needed but not provided

        """
        if self._left is nada:
            if alt is nada:
                raise ValueError('Alternate return value needed but not provided.')
            else:
                return cast(L, alt)
        else:
            return cast(L, self._left)

    def getRight(self, alt: R|Nada=nada) -> R:
        """
        ##### Get value if `XOR` is a Right.

        * if XOR is a right, return its value
        * otherwise return an alternate value of type ~R
        * raises `ValueError` if alternate value needed but not provided

        """
        if not self:
            if self._right is not nada:
                return cast(R, self._right)
            elif alt is not nada:
                return cast(R, alt)
            else:
                raise ValueError('Alternate return type needed but not provided.')
        else:
            if alt is not nada:
                return cast(R, alt)
            else:
                raise ValueError('Alternate return type needed but not provided.')

    def getDefaultRight(self) -> R:
        """
        ##### Get default right value

        Get value if a "right" otherwise get the default "right" value.
        """
        return cast(R, self._right)

    def map(self, f: Callable[[L], S], right: R|Nada=nada) -> XOR[S, R]:
        """
        ##### Map over an XOR.

        TODO: catch any errors `f` may throw

        * if `XOR` is a "left" then map `f`
          * if `f` successful, return a "left" XOR[S, R]
          * if `f` unsuccessful and `right` given, return `XOR(right=right)`
          * if `f` unsuccessful and `right` not given, return `XOR(right=self.right)`
        * if `XOR` is a "right"
          * if `right` is given, return `XOR(right=right)`
          * if `right` is not given, return `XOR(right=self.right)`

        """
        if self._left is nada:
            if right is nada:
                return XOR(right=self._right)
            else:
                return XOR(right=right)

        if right is nada:
            return XOR(f(cast(L, self._left)), self._right)
        else:
            return XOR(f(cast(L, self._left)), right)

    def mapRight(self, g: Callable[[R], R]) -> XOR[L, R]:
        """Map over a "right" value."""
        if self._left is nada:
            return XOR(nada, g(cast(R,self._right)))
        return self

    def flatMap(self, f: Callable[[L], XOR[S, R]]) -> XOR[S, R]:
        """Map and flatten a Left value, propagate Right values."""
        if self._left is nada:
            return XOR(nada, self._right)
        else:
            return f(cast(L, self._left))

# Conversion functions

def mb_to_xor(m: MB[T], right: R) -> XOR[T, R]:
    """
    #### Convert a MB to an XOR.

    """
    if m:
        return XOR(m.get(), right)
    else:
        return XOR(nada, right)

def xor_to_mb(e: XOR[T,S]) -> MB[T]:
    """
    ####Convert an XOR to a MB.

    """
    if e:
        return MB(e.get())
    else:
        return MB()
