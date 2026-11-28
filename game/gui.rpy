################################################################################
## gui.rpy - palette, fonts, base styles and the CourtPanel displayable.
##
## Every panel in Fumo Court is drawn from flat rectangles (Solid) plus small
## SVG ornaments, so borders stay pixel-sharp at any size and any window scale.
################################################################################

init offset = -2

init python:
    gui.init(1920, 1080)


################################################################################
## Palette
################################################################################

define CRIMSON = "#4A0E17"         # deep lacquer crimson
define CRIMSON_HI = "#6E1A28"
define CRIMSON_DEEP = "#2B070D"
define GOLD = "#D4AF37"            # imperial gold
define GOLD_HI = "#F2D47C"
define GOLD_LO = "#8E6F1E"
define PARCHMENT = "#F5EEDB"       # warm washi
define PARCHMENT_SHADE = "#E9DDBF"
define INK = "#1E1916"             # dark ink
define INDIGO = "#1B263B"          # judge accent
define INDIGO_HI = "#2C3E5C"
define VERMILION = "#C41E3A"       # verdict stamp red
define LINE = "#160406"            # outer keyline around panels


################################################################################
## Fonts (Shippori Mincho B1, SIL OFL 1.1, subset by tools/build_fonts.py)
################################################################################

define FONT_BODY = "fonts/ShipporiMinchoB1-Bold-sub.ttf"
define FONT_HEAD = "fonts/ShipporiMinchoB1-ExtraBold-sub.ttf"

## Simplified Chinese uses Noto Serif SC, cut down by tools/build_fonts.py to
## the characters in game/tl/schinese. Swapped in by translations.rpy.
define FONT_SC_BODY = "fonts/NotoSerifSC-SemiBold-sub.ttf"
define FONT_SC_HEAD = "fonts/NotoSerifSC-Black-sub.ttf"


################################################################################
## Layout constants (virtual pixels at 1920x1080)
################################################################################

## The parchment dialogue box. Testimony and plaques share this geometry.
define BOX_X = 150
define BOX_Y = 704
define BOX_W = 1620
define BOX_H = 236

## Text inset inside the box (keeps ink well clear of the gold border).
define BOX_PAD_X = 70
define BOX_PAD_TOP = 56

## Where the plaques sit under the box.
define PLAQUE_Y = 948

## Stage. The stand image's top edge, and where a fumo's feet rest on its
## cushion. Fumo sprites live in a fixed 480x500 slot (see script.rpy), so
## swapping in a PNG of any size keeps the same footing.
define STAND_Y = 544
define FUMO_FEET = 596
define FUMO_SLOT_W = 480
define FUMO_SLOT_H = 500
define FUMO_CENTER_LIFT = -250

## Contact shadow under a fumo, on the cushion.
define FUMO_SHADOW_Y = 590


################################################################################
## CourtPanel
################################################################################

init python:

    class CourtPanel(renpy.Displayable):
        """
        A framed panel in the courtroom style, rendered at whatever size it
        is given (so it works as a frame, window or button background).

        Layers, outside in:
            optional drop shadow
            1px keyline (`line`)
            `edge` border, `edge_w` thick
            optional `inner` band, `inner_w` thick
            `fill`
            optional `rule`: a thin inset line, `rule_inset` from the outside
            optional gold corner fittings
        """

        def __init__(self, fill, edge=GOLD, edge_w=4, inner=None, inner_w=3,
                     rule=None, rule_inset=12, rule_w=2, corners=False,
                     corner_size=40, shadow=0, line=LINE, **kwargs):

            super(CourtPanel, self).__init__(**kwargs)

            self.fill = fill
            self.edge = edge
            self.edge_w = edge_w
            self.inner = inner
            self.inner_w = inner_w
            self.rule = rule
            self.rule_inset = rule_inset
            self.rule_w = rule_w
            self.shadow = shadow
            self.line = line
            self.corner_size = corner_size

            self.solids = { }

            if corners:
                z = corner_size / 56.0
                c = "gui/corner.svg"
                self.corners = [
                    Transform(c, zoom=z),
                    Transform(c, zoom=z, xzoom=-1.0),
                    Transform(c, zoom=z, yzoom=-1.0),
                    Transform(c, zoom=z, xzoom=-1.0, yzoom=-1.0),
                    ]
            else:
                self.corners = [ ]

        def solid(self, color):
            rv = self.solids.get(color)
            if rv is None:
                rv = self.solids[color] = Solid(color)
            return rv

        def render(self, width, height, st, at):

            w = int(width)
            h = int(height)
            rv = renpy.Render(w, h)

            def rect(color, x, y, rw, rh):
                if color is None or rw <= 0 or rh <= 0:
                    return
                rv.blit(renpy.render(self.solid(color), rw, rh, st, at), (x, y))

            def frame(color, inset, thick):
                if color is None or thick <= 0:
                    return
                i = inset
                rect(color, i, i, w - 2 * i, thick)
                rect(color, i, h - i - thick, w - 2 * i, thick)
                rect(color, i, i + thick, thick, h - 2 * i - 2 * thick)
                rect(color, w - i - thick, i + thick, thick, h - 2 * i - 2 * thick)

            if self.shadow:
                rect("#0000008c", self.shadow, self.shadow, w, h)

            frame(self.line, 0, 1)
            frame(self.edge, 1, self.edge_w)

            o = 1 + self.edge_w
            frame(self.inner, o, self.inner_w)

            if self.inner is not None:
                o += self.inner_w

            rect(self.fill, o, o, w - 2 * o, h - 2 * o)

            if self.rule is not None:
                frame(self.rule, self.rule_inset, self.rule_w)

            if self.corners and w > 2 * self.corner_size and h > 2 * self.corner_size:
                cs = self.corner_size
                spots = [ (0, 0), (w - cs, 0), (0, h - cs), (w - cs, h - cs) ]
                for d, pos in zip(self.corners, spots):
                    rv.blit(renpy.render(d, cs, cs, st, at), pos)

            return rv

        def visit(self):
            return list(self.corners)


    class Track(renpy.Displayable):
        """A thin horizontal line, vertically centred: the groove of a slider."""

        def __init__(self, color, thick=8, **kwargs):
            super(Track, self).__init__(**kwargs)
            self.solid = Solid(color)
            self.thick = thick

        def render(self, width, height, st, at):
            w, h = int(width), int(height)
            rv = renpy.Render(w, h)
            rv.blit(renpy.render(self.solid, w, self.thick, st, at), (0, (h - self.thick) // 2))
            return rv


    def SVG(filename, scale=1.0):
        """
        An SVG rendered directly at `scale`, so it stays sharp instead of being
        rasterised at full size and then shrunk.
        """
        return Image(filename, dpi=96.0 * scale)


    def ParchmentPanel(**kwargs):
        """The washi dialogue / content panel."""
        args = dict(fill=PARCHMENT, edge=GOLD, edge_w=5, inner=CRIMSON, inner_w=3,
                    rule=GOLD, rule_inset=16, rule_w=2, corners=True, corner_size=44, shadow=8)
        args.update(kwargs)
        return CourtPanel(**args)


    def LacquerPanel(**kwargs):
        """Crimson lacquer plate with a gold frame."""
        args = dict(fill=CRIMSON, edge=GOLD, edge_w=4, rule=GOLD_LO, rule_inset=10, rule_w=2, shadow=6)
        args.update(kwargs)
        return CourtPanel(**args)


    def IndigoPanel(**kwargs):
        """Indigo judge plate."""
        args = dict(fill=INDIGO, edge=GOLD, edge_w=3, rule=None, shadow=5)
        args.update(kwargs)
        return CourtPanel(**args)


################################################################################
## Base styles
################################################################################

style default:
    font FONT_BODY
    size 34
    color INK
    language "unicode"
    outlines [ ]
    layout "subtitle"

style text_ink is default:
    color INK

style text_parchment is default:
    color PARCHMENT

style text_gold is default:
    font FONT_HEAD
    color GOLD
    outlines [ (absolute(2), CRIMSON_DEEP, 0, 0) ]

style heading is default:
    font FONT_HEAD
    size 52
    color GOLD
    outlines [ (absolute(3), CRIMSON_DEEP, absolute(0), absolute(2)) ]

style hyperlink_text is default:
    color CRIMSON
    hover_color VERMILION
    underline True

style input is default:
    color INDIGO
    adjust_spacing False

style button is default:
    focus_mask None

style button_text is default:
    font FONT_HEAD
    color PARCHMENT
    hover_color GOLD_HI
    insensitive_color "#9a8c80"
    selected_color GOLD
    yalign 0.5

style frame is default:
    background ParchmentPanel()
    padding (40, 34)

style window is default

style bar:
    ysize 34
    left_bar Track(GOLD, 8)
    right_bar Track("#00000059", 8)
    thumb "gui/slider_thumb.svg"
    thumb_offset 17
    left_gutter 0
    right_gutter 0

style slider is bar:
    xsize 640

style vscrollbar:
    xsize 14
    base_bar Solid("#00000040")
    thumb Solid(GOLD)
    unscrollable "hide"

style vslider:
    xsize 22
    base_bar Solid(CRIMSON_DEEP)
    thumb Solid(GOLD)
