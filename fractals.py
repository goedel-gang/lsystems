"""
Using Python turtle to draw L-system fractals
It uses layered lazy generators so it is very memory-efficient - effectively
using a call-stack of the size of the number of iterations. See [1].

[1]: https://en.wikipedia.org/wiki/L-system
"""

from collections import namedtuple
from operator import mul

LSystemFractalTuple = namedtuple("LSystemFractalTuple",
                                 """name start size_func rules draw_rules
                                    iterations""")

FRACTAL_REGISTRY = []

class LSystemFractal(LSystemFractalTuple):
    """
    Class representing an L-system fractal. This is a thin wrapper around the
    namedtuple that stores the fields, but additionally, this automatically
    registers any new fractals in the FRACTAL_REGISTRY. Fractals should expect
    to be drawn in a square box with one corner at (0, 0), and the other corner
    accessible as a parameter to the appropriate functions.
    The initial drawing state will be a turtle at (0, 0) facing in the direction
    of the x-axis. This can be modified by prefixing the initial string with a
    dummy "0" symbol, and using that symbol to perform setup. To execute
    multiple lines of setup in a single line, you can use a tuple.
    Properties:
    start:      initial string
    size_func:  A function taking an integer (the number of iterations) and
                returning the expected number of steps to take. This is needed
                for colouring.
    rules:      The rules for rewriting at each iteration, as a mapping object.
    draw_rules: The action to take when drawing for each symbol of the alphabet,
                as a mapping again, this time mapping to nullary functions. This
                is a function of a turtle-like object, the depth of the fractal,
                and the width of the square it should be drawn in, so the
                fractal can make adjustments for itself and access drawing
                methods.
    iterations: The default number of iterations to perform.
    """
    def __init__(self, *args, **kwargs):
        FRACTAL_REGISTRY.append(self)
        super(LSystemFractalTuple, self).__init__(*args, **kwargs)

def substitute(sequence, rules):
    """
    Lazy generator that replaces a set of symbols in its iterable input as
    instructed. Very flexible/abstract - works so long as you have a correctly
    behaving lookup of "rules" for any symbols, which understand indexing, "in",
    "not in" and map to iterables of other symbols.
    """
    for symbol in sequence:
        if symbol not in rules:
            yield symbol
        else:
            for sym in rules[symbol]:
                yield sym

def nop():
    pass

sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F-G-G",
    lambda d: 3 ** d * 3,
    {"F": "F-G+F+G-F",
     "G": "GG"},
    lambda t, d, w: {"F": lambda: t.forward(w * 2 ** -d),
                     "G": lambda: t.forward(w * 2 ** -d),
                     "-": lambda: t.turn_degrees(+120),
                     "+": lambda: t.turn_degrees(-120)},
    9)

dragon = LSystemFractal(
    "The Dragon Curve",
    "0FX",
    lambda d: 2 ** d,
    {"X": "X+YF+",
     "Y": "-FX-Y"},
    lambda t, d, w: {"F": lambda: t.forward(w * 0.5 * 2 ** -(d / 2)),
                     "-": lambda: t.turn_degrees(+90),
                     "+": lambda: t.turn_degrees(-90),
                     "0": lambda: (t.turn_degrees(45 + 45 * d),
                                   t.jump(w * 0.35, w * 0.25)),
                     "X": nop,
                     "Y": nop},
    15)

class Matrix:
    """
    Very bare bones matrix class, doing just enough for debugging and the
    fern_steps function. This provides a nice asymptotically fast way to
    calculate the outcome of a bunch of linear transitions, which is useful in
    projecting the number of lines you will have to draw in an L-system.
    Realistically, it won't occur any overhead to simply compute it by brute
    force in linear time, and this is mostly just here for fun.

    Gotcha: it doesn't necessarily perform copying when raising to a power of 1.

    Doesn't perform any error checking.
    """
    def __init__(self, values):
        self.array = values

    def __mul__(self, other):
        """
        Matrix multiplication
        """
        return Matrix([[sum(map(mul, row, col))
                        for col in zip(*other.array)]
                        for row in self.array])

    @classmethod
    def identity(cls, n):
        """
        Get an n by n identity matrix
        """
        return cls([[int(x == y) for x in xrange(n)] for y in xrange(n)])

    def __pow__(self, n):
        """
        Logarithmic (in the exponent) time exponentiation, using "Exponentiation
        by Squaring". This is a divide and conquer strategy capitalising on the
        fact that M ^ (2n + 1) == M ^ n M ^ n M, and
                  M ^ 2n       == M ^ n M ^ n.
        """
        if n == 0:
            return self.identity(len(self.array))
        if n == 1:
            return self
        square = self ** (n // 2)
        if n & 1:
            return self * square * square
        return square * square

    def __str__(self):
        return "\n".join("[{}]".format(" ".join("{:3}".format(i) for i in row))
                for row in self.array)

def fern_steps(depth):
    r"""
    Helper function to calculate the number of steps for a Lindenmayer fern.
    This should be logarithmic in the number of iterations, as it uses
    exponentiation by squaring on the transition matrix. This is an entirely
    unnecessary optimisation, but it's a fun one to implement.

    Letting the state after `n` iterations be encoded in some matrix
          / F_n \ <- number of 'F's in the string at the `n`th iteration
    M_n = |     |
          \ X_n / <- number of 'X's "
    so then
          / 0 \
    M_0 = |   |
          \ 1 /
    and the transition to M_{n + 1} is encoded by
    M_{n + 1} = T M_n, where
        / 3  2 \
    T = |      |
        \ 0  4 /
    So then
    M_n = T ^ n M_0, and we can extract the value of F_n.

    Of course this could be inlined but then I would have to sacrifice this
    beautiful docstring.
    """
    return (Matrix([[3, 2], [0, 4]]) ** depth * Matrix([[0], [1]])).array[0][0]

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    fern_steps,
    {"X": "F+[[X]-X]-F[-FX]+X",
     "F": "FF"},
    # TODO: better approach to this
    lambda t, d, w: {"F": lambda: t.forward(w * 10 * 3 ** -(d)),
                     "-": lambda: t.turn_degrees(+25),
                     "+": lambda: t.turn_degrees(-25),
                     "X": nop,
                     "[": t.save_state,
                     "]": t.restore_state,
                     "0": lambda: (t.jump(w / 2, 0),
                                   t.setheading_degrees(90))},
    8)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "0F",
    lambda d: 2 ** d,
    {"F": "+F--F+"},
    lambda t, d, w: {"F": lambda: t.forward(w * 0.5 * 2 ** -(d / 2)),
                     "-": lambda: t.turn_degrees(-45),
                     "+": lambda: t.turn_degrees(+45),
                     "0": lambda: t.jump(0.25 * w, 0.25 * w)},
    14)

hilbert = LSystemFractal(
    "Hilbert's Space-Filling Curve",
    "A",
    lambda d: 4 ** d,
    {"A": "-BF+AFA+FB-",
     "B": "+AF-BFB-FA+"},
    lambda t, d, w: {"F": lambda: t.forward(w * 2 ** -(d)),
                     "A": nop,
                     "B": nop,
                     "-": lambda: t.turn_degrees(+90),
                     "+": lambda: t.turn_degrees(-90)},
    8)

sierp_hex = LSystemFractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "A",
    lambda d: 3 ** d,
    {"A": "B-A-B",
     "B": "A+B+A"},
    lambda t, d, w: {"A": lambda: t.forward(w * 2 ** -d),
                     "B": lambda: t.forward(w * 2 ** -d),
                     "-": lambda: t.turn_degrees(+60),
                     "+": lambda: t.turn_degrees(-60)},
    9)

koch = LSystemFractal(
    "Koch Snowflake",
    "0F--F--F",
    lambda d: 3 * 4 ** d,
    {"F": "F+F--F+F"},
    lambda t, d, w: {"F": lambda: t.forward(3 / (2 * sqrt(3))
                                          * w * 3 ** -d),
                     "-": lambda: t.turn_degrees(60),
                     "+": lambda: t.turn_degrees(-60),
                     "0": lambda: t.jump(0.5 * (1 - 3 / (2 * sqrt(3))) * w,
                                         0.25 * w)},
    7)

koch_square = LSystemFractal(
    "Square Koch Curve",
    "0F--F",
    lambda d: 2 * 5 ** d,
    {"F": "F+F-F-F+F"},
    lambda t, d, w: {"F": lambda: t.forward(w * 3 ** -d),
                     "-": lambda: t.turn_degrees(-90),
                     "+": lambda: t.turn_degrees(+90),
                     "0": lambda: t.jump(0, 0.5 * w)},
    7)
