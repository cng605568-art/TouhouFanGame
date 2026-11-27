################################################################################
## audio.rpy - sound effects.
##
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
##   blip          text blip, looped while dialogue types out
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
        """Character callback: loops the blip while a line is typing out."""

        def __call__(self, event, interact=True, **kwargs):
            if not interact:
                return
            if event == "show":
                filename = sfx_file("blip")
                if filename and preferences.text_cps:
                    renpy.music.play(filename, channel="blip", loop=True)
            elif event in ("slow_done", "end"):
                renpy.music.stop(channel="blip")

    config.all_character_callbacks.append(TextBlip())

    # Button sounds for the styles in screens.rpy (set here, at init -1, so
    # they exist before those styles are built).
    SFX_HOVER = sfx_file("ui_hover")
    SFX_CONFIRM = sfx_file("ui_confirm")
    SFX_CANCEL = sfx_file("ui_cancel")
    SFX_NAV = sfx_file("nav")
