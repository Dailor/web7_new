def get_scale(p1, p2):
    (x1, y1), (x2, y2) = map(lambda x: map(float, x), (p1, p2))
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx, dy
