"""
Instances of L-system fractals. See

- https://en.wikipedia.org/wiki/L-system
- http://paulbourke.net/fractals/lsys/
- https://youtu.be/E1B4UoSQMFw
"""

from fractal_base import LSystemFractal

def draw(*args):
    """
    Dummy function that returns True, for nicer semantics in defining L systems.
    You pass each thing you want to be executed as an argument. Generally I've
    favoured lambda functions over functools.partial because I think they're
    cooler.
    """
    return True

def nodraw(*args):
    """
    Similar to draw(). With no arguments, can act as a no-op
    """
    return False

def standard_rules(t, d, angle=90, additions={}):
    """
    Provide the "standard" rule set, given the angle and the turtle and depth
    arguments. Can also append further rules, which may override standard rules.
    """
    rules = {"F": lambda: draw(t.forward(1)),
             "G": lambda: draw(t.forward(1)),
             "-": lambda: nodraw(t.turn_degrees(-angle)),
             "+": lambda: nodraw(t.turn_degrees(angle)),
             "[": lambda: nodraw(t.save_state()),
             "]": lambda: nodraw(t.restore_state()),
             "X": nodraw,
             "Y": nodraw}
    rules.update(additions)
    return rules

sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F+G+G",
    lambda d: 2 ** d,
    {"F": "F+G-F-G+F",
     "G": "GG"},
    lambda t, d: standard_rules(t, d, 120),
    10)

dragon = LSystemFractal(
    "The Dragon Curve",
    "0[FX]+[FX]+[FX]+FX",
    lambda d: 2 * 2 ** (d / 2.0),
    {"X": "X-YF-",
     "Y": "+FX+Y"},
    lambda t, d: standard_rules(t, d, 90, additions=
                {"0": lambda: nodraw(t.jump(0.5, 0.5),
                                     t.turn_degrees(45 * (d % 2 + 1)))}),
    15)

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    # This is basically just noting that it doubles its dimension along each
    # branch, and that it has some limit it approaches at infinity, found
    # by trial and error. It would be nice to find this more exactly in terms of
    # trigonometric functions of 25 degrees. (TODO)
    lambda d: 2.718281828 * 2 ** d,
    {"X": "F-[[X]+X]+F[+FX]-X",
     "F": "FF"},
    lambda t, d: standard_rules(t, d, 25, additions=
                {"0": lambda: nodraw(t.jump(0.5, 0),
                                     t.setheading_degrees(90))}),
    8)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "0F",
    lambda d: 2 * 2 ** (d / 2.0),
    {"F": "+F--F+"},
    lambda t, d: standard_rules(t, d, 45, additions=
                {"0": lambda: nodraw(t.jump(0.25, 0.25))}),
    18)

hilbert = LSystemFractal(
    "Hilbert's Space-Filling Curve",
    "X",
    lambda d: 2 ** d - 1,
    {"X": "+YF-XFX-FY+",
     "Y": "-XF+YFY+FX-"},
    lambda t, d: standard_rules(t, d, 90),
    8)

sierp_hex = LSystemFractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "F",
    lambda d: 2 ** d,
    {"F": "G-F-G",
     "G": "F+G+F"},
    lambda t, d: standard_rules(t, d, (-1) ** d * 60),
    8)

koch = LSystemFractal(
    "Koch Snowflake",
    "0F++F++F",
    lambda d: 2 * sqrt(3) / 3 * 3 ** d,
    {"F": "F-F++F-F"},
    lambda t, d: standard_rules(t, d, 60, additions=
            {"0": lambda: nodraw(t.jump(0.5 * (1 - 3 / (2 * sqrt(3))), 0.25))}),
    8)

koch_square = LSystemFractal(
    "Square Koch Curve",
    "0F-F-F-F",
    lambda d: 2 * 3 ** d,
    {"F": "F+F-F-F+F"},
    lambda t, d: standard_rules(t, d, 90, additions=
            {"0": lambda: nodraw(t.jump(0.25, 0.75))}),
    6)

# TODO: ParametrisedLSystemFractal
binary_tree = LSystemFractal(
    "Binary Tree",
    "0F",
    # A messy, but not intrinsically hugely complicated pair of interlaced
    # geometric progressions
    # TODO: scale with depth, rather than assume infinity. Remember leaves are
    #       weird
    lambda d: 1 + 2 ** (d - 1) * 4 / 3 * (1 + 0.25 * sqrt(2)),
    {"G": "GG",
     "F": "G[+F]-F"},
    lambda t, d: standard_rules(t, d, 45, additions=
            {"0": lambda: nodraw(t.jump(0.5, 0), t.setheading_degrees(90))}),
    10)
