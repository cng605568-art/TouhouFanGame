################################################################################
## fight.rpy - Mokou's rampage at the end of Case 09, staged as an anime fight.
##
##   mokou_entrance   a cut-in ("FUJIWARA NO MOKOU"), then she lands on the
##                    stand hard enough to crack the court in two
##   fight_faceoff    the screen splits: her eyes, Kaguya's eyes, lightning
##   fight_rush       seven blows in a second, sparks and afterimages
##   fight_finisher   time slows, then one enormous hit
##   fight_dash_exit  she grabs Kaguya and is gone in a burst of dust
##
## Impact frames come from a two-tone shader on the camera (ink on paper,
## inverted, then red). Sparks, fire, rings and smoke are Kenney's CC0
## particle sprites in gui/vfx/ (tools/make_vfx.py); the focus lines, speed
## streaks and cut-in band are drawn by the same script. Sounds: the fight_*
## slots in tools/build_sfx.py. All the effects sit on the master layer, so
## camera moves and impact frames hit them as well as the fumos.
################################################################################

## Runs after script.rpy (the cast, shots) and reactions.rpy.
init offset = 2


init python:

    # Manga impact frames: every pixel snaps to ink or paper by brightness.
    renpy.register_shader("fumo.impact", variables="""
        uniform float u_impact;
        uniform float u_cut;
        uniform vec4 u_ink;
        uniform vec4 u_paper;
    """, fragment_300="""
        float fumo_l = dot(gl_FragColor.rgb, vec3(0.299, 0.587, 0.114));
        vec3 fumo_two = mix(u_ink.rgb, u_paper.rgb, step(u_cut, fumo_l)) * gl_FragColor.a;
        gl_FragColor.rgb = mix(gl_FragColor.rgb, fumo_two, u_impact);
    """)

    # Close-ups cut from the fumo photos: (x, y, width, height) in the PNG.
    FIGHT_FACE = { "mokou": (60, 170, 560, 390), "kaguya": (110, 120, 610, 400) }
    FIGHT_EYES = { "mokou": (40, 280, 600, 200), "kaguya": (100, 290, 640, 190) }

    def fight_crop(who, box, zoom):
        return Transform(Crop(box, "images/%s_fumo.png" % who), zoom=zoom)

    def faceoff_half(who, tint, mask, eyes_pos, zoom):
        """One side of the split screen: a colour field and a pair of eyes."""
        return AlphaMask(
            Fixed(Solid(tint),
                  Transform(fight_crop(who, FIGHT_EYES[who], zoom), pos=eyes_pos),
                  xysize=(1920, 1080)),
            mask)

    FACEOFF_LEFT = faceoff_half("mokou", "#5C0E08", "gui/vfx/split_left.svg", (-40, 360), 1.8)
    FACEOFF_RIGHT = faceoff_half("kaguya", "#14123C", "gui/vfx/split_right.svg", (820, 380), 1.7)


## Fumos named here keep their fight pose while they talk (no talk hop).
default fumo_freeze = set()


################################################################################
## Images
################################################################################

## Focus lines that flicker between three drawings, as in a manga panel.
image focus_lines:
    "gui/vfx/focus_0.svg"
    pause 0.05
    "gui/vfx/focus_1.svg"
    pause 0.05
    "gui/vfx/focus_2.svg"
    pause 0.05
    repeat

image focus_lines_white:
    "gui/vfx/focus_red_0.svg"
    pause 0.05
    "gui/vfx/focus_red_1.svg"
    pause 0.05
    "gui/vfx/focus_red_2.svg"
    pause 0.05
    repeat

image speed_streaks:
    "gui/vfx/streaks_0.svg"
    pause 0.04
    "gui/vfx/streaks_1.svg"
    pause 0.04
    repeat


################################################################################
## Camera
################################################################################

## The three impact frames, then a hard shake that dies away.
transform impact_cam:
    shader "fumo.impact"
    u_cut 0.32 u_impact 1.0
    u_ink (0.03, 0.02, 0.04, 1.0) u_paper (1.0, 0.97, 0.92, 1.0)
    xoffset 26 yoffset -16
    pause 0.05
    u_ink (1.0, 0.97, 0.92, 1.0) u_paper (0.05, 0.01, 0.03, 1.0)
    xoffset -24 yoffset 18
    pause 0.05
    u_ink (0.12, 0.0, 0.03, 1.0) u_paper (0.96, 0.16, 0.18, 1.0)
    xoffset 18 yoffset 10
    pause 0.05
    u_impact 0.0
    xoffset -14 yoffset -8
    pause 0.04
    xoffset 10 yoffset 6
    pause 0.04
    xoffset -6 yoffset -3
    pause 0.04
    xoffset 3 yoffset 2
    pause 0.04
    xoffset 0 yoffset 0

## The rush: a jolt on every blow, impact frames on the last.
transform rush_cam:
    shader "fumo.impact"
    u_cut 0.32 u_impact 0.0
    u_ink (0.03, 0.02, 0.04, 1.0) u_paper (1.0, 0.97, 0.92, 1.0)
    xoffset 0 yoffset 0
    block:
        xoffset 14 yoffset -6
        pause 0.04
        xoffset -12 yoffset 5
        pause 0.04
        xoffset 6 yoffset -2
        pause 0.04
        xoffset 0 yoffset 0
        pause 0.04
        repeat 6
    u_impact 1.0 xoffset 22 yoffset -12
    pause 0.05
    u_ink (1.0, 0.97, 0.92, 1.0) u_paper (0.05, 0.01, 0.03, 1.0)
    xoffset -20 yoffset 12
    pause 0.05
    u_impact 0.0 xoffset 8 yoffset -4
    pause 0.05
    xoffset 0 yoffset 0

## Time slows: the court drains of colour and the camera creeps in on Kaguya.
transform slowmo_cam:
    subpixel True
    xanchor 0.56 xpos 0.56 yanchor 0.4 ypos 0.4
    zoom 1.0 matrixcolor SaturationMatrix(1.0)
    parallel:
        easein 1.15 zoom 1.22
    parallel:
        linear 0.35 matrixcolor SaturationMatrix(0.12)

## The last blow: impact frames, a punch-in, then a long, heavy shake back out.
transform final_cam:
    subpixel True
    shader "fumo.impact"
    xanchor 0.56 xpos 0.56 yanchor 0.4 ypos 0.4
    u_cut 0.3 u_impact 1.0
    zoom 1.32 matrixcolor SaturationMatrix(1.0)
    u_ink (0.03, 0.02, 0.04, 1.0) u_paper (1.0, 0.97, 0.92, 1.0)
    xoffset 30 yoffset -18
    pause 0.06
    u_ink (1.0, 0.97, 0.92, 1.0) u_paper (0.05, 0.01, 0.03, 1.0)
    xoffset -28 yoffset 20
    pause 0.06
    u_ink (0.12, 0.0, 0.03, 1.0) u_paper (0.96, 0.16, 0.18, 1.0)
    xoffset 22 yoffset 12
    pause 0.06
    u_impact 0.0
    parallel:
        easeout 0.7 zoom 1.0
    parallel:
        block:
            xoffset -18 yoffset -10
            pause 0.04
            xoffset 16 yoffset 9
            pause 0.04
            repeat 3
        block:
            xoffset -9 yoffset -5
            pause 0.05
            xoffset 8 yoffset 4
            pause 0.05
            repeat 3
        xoffset 0 yoffset 0


################################################################################
## Fumo moves
################################################################################

## A fumo sprite is 500 px tall, feet on FUMO_FEET. Moves that spin a fumo
## anchor its middle, so a tilt never lifts it off the cushion.
define FUMO_MID = FUMO_FEET - 250

## Mokou drops out of the sky onto the stand.
transform mokou_land:
    subpixel True
    xanchor 0.5 yanchor 1.0 ypos FUMO_FEET xpos 700
    xoffset 0 yoffset -1150 rotate None zoom 1.0 xzoom 1.0 yzoom 1.0 alpha 1.0
    easein 0.16 yoffset 0
    easeout 0.06 xzoom 1.2 yzoom 0.78
    easein 0.22 xzoom 1.0 yzoom 1.0
    block:
        ease 0.9 yzoom 1.015
        ease 0.9 yzoom 1.0
        repeat

## Kaguya is blown sideways by the landing.
transform kaguya_recoil:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID
    xoffset 0 yoffset 0 rotate 0
    easeout 0.12 xpos 1200 rotate 12 yoffset -50
    easein 0.28 xpos 1180 rotate 4 yoffset 0

## The rush: Mokou lunges seven times.
transform mokou_rush:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID xpos 700
    yzoom 1.0 rotate 0
    block:
        easeout 0.05 xpos 940 rotate 8
        easein 0.11 xpos 820 rotate 0
        repeat 6
    easeout 0.06 xpos 980 rotate 12
    easein 0.3 xpos 820 rotate 0

## ...and Kaguya rocks back under each one, flashing white.
transform kaguya_rushed:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID xpos 1180 rotate 4
    xoffset 0 yoffset 0 matrixcolor BrightnessMatrix(0.0)
    block:
        pause 0.04
        matrixcolor BrightnessMatrix(0.65)
        easeout 0.04 xoffset 34 rotate 14
        matrixcolor BrightnessMatrix(0.0)
        easein 0.08 xoffset 8 rotate 4
        repeat 6
    pause 0.02
    matrixcolor BrightnessMatrix(0.8)
    easeout 0.08 xoffset 70 rotate 24 yoffset -30
    matrixcolor BrightnessMatrix(0.0)
    easein 0.3 xoffset 40 rotate 10 yoffset 0

## Winding up for the last blow, in slow motion, fire gathering.
transform mokou_windup:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID xpos 820
    rotate 0 yzoom 1.0 xzoom 1.0
    ease 1.1 xpos 760 rotate -10 xzoom 0.94 yzoom 1.05

transform kaguya_brace:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID xpos 1220
    xoffset 0 yoffset 0 rotate 10
    ease 1.1 rotate 2 xoffset -6

## The blow itself.
transform mokou_strike:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID xpos 760
    rotate -10 xzoom 1.0 yzoom 1.0
    easeout 0.06 xpos 1060 rotate 16 xzoom 1.15 yzoom 0.92
    easein 0.5 xpos 860 rotate 0 xzoom 1.0 yzoom 1.0
    block:
        ease 0.9 yzoom 1.015
        ease 0.9 yzoom 1.0
        repeat

## Kaguya flies up, comes down flat, and stays there seeing stars.
transform kaguya_floored:
    subpixel True
    xanchor 0.5 yanchor 0.5 ypos FUMO_MID xpos 1220
    xoffset 0 yoffset 0 rotate 2 matrixcolor BrightnessMatrix(0.9)
    parallel:
        linear 0.3 matrixcolor BrightnessMatrix(0.0)
    parallel:
        easeout 0.28 yoffset -420 xoffset 90 rotate 220
        easein 0.3 yoffset 40 xoffset 100 rotate 450
        easeout 0.08 yoffset 12
        easein 0.1 yoffset 40
    block:
        ease 0.6 rotate 446
        ease 0.6 rotate 454
        repeat

## Mokou grabs her and they're gone: a crouch, then a smear off stage right.
transform dash_exit(delay=0.0):
    subpixel True
    pause delay
    easeout 0.12 xoffset -40 xzoom 0.9 yzoom 1.08
    easein 0.22 xpos 2700 xzoom 1.9 yzoom 0.85


################################################################################
## Particle moves
################################################################################

## A sprite that pops in, spins and fades: hit flares, sparks.
transform pop_fx(x, y, delay, size=1.0, rot=0, tint="#FFFFFF", life=0.22):
    anchor (0.5, 0.5) pos (x, y) zoom 0.0 alpha 0.0 rotate rot
    matrixcolor TintMatrix(tint)
    blend "add"
    pause delay
    alpha 1.0
    parallel:
        easeout 0.07 zoom size
        linear (life - 0.07) zoom size * 1.25
    parallel:
        pause life * 0.4
        linear life * 0.6 alpha 0.0

## A flat ring that races out along the floor (or a full one in the air).
transform shock_ring(x, y, delay, size, flat=0.35, tint="#FFF2C8"):
    anchor (0.5, 0.5) pos (x, y) zoom 0.05 yzoom flat alpha 0.0
    matrixcolor TintMatrix(tint)
    blend "add"
    pause delay
    alpha 1.0
    parallel:
        easeout 0.5 zoom size
    parallel:
        linear 0.5 alpha 0.0

## Smoke or dust that rolls outward and fades.
transform puff(x, y, dx, dy, delay, size=1.0, tint="#D8C8B8", life=0.9):
    anchor (0.5, 0.5) pos (x, y) zoom size * 0.3 alpha 0.0 rotate 0
    matrixcolor TintMatrix(tint)
    pause delay
    alpha 0.9
    parallel:
        easeout life xoffset dx yoffset dy zoom size
    parallel:
        linear life rotate 40
    parallel:
        pause life * 0.35
        linear life * 0.65 alpha 0.0

## An ember flung out of an explosion, cooling as it flies.
transform ember(x, y, dx, dy, delay):
    anchor (0.5, 0.5) pos (x, y) zoom 0.0 alpha 0.0
    matrixcolor TintMatrix("#FFB04A")
    blend "add"
    pause delay
    alpha 1.0 zoom 0.5
    parallel:
        easeout 0.7 xoffset dx yoffset dy zoom 0.25
    parallel:
        linear 0.7 rotate 180
    parallel:
        pause 0.35
        linear 0.35 alpha 0.0

## Fire that bursts and flickers.
transform blaze(x, y, delay, size=1.0, tint="#FF8A2A", life=0.8, rot=0):
    anchor (0.5, 0.5) pos (x, y) zoom size * 0.2 alpha 0.0 rotate rot
    matrixcolor TintMatrix(tint)
    blend "add"
    pause delay
    alpha 1.0
    parallel:
        easeout 0.18 zoom size
        linear (life - 0.18) zoom size * 1.15
    parallel:
        linear life rotate rot + 30
    parallel:
        pause life * 0.5
        linear life * 0.5 alpha 0.0

## A full-screen overlay that shows for a while: focus lines, streaks.
transform overlay_window(delay, dur, peak=1.0):
    alpha 0.0
    pause delay
    alpha peak
    pause dur
    linear 0.15 alpha 0.0

## A full-screen flash of colour.
transform flash_once(delay=0.0, peak=1.0, fade=0.25):
    alpha 0.0
    pause delay
    alpha peak
    linear fade alpha 0.0

## Manga sound-effect lettering: slams in big, jitters, fades.
transform sfx_letters(x, y, delay, rot=-8, size=1.0):
    anchor (0.5, 0.5) pos (x, y) rotate rot zoom size * 2.4 alpha 0.0
    pause delay
    alpha 1.0
    easeout 0.1 zoom size
    block:
        xoffset 5 yoffset -3
        pause 0.035
        xoffset -5 yoffset 3
        pause 0.035
        repeat 6
    xoffset 0 yoffset 0
    linear 0.18 alpha 0.0 zoom size * 1.12

## Afterimages of Mokou behind her lunge.
transform ghost(x, delay):
    xanchor 0.5 yanchor 1.0 ypos FUMO_FEET xpos x
    alpha 0.0 matrixcolor TintMatrix("#FF9A50")
    blend "add"
    pause delay
    alpha 0.45
    linear 0.25 alpha 0.0

## A star circling over Kaguya's head while she's dazed.
transform dizzy_star(cx, cy, phase):
    anchor (0.5, 0.5) zoom 0.42
    matrixcolor TintMatrix("#FFE27A")
    blend "add"
    around (cx, cy) radius 140 angle phase
    linear 1.4 angle phase + 360
    repeat

## The cut-in band slides across, drifts, and shoots off.
transform cutin_slide:
    subpixel True
    anchor (0.5, 0.5) pos (960, 440) rotate -7
    xoffset -2700
    easeout 0.16 xoffset 70
    linear 0.8 xoffset -50
    easein 0.14 xoffset 2700

transform cutin_streaks:
    xoffset 0
    linear 0.5 xoffset -1920
    xoffset 0
    repeat

transform cutin_face:
    subpixel True
    xpos 1520 ypos 14 xoffset 120
    easeout 0.4 xoffset 0
    linear 0.8 xoffset -40

## The two halves of the face-off slide in from either side.
transform faceoff_in(dx):
    subpixel True
    xoffset dx alpha 1.0
    easeout 0.2 xoffset 0
    linear 1.1 xoffset dx * -0.02
    linear 0.15 alpha 0.0

## The lightning down the seam.
transform seam_bolt(delay):
    anchor (0.5, 0.5) pos (960, 540) rotate 16 yzoom 3.3 xzoom 1.4 alpha 0.0
    matrixcolor TintMatrix("#FFF0B0")
    blend "add"
    pause delay
    block:
        alpha 1.0
        pause 0.05
        alpha 0.35
        pause 0.04
        repeat 6
    linear 0.15 alpha 0.0


################################################################################
## Effect screens (on the master layer, under the camera)
################################################################################

style fight_letters is default:
    font FONT_HEAD
    size 150
    color "#FFF4D6"
    outlines [ (absolute(10), "#1A0508", absolute(0), absolute(0)), (absolute(18), "#E0441C", absolute(0), absolute(0)) ]

style fight_cutin_name is default:
    font FONT_HEAD
    size 84
    color "#FFE9A8"
    kerning 6
    outlines [ (absolute(6), "#1A0508", absolute(0), absolute(0)) ]

style fight_cutin_sub is default:
    font FONT_HEAD
    size 62
    color "#FFFFFF"
    kerning 10
    outlines [ (absolute(5), "#C0281C", absolute(0), absolute(0)) ]

## Manga sound-effect lettering for one beat: (text, x, y, delay, rotation,
## font size). On the screens layer, so it stays put while the camera shakes.
screen fight_letters(tag, items, life=2.0):
    zorder 45
    for word, x, y, d, rot, sz in items:
        text word style "fight_letters" size sz at sfx_letters(x, y, d, rot)
    timer life action Hide(tag)

init python:
    def fight_say(tag, items, life=2.0):
        renpy.show_screen("fight_letters", tag, items, life, _tag=tag)

## "FUJIWARA NO MOKOU": the band, her face, speed streaks, fire.
screen fight_cutin(who, name, sub):
    layer "master"
    zorder 60
    add Solid("#0A0205") at flash_once(0.0, 0.6, 1.2)
    fixed at cutin_slide:
        xysize (2400, 420)
        add "gui/vfx/cutin_band.svg"
        fixed:
            xysize (2400, 420)
            add Crop((0, 330, 1920, 420), "gui/vfx/streaks_0.svg") at cutin_streaks
            add Crop((0, 330, 1920, 420), "gui/vfx/streaks_1.svg") xpos 1920 at cutin_streaks
        add fight_crop(who, FIGHT_FACE[who], 1.0) at cutin_face
        for x, d in ((1560, 0.05), (1800, 0.12), (2060, 0.02), (1680, 0.22), (1940, 0.3)):
            add "gui/vfx/flame_lick.png" at blaze(x, 360, d, 1.1, "#FF7A2A", 0.6)
        vbox:
            xpos 380 yalign 0.5
            spacing 4
            text name style "fight_cutin_name"
            text sub style "fight_cutin_sub"
    timer 1.4 action Hide("fight_cutin")

## Landing: rings along the floor, dust, debris, focus lines, lettering.
screen fight_land_fx():
    layer "master"
    zorder 40
    add Solid("#FFFFFF") at flash_once(0.0, 0.85, 0.2)
    add "focus_lines" at overlay_window(0.0, 0.5, 0.9)
    add "gui/vfx/ring.png" at shock_ring(700, 585, 0.0, 3.2)
    add "gui/vfx/ring.png" at shock_ring(700, 585, 0.07, 5.0)
    add "gui/vfx/glow.png" at pop_fx(700, 540, 0.0, 3.0, 0, "#FFD38A", 0.35)
    for dx, d in ((-380, 0.0), (360, 0.02), (-200, 0.06), (220, 0.05), (-520, 0.1), (500, 0.08)):
        add "gui/vfx/smoke_a.png" at puff(700, 590, dx, -90, d, 1.3)
    add "gui/vfx/debris.png" at puff(700, 520, -240, -260, 0.0, 1.2, "#5A3A2A", 0.7)
    add "gui/vfx/debris.png" at puff(700, 520, 260, -240, 0.03, 1.1, "#5A3A2A", 0.7)
    for x, d, r in ((560, 0.02, -30), (840, 0.04, 30), (700, 0.0, 0)):
        add "gui/vfx/flame_jet.png" at blaze(x, 470, d, 1.4, "#FF7A2A", 0.7, r)
    timer 2.0 action Hide("fight_land_fx")

## The face-off: the screen splits on a diagonal, her eyes against Kaguya's.
screen fight_faceoff():
    layer "master"
    zorder 60
    add Solid("#000000") at flash_once(0.0, 0.92, 1.6)
    add FACEOFF_LEFT at faceoff_in(-900)
    add FACEOFF_RIGHT at faceoff_in(900)
    for x, y, d in ((160, 760, 0.1), (420, 860, 0.2), (700, 780, 0.0), (300, 640, 0.3), (560, 700, 0.4)):
        add "gui/vfx/flame_lick.png" at blaze(x, y, d, 1.4, "#FF6A1A", 0.9)
    for x, y, d in ((1300, 260, 0.05), (1560, 180, 0.2), (1760, 320, 0.35), (1420, 140, 0.5)):
        add "gui/vfx/flare_star.png" at pop_fx(x, y, d, 0.6, 0, "#B8C8FF", 0.6)
    add "gui/vfx/split_edge.svg" at overlay_window(0.12, 1.1)
    add "gui/vfx/bolt_b.png" at seam_bolt(0.12)
    add Solid("#FFFFFF") at flash_once(0.12, 0.8, 0.15)
    timer 1.7 action Hide("fight_faceoff")

## The rush: a flare and a spark on every blow, afterimages, lettering.
screen fight_rush_fx():
    layer "master"
    zorder 40
    add "focus_lines" at overlay_window(0.0, 1.0, 0.8)
    for i, t in enumerate((0.04, 0.2, 0.36, 0.52, 0.68, 0.84)):
        add "gui/vfx/flare_cross.png" at pop_fx(1130 + (i % 3 - 1) * 40, 300 + (i % 2) * 90, t, 1.0 + (i % 2) * 0.3, i * 25, "#FFF0B8")
        add "gui/vfx/crackle.png" at pop_fx(1150, 330, t, 0.9, i * 60, "#FFE08A", 0.18)
        add "mokou_fumo" at ghost(840 - i * 30, t)
    add "gui/vfx/flare_cross.png" at pop_fx(1170, 320, 0.98, 2.0, 15, "#FFFFFF", 0.3)
    add "gui/vfx/ring.png" at shock_ring(1170, 320, 0.98, 2.4, 1.0)
    timer 1.6 action Hide("fight_rush_fx")

## Slow motion: embers drift up through the grey, fire gathers in her fist.
screen fight_slowmo_fx():
    layer "master"
    zorder 40
    add "focus_lines_white" at overlay_window(0.0, 1.1, 0.35)
    for x, d in ((620, 0.0), (760, 0.25), (880, 0.5), (700, 0.7), (820, 0.15)):
        add "gui/vfx/flame_lick.png" at puff(x, 560, (x - 760) // 4, -260, d, 0.7, "#FF8A2A", 1.2)
    add "gui/vfx/swirl.png" at blaze(820, 330, 0.0, 2.2, "#FF9A40", 1.2)
    add "gui/vfx/glow.png" at blaze(820, 330, 0.3, 1.8, "#FFB050", 0.9)
    timer 1.3 action Hide("fight_slowmo_fx")

## The last blow: an explosion of fire, rings, debris and smoke.
screen fight_final_fx():
    layer "master"
    zorder 40
    add Solid("#FFFFFF") at flash_once(0.0, 1.0, 0.3)
    add "focus_lines" at overlay_window(0.0, 0.7, 1.0)
    add "gui/vfx/fireball_a.png" at blaze(1200, 330, 0.0, 3.4, "#FF7A22", 1.0)
    add "gui/vfx/fireball_b.png" at blaze(1240, 300, 0.06, 2.8, "#FFB03A", 0.9, 40)
    add "gui/vfx/glow.png" at pop_fx(1200, 330, 0.0, 6.0, 0, "#FFE0A0", 0.5)
    add "gui/vfx/ring.png" at shock_ring(1200, 330, 0.0, 4.5, 1.0, "#FFE8B0")
    add "gui/vfx/ring.png" at shock_ring(1200, 330, 0.1, 7.0, 1.0, "#FFB060")
    add "gui/vfx/ring.png" at shock_ring(1200, 585, 0.04, 6.0, 0.3)
    for dx, dy, d in ((-560, -220, 0.02), (580, -260, 0.03), (-340, -460, 0.05), (400, -420, 0.04),
                      (0, -520, 0.06), (-700, -60, 0.03), (720, -40, 0.04), (-180, -560, 0.07)):
        add "gui/vfx/flare_star.png" at ember(1200, 330, dx, dy, d)
    add "gui/vfx/debris.png" at puff(1200, 420, -320, -200, 0.02, 0.9, "#9A7A5A", 0.7)
    add "gui/vfx/debris.png" at puff(1200, 420, 340, -180, 0.03, 0.9, "#9A7A5A", 0.7)
    for dx, d in ((-600, 0.2), (620, 0.22), (-350, 0.3), (400, 0.28)):
        add "gui/vfx/smoke_a.png" at puff(1200, 470, dx, -140, d, 1.6, "#EADCCF", 1.3)
    timer 2.0 action Hide("fight_final_fx")

## Kaguya, flat out and seeing stars.
screen fight_dizzy():
    layer "master"
    zorder 41
    for ph in (0, 90, 180, 270):
        add "gui/vfx/flare_star.png" at dizzy_star(1450, 250, ph)

## Off they go: a burst of dust, streaks across the court, a scorch mark left
## behind, smoke hanging in the air.
screen fight_dash_fx():
    layer "master"
    zorder 40
    add "speed_streaks" at overlay_window(0.1, 0.35, 0.9)
    for dx, d in ((-260, 0.0), (-120, 0.03), (-380, 0.06), (60, 0.08), (-200, 0.12)):
        add "gui/vfx/smoke_a.png" at puff(900, 560, dx, -80, d, 1.5, "#E2D4C6", 1.1)
    add "gui/vfx/scorch.png" at puff(980, 600, 0, 0, 0.1, 1.6, "#1A0A08", 6.0)
    add "gui/vfx/smoke_b.png" at puff(1000, 480, 900, -60, 0.15, 2.0, "#9A8A80", 1.6)
    timer 2.2 action Hide("fight_dash_fx")


################################################################################
## The fight, beat by beat. Case 09 calls these between Mokou's lines.
################################################################################

label mokou_entrance:
    $ fumo_freeze = { "mokou_fumo", "kaguya_fumo" }
    $ sfx("fight_cutin")
    show screen fight_cutin("mokou", _("FUJIWARA NO MOKOU"), "藤原妹紅、参上！")
    pause 1.15
    show mokou_fumo at mokou_land
    pause 0.16
    $ sfx("fight_land")
    show kaguya_fumo at kaguya_recoil
    show screen fight_land_fx
    $ fight_say("fl_land", [ (_("ドンッ！"), 470, 220, 0.0, -10, 150) ])
    camera at impact_cam
    pause 0.9
    camera
    return

label fight_faceoff:
    $ sfx("fight_vs")
    show screen fight_faceoff
    $ fight_say("fl_vs", [ ("VS", 960, 540, 0.15, -6, 190) ], 1.7)
    pause 1.55
    return

label fight_rush:
    $ sfx("fight_rush")
    show mokou_fumo at mokou_rush
    show kaguya_fumo at kaguya_rushed
    show screen fight_rush_fx
    $ fight_say("fl_rush", [ (_("ドドドドッ！"), 1260, 130, 0.1, 8, 120), (_("バキッ！"), 1480, 520, 0.95, -12, 150) ], 1.6)
    camera at rush_cam
    pause 1.25
    return

label fight_finisher:
    $ renpy.music.set_volume(0.25, delay=0.25, channel="music")
    $ sfx("fight_slowmo")
    show mokou_fumo at mokou_windup
    show kaguya_fumo at kaguya_brace
    show screen fight_slowmo_fx
    $ fight_say("fl_slow", [ (_("ゴゴゴゴ…"), 560, 150, 0.1, -4, 110) ], 1.3)
    camera at slowmo_cam
    pause 1.2
    $ sfx("fight_final")
    $ renpy.music.set_volume(1.0, delay=1.0, channel="music")
    show mokou_fumo at mokou_strike
    show kaguya_fumo at kaguya_floored
    show screen fight_final_fx
    $ fight_say("fl_final", [ (_("ドゴォォン！！"), 760, 190, 0.04, -10, 170) ])
    camera at final_cam
    pause 1.5
    camera
    show screen fight_dizzy
    return

label fight_dash_exit:
    hide screen fight_dizzy
    $ sfx("fight_dash")
    show screen fight_dash_fx
    $ fight_say("fl_dash", [ (_("ビュンッ！"), 1500, 260, 0.12, 6, 130) ], 1.6)
    show mokou_fumo at dash_exit(0.0)
    show kaguya_fumo at dash_exit(0.05)
    show fumo_shadow at shadow_gone
    pause 0.9
    hide mokou_fumo
    hide kaguya_fumo
    $ fumo_freeze = set()
    return

## Clears any fight effects still running (before a cut).
label fight_cleanup:
    hide screen fight_dash_fx
    hide screen fight_dizzy
    hide screen fight_final_fx
    $ fumo_freeze = set()
    camera
    return
