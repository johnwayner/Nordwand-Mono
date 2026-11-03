"""Math operators: minus, comparisons and approximations.

Built from the ASCII `-`, `=`, `<`, `>` and `~` so they match them.  Without
these a fallback font draws them, usually proportional, which knocks every
column after them out of alignment (e.g. a negative number in a table).
"""

from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen

from draw.chevron import draw_chevron
from draw.rect import draw_rect
from draw.symbols import draw_segment
from glyphs import Glyph
from glyphs.special.equals_sign import EqualsSignGlyph
from glyphs.special.greater_than_sign import GreaterThenSignGlyph
from glyphs.special.plus_sign import PlusSignGlyph
from glyphs.special.tilde import TildeGlyph


def bar(pen, dc, y, side_offset, stroke):
    so = side_offset * dc.window_width
    draw_rect(pen, so, y - stroke / 2, dc.window_width - so, y + stroke / 2)


class MinusSignGlyph(Glyph):
    """− -- the horizontal bar of `+`, so it is as wide as the plus."""

    name = "minus_sign"
    unicode = "0x2212"
    offset = 0

    def draw(self, pen, dc):
        p = PlusSignGlyph
        bar(pen, dc, dc.math, p.side_offset, p.stroke_ratio * dc.stroke_x)


class IdenticalToGlyph(Glyph):
    name = "identical_to"
    unicode = "0x2261"
    offset = 0
    gap = 0.38  # Distance between bars, relative to the x-height

    def draw(self, pen, dc):
        e = EqualsSignGlyph
        s = e.stroke_ratio * dc.stroke_x
        g = self.gap * dc.x_height
        for y in (dc.math - g, dc.math, dc.math + g):
            bar(pen, dc, y, e.side_offset, s)


class NotEqualToGlyph(Glyph):
    name = "not_equal_to"
    unicode = "0x2260"
    offset = 0
    slash_x = 0.2  # Horizontal reach of the slash from the centre, per width
    slash_y = 0.42  # Vertical reach of the slash from the math axis, per x-height

    def draw(self, pen, dc):
        EqualsSignGlyph().draw(pen, dc)
        w = dc.window_width
        dx, dy = self.slash_x * w, self.slash_y * dc.x_height
        s = self.diag_stroke_dampening(EqualsSignGlyph.stroke_ratio, dc.stroke_x)
        draw_segment(
            pen, (w / 2 - dx, dc.math - dy), (w / 2 + dx, dc.math + dy), s
        )


class LessThanOrEqualToGlyph(Glyph):
    """≤ -- a shorter `<` raised above a bar."""

    name = "less_than_or_equal_to"
    unicode = "0x2264"
    offset = 0
    points_right = False
    span = 0.44  # Chevron height, relative to the parenthesis length
    rise = 0.14  # Chevron centre above the math axis, relative to the x-height
    drop = 0.46  # Bar below the math axis, relative to the x-height

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="x_height", width_ratio=1)
        h = dc.parenthesis_length * self.span
        s = self.diag_stroke_dampening(
            GreaterThenSignGlyph.stroke_ratio, dc.stroke_x, coef=0.2
        )
        tip, back = (b.x2, b.x1) if self.points_right else (b.x1, b.x2)
        draw_chevron(pen, s, s, tip, back, dc.math + self.rise * dc.x_height, h, delta=s)
        e = EqualsSignGlyph
        bar(
            pen,
            dc,
            dc.math - self.drop * dc.x_height,
            e.side_offset,
            e.stroke_ratio * dc.stroke_x,
        )


class GreaterThanOrEqualToGlyph(LessThanOrEqualToGlyph):
    name = "greater_than_or_equal_to"
    unicode = "0x2265"
    points_right = True


class AlmostEqualToGlyph(TildeGlyph):
    """≈ -- two flattened tildes."""

    name = "almost_equal_to"
    unicode = "0x2248"
    height_ratio = 0.16
    gap = 0.4  # Distance between the tildes, relative to the x-height

    def draw(self, pen, dc):
        d = self.gap * dc.x_height / 2
        for dy in (d, -d):
            super().draw(TransformPen(pen, Transform().translate(0, dy)), dc)
