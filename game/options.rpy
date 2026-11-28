################################################################################
## options.rpy - project configuration for Fumo Court.
################################################################################

## Basics ######################################################################

## Catch styles that set conflicting properties (e.g. xpos and xalign).
define config.check_conflicting_properties = True

define config.name = _("Fumo Court")

## The title screen draws its own logo.
define gui.show_name = False

define config.version = "0.4.0"

define gui.about = _p("""
Fumo Court: Shiki Eiki's Logic Trials is a free, non-commercial fan game.

Touhou Project and all of its characters belong to Team Shanghai Alice (ZUN). This game is an unofficial fan work. It is not affiliated with, endorsed by, or produced by Team Shanghai Alice. Please support the official games.

The character sprites are photographs of the official Fumo plushies by Gift. Their backgrounds were removed with the open BiRefNet segmentation model and they were relit to match the courtroom. Everything else is hand-written vector code: plain SVG shapes and Ren'Py styles. Nothing in the game is AI-generated art.

Sound effects by Warsong, from the Petaldust and Nostalgiac Blues sound packs (CC0).

Music by +TEK, arrangements of ZUN's compositions, used under CC BY 4.0 (creativecommons.org/licenses/by/4.0). Each was cut to loop seamlessly, loudness-normalised and re-encoded.
  Title: "Scarlet Beyond a Crimson Dream", from Embodiment of Frequency Modulation.
  Cirno's theme: "Beloved Tomboyish Girl" (おてんば恋娘), from Story of Modulated Frequency.
  Marisa's theme: "Love-coloured Master Spark" (恋色マスタースパーク), from Embodiment of Frequency Modulation.
  Sakuya's theme: "Lunar Clock ~ Luna Dial" (月時計 ～ ルナ・ダイアル), from Embodiment of Frequency Modulation.
  Reisen's theme: "Lunatic Eyes ~ Invisible Full Moon" (狂気の瞳), from Embodiment of Frequency Modulation.
  Case 05 and Mokou: "Reach for the Moon, Immortal Smoke" (月まで届け、不死の煙), from Embodiment of Frequency Modulation.
  Meiling's theme: "Shanghai Teahouse ~ Chinese Tea" (上海紅茶館 ～ Chinese Tea), from Story of Modulated Frequency.
  Alice's theme: "The Doll Maker of Bucuresti" (ブクレシュティの人形師), from Phantasmagoria of F.M.
  Reimu's theme: "Maiden's Capriccio ~ Dream Battle" (少女綺想曲 ～ Dream Battle), from Phantasmagoria of F.M.
  Kaguya's theme: "Gensokyo Millenium ~ History of the Moon" (千年幻想郷 ～ History of the Moon), from Story of Modulated Frequency.
  Aya's theme: "Because Princess Inada Is Scolding Me" (稲田姫様に叱られるから), from Phantasmagoria of F.M.
  Pursuits, Cases 01 to 11: "U.N. Owen Was Her S", "Bad Apple!!", "Flowering Night", "Pierrot of the Star-Spangled Banner", "Heian Alien", "Nostalgic Blood of the East ~ Old World", "Doll Judgment ~ the Girl Who Played with People's Shapes", "Native Faith", "Reverse Ideology", "Captain Murasa" and "Joutounin of Ceramics", from Embodiment of Frequency Modulation, Story of Modulated Frequency and Phantasmagoria of F.M.

Text is set in Shippori Mincho B1 by FONTDASU and Noto Serif SC by Google, under the SIL Open Font License 1.1 (see game/fonts/).

Built with Ren'Py.
""")

## Short name used for the build directory and archive names. ASCII only,
## no spaces, colons or semicolons.
define build.name = "FumoCourt"


## Audio #######################################################################

## Sound effects and witness themes (see audio.rpy); no voice acting.
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.default_sfx_volume = 0.8
define config.default_music_volume = 0.65


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
    build.classify("art_src/**", None)
    build.classify("README.md", None)
    build.classify("ci_test/**", None)
    build.classify("android-*", None)
    build.classify("*.keystore", None)
    build.classify(".android.json", None)

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
