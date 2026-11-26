################################################################################
## options.rpy - project configuration for Fumo Court.
################################################################################

## Basics ######################################################################

## Catch styles that set conflicting properties (e.g. xpos and xalign).
define config.check_conflicting_properties = True

define config.name = _("Fumo Court")

## The title screen draws its own logo.
define gui.show_name = False

define config.version = "0.1.0"

define gui.about = _p("""
Fumo Court: Shiki Eiki's Logic Trials is a free, non-commercial fan game.

Touhou Project and all of its characters belong to Team Shanghai Alice (ZUN). This game is an unofficial fan work. It is not affiliated with, endorsed by, or produced by Team Shanghai Alice. Please support the official games.

All art in this build is hand-written vector code: plain SVG shapes and Ren'Py styles. No AI-generated art.

Text is set in Shippori Mincho B1 by FONTDASU, under the SIL Open Font License 1.1 (see game/fonts/OFL.txt).

Built with Ren'Py.
""")

## Short name used for the build directory and archive names. ASCII only,
## no spaces, colons or semicolons.
define build.name = "FumoCourt"


## Audio #######################################################################

## This build ships without sound, so the mixer settings stay hidden.
define config.has_sound = False
define config.has_music = False
define config.has_voice = False


## Transitions ##################################################################

define config.enter_transition = Dissolve(0.25)
define config.exit_transition = Dissolve(0.25)
define config.intra_transition = Dissolve(0.15)
define config.after_load_transition = Dissolve(0.25)
define config.end_game_transition = Dissolve(0.5)


## Text box ######################################################################

## Shown during dialogue and hidden for menus and screens. Scene changes keep
## it up, so the whip pans between bench and stand don't blink the box.
define config.window = "auto"
define config.window_auto_hide = [ "call screen", "menu", "say-centered", "say-bubble" ]
define config.window_show_transition = Dissolve(0.15)
define config.window_hide_transition = Dissolve(0.15)

define config.history_length = 250


## Preference defaults ############################################################

default preferences.text_cps = 50
default preferences.afm_time = 15


## Saves ###########################################################################

## Where saves live on Windows/Linux/macOS. Keep this stable between releases
## or players lose their saves.
define config.save_directory = "FumoCourt-1764166800"

define config.thumbnail_width = 384
define config.thumbnail_height = 216


## Window and icons ################################################################

## Title-bar and taskbar icon while the game runs. The Windows .exe icon is
## icon.ico and the web/PWA icon is web-icon.png, both in the project root;
## the launcher's distribute and web_build commands pick them up on their own.
define config.window_icon = "gui/window_icon.png"

define config.default_fullscreen = False


## Build configuration ###############################################################

init python:

    ## Never ship editor junk, repository files or source-only tooling.
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
    build.classify("tools/**", None)
    build.classify("README.md", None)

    ## Read straight from the project folder by the launcher; not game data.
    build.classify("icon.ico", None)
    build.classify("web-icon.png", None)
    build.classify("web-presplash.png", None)
    build.classify("progressive_download.txt", None)

    build.documentation("*.html")
    build.documentation("*.txt")

## Leave out the legacy pre-6.x themes; they add size and nothing uses them.
define build.include_old_themes = False

## The win package needs only the 64-bit Windows runtime.
define build.include_i686 = False
