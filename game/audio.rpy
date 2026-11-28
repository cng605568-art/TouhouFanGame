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
## A witness theme starts when its witness takes the stand to testify and
## carries through the cross-examination. When the witness is cornered (a
## press brings out a new statement, or the right fallacy needs its proof) the
## pursuit theme takes over, and the music is cut when the case breaks open.
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
        # Case 05, when Eiki herself takes the stand.
        "eiki": Theme(
            "finale_theme",
            "Reach for the Moon, Immortal Smoke",
            u"月まで届け、不死の煙",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=1.700136,
        ),
        # Arc two. Loop points from tools/build_music.py --find-loop.
        "meiling": Theme(
            "meiling_theme",
            "Shanghai Teahouse ~ Chinese Tea",
            u"上海紅茶館 ～ Chinese Tea",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=14.170181,
        ),
        "alice": Theme(
            "alice_theme",
            "The Doll Maker of Bucuresti",
            u"ブクレシュティの人形師",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=1.139705,
        ),
        "reimu": Theme(
            "reimu_theme",
            "Maiden's Capriccio ~ Dream Battle",
            u"少女綺想曲 ～ Dream Battle",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=7.139705,
        ),
        "kaguya": Theme(
            "kaguya_theme",
            "Gensokyo Millenium ~ History of the Moon",
            u"千年幻想郷 ～ History of the Moon",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=0.580408,
        ),
        # Mokou bursts in to her own theme (the same file as Eiki's case).
        "mokou": Theme(
            "finale_theme",
            "Reach for the Moon, Immortal Smoke",
            u"月まで届け、不死の煙",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=1.700136,
        ),
        # The pursuit: takes over from the witness theme when the witness is
        # cornered (court.rpy). No clean second pass in this arrangement, so
        # the loop points were set by hand where a passage repeats 68.9 s
        # later (build_music.py --loop 47.224694 116.127914 --xfade 0.2).
        "pursuit": Theme(
            "pursuit_theme",
            "U.N. Owen Was Her?",
            u"U.N.オーエンは彼女なのか？",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=47.224694,
        ),
        # Each case's own pursuit (Case 01 keeps U.N. Owen). A case whose
        # file is missing falls back to "pursuit" (court.rpy: pursuit_theme).
        "bad_apple": Theme(   # pursuit, Case 02, Marisa
            "bad_apple_theme",
            "Bad Apple!!",
            u"Bad Apple!!",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "flowering_night": Theme(   # pursuit, Case 03, Sakuya
            "flowering_night_theme",
            "Flowering Night",
            u"フラワリングナイト",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "pierrot": Theme(   # pursuit, Case 04, Reisen
            "pierrot_theme",
            "Pierrot of the Star-Spangled Banner",
            u"星条旗のピエロ",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "heian_alien": Theme(   # pursuit, Case 05, Eiki
            "heian_alien_theme",
            "Heian Alien",
            u"平安のエイリアン",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "old_world": Theme(   # pursuit, Case 06, Meiling
            "old_world_theme",
            "Nostalgic Blood of the East ~ Old World",
            u"懐かしき東方の血 ～ Old World",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "doll_judgment": Theme(   # pursuit, Case 07, Alice
            "doll_judgment_theme",
            "Doll Judgment ~ the Girl Who Played with People's Shapes",
            u"人形裁判 ～ 人の形弄びし少女",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "native_faith": Theme(   # pursuit, Case 08, Reimu
            "native_faith_theme",
            "Native Faith",
            u"ネイティブフェイス",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "reverse_ideology": Theme(   # pursuit, Case 09, Kaguya
            "reverse_ideology_theme",
            "Reverse Ideology",
            u"リバースイデオロギー",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "captain_murasa": Theme(   # pursuit, Case 10, Mokou
            "captain_murasa_theme",
            "Captain Murasa",
            u"キャプテン・ムラサ",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        "joutounin": Theme(   # pursuit, Case 11, Aya
            "joutounin_theme",
            "Joutounin of Ceramics",
            u"セラミックスの杖刀人",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
        ),
        # Case 11: Aya's witness theme.
        "aya": Theme(
            "aya_theme",
            "Because Princess Inada Is Scolding Me",
            u"稲田姫様に叱られるから",
            "arr. +TEK  ·  comp. ZUN (Team Shanghai Alice)",
            loop=None,
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

    def bgm(name, fadein=1.0, card_delay=1.9, fadeout=None):
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
        renpy.music.play(filename, channel="music", loop=True, fadein=fadein, fadeout=fadeout)
        renpy.show_screen("bgm_title", theme, card_delay)

    def bgm_stop(fadeout=0.5):
        """Stops whatever theme is playing."""
        renpy.music.stop("music", fadeout=fadeout)
        renpy.hide_screen("bgm_title")


## The title screen theme, from BGM above.
define config.main_menu_music = BGM["title"].filename
define config.main_menu_music_fadein = 1.5
