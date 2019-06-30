"""
Provides the Matrix class
"""

from operator import mul
from itertools import starmap, chain, repeat, izip

def intersperse_it(_it, int_it):
    """
    Intersperse some *iterable* in another iterable. The interspersing iterable
    should be persistent to iterations.
    """
    it = iter(_it)
    yield next(it)
    for i in it:
        for int_i in int_it:
            yield int_i
        yield i

class Matrix(object):
    """
    Very bare bones matrix class, doing just enough for debugging and the
    project_steps function. This provides a nice asymptotically fast way to
    calculate the outcome of a bunch of linear transitions, which is useful in
    projecting the number of lines you will have to draw in an L-system.
    Realistically, it won't incur any overhead to simply compute it by brute
    force in linear time, and this is mostly just here for fun.

    No restraints on the type of the elements of the matrix, so long as they
    support all the operations you want to use on them. (eg multiplication if
    you want to multiply the matrix, str() if you want to use str() on the
    matrix). This means that for example if you care about exact computation,
    you can just pass a fractions.Fraction.

    No kind of inversion implemented as yet.

    Gotcha: it doesn't necessarily perform deep copying when raising to a power
    of 1.

    Doesn't perform any error checking.
    """
    def __init__(self, values):
        self.array = values

    def __mul__(self, other):
        """
        Matrix multiplication
        """
        return Matrix([[sum(map(mul, row, col))
                        for col in izip(*other.array)]
                        for row in self.array])

    @classmethod
    def identity(cls, n):
        """
        Get an n by n identity matrix. Uses the kind of Kronecker delta-like
        property of booleans.
        """
        return cls([[int(x == y) for x in xrange(n)] for y in xrange(n)])

    def __pow__(self, n):
        """
        Logarithmic (in the exponent) time exponentiation, using "Exponentiation
        by Squaring". This is a divide and conquer strategy capitalising on the
        fact that M ^ (2n + 1) == M ^ n M ^ n M, and
                  M ^ 2n       == M ^ n M ^ n.
        Doesn't support negative or non-integral exponents.
        """
        if n == 0:
            return self.identity(len(self.array))
        if n == 1:
            return self
        square = self ** (n // 2)
        # shorthand for n % 2. Guarantees short-circuit as 0 <= n % 2 < 2,
        # necessarily.
        return self ** (n & 1) * square * square

    def spaced_str(self, n=1):
        """
        Format the matrix, with a set spacing between each row. This spacing is
        basically just so you can set it to 1 to make the string have an odd
        number of lines, so that it's easier to typeset with other things, but
        it's kept as `n` so that you can also set it to 0 without the need for
        code duplication in __str__.
        """
        if len(self.array) == 0:
            return "[]"
        elif len(self.array) == 1:
            delims = "[]",
        else:
            delims = chain(["/\\"],
                           repeat("||", len(self.array) - 2),
                           [r"\/"])
        widths = [max(len(str(i)) for i in col) for col in izip(*self.array)]
        return "\n".join("{}{}{}".format(ldelim,
                                         " ".join(starmap("{!s:>{}}".format,
                                                          izip(row, widths))),
                                         rdelim)
                for row, (ldelim, rdelim) in
                    intersperse_it(izip(self.array, delims),
                                   (([""] * len(self.array[0]), "||"),) * n))

    def __iter__(self):
        return iter(self.array)

    def __str__(self):
        return self.spaced_str(0)

    def __repr__(self):
        return "Matrix({!r})".format(self.array)

# test if the Matrix class is roughly working
if __name__ == "__main__":
    print Matrix.identity(1)
    print Matrix.identity(2)
    print Matrix.identity(3)
    print Matrix([ [1234, 342], [13, 3453] ]) * Matrix([ [1, 0], [0, 1] ])
    print (Matrix([ [1, 2], [3, 4] ]) ** 10).spaced_str()
    print (Matrix([ [1, 2, 3, 4] ])
         * Matrix([ [9, 10], [11, 12], [13, 14], [15, 16] ])).spaced_str(2)
    print (Matrix([ [1, 2, 3, 4], [5, 6, 7, 8] ])
         * Matrix([ [9], [11], [13], [15] ])).spaced_str(3)
    print Matrix([ [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12] ])
    print repr(Matrix([ [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12] ]))
