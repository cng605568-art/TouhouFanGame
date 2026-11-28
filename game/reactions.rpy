################################################################################
## reactions.rpy - witness breakdowns and quick reactions.
##
## breakdown(who) is the moment a witness is caught: each one falls apart in
## their own way, with props drawn as plain objects (ice shards, stars, a
## pocket watch, red rings, the scales of judgement).
##
## react(who, kind) is a beat inside a conversation: nervous, smug, angry,
## shock or gloom. If art_src/ has a photo of that pose, named
## <who>_fumo_<kind>.jpg, the sprite workflow makes images/<who>_fumo_<kind>.png,
## which becomes the image "<who>_fumo <kind>", and react() swaps to it.
## Otherwise the fumo moves to suit and an emote pops up beside its head.
################################################################################

init -1 python:

    # Emote for each reaction kind.
    REACT_EMOTE = {"nervous": "sweat", "smug": "sparkle", "angry": "anger",
                   "shock": "exclaim", "gloom": "gloom"}

    def react(who, kind):
        """A quick reaction from whoever is on the stand or the bench."""
        tag = who + "_fumo"
        if not renpy.showing(tag):
            return
        # Drop any photo pose from the last reaction.
        for old in renpy.get_attributes(tag) or ():
            renpy.show((tag, "-" + old))
        if renpy.has_image((tag, kind), exact=True):
            renpy.show((tag, kind), at_list=[ fumo_talk ])
        else:
            renpy.show(tag, at_list=[ getattr(store, "fumo_" + kind) ])
            renpy.show_screen("emote", REACT_EMOTE[kind])
        # The next line keeps the reaction instead of hopping over it.
        store.fumo_hold = tag


label breakdown(who):
    $ renpy.show(who + "_fumo", at_list=[ BREAKDOWN_FUMO.get(who, fumo_shock) ])
    $ fumo_hold = who + "_fumo"
    $ sfx("break_" + who)
    show screen breakdown_fx(who)
    if who == "sakuya":
        camera at time_stop
    elif who == "reisen":
        camera at lunatic_wobble
    with vpunch
    return


################################################################################
## Screens
################################################################################

## Particles fly from the fumo's chest, around (960, 300).
screen breakdown_fx(who):
    zorder 35

    if who == "cirno":
        for dx, dy, rot, delay in ((-300, -160, -220, 0.0), (280, -190, 260, 0.03), (-360, 60, 180, 0.06),
                                   (340, 90, -200, 0.02), (-150, -280, 140, 0.08), (170, -300, -160, 0.05),
                                   (-240, 230, 300, 0.10), (250, 220, -280, 0.07)):
            add "gui/fx_shard.svg" at particle(960, 300, dx, dy, rot, delay)

    elif who == "marisa":
        for dx, dy, rot, delay in ((-320, -120, -360, 0.0), (310, -150, 360, 0.02), (-260, 140, 300, 0.05),
                                   (280, 160, -300, 0.04), (0, -320, 200, 0.07), (-120, 260, -240, 0.09),
                                   (140, 280, 240, 0.08), (0, 0, 720, 0.0)):
            add "gui/fx_star.svg" at particle(960, 280, dx, dy, rot, delay)

    elif who == "sakuya":
        fixed at watch_break:
            xysize (200, 200)
            add "gui/fx_watch.svg"
            add "gui/fx_crack.svg" at crack_in

    elif who == "reisen":
        for delay in (0.0, 0.25, 0.5):
            add "gui/fx_ring.svg" at ring_out(960, 250, delay)

    elif who == "eiki":
        add "gui/fx_scales_tip.svg" at scales_fall

    elif who == "meiling":
        # A rainbow of diamonds: Meiling's colourful qi, scattered.
        for i, (dx, dy, rot, delay) in enumerate(((-320, -150, -200, 0.0), (300, -170, 220, 0.02), (-340, 80, 160, 0.04),
                                                  (330, 100, -180, 0.03), (-160, -290, 120, 0.06), (180, -300, -140, 0.05),
                                                  (-260, 240, 260, 0.08), (250, 230, -240, 0.07), (0, -330, 90, 0.09))):
            add "gui/fx_diamond.svg" at particle(960, 300, dx, dy, rot, delay):
                matrixcolor TintMatrix(RAINBOW[i % len(RAINBOW)])

    elif who == "alice":
        # Doll strings snap and fall away.
        for dx, dy, rot, delay in ((-260, 200, -60, 0.0), (240, 220, 70, 0.03), (-140, 260, 30, 0.06),
                                   (150, 250, -40, 0.05), (-330, 120, -90, 0.08), (320, 140, 100, 0.07)):
            add "gui/fx_thread.svg" at particle(960, 200, dx, dy, rot, delay)

    elif who == "reimu":
        # Her ofuda flutter out of her sleeves.
        for dx, dy, rot, delay in ((-330, -100, -300, 0.0), (310, -120, 320, 0.02), (-280, 160, 260, 0.05),
                                   (300, 170, -280, 0.04), (-120, -300, 200, 0.07), (130, -290, -220, 0.06),
                                   (-60, 280, 360, 0.09), (70, 270, -360, 0.08)):
            add "gui/fx_ofuda.svg" at particle(960, 300, dx, dy, rot, delay)

    elif who == "kaguya":
        # Her impossible treasures scatter.
        for dx, dy, rot, delay in ((-300, -180, -160, 0.0), (290, -190, 170, 0.02), (-330, 90, 130, 0.04),
                                   (320, 110, -150, 0.03), (0, -320, 90, 0.06), (-180, 260, 200, 0.08), (190, 250, -210, 0.07)):
            add "gui/fx_jewel.svg" at particle(960, 300, dx, dy, rot, delay)

    timer 1.9 action Hide("breakdown_fx")


## Mokou's entrance: flames burst around Kaguya, at her knocked-back spot.
screen mokou_fire():
    zorder 35
    for dx, dy, rot, delay in ((-220, -160, -40, 0.0), (210, -170, 40, 0.03), (-260, 40, -20, 0.05), (250, 60, 25, 0.02),
                               (-120, -260, -10, 0.07), (130, -250, 15, 0.06), (0, -300, 0, 0.09)):
        add "gui/fx_flame.svg" at particle(1180, 330, dx, dy, rot, delay)
    timer 1.9 action Hide("mokou_fire")

## A reaction emote by the head of the fumo at centre stage.
screen emote(kind):
    zorder 36
    add "gui/emote_%s.svg" % kind at emote_pop
    timer 1.7 action Hide("emote")


################################################################################
## Transforms
################################################################################

## One particle: bursts out from (x, y), spins, fades.
transform particle(x, y, dx, dy, rot, delay):
    anchor (0.5, 0.5) pos (x, y) alpha 0.0 zoom 0.6 rotate 0
    pause delay
    alpha 1.0
    parallel:
        easeout 0.75 xoffset dx yoffset dy zoom 1.0
    parallel:
        linear 0.9 rotate rot
    parallel:
        pause 0.55
        linear 0.35 alpha 0.0

## Sakuya's pocket watch: pops in over her head, cracks, drops away.
transform watch_break:
    anchor (0.5, 0.5) pos (960, 200) zoom 0.2 alpha 0.0
    easeout 0.18 zoom 1.0 alpha 1.0
    pause 0.65
    parallel:
        easein 0.55 yoffset 260 rotate 40
    parallel:
        pause 0.25
        linear 0.3 alpha 0.0

transform crack_in:
    alpha 0.0
    pause 0.3
    linear 0.04 alpha 1.0

## Reisen's lunatic rings: spread from her eyes and fade.
transform ring_out(x, y, delay):
    anchor (0.5, 0.5) pos (x, y) zoom 0.2 alpha 0.0
    pause delay
    alpha 0.9
    parallel:
        easeout 1.0 zoom 4.0
    parallel:
        linear 1.0 alpha 0.0

## Eiki's scales tip over and fall past her.
transform scales_fall:
    anchor (0.5, 0.5) pos (960, 110) rotate 0 alpha 0.0
    linear 0.12 alpha 1.0
    easein 0.35 rotate -35
    parallel:
        easein 0.6 yoffset 520 rotate -120
    parallel:
        pause 0.35
        linear 0.25 alpha 0.0

transform emote_pop:
    anchor (0.5, 0.5) pos (1130, 170) zoom 0.4 alpha 0.0
    easeout 0.14 zoom 1.1 alpha 1.0
    easein 0.10 zoom 1.0
    pause 1.1
    linear 0.25 alpha 0.0

## Cirno freezes: an icy flash and a shiver.
transform fumo_frozen:
    subpixel True
    xoffset 0 yoffset 0 rotate None xzoom 1.0 yzoom 1.0 zoom 1.0
    matrixcolor TintMatrix("#BFE6FF") * BrightnessMatrix(0.35)
    parallel:
        linear 0.35 matrixcolor TintMatrix("#D8F0FF") * BrightnessMatrix(0.08)
        pause 0.8
        linear 0.6 matrixcolor TintMatrix("#FFFFFF") * BrightnessMatrix(0.0)
    parallel:
        block:
            linear 0.03 xoffset -4
            linear 0.03 xoffset 4
            repeat 20
        linear 0.03 xoffset 0

## Marisa spins like a dropped broom and wobbles to a stop.
transform fumo_spin:
    subpixel True
    xoffset 0 yoffset 0 rotate 0 xzoom 1.0 yzoom 1.0 zoom 1.0
    matrixcolor BrightnessMatrix(0.5)
    parallel:
        linear 0.25 matrixcolor BrightnessMatrix(0.0)
    parallel:
        easeout 0.12 yoffset -60
        easein 0.24 yoffset 0
    parallel:
        easein 0.45 rotate 360
        rotate 0
        ease 0.12 rotate -8
        ease 0.12 rotate 6
        ease 0.10 rotate -3
        ease 0.10 rotate 0

## Quick reactions (react()).
transform fumo_nervous:
    subpixel True
    xoffset 0 yoffset 0 rotate None xzoom 1.0 yzoom 1.0 zoom 1.0
    block:
        linear 0.04 xoffset -3
        linear 0.04 xoffset 3
        repeat 10
    linear 0.04 xoffset 0
    block:
        ease 1.4 yzoom 1.012
        ease 1.4 yzoom 1.0
        repeat

transform fumo_smug:
    subpixel True
    xoffset 0 yoffset 0 xzoom 1.0 yzoom 1.0 zoom 1.0 rotate 0
    ease 0.35 rotate 4 zoom 1.03
    pause 0.9
    ease 0.4 rotate 0 zoom 1.0

transform fumo_angry:
    subpixel True
    xoffset 0 yoffset 0 rotate None xzoom 1.0 yzoom 1.0 zoom 1.0
    matrixcolor TintMatrix("#FFD0C8")
    easeout 0.07 yoffset -24
    easein 0.09 yoffset 0
    easeout 0.07 yoffset -16
    easein 0.09 yoffset 0
    linear 0.4 matrixcolor TintMatrix("#FFFFFF")

transform fumo_gloom:
    subpixel True
    xoffset 0 yoffset 0 rotate None zoom 1.0
    ease 0.4 xzoom 1.03 yzoom 0.95 matrixcolor BrightnessMatrix(-0.12)
    pause 1.0
    ease 0.5 xzoom 1.0 yzoom 1.0 matrixcolor BrightnessMatrix(0.0)

## Whole-picture effects for a breakdown (camera transforms).
transform time_stop:
    matrixcolor SaturationMatrix(0.0)
    pause 0.5
    linear 0.4 matrixcolor SaturationMatrix(1.0)

## Mokou charges in from the left and plants herself beside the stand.
transform mokou_charge:
    subpixel True
    xanchor 0.5 yanchor 1.0 ypos FUMO_FEET xpos -320
    xoffset 0 yoffset 0 rotate None zoom 1.0 xzoom 1.0 yzoom 1.0
    easein 0.32 xpos 760
    easeout 0.06 xpos 800
    easein 0.16 xpos 700
    block:
        ease 1.4 yzoom 1.012
        ease 1.4 yzoom 1.0
        repeat

## Kaguya takes the hit and is knocked across the stand.
transform fumo_knocked:
    subpixel True
    xoffset 0 yoffset 0 zoom 1.0 xzoom 1.0 yzoom 1.0 rotate 0
    pause 0.36
    matrixcolor BrightnessMatrix(0.7)
    parallel:
        linear 0.25 matrixcolor BrightnessMatrix(0.0)
    parallel:
        easeout 0.14 xpos 1180 rotate 22
        easein 0.30 rotate 9
    parallel:
        easeout 0.10 yoffset -40
        easein 0.20 yoffset 0

## Off they go: Mokou drags Kaguya out of the court, right.
transform duo_exit(delay=0.0):
    subpixel True
    pause delay
    parallel:
        easein 0.75 xpos 2500
    parallel:
        block:
            easeout 0.12 yoffset -50
            easein 0.12 yoffset 0
            repeat 3

## The court flushes orange for a moment.
transform fire_flash:
    matrixcolor TintMatrix("#FFB070")
    linear 0.9 matrixcolor TintMatrix("#FFFFFF")

transform lunatic_wobble:
    matrixcolor TintMatrix("#FFC4C4")
    parallel:
        block:
            ease 0.12 xoffset -10
            ease 0.12 xoffset 10
            repeat 4
        ease 0.1 xoffset 0
    parallel:
        linear 1.0 matrixcolor TintMatrix("#FFFFFF")


## Defined after the transforms they name.
define BREAKDOWN_FUMO = { "cirno": fumo_frozen, "marisa": fumo_spin }

## Transforms the talk hop leaves alone (FumoHop in script.rpy).
define FUMO_STAY = (fumo_frozen, fumo_spin, mokou_charge, fumo_knocked, duo_exit)

## Meiling's breakdown colours.
define RAINBOW = [ "#FF5A5A", "#FFA43A", "#FFE04A", "#6BD66B", "#4AB8FF", "#8A6BFF", "#E46BFF" ]

default fumo_hold = None
