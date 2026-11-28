################################################################################
## audio.rpy - sound effects and music.
##
## Sound effects
## -------------
## Each sound is named after the moment it plays at and lives in
## game/audio/sfx/ as <name>.ogg (or .opus / .wav / .mp3). To change a sound,
## replace that one file. A missing file is skipped silently, so the game also
## runs with no sounds at all.
##
##   ui_hover      pointer moves onto a button
##   ui_confirm    a button is clicked
##   ui_cancel     Withdraw / Return
##   nav           previous / next testimony statement
##   shout_hold    HOLD IT! (pressing a statement)
##   shout_objection  OBJECTION!
##   penalty       a magatama of spirit is lost
##   gavel         the gavel comes down
##   stamp         the GUILTY stamp lands
##   banner        WITNESS TESTIMONY / CROSS-EXAMINATION title
##   breakthrough  the right fallacy on the right statement
##   shock         a witness is caught out
##   yeet          a defendant leaves the stand at speed
##   case_closed   CASE CLOSED
##   mistrial      spirit runs out
##   blip          text blip, looped while dialogue types out; blip_hi,
##                 blip_up, blip_dn, blip_lo and blip_deep are the same blip
##                 at each speaker's pitch (see the cast in script.rpy)
##   break_<who>   a witness breaks down (reactions.rpy)
##
## Music
## -----
## Every piece lives in game/audio/music/ and is listed in BGM below.
##
## The title theme plays on the main menu and stops when a trial begins.
## A witness theme starts when its witness takes the stand to testify, carries
## through the cross-examination, and is cut when the right objection lands.
## As in a Touhou stage, a title card slides in at the bottom right whenever a
## witness theme starts. tools/build_music.py prepares a downloaded track and
## finds its loop; a missing file is skipped silently, like a missing sound
## effect.
################################################################################

init -1 python:

    SFX_DIR = "audio/sfx/"

    def sfx_file(name):
        """The file for a named sound effect, or None if it isn't there."""
        for ext in (".ogg", ".opus", ".wav", ".mp3", ".flac"):
            filename = SFX_DIR + name + ext
            if renpy.loadable(filename):
                return filename
        return None

    def sfx(name):
        """Plays a named sound effect on the event channel, if it exists."""
        filename = sfx_file(name)
        if filename:
            renpy.music.play(filename, channel="event", loop=False)

    # Story beats get their own channel so a button click never cuts off an
    # OBJECTION!; text blips get another so they can loop under dialogue.
    renpy.music.register_channel("event", mixer="sfx", loop=False, stop_on_mute=True)
    renpy.music.register_channel("blip", mixer="sfx", loop=True, stop_on_mute=True)


    class TextBlip(object):
        """
        Character callback: loops a blip while a line is typing out. Each
        speaker has their own pitch (blip_hi ... blip_deep in build_sfx.py).
        """

        def __init__(self, voice="blip"):
            self.voice = voice

        def __call__(self, event, interact=True, **kwargs):
            if not interact:
                return
            if event == "show":
                filename = sfx_file(self.voice) or sfx_file("blip")
                if filename and preferences.text_cps:
                    renpy.music.play(filename, channel="blip", loop=True)
            elif event in ("slow_done", "end"):
                renpy.music.stop(channel="blip")


    class Callbacks(object):
        """Several character callbacks as one."""

        def __init__(self, *callbacks):
            self.callbacks = callbacks

        def __call__(self, event, **kwargs):
            for cb in self.callbacks:
                cb(event, **kwargs)

    # Button sounds for the styles in screens.rpy (set here, at init -1, so
    # they exist before those styles are built).
    SFX_HOVER = sfx_file("ui_hover")
    SFX_CONFIRM = sfx_file("ui_confirm")
    SFX_CANCEL = sfx_file("ui_cancel")
    SFX_NAV = sfx_file("nav")


    ## Music ###################################################################

    MUSIC_DIR = "audio/music/"

    class Theme(object):
        """A piece of music and the credit line shown when it starts."""

        def __init__(self, name, title, original, credit, loop=None):
            self.name = name            # file stem in game/audio/music/
            self.title = title          # shown in the title card
            self.original = original    # ZUN's title, shown beside it
            self.credit = credit
            self.loop = loop            # seconds to loop back to, after the intro

        @property
        def filename(self):
            """What to play, with the loop point, or None if the file is missing."""
            for ext in (".ogg", ".opus", ".mp3", ".flac", ".wav"):
                filename = MUSIC_DIR + self.name + ext
                if renpy.loadable(filename):
                    if self.loop is not None:
                        filename = "<loop {:.6f}>{}".format(self.loop, filename)
                    return filename
            return None

    BGM = {
        "cirno": Theme(
            "cirno_theme",
            "Beloved Tomboyish Girl",
            u"おてんば恋娘",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            # From tools/build_music.py --find-loop: the file stops where the
            # tune starts its second pass, and play loops back to here.
            loop=4.389705,
        ),
        "marisa": Theme(
            "marisa_theme",
            "Love-coloured Master Spark",
            u"恋色マスタースパーク",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=10.844785,
        ),
        "sakuya": Theme(
            "sakuya_theme",
            "Lunar Clock ~ Luna Dial",
            u"月時計 ～ ルナ・ダイアル",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=1.545488,
        ),
        "reisen": Theme(
            "reisen_theme",
            "Lunatic Eyes ~ Invisible Full Moon",
            u"狂気の瞳",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=10.839796,
        ),
        # Main menu. Never announced with a title card; credited in About.
        "title": Theme(
            "title_theme",
            "Scarlet Beyond a Crimson Dream",
            u"",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=26.264989,
        ),
    }

    def bgm(name, fadein=1.0, card_delay=1.9):
        """
        Starts a theme, unless it is already playing. The title card waits
        `card_delay` seconds so it lands after the banner that opens a
        testimony or cross-examination.
        """
        theme = BGM[name]
        filename = theme.filename
        if filename is None:
            return
        if renpy.music.get_playing("music") == filename:
            return
        renpy.music.play(filename, channel="music", loop=True, fadein=fadein)
        renpy.show_screen("bgm_title", theme, card_delay)

    def bgm_stop(fadeout=0.5):
        """Stops whatever theme is playing."""
        renpy.music.stop("music", fadeout=fadeout)
        renpy.hide_screen("bgm_title")


## The title screen theme, from BGM above.
define config.main_menu_music = BGM["title"].filename
define config.main_menu_music_fadein = 1.5
