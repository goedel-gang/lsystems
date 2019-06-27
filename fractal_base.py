"""
Abstract classes and instances to draw L-system fractals.
See [1], and the various other wikipedia pages on fractals.

[1]: https://en.wikipedia.org/wiki/L-system
"""

from collections import namedtuple, Counter

from matrix import Matrix

LSystemFractalTuple = namedtuple(
        "LSystemFractalTuple",
        "name start size_func rules draw_rules iterations")

FRACTAL_REGISTRY = []

class DummyTurtle(object):
    """
    Dummy turtle class, used to probe whether or not certain symbols correspond
    to steps. See the LSystemFractal class.

    Written in the most hacky, lazy way possible
    """
    def __init__(self):
        for i in """forward turn setheading_degrees save_state restore_state
                turn_degrees jump""".split():
            self.__dict__[i] = lambda *args: None

class LSystemFractal(LSystemFractalTuple):
    """
    Class representing an L-system fractal. This is a thin wrapper around the
    namedtuple that stores the fields, but additionally, this automatically
    registers any new fractals in the FRACTAL_REGISTRY. Fractals should expect
    to be drawn in a square box with side length 1 and one corner at (0, 0).
    The initial drawing state will be a turtle at (0, 0) facing in the direction
    of the x-axis. This can be modified by prefixing the initial string with a
    dummy "0" symbol, and using that symbol to perform setup. To execute
    multiple lines of setup in a single line, you can use a tuple.
    The turtle's forward() method should be scaled so that if you use forward(1)
    for each accounted drawing step, it will fit in the square. The setpos() and
    jump() methods take inputs in [0, 1]^2 though.
    Properties:
    start:      initial string
    size_func:  A function taking an integer (the number of iterations) and
                returning the expected largest dimension of the fractal (height
                or width), given in unit drawing steps.
    rules:      The rules for rewriting at each iteration, as a mapping object.
    draw_rules: The action to take when drawing for each symbol of the alphabet,
                as a mapping again, this time mapping to nullary functions. This
                is a function of a turtle-like object, the depth of the fractal,
                and the width of the square it should be drawn in, so the
                fractal can make adjustments for itself and access drawing
                methods. If a rule returns a truthy value when called, that is
                taken to mean that it has constituted a step.
    iterations: The default number of iterations to perform.
    """
    def __init__(self, *args, **kwargs):
        FRACTAL_REGISTRY.append(self)
        super(LSystemFractalTuple, self).__init__(*args, **kwargs)
        self.generate_transition_matrix()

    def generate_transition_matrix(self):
        """
        Generate the transition matrix for a single rewrite of an L-system. This
        can then be used to calculate the number of steps taken, in logarithmic
        time (in the number of iterations). This is because can use
        exponentiation by squaring on the transition matrix. This is an entirely
        unnecessary optimisation, but it's a fun one to implement.

        It's sometimes possible to actually solve the recurrence to give a
        totally closed form for the number of times each symbol occurs. This
        requires you to diagonalise the matrix though, which is generally messy
        as
        1) It doesn't leave you with integers (or necessarily rationals (or
           necessarily reals))
        2) This isn't solvable by an algorithm for an n by n matrix, as if you
           could solve arbitrary characteristic equations you could solve
           arbitrary polynomials.
        3) It isn't even asymptotically more optimal. In both cases you will
           need to perform exponentiation, although the exponentiation of a
           diagonal matrix obviously has the potential to be a little faster.
        """
        # TODO: probably we could do a little static analysis here in order to
        #       not consider symbols with no impact, although that's a little
        #       too on the graph theoretic side for now, methinks
        t = DummyTurtle()
        draw_rules = self.draw_rules(t, 1)
        self.symbols = list(draw_rules)
        # I don't even know if Python 2 has dictionary comprehensions, and I
        # don't really want to find out
        rule_counter = dict((symbol, Counter(self.rules.get(symbol, symbol)))
                for symbol in self.symbols)
        self.transition_matrix = Matrix(
                [[rule_counter[symbol_to][symbol_from]
                    for symbol_to in self.symbols]
                    for symbol_from in self.symbols])
        initial_counter = Counter(self.start)
        self.initial_vector = Matrix([[initial_counter[symbol]] for symbol in
                self.symbols])
        self.stepping_symbols = set(symbol for symbol in self.symbols if
                draw_rules[symbol]())

    def project_steps(self, iterations):
        """
        Project the number of steps needed for a certain number of iterations.
        In previous iterations, this function was crafted by hand for each
        fractal, but then I had to implement a matrix class to efficiently
        calculate this for the fern function, so I decided to automated the
        whole thing, and take out a point of failure.
        """
        return sum(i[0] for i, sym in
                zip(self.transition_matrix ** iterations * self.initial_vector,
                    self.symbols)
                if sym in self.stepping_symbols)

    def generate(self, depth):
        """
        Lazy generator that actually performs the substitution. It does so
        lazily, so it effectively needs to store only a call stack of the size
        of the depth.
        """
        if depth <= 0:
            for sym in self.start:
                yield sym
        else:
            for sym in self.generate(depth - 1):
                for gen_sym in self.rules.get(sym, sym):
                    yield gen_sym
