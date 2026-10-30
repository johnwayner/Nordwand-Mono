"""Asterisks, stars, check marks and ballot crosses (Dingbats block).

The spoked asterisks and the star are drawn as one family centred on the
middle dot, so that the sequence · ✢ ✳ ✶ ✻ ✽ (a common terminal spinner)
reads as one shape blooming, with no jumps in position or size.
"""

from draw.symbols import (
    symbol_stroke,
    draw_polyline,
    draw_segment,
    draw_star,
    draw_teardrop,
)
from glyphs import Glyph


class DingbatGlyph(Glyph):
    offset = 0
    italic_skew = False
    radius_ratio = 0.46  # Outer radius, relative to the advance width

    def centre(self, dc):
        return dc.window_width / 2, dc.math

    def radius(self, dc):
        return self.radius_ratio * dc.window_width


class TeardropAsteriskGlyph(DingbatGlyph):
    """Teardrop spokes meeting at a point in the centre."""

    spokes = 8
    start = 90
    end_ratio = 0.17  # Radius of the round ends, relative to the outer radius

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        r = self.radius(dc)
        # Heavier weights get rounder ends
        r_end = self.end_ratio * r * (dc.stroke_x / dc.default_stroke) ** 0.5
        for i in range(self.spokes):
            draw_teardrop(pen, cx, cy, self.start + 360 * i / self.spokes, r, r_end)


class FourTeardropSpokedAsteriskGlyph(TeardropAsteriskGlyph):
    name = "four_teardrop_spoked_asterisk"
    unicode = "0x2722"
    spokes = 4
    radius_ratio = 0.42
    end_ratio = 0.25


class TeardropSpokedAsteriskGlyph(TeardropAsteriskGlyph):
    name = "teardrop_spoked_asterisk"
    unicode = "0x273B"
    end_ratio = 0.15


class HeavyTeardropSpokedAsteriskGlyph(TeardropAsteriskGlyph):
    name = "heavy_teardrop_spoked_asterisk"
    unicode = "0x273D"
    end_ratio = 0.2


class EightSpokedAsteriskGlyph(DingbatGlyph):
    name = "eight_spoked_asterisk"
    unicode = "0x2733"
    radius_ratio = 0.44
    stroke_ratio = 1.15  # Relative to stroke_alt

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        r = self.radius(dc)
        s = self.stroke_ratio * dc.stroke_alt
        for a, b in (((0, r), (0, -r)), ((r, 0), (-r, 0))):
            draw_segment(pen, (cx + a[0], cy + a[1]), (cx + b[0], cy + b[1]), s)
        d = r * 0.7071
        draw_segment(pen, (cx - d, cy - d), (cx + d, cy + d), s)
        draw_segment(pen, (cx - d, cy + d), (cx + d, cy - d), s)


class SixPointedBlackStarGlyph(DingbatGlyph):
    name = "six_pointed_black_star"
    unicode = "0x2736"
    inner_ratio = 0.5

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        r = self.radius(dc)
        draw_star(pen, cx, cy, r, self.inner_ratio * r, 6)


# Check marks and crosses


class CheckMarkGlyph(DingbatGlyph):
    name = "check_mark"
    unicode = "0x2713"
    stroke_ratio = 1.0  # Relative to stroke_x

    def draw(self, pen, dc):
        w = dc.window_width
        s = symbol_stroke(dc, self.stroke_ratio)
        top = dc.x_height + 60
        draw_polyline(
            pen,
            [(0.12 * w, 0.45 * dc.x_height), (0.4 * w, 0), (0.9 * w, top)],
            s,
        )


class HeavyCheckMarkGlyph(CheckMarkGlyph):
    name = "heavy_check_mark"
    unicode = "0x2714"
    stroke_ratio = 1.8


class MultiplicationXGlyph(DingbatGlyph):
    name = "multiplication_x"
    unicode = "0x2715"
    stroke_ratio = 1.0
    size_ratio = 0.6  # Relative to the advance width
    lift = 0  # Extra height of the rising stroke's top, relative to the size

    def draw(self, pen, dc):
        cx, cy = self.centre(dc)
        h = self.size_ratio * dc.window_width / 2
        s = symbol_stroke(dc, self.stroke_ratio)
        draw_segment(pen, (cx - h, cy - h), (cx + h, cy + h + self.lift * 2 * h), s)
        draw_segment(pen, (cx - h, cy + h), (cx + h, cy - h), s)


class HeavyMultiplicationXGlyph(MultiplicationXGlyph):
    name = "heavy_multiplication_x"
    unicode = "0x2716"
    stroke_ratio = 1.8


class BallotXGlyph(MultiplicationXGlyph):
    """Like the multiplication x, but taller and with a longer rising stroke,
    as if handwritten."""

    name = "ballot_x"
    unicode = "0x2717"
    size_ratio = 0.7
    lift = 0.12


class HeavyBallotXGlyph(BallotXGlyph):
    name = "heavy_ballot_x"
    unicode = "0x2718"
    stroke_ratio = 1.8


# Ornaments


class HeavyRightPointingAngleQuotationMarkOrnamentGlyph(DingbatGlyph):
    name = "heavy_right_pointing_angle_quotation_mark_ornament"
    unicode = "0x276F"
    width_ratio = 0.42  # Relative to the advance width
    height_ratio = 0.75  # Relative to the x-height
    stroke_ratio = 1.5
    points_right = True

    def draw(self, pen, dc):
        w = dc.window_width
        hw = self.width_ratio * w / 2
        hh = self.height_ratio * dc.x_height / 2
        cx, cy = w / 2, dc.x_height / 2
        tip, back = (cx + hw, cx - hw) if self.points_right else (cx - hw, cx + hw)
        draw_polyline(
            pen,
            [(back, cy + hh), (tip, cy), (back, cy - hh)],
            symbol_stroke(dc, self.stroke_ratio),
        )


class HeavyLeftPointingAngleQuotationMarkOrnamentGlyph(
    HeavyRightPointingAngleQuotationMarkOrnamentGlyph
):
    name = "heavy_left_pointing_angle_quotation_mark_ornament"
    unicode = "0x276E"
    points_right = False
