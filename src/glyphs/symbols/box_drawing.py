"""Box drawing characters (U+2500-U+257F), except the double lines.

The lines span the full line height (window descent to window ascent) and
the full advance width, plus a small bleed past the cell edges, so they join
across rows and columns without seams. Most glyphs are generated from their
Unicode names, which spell out the weight of each arm, e.g. "BOX DRAWINGS
DOWN LIGHT AND RIGHT HEAVY".
"""

import re
import unicodedata

from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen

from config import FontConfig as fc
from draw.polygon import draw_polygon
from draw.rect import draw_rect
from glyphs import Glyph

K = 0.5523  # Bezier handle length of a quarter circle, relative to its radius

DIRECTIONS = {
    "LEFT": ("left",),
    "RIGHT": ("right",),
    "UP": ("up",),
    "DOWN": ("down",),
    "HORIZONTAL": ("left", "right"),
    "VERTICAL": ("up", "down"),
}
WEIGHTS = {"LIGHT": 1, "HEAVY": 2}
DASHES = {"DOUBLE": 2, "TRIPLE": 3, "QUADRUPLE": 4}


class BoxDrawingGlyph(Glyph):
    """A box drawing character spanning the whole cell."""

    offset = 0
    italic_skew = False
    light_ratio = 1.0  # Light line weight, relative to stroke_y
    heavy_ratio = 2.0  # Heavy line weight, relative to the light weight
    bleed = 20  # Units the lines extend past the cell edges

    def light(self, dc):
        return self.light_ratio * dc.stroke_y

    def weight(self, dc, w):
        return {0: 0, 1: 1, 2: self.heavy_ratio}[w] * self.light(dc)

    def cell(self, dc):
        """(x1, y1, x2, y2, cx, cy) of the cell, bleed included."""
        x1, x2 = -self.bleed, dc.window_width + self.bleed
        y1, y2 = fc.window_descent - self.bleed, fc.window_ascent + self.bleed
        cx = dc.window_width / 2
        cy = (fc.window_descent + fc.window_ascent) / 2
        return x1, y1, x2, y2, cx, cy


class BoxLinesGlyph(BoxDrawingGlyph):
    """Straight arms from the cell centre, each light, heavy or absent."""

    arms = {}  # direction -> 1 (light) or 2 (heavy)
    dashes = 0  # Number of dashes per cell along the line, 0 when solid
    dash_gap = 0.45  # Gap between dashes, relative to the dash period

    def draw(self, pen, dc):
        x1, y1, x2, y2, cx, cy = self.cell(dc)
        w = {d: self.weight(dc, self.arms.get(d, 0)) for d in DIRECTIONS_ORDER}
        if self.dashes:
            self.draw_dashed(pen, dc, w)
            return
        # Each arm runs past the centre by half the widest perpendicular arm,
        # so corners and junctions come out square.
        horizontal = max(w["left"], w["right"])
        vertical = max(w["up"], w["down"])
        if w["left"]:
            draw_rect(pen, x1, cy - w["left"] / 2, cx + vertical / 2, cy + w["left"] / 2)
        if w["right"]:
            draw_rect(pen, cx - vertical / 2, cy - w["right"] / 2, x2, cy + w["right"] / 2)
        if w["down"]:
            draw_rect(pen, cx - w["down"] / 2, y1, cx + w["down"] / 2, cy + horizontal / 2)
        if w["up"]:
            draw_rect(pen, cx - w["up"] / 2, cy - horizontal / 2, cx + w["up"] / 2, y2)

    def draw_dashed(self, pen, dc, w):
        _, _, _, _, cx, cy = self.cell(dc)
        n = self.dashes
        if w["left"]:
            s, period = w["left"], dc.window_width / n
            for i in range(n):
                a = i * period + period * self.dash_gap / 2
                draw_rect(pen, a, cy - s / 2, a + period * (1 - self.dash_gap), cy + s / 2)
        else:
            s = w["up"]
            period = (fc.window_ascent - fc.window_descent) / n
            for i in range(n):
                a = fc.window_descent + i * period + period * self.dash_gap / 2
                draw_rect(pen, cx - s / 2, a, cx + s / 2, a + period * (1 - self.dash_gap))


DIRECTIONS_ORDER = ("left", "right", "up", "down")


def parse_box_name(name):
    """Return (arms, dashes) from a box drawing character name.

    The weight in each " AND " segment applies to that segment's directions;
    a segment without one inherits the first weight in the name.
    """
    name = name.removeprefix("BOX DRAWINGS ")
    dashes = 0
    m = re.search(r"\b(DOUBLE|TRIPLE|QUADRUPLE) DASH ", name)
    if m:
        dashes = DASHES[m.group(1)]
        name = name.replace(m.group(0), "")
    segments = [s.split() for s in name.split(" AND ")]
    default = next(WEIGHTS[t] for s in segments for t in s if t in WEIGHTS)
    arms = {}
    for tokens in segments:
        weight = next((WEIGHTS[t] for t in tokens if t in WEIGHTS), default)
        for t in tokens:
            for d in DIRECTIONS.get(t, ()):
                arms[d] = weight
    return arms, dashes


def glyph_name(code):
    return re.sub(r"[^a-z0-9]+", "_", unicodedata.name(chr(code)).lower())


for _code in list(range(0x2500, 0x254C + 4)) + list(range(0x2574, 0x2580)):
    _name = unicodedata.name(chr(_code))
    if "DOUBLE" in _name and "DASH" not in _name:
        continue
    _arms, _dashes = parse_box_name(_name)
    _cls = type(
        f"BoxLines{_code:04X}Glyph",
        (BoxLinesGlyph,),
        {
            "name": glyph_name(_code),
            "unicode": hex(_code),
            "arms": _arms,
            "dashes": _dashes,
        },
    )
    globals()[_cls.__name__] = _cls


class LightArcDownAndRightGlyph(BoxDrawingGlyph):
    """Rounded corner; the other three arcs mirror it about the cell centre."""

    name = "box_drawings_light_arc_down_and_right"
    unicode = "0x256D"
    flip_x = False
    flip_y = False

    def draw(self, pen, dc):
        x1, y1, x2, y2, cx, cy = self.cell(dc)
        sx, sy = (-1 if self.flip_x else 1), (-1 if self.flip_y else 1)
        pen = TransformPen(
            pen, Transform(sx, 0, 0, sy, cx - sx * cx, cy - sy * cy)
        )
        s = self.light(dc)
        r = dc.window_width / 2
        # Centre of curvature, below and right of the cell centre
        ox, oy = cx + r, cy - r
        ro, ri = r + s / 2, r - s / 2
        draw_rect(pen, cx - s / 2, y1, cx + s / 2, oy)
        draw_rect(pen, ox, cy - s / 2, x2, cy + s / 2)
        # Quarter ring from the bottom arm to the right arm
        pen.moveTo((ox - ro, oy))
        pen.curveTo((ox - ro, oy + K * ro), (ox - K * ro, oy + ro), (ox, oy + ro))
        pen.lineTo((ox, oy + ri))
        pen.curveTo((ox - K * ri, oy + ri), (ox - ri, oy + K * ri), (ox - ri, oy))
        pen.closePath()


class LightArcDownAndLeftGlyph(LightArcDownAndRightGlyph):
    name = "box_drawings_light_arc_down_and_left"
    unicode = "0x256E"
    flip_x = True


class LightArcUpAndLeftGlyph(LightArcDownAndRightGlyph):
    name = "box_drawings_light_arc_up_and_left"
    unicode = "0x256F"
    flip_x = True
    flip_y = True


class LightArcUpAndRightGlyph(LightArcDownAndRightGlyph):
    name = "box_drawings_light_arc_up_and_right"
    unicode = "0x2570"
    flip_y = True


class LightDiagonalGlyph(BoxDrawingGlyph):
    """Corner-to-corner diagonals; `rising` and/or `falling`."""

    rising = False
    falling = False

    def draw(self, pen, dc):
        x1, y1, x2, y2, _, _ = self.cell(dc)
        s = self.light(dc)
        # Half the horizontal width of a line of weight s
        dx, dy = x2 - x1, y2 - y1
        h = s / 2 * (dx * dx + dy * dy) ** 0.5 / dy
        if self.rising:
            draw_polygon(pen, [(x1 - h, y1), (x1 + h, y1), (x2 + h, y2), (x2 - h, y2)])
        if self.falling:
            draw_polygon(pen, [(x2 - h, y1), (x2 + h, y1), (x1 + h, y2), (x1 - h, y2)])


class LightDiagonalRisingGlyph(LightDiagonalGlyph):
    name = "box_drawings_light_diagonal_upper_right_to_lower_left"
    unicode = "0x2571"
    rising = True


class LightDiagonalFallingGlyph(LightDiagonalGlyph):
    name = "box_drawings_light_diagonal_upper_left_to_lower_right"
    unicode = "0x2572"
    falling = True


class LightDiagonalCrossGlyph(LightDiagonalGlyph):
    name = "box_drawings_light_diagonal_cross"
    unicode = "0x2573"
    rising = True
    falling = True
