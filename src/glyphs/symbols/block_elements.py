"""Block elements (U+2580-U+259F).

Blocks fill fractions of the full cell (window descent to window ascent) and
bleed past the cell edges they touch, so adjacent blocks merge seamlessly.
"""

from config import FontConfig as fc
from draw.rect import draw_rect
from glyphs import Glyph


class BlockGlyph(Glyph):
    """Union of rectangles given as cell fractions (x1, y1, x2, y2), y up."""

    offset = 0
    italic_skew = False
    bleed = 20
    rects = ()

    def draw(self, pen, dc):
        w = dc.window_width
        b, t = fc.window_descent, fc.window_ascent
        for fx1, fy1, fx2, fy2 in self.rects:
            x1, x2 = fx1 * w, fx2 * w
            y1, y2 = b + fy1 * (t - b), b + fy2 * (t - b)
            # Only bleed on the edges lying on the cell boundary
            x1 -= self.bleed if fx1 == 0 else 0
            x2 += self.bleed if fx2 == 1 else 0
            y1 -= self.bleed if fy1 == 0 else 0
            y2 += self.bleed if fy2 == 1 else 0
            draw_rect(pen, x1, y1, x2, y2)


UL, UR, LL, LR = (0, 0.5, 0.5, 1), (0.5, 0.5, 1, 1), (0, 0, 0.5, 0.5), (0.5, 0, 1, 0.5)

BLOCKS = {
    0x2580: ("upper_half_block", [(0, 0.5, 1, 1)]),
    **{
        0x2580 + i: (f"lower_{i}_eighths_block", [(0, 0, 1, i / 8)])
        for i in range(1, 8)
    },
    0x2588: ("full_block", [(0, 0, 1, 1)]),
    **{
        0x2588 + i: (f"left_{8 - i}_eighths_block", [(0, 0, (8 - i) / 8, 1)])
        for i in range(1, 8)
    },
    0x2590: ("right_half_block", [(0.5, 0, 1, 1)]),
    0x2594: ("upper_one_eighth_block", [(0, 7 / 8, 1, 1)]),
    0x2595: ("right_one_eighth_block", [(7 / 8, 0, 1, 1)]),
    0x2596: ("quadrant_lower_left", [LL]),
    0x2597: ("quadrant_lower_right", [LR]),
    0x2598: ("quadrant_upper_left", [UL]),
    0x2599: ("quadrant_upper_left_and_lower_left_and_lower_right", [UL, LL, LR]),
    0x259A: ("quadrant_upper_left_and_lower_right", [UL, LR]),
    0x259B: ("quadrant_upper_left_and_upper_right_and_lower_left", [UL, UR, LL]),
    0x259C: ("quadrant_upper_left_and_upper_right_and_lower_right", [UL, UR, LR]),
    0x259D: ("quadrant_upper_right", [UR]),
    0x259E: ("quadrant_upper_right_and_lower_left", [UR, LL]),
    0x259F: ("quadrant_upper_right_and_lower_left_and_lower_right", [UR, LL, LR]),
}

for _code, (_name, _rects) in BLOCKS.items():
    _cls = type(
        f"Block{_code:04X}Glyph",
        (BlockGlyph,),
        {"name": _name, "unicode": hex(_code), "rects": _rects},
    )
    globals()[_cls.__name__] = _cls


class ShadeGlyph(Glyph):
    """Shades as a grid of squares: `pattern` rows of 0/1, top row first."""

    offset = 0
    italic_skew = False
    columns = 4
    rows = 8

    def draw(self, pen, dc):
        w = dc.window_width
        b, t = fc.window_descent, fc.window_ascent
        cw, ch = w / self.columns, (t - b) / self.rows
        for r in range(self.rows):
            for c in range(self.columns):
                if self.filled(r, c):
                    y2 = t - r * ch
                    draw_rect(pen, c * cw, y2 - ch, (c + 1) * cw, y2)


class LightShadeGlyph(ShadeGlyph):
    name = "light_shade"
    unicode = "0x2591"

    def filled(self, r, c):
        return (r % 2 == 0) and ((c + r // 2) % 2 == 0)


class MediumShadeGlyph(ShadeGlyph):
    name = "medium_shade"
    unicode = "0x2592"

    def filled(self, r, c):
        return (r + c) % 2 == 0


class DarkShadeGlyph(ShadeGlyph):
    name = "dark_shade"
    unicode = "0x2593"

    def filled(self, r, c):
        return not ((r % 2 == 1) and ((c + r // 2) % 2 == 0))
