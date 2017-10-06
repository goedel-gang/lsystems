from hilbert import gen_l, directions

class KocA:
    F = 0
    L = 1
    R = 2

RULES = {KocA.F: [KocA.F,
                  KocA.R,
                  KocA.F,
                  KocA.L,
                  KocA.F,
                  KocA.L,
                  KocA.F,
                  KocA.R,
                  KocA.F]}

def draw_koc(depth=10, width=1000, x=0, y=0, direction=1):
    tlines = 0
    exlines = float(5 ** (depth - 1))
    twidth = float(3 ** (depth - 1))
    x *= twidth
    y *= twidth
    strokeWeight(float(width) / twidth / 5.0)
    for action in gen_l(depth, pattern=[KocA.F], rules=RULES):
        if action == KocA.F:
            tlines += 1
            stroke(tlines * 255 / exlines, 255, 255)
            cx, cy = directions[direction % 4]
            nx = x + cx
            ny = y + cy
            line(x * width / twidth, y * width / twidth, nx * width / twidth, ny * width / twidth)
            x, y = nx, ny
            yield
        elif action == KocA.L:
            direction += 1
        elif action == KocA.R:
            direction -= 1
    print("done")