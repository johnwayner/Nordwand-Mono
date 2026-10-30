"""Drawing helpers for geometric symbols. Contours are drawn counterclockwise,
holes clockwise, so overlapping pieces union under the nonzero rule."""

from math import asin, cos, hypot, pi, radians, sin, sqrt

from draw.circle import draw_circle
from draw.polygon import draw_polygon
from draw.rect import draw_rect


def symbol_stroke(dc, ratio=1.0, damping=0.5):
    """Stroke for symbol details: `ratio` of the regular stroke_x, changing
    with the weight at `damping` times the rate of the text strokes, so small
    symbols stay open in heavy weights and visible in light ones."""
    return ratio * (dc.default_stroke + damping * (dc.stroke_x - dc.default_stroke))


def ccw(points):
    """Return the polygon's points in counterclockwise order."""
    area = sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1])
    )
    return points if area > 0 else points[::-1]


def draw_segment(pen, p1, p2, w, ext1=0, ext2=0):
    """A straight stroke of width `w` from p1 to p2, butt ends extended by
    ext1 / ext2 along its direction."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy * w / 2, ux * w / 2
    a = (p1[0] - ux * ext1, p1[1] - uy * ext1)
    b = (p2[0] + ux * ext2, p2[1] + uy * ext2)
    draw_polygon(
        pen,
        [
            (a[0] - nx, a[1] - ny),
            (b[0] - nx, b[1] - ny),
            (b[0] + nx, b[1] + ny),
            (a[0] + nx, a[1] + ny),
        ],
    )


def draw_polyline(pen, points, w):
    """Connected strokes; inner joints are covered by extending each end."""
    for i, (p1, p2) in enumerate(zip(points, points[1:])):
        draw_segment(
            pen,
            p1,
            p2,
            w,
            ext1=w / 2 if i > 0 else 0,
            ext2=w / 2 if i < len(points) - 2 else 0,
        )


def draw_ring(pen, cx, cy, r, w):
    """Circle outline of radius `r` (outer edge) and thickness `w`."""
    draw_circle(pen, cx, cy, r)
    draw_circle(pen, cx, cy, r - w, clockwise=True)


def draw_square(pen, cx, cy, side, w=None):
    """Filled square, or its outline of thickness `w`."""
    h = side / 2
    draw_rect(pen, cx - h, cy - h, cx + h, cy + h)
    if w is not None:
        draw_rect(pen, cx - h + w, cy - h + w, cx + h - w, cy + h - w, clockwise=True)


def draw_half_disc(pen, cx, cy, r, angle):
    """Half disc whose round side faces `angle` degrees (0 = right)."""
    k = 4 * (sqrt(2) - 1) / 3
    a = radians(angle)

    def pt(x, y):
        return (cx + x * cos(a) - y * sin(a), cy + x * sin(a) + y * cos(a))

    pen.moveTo(pt(0, -r))
    pen.curveTo(pt(k * r, -r), pt(r, -k * r), pt(r, 0))
    pen.curveTo(pt(r, k * r), pt(k * r, r), pt(0, r))
    pen.closePath()


def draw_triangle(pen, points, w=None):
    """Filled triangle, or its outline of thickness `w` (inset about the
    incentre, so all three sides keep the same thickness)."""
    points = ccw(list(points))
    draw_polygon(pen, points)
    if w is None:
        return
    (ax, ay), (bx, by), (cx, cy) = points
    a = hypot(bx - cx, by - cy)
    b = hypot(ax - cx, ay - cy)
    c = hypot(ax - bx, ay - by)
    p = a + b + c
    ix, iy = (a * ax + b * bx + c * cx) / p, (a * ay + b * by + c * cy) / p
    area = abs((bx - ax) * (cy - ay) - (cx - ax) * (by - ay)) / 2
    r = 2 * area / p
    k = (r - w) / r
    inner = [(ix + (x - ix) * k, iy + (y - iy) * k) for x, y in points]
    draw_polygon(pen, inner[::-1])


def regular_points(cx, cy, r, n, start=90):
    """Vertices of a regular polygon, counterclockwise from `start` degrees."""
    return [
        (cx + r * cos(radians(start + 360 * i / n)), cy + r * sin(radians(start + 360 * i / n)))
        for i in range(n)
    ]


def draw_star(pen, cx, cy, r_outer, r_inner, n, start=90):
    """Filled star with `n` points."""
    points = []
    for i in range(2 * n):
        r = r_outer if i % 2 == 0 else r_inner
        a = radians(start) + pi * i / n
        points.append((cx + r * cos(a), cy + r * sin(a)))
    draw_polygon(pen, points)


def draw_teardrop(pen, cx, cy, angle, length, r_end):
    """Teardrop spoke from a point at (cx, cy) to a round end of radius
    `r_end`, `length` away (outer edge) in direction `angle` degrees."""
    d = length - r_end
    a = radians(angle)
    ex, ey = cx + d * cos(a), cy + d * sin(a)
    draw_circle(pen, ex, ey, r_end)
    alpha = asin(r_end / d)
    t = sqrt(d * d - r_end * r_end)
    draw_polygon(
        pen,
        [
            (cx, cy),
            (cx + t * cos(a - alpha), cy + t * sin(a - alpha)),
            (cx + t * cos(a + alpha), cy + t * sin(a + alpha)),
        ],
    )
