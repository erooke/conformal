import cmath
import math

""" 
Defines some basic conformal maps
"""

class ComplexMap():
    def __call__(self, z: complex) -> complex:
        raise NotImplementedError()


class Mobius(ComplexMap):
    """
    Mobius transformation.

    Parameters
    ----------
    a : complex number
    b : complex number
    c : complex number
    d : complex number

    Returns
    -------
    function from C -> C
    """
    def __init__(self, a: complex, b: complex, c: complex, d: complex) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __call__(self, z: complex) -> complex:
        return (self.a * z + self.b) / (self.c * z + self.d)


class Mobius_Inverse(ComplexMap):
    """
    Inverse of a Mobius transformation.

    Parameters
    ----------
    a : complex number
    b : complex number
    c : complex number
    d : complex number

    Returns
    -------
    function from C -> C
    """
    def __init__(self, a: complex, b: complex, c: complex, d: complex) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __call__(self, z: complex) -> complex:
        return  (self.d * z - self.b) / (-self.c * z + self.a)

class Spiral(ComplexMap):
    """
    The inverse of a spiral map.

    This is currenly broken, there is a discontinuity due to a branch
    cut which I think is fixable due to the fact we know something about
    the preimage in theory.

    The idea behind the math is that e^z sends vertical lines to circles,
    so we scale to make it so the diagonal of the image becomes 2pi in
    length, then rotate the image so the diagonal is vertical. In theory
    then mapping the points forward with e^z should cause the image to
    spiral.

    This function does all that in reverse:

    log z -> rotate by -phi -> scale mapping 2pi to the length of the diagonal

    Parameters
    ----------
    height: int
        height of the reigon you want to spiral
    width: int
        width of the reigon you want to spiral
    z: complex
        the image of the spiral map

    Returns
    -------
    complex preimage of z under the spiral
    """
    def __init__(self, height: int, width: int) -> None:
        self.diagonal = math.sqrt(height ** 2 + width ** 2)
        self.phi = math.atan2(height, width)

    def __call__(self, z: complex) -> complex:
        z = complex(math.log(abs(z)), cmath.phase(z))
        z *= cmath.exp(-1j * math.pi / 4)
        z *= (self.diagonal / (2 * math.pi))
        return z
