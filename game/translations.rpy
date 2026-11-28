################################################################################
## translations.rpy - language switching.
##
## The translations themselves live in game/tl/japanese and game/tl/schinese.
## Japanese uses the game's own Shippori Mincho fonts. Simplified Chinese
## needs Chinese glyph shapes, so while it's selected every use of the two
## Shippori fonts is redirected to Noto Serif SC.
################################################################################

translate None python:
    config.font_replacement_map.clear()

translate japanese python:
    config.font_replacement_map.clear()

translate schinese python:
    config.font_replacement_map.clear()
    config.font_replacement_map[(FONT_BODY, False, False)] = (FONT_SC_BODY, False, False)
    config.font_replacement_map[(FONT_HEAD, False, False)] = (FONT_SC_HEAD, False, False)

## Line breaking: kinsoku rules for Japanese, plain Unicode rules otherwise.
translate japanese style default:
    language "japanese-normal"
