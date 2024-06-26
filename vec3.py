from __future__ import annotations

import math as _math
import random as _random
import typing as _typing

from collections.abc import Iterator as _Iterator


def _clamp(num: float, min_val: float, max_val: float) -> float:
    return max(min(num, max_val), min_val)

class Vec3:
    __slots__ = 'x', 'y', 'z'

    """A three-dimensional vector represented as X Y Z coordinates."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self) -> _Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    @_typing.overload
    def __getitem__(self, item: int) -> float:
        ...

    @_typing.overload
    def __getitem__(self, item: slice) -> tuple[float, ...]:
        ...

    def __getitem__(self, item):
        return (self.x, self.y, self.z)[item]

    def __setitem__(self, key, value):
        if type(key) is slice:
            for i, attr in enumerate(['x', 'y', 'z'][key]):
                setattr(self, attr, value[i])
        else:
            setattr(self, ['x', 'y', 'z'][key], value)

    def __len__(self) -> int:
        return 3

    @property
    def mag(self) -> float:
        """The magnitude, or length of the vector. The distance between the coordinates and the origin.

        Alias of abs(self).

        :type: float
        """
        return self.__abs__()
    
    @property
    def mag_sq(self) -> float:
        """Squared magnitude, or length of the vector.
        
        Alias of self.dot(self).
        
        :type: float
        """
        return self.dot(self)

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    @_typing.overload
    def __mul__(self, other: Vec3) -> Vec3:
        ...
        
    @_typing.overload
    def __mul__(self, other: float) -> Vec3:
        ...
        
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            scalar = other
            return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> Vec3:
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __floordiv__(self, scalar: float) -> Vec3:
        return Vec3(self.x // scalar, self.y // scalar, self.z // scalar)

    def __abs__(self) -> float:
        return _math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def __round__(self, ndigits: int | None = None) -> Vec3:
        return Vec3(*(round(v, ndigits) for v in self))

    def __radd__(self, other: Vec3 | int) -> Vec3:
        """Reverse add. Required for functionality with sum()"""
        if other == 0:
            return self
        else:
            return self.__add__(_typing.cast(Vec3, other))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vec3) and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: object) -> bool:
        return not isinstance(other, Vec3) or self.x != other.x or self.y != other.y or self.z != other.z

    def from_magnitude(self, magnitude: float) -> Vec3:
        """Create a new Vector of the given magnitude by normalizing,
        then scaling the vector. The rotation remains unchanged.
        """
        return self.normalize() * magnitude

    def limit(self, maximum: float) -> Vec3:
        """Limit the magnitude of the vector to the passed maximum value."""
        if self.x ** 2 + self.y ** 2 + self.z ** 2 > maximum * maximum * maximum:
            return self.from_magnitude(maximum)
        return self

    def cross(self, other: Vec3) -> Vec3:
        """Calculate the cross product of this vector and another 3D vector."""
        return Vec3((self.y * other.z) - (self.z * other.y),
                    (self.z * other.x) - (self.x * other.z),
                    (self.x * other.y) - (self.y * other.x))

    def dot(self, other: Vec3) -> float:
        """Calculate the dot product of this vector and another 3D vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def lerp(self, other: Vec3, alpha: float) -> Vec3:
        """Create a new Vec3 linearly interpolated between this vector and another Vec3.

        The `alpha` parameter dictates the amount of interpolation.
        This should be a value between 0.0 (this vector) and 1.0 (other vector).
        For example; 0.5 is the midway point between both vectors.
        """
        return Vec3(self.x + (alpha * (other.x - self.x)),
                    self.y + (alpha * (other.y - self.y)),
                    self.z + (alpha * (other.z - self.z)))

    def distance(self, other: Vec3) -> float:
        """Get the distance between this vector and another 3D vector."""
        return _math.sqrt(((other.x - self.x) ** 2) +
                          ((other.y - self.y) ** 2) +
                          ((other.z - self.z) ** 2))

    def normalize(self) -> Vec3:
        """Normalize the vector to have a magnitude of 1. i.e. make it a unit vector."""
        try:
            d = self.__abs__()
            return Vec3(self.x / d, self.y / d, self.z / d)
        except ZeroDivisionError:
            return self

    def clamp(self, min_val: float, max_val: float) -> Vec3:
        """Restrict the value of the X, Y and Z components of the vector to be within the given values."""
        return Vec3(_clamp(self.x, min_val, max_val),
                    _clamp(self.y, min_val, max_val),
                    _clamp(self.z, min_val, max_val))
    
    def random(min: float = 0, max: float = 1) -> Vec3:
        x = _random.uniform(min, max)
        y = _random.uniform(min, max)
        z = _random.uniform(min, max)
        return Vec3(x, y, z)
    
    def rand_unit_vector() -> Vec3:
        z1 = _random.uniform(0, 1)
        z2 = _random.uniform(0, 1)
        th = _math.acos(1 - z1)
        pi = 2 * _math.pi * z2
        x = _math.cos(pi) * _math.sin(th)
        y = _math.sin(pi) * _math.sin(th)
        z = _math.cos(th)
        return Vec3(x, y, z)
        
    def rand_on_hemisphere(self) -> Vec3:
        on_unit_sphere = self.rand_unit_vector()
        if on_unit_sphere.dot(self) > 0.0: return on_unit_sphere
        else: return -on_unit_sphere
        
    def rand_in_unit_disk() -> Vec3:
        while True:
            p = Vec3(_random.uniform(-1,1), _random.uniform(-1,1), 0)
            if p.mag_sq < 1:
                return p
        
    def near_zero(self) -> bool:
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s
        
    def reflect(self, n: Vec3) -> Vec3:
        return self - n * 2 * self.dot(n)
    
    def refract(self, n: Vec3, etai_over_etat: float) -> Vec3:
        cos_theta = min(-self.dot(n), 1)
        r_out_perp =  (self + n * cos_theta) * etai_over_etat
        r_out_parallel = n * -_math.sqrt(abs(1.0 - r_out_perp.mag_sq))
        return r_out_perp + r_out_parallel
    
    def __getattr__(self, attrs: str) -> list:
        try:
            # Allow swizzled getting of attrs
            return [*(self['xyz'.index(c)] for c in attrs)]
        except Exception:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attrs}'"
            ) from None

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"

Point3 = Vec3
Color = Vec3