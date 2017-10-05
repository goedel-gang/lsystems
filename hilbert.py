directions = [(0, 1),
              (1, 0),
              (0, -1),
              (-1, 0)]

class HilA:
    F = 0
    L = 1
    R = 2
    A = 3
    B = 4

RULES = {HilA.A: [HilA.L,
                  HilA.B,
                  HilA.F,
                  HilA.R,
                  HilA.A,
                  HilA.F,
                  HilA.A,
                  HilA.R,
                  HilA.F,
                  HilA.B,
                  HilA.L],
         HilA.B: [HilA.R,
                  HilA.A,
                  HilA.F,
                  HilA.L,
                  HilA.B,
                  HilA.F,
                  HilA.B,
                  HilA.L,
                  HilA.F,
                  HilA.A,
                  HilA.R]}

def gen_l(depth, pattern=RULES[HilA.A], rules=RULES):
    if depth > 1:
        for i in pattern:
            if i in rules:
                for y in gen_l(depth - 1, pattern=rules[i], rules=rules):
                    yield y
            else:
               yield i
    else:
        for i in pattern:
            yield i

def draw_hil(depth=9, width=1000, x=0, y=0, direction=0):
    tlines = 0
    exlines = float(4 ** depth - 1)
    twidth = float(1 << depth)
    strokeWeight(float(width) / twidth / 5.0)
    for action in gen_l(depth):
        if action == HilA.F:
            tlines += 1
            stroke(tlines * 255 / exlines, 255, 255)
            cx, cy = directions[direction % 4]
            nx = x + cx
            ny = y + cy
            line(x * width / twidth, y * width / twidth, nx * width / twidth, ny * width / twidth)
            x, y = nx, ny
            yield
        elif action == HilA.L:
            direction += 1
        elif action == HilA.R:
            direction -= 1
    print("done")