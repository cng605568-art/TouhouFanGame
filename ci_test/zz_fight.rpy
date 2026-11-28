## CI only: plays Mokou's fight on its own, with auto-advancing lines, so the
## fight-preview workflow can record it.
##
## Picture pass (RENPY_TIMEWARP slows game time): every sound effect is logged
## with its game time to fight_events.txt, measured from the white sync flash.
## Sound pass (FIGHT_AUDIO_PASS=1, real time): the demo runs once muted to
## warm the caches, then again for real; the gavel at the flash is heard, then
## the effects channel is muted, since the effects are mixed back in from the
## log, exactly on time.

init -1 python:
    import os as ci_os
    CI_AUDIO_PASS = bool(ci_os.environ.get("FIGHT_AUDIO_PASS"))

init 999 python:
    config.default_fullscreen = True
    ci_events = [ ]
    ci_sfx_real = sfx

    def sfx(name):
        fn = sfx_file(name)
        if fn:
            ci_events.append((renpy.display.core.get_time(), fn))
        ci_sfx_real(name)

    def ci_mark(tag):
        ci_events.append((renpy.display.core.get_time(), tag))

    def ci_write_events():
        if CI_AUDIO_PASS:
            return
        sync = [ t for t, f in ci_events if f == "SYNC" ][-1]
        with open(ci_os.path.join(config.basedir, "fight_events.txt"), "w") as f:
            for t, fn in ci_events:
                if t >= sync and fn != "SYNC":
                    f.write("%.4f %s\n" % (t - sync, fn))

    def ci_mute(on):
        setv = getattr(_preferences, "set_mixer", None) or _preferences.set_volume
        for m in ("music", "sfx", "voice"):
            setv(m, 0.0 if on else (config.default_music_volume if m == "music" else config.default_sfx_volume))

label ci_fight_demo:
    $ preferences.text_cps = 45
    $ difficulty = "normal"
    $ spirit_reset()
    if CI_AUDIO_PASS:
        $ ci_mute(True)
        call ci_fight_body
        $ renpy.music.stop(channel="music", fadeout=0)
        $ renpy.music.stop(channel="event", fadeout=0)
        $ ci_mute(False)
    $ ci_events[:] = [ ]
    call ci_fight_body(True)
    $ ci_write_events()
    $ renpy.quit()

label ci_fight_body(real=False):
    $ renpy.music.stop(channel="music", fadeout=0)
    window hide
    hide screen court_hud
    scene black
    pause 1.5
    if real:
        $ ci_mark("SYNC")
        $ ci_sfx_real("gavel")
        show expression Solid("#FFFFFF") as ci_sync
        pause 0.25
        hide ci_sync
        pause 0.55
        if CI_AUDIO_PASS:
            $ renpy.music.set_volume(0.0, channel="event")
    $ case_number = _("CASE 09")
    $ case_title = _("The Five Impossible Chores")
    $ case_key = "case9"
    show screen court_hud
    call shot_eiki(None)
    pause 0.8
    eiki "Every cup. Bailiff.{w=0.9}{nw}"
    komachi "On it, boss.{w=0.7}{nw}"
    window hide
    call shot_kaguya
    $ bgm("mokou", fadein=0.3, card_delay=2.4, fadeout=0.2)
    call mokou_entrance
    window auto
    mokou "KAGUYAAA!{w=0.9}{nw}"
    kaguya "Oh no. Not now. Not in court.{w=0.9}{nw}"
    mokou "Great. I'll take custody.{w=0.9}{nw}"
    window hide
    call fight_faceoff
    call fight_rush
    call fight_finisher
    window auto
    kaguya "Ow! Ow! My face is priceless!{w=1.1}{nw}"
    mokou "So's this. Free of charge.{w=0.9}{nw}"
    window hide
    call fight_dash_exit
    window auto
    kaguya "Eirin! Somebody! Bailiff!{w=1.1}{nw}"
    call fight_cleanup
    call shot_eiki
    komachi "...Want me to chase them, boss?{w=1.5}{nw}"
    window hide
    pause 0.5
    return

testcase fight:
    pause 2.0
    run Start("ci_fight_demo")
    pause 3000.0
