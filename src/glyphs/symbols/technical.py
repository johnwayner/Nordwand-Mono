"""Arrows and miscellaneous technical / punctuation symbols."""

from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen

from config import FontConfig as fc
from draw.rect import draw_rect
from draw.symbols import draw_segment, draw_square
from glyphs import Glyph
from glyphs.special.middle_dot import MiddleDotGlyph
from glyphs.special.right_arrow import RightArrowGlyph


class RotatedRightArrowGlyph(RightArrowGlyph):
    """The right arrow turned about the centre of its cell on the math axis."""

    generated_only = True  # Only the rotated subclasses are glyphs
    italic_skew = False
    angle = 0

    def draw(self, pen, dc):
        t = Transform().translate(dc.window_width / 2, dc.math)
        t = t.rotate(self.angle * 3.141592653589793 / 180)
        t = t.translate(-dc.window_width / 2, -dc.math)
        super().draw(TransformPen(pen, t), dc)


class LeftArrowGlyph(RotatedRightArrowGlyph):
    name = "left_arrow"
    generated_only = False
    unicode = "0x2190"
    angle = 180


class UpArrowGlyph(RotatedRightArrowGlyph):
    name = "up_arrow"
    generated_only = False
    unicode = "0x2191"
    angle = 90


class DownArrowGlyph(RotatedRightArrowGlyph):
    name = "down_arrow"
    generated_only = False
    unicode = "0x2193"
    angle = 270


class BottomLeftCornerGlyph(Glyph):
    """⎿ -- a corner from the ascender down to the math axis, then to the
    right edge of the cell (it leads into the text that follows)."""

    name = "bottom_left_corner"
    unicode = "0x23BF"
    offset = 0
    italic_skew = False
    x_ratio = 0.4  # Position of the vertical stroke, relative to the width

    def draw(self, pen, dc):
        x = self.x_ratio * dc.window_width
        sx, sy = dc.stroke_x, dc.stroke_y
        y = dc.math
        draw_rect(pen, x - sx / 2, y - sy / 2, x + sx / 2, dc.ascent)
        draw_rect(pen, x - sx / 2, y - sy / 2, dc.window_width, y + sy / 2)


class HorizontalLineExtensionGlyph(Glyph):
    name = "horizontal_line_extension"
    unicode = "0x23AF"
    offset = 0
    italic_skew = False
    bleed = 20

    def draw(self, pen, dc):
        s = dc.stroke_y
        draw_rect(
            pen, -self.bleed, dc.math - s / 2, dc.window_width + self.bleed, dc.math + s / 2
        )


class ThereforeGlyph(Glyph):
    """Three middle-dot sized squares in a triangle."""

    name = "therefore"
    unicode = "0x2234"
    offset = 0
    italic_skew = False
    spread = 0.26  # Horizontal distance of the outer dots from the centre
    pointing_up = True

    def draw(self, pen, dc):
        w = dc.window_width
        s = MiddleDotGlyph.stroke_ratio * dc.stroke_x
        low, high = s / 2, dc.x_height - s / 2
        apex, base = (high, low) if self.pointing_up else (low, high)
        draw_square(pen, w / 2, apex, s)
        draw_square(pen, w / 2 - self.spread * w, base, s)
        draw_square(pen, w / 2 + self.spread * w, base, s)


class BecauseGlyph(ThereforeGlyph):
    name = "because"
    unicode = "0x2235"
    pointing_up = False


class ReferenceMarkGlyph(Glyph):
    """※ -- a saltire with a dot in each of its four openings."""

    name = "reference_mark"
    unicode = "0x203B"
    offset = 0
    italic_skew = False
    size_ratio = 0.72

    def draw(self, pen, dc):
        w = dc.window_width
        cx, cy = w / 2, dc.math
        h = self.size_ratio * w / 2
        s = 0.8 * dc.stroke_x
        draw_segment(pen, (cx - h, cy - h), (cx + h, cy + h), s)
        draw_segment(pen, (cx - h, cy + h), (cx + h, cy - h), s)
        d = 1.3 * dc.stroke_x
        o = 0.72 * h
        for dx, dy in ((o, 0), (-o, 0), (0, o), (0, -o)):
            draw_square(pen, cx + dx, cy + dy, d)


class TwoJoinedSquaresGlyph(Glyph):
    """⧉ -- two overlapping square outlines."""

    name = "two_joined_squares"
    unicode = "0x29C9"
    offset = 0
    italic_skew = False
    size_ratio = 0.56
    shift_ratio = 0.3

    def draw(self, pen, dc):
        w = dc.window_width
        side = self.size_ratio * w
        d = self.shift_ratio * w / 2
        s = 0.75 * dc.stroke_x
        draw_square(pen, w / 2 - d, dc.math + d, side, s)
        draw_square(pen, w / 2 + d, dc.math - d, side, s)
