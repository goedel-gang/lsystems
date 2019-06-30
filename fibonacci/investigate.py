"""
Figuring out how the dimensions of the Fibonacci word fractal work.

Best run with PyPy3

Conclusions:
DF_3k     <=> https://oeis.org/A000129
DF_{3k+1} <=> https://oeis.org/A005409
DF_{3k+2} <=> https://oeis.org/A001333
F_
"""

CARDINAL_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def fibonacci_word(n):
    if n <= 0:
        yield 0
    else:
        for d in fibonacci_word(n - 1):
            if d == 1:
                yield 0
            else:
                yield 0
                yield 1

def mock_draw(word, verbose=False):
    min_x, min_y = max_x, max_y = x, y = 0, 0
    heading = 0
    for ind, d in enumerate(word, 1):
        dx, dy = CARDINAL_DIRECTIONS[heading % 4]
        verbose and print("index {}, digit {}".format(ind, d))
        verbose and print("x+dx (min-max): {}{:+} ({}-{})".format(
            x, dx, min_x, max_x))
        verbose and print("y+dy (min-max): {}{:+} ({}-{})".format(
            y, dy, min_y, max_y))
        x += dx
        y += dy
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        if d == 0:
            heading += (ind % 2) * 2 - 1
    return max_x - min_x, max_y - min_y, min_x, max_x, min_y, max_y

mock_draw(fibonacci_word(4), verbose=True)

for i in range(5):
    print(list(fibonacci_word(i)))

for i in range(30):
    info = mock_draw(fibonacci_word(i))
    print("{:5}: {:5}, {:5} ({:5} -- {:5}, {:5} -- {:5})".format(i, *info))
