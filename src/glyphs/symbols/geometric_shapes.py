"""Circles, squares, triangles, media controls and ballot boxes.

Everything is centred on the math axis, like the middle dot and bullet.
"""

from math import sqrt

from draw.rect import draw_rect
from draw.symbols import (
    symbol_stroke,
    draw_half_disc,
    draw_polyline,
    draw_ring,
    draw_segment,
    draw_square,
    draw_triangle,
)
from draw.circle import draw_circle
from glyphs import Glyph


class GeometricGlyph(Glyph):
    offset = 0
    italic_skew = False
    size_ratio = 0.72  # Width of the shape, relative to the advance width
    stroke_ratio = 0.9  # Outline weight, relative to stroke_x
    outline = False

    def centre(self, dc):
        return dc.window_width / 2, dc.math

    def size(self, dc):
        return self.size_ratio * dc.window_width

    def stroke(self, dc):
        return symbol_stroke(dc, self.stroke_ratio)


# Circles


class BlackCircleGlyph(GeometricGlyph):
    name = "black_circle"
    unicode = "0x25CF"

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        r = self.size(dc) / 2
        if self.outline:
            draw_ring(pen, cx, cy, r, self.stroke(dc))
        else:
            draw_circle(pen, cx, cy, r)


class WhiteCircleGlyph(BlackCircleGlyph):
    name = "white_circle"
    unicode = "0x25CB"
    outline = True


class LargeCircleGlyph(BlackCircleGlyph):
    name = "large_circle"
    unicode = "0x25EF"
    size_ratio = 0.96
    outline = True


class BlackCircleForRecordGlyph(BlackCircleGlyph):
    name = "black_circle_for_record"
    unicode = "0x23FA"


class FisheyeGlyph(BlackCircleGlyph):
    name = "fisheye"
    unicode = "0x25C9"
    dot_ratio = 0.45  # Inner dot diameter, relative to the circle

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        r = self.size(dc) / 2
        draw_ring(pen, cx, cy, r, self.stroke(dc))
        draw_circle(pen, cx, cy, self.dot_ratio * r)


class HalfBlackCircleGlyph(GeometricGlyph):
    """Circle outline with the half facing `angle` filled."""

    angle = 180

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        r = self.size(dc) / 2
        draw_ring(pen, cx, cy, r, self.stroke(dc))
        draw_half_disc(pen, cx, cy, r, self.angle)


class CircleWithLeftHalfBlackGlyph(HalfBlackCircleGlyph):
    name = "circle_with_left_half_black"
    unicode = "0x25D0"
    angle = 180


class CircleWithRightHalfBlackGlyph(HalfBlackCircleGlyph):
    name = "circle_with_right_half_black"
    unicode = "0x25D1"
    angle = 0


class CircleWithLowerHalfBlackGlyph(HalfBlackCircleGlyph):
    name = "circle_with_lower_half_black"
    unicode = "0x25D2"
    angle = 270


class CircleWithUpperHalfBlackGlyph(HalfBlackCircleGlyph):
    name = "circle_with_upper_half_black"
    unicode = "0x25D3"
    angle = 90


# Squares


class BlackSquareGlyph(GeometricGlyph):
    name = "black_square"
    unicode = "0x25A0"
    size_ratio = 0.66

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        draw_square(
            pen, cx, cy, self.size(dc), self.stroke(dc) if self.outline else None
        )


class WhiteSquareGlyph(BlackSquareGlyph):
    name = "white_square"
    unicode = "0x25A1"
    outline = True


class BlackSmallSquareGlyph(BlackSquareGlyph):
    name = "black_small_square"
    unicode = "0x25AA"
    size_ratio = 0.36


class WhiteSmallSquareGlyph(BlackSmallSquareGlyph):
    name = "white_small_square"
    unicode = "0x25AB"
    outline = True
    stroke_ratio = 0.6


class BlackMediumSquareGlyph(BlackSquareGlyph):
    name = "black_medium_square"
    unicode = "0x25FC"
    size_ratio = 0.56


class WhiteMediumSquareGlyph(BlackMediumSquareGlyph):
    name = "white_medium_square"
    unicode = "0x25FB"
    outline = True


class BlackMediumSmallSquareGlyph(BlackSquareGlyph):
    name = "black_medium_small_square"
    unicode = "0x25FE"
    size_ratio = 0.46


class WhiteMediumSmallSquareGlyph(BlackMediumSmallSquareGlyph):
    name = "white_medium_small_square"
    unicode = "0x25FD"
    outline = True
    stroke_ratio = 0.75


class BlackVerySmallSquareGlyph(BlackSquareGlyph):
    name = "black_very_small_square"
    unicode = "0x2B1D"
    size_ratio = 0.24


class StopButtonGlyph(BlackSquareGlyph):
    name = "black_square_for_stop"
    unicode = "0x23F9"
    size_ratio = 0.6


class PauseButtonGlyph(GeometricGlyph):
    name = "double_vertical_bar"
    unicode = "0x23F8"
    size_ratio = 0.6
    bar_ratio = 0.34  # Bar width, relative to the size

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        h = self.size(dc) / 2
        b = self.bar_ratio * 2 * h
        draw_rect(pen, cx - h, cy - h, cx - h + b, cy + h)
        draw_rect(pen, cx + h - b, cy - h, cx + h, cy + h)


# Ballot boxes


class BallotBoxGlyph(GeometricGlyph):
    name = "ballot_box"
    unicode = "0x2610"
    size_ratio = 0.86
    stroke_ratio = 0.8
    mark = None

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        side, s = self.size(dc), self.stroke(dc)
        draw_square(pen, cx, cy, side, s)
        # Half-size of the mark: a fixed clearance inside the outline
        h = side / 2 - s - 0.75 * dc.default_stroke
        s = 0.85 * s
        if self.mark == "check":
            draw_polyline(
                pen,
                [(cx - h, cy), (cx - 0.25 * h, cy - 0.75 * h), (cx + h, cy + h)],
                s,
            )
        elif self.mark == "x":
            draw_segment(pen, (cx - h, cy - h), (cx + h, cy + h), s)
            draw_segment(pen, (cx - h, cy + h), (cx + h, cy - h), s)


class BallotBoxWithCheckGlyph(BallotBoxGlyph):
    name = "ballot_box_with_check"
    unicode = "0x2611"
    mark = "check"


class BallotBoxWithXGlyph(BallotBoxGlyph):
    name = "ballot_box_with_x"
    unicode = "0x2612"
    mark = "x"


# Triangles


class TriangleGlyph(GeometricGlyph):
    """Equilateral-ish triangle pointing `direction` (up/down/left/right)."""

    direction = "right"
    size_ratio = 0.72

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        # Pointing right: height `size` across, base `size * 2 / sqrt(3)` tall,
        # capped to the size so wide triangles do not overflow vertically
        h = self.size(dc)
        base = min(h * 2 / sqrt(3), h * 1.15)
        # Centre the triangle on its centroid
        pts = [(-h / 3, -base / 2), (2 * h / 3, 0), (-h / 3, base / 2)]
        rot = {
            "right": lambda x, y: (x, y),
            "left": lambda x, y: (-x, y),
            "up": lambda x, y: (y, x),
            "down": lambda x, y: (y, -x),
        }[self.direction]
        pts = [rot(x, y) for x, y in pts]
        # Visually centre on the bounding box rather than the centroid
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        ox, oy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        pts = [(cx + x - ox, cy + y - oy) for x, y in pts]
        draw_triangle(pen, pts, self.stroke(dc) if self.outline else None)


TRIANGLES = [
    # (code, name, direction, size_ratio, outline)
    (0x25B2, "black_up_pointing_triangle", "up", 0.72, False),
    (0x25B3, "white_up_pointing_triangle", "up", 0.72, True),
    (0x25B4, "black_up_pointing_small_triangle", "up", 0.46, False),
    (0x25B5, "white_up_pointing_small_triangle", "up", 0.46, True),
    (0x25B6, "black_right_pointing_triangle", "right", 0.72, False),
    (0x25B7, "white_right_pointing_triangle", "right", 0.72, True),
    (0x25B8, "black_right_pointing_small_triangle", "right", 0.46, False),
    (0x25B9, "white_right_pointing_small_triangle", "right", 0.46, True),
    (0x25BC, "black_down_pointing_triangle", "down", 0.72, False),
    (0x25BD, "white_down_pointing_triangle", "down", 0.72, True),
    (0x25BE, "black_down_pointing_small_triangle", "down", 0.46, False),
    (0x25BF, "white_down_pointing_small_triangle", "down", 0.46, True),
    (0x25C0, "black_left_pointing_triangle", "left", 0.72, False),
    (0x25C1, "white_left_pointing_triangle", "left", 0.72, True),
    (0x25C2, "black_left_pointing_small_triangle", "left", 0.46, False),
    (0x25C3, "white_left_pointing_small_triangle", "left", 0.46, True),
    (0x23F4, "black_medium_left_pointing_triangle", "left", 0.6, False),
    (0x23F5, "black_medium_right_pointing_triangle", "right", 0.6, False),
    (0x23F6, "black_medium_up_pointing_triangle", "up", 0.6, False),
    (0x23F7, "black_medium_down_pointing_triangle", "down", 0.6, False),
]

for _code, _name, _direction, _size, _outline in TRIANGLES:
    _cls = type(
        f"Triangle{_code:04X}Glyph",
        (TriangleGlyph,),
        {
            "name": _name,
            "unicode": hex(_code),
            "direction": _direction,
            "size_ratio": _size,
            "outline": _outline,
            "stroke_ratio": 0.8 if _size > 0.5 else 0.6,
        },
    )
    globals()[_cls.__name__] = _cls


class WarningSignGlyph(GeometricGlyph):
    name = "warning_sign"
    unicode = "0x26A0"
    size_ratio = 0.94
    stroke_ratio = 0.8

    def draw(self, pen, dc):
        w = dc.window_width
        s = self.stroke(dc)
        half = self.size(dc) / 2
        bottom = -20
        top = bottom + half * sqrt(3)
        draw_triangle(pen, [(w / 2 - half, bottom), (w / 2 + half, bottom), (w / 2, top)], s)
        # Exclamation mark
        b = symbol_stroke(dc, 0.9)
        dot_top = bottom + 2.2 * s + b
        draw_rect(pen, w / 2 - b / 2, bottom + 2.2 * s, w / 2 + b / 2, dot_top)
        draw_rect(pen, w / 2 - b / 2, dot_top + 0.8 * b, w / 2 + b / 2, top - 3.4 * s)
