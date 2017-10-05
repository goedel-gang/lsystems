from hilbert import gen_l

directions = [ (sin(th * QUARTER_PI), cos(th * QUARTER_PI) ) for th in range(8) ]

class LevA:
    L = 0
    R = 1
    F = 2

RULES = {LevA.F: [LevA.R, LevA.F, LevA.L, LevA.L, LevA.F, LevA.R]}

def draw_lev(depth=10, width=1000, x=0.5, y=0.5, direction=0):
    tlines = 0
    exlines = float(1 << (depth - 1))
    twidth = sqrt(2 << depth) * 2
    x *= twidth
    y *= twidth
    strokeWeight(float(width) / twidth / 5.0)
    for action in gen_l(depth, pattern=[LevA.F], rules=RULES):
        if action == LevA.F:
            tlines += 1
            stroke(tlines * 255 / exlines, 255, 255)
            cx, cy = directions[direction % 8]
            nx = x + cx
            ny = y + cy
            line(x * width / twidth, y * width / twidth, nx * width / twidth, ny * width / twidth)
            x, y = nx, ny
            yield
        elif action == LevA.L:
            direction += 1
        elif action == LevA.R:
            direction -= 1
    print("done")