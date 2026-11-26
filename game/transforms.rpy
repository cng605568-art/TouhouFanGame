################################################################################
## transforms.rpy - Fumo juice, camera moves and UI animation.
##
## Character transforms only animate offsets, zoom and rotation. Position comes
## from the transform the sprite was first shown with (on_stand), and Ren'Py
## carries it over whenever a new transform replaces the old one, so you can
## write  `show cirno_fumo at fumo_talk`  without repeating coordinates.
################################################################################


################################################################################
## Vignette shader (used by eiki_lecture)
################################################################################

init python:

    # Darkens each pixel by its distance from the centre of the window.
    # Screen-space, so it stays put while the camera zooms underneath it.
    renpy.register_shader("fumo.vignette", variables="""
        uniform float u_vignette;
        uniform vec4 u_viewport;
    """, fragment_300="""
        vec2 fumo_uv = (gl_FragCoord.xy - u_viewport.xy) / u_viewport.zw;
        float fumo_d = distance(fumo_uv, vec2(0.5, 0.5));
        gl_FragColor.rgb *= 1.0 - smoothstep(0.28, 0.82, fumo_d) * u_vignette;
    """)


################################################################################
## Staging
################################################################################

## The witness stand / judge's bench, centred under the character.
transform stand_pos:
    xpos 960 xanchor 0.5
    ypos STAND_Y yanchor 0.0

## A fumo sitting on the stand's cushion, breathing very slightly.
transform on_stand:
    subpixel True
    xpos 960 xanchor 0.5
    ypos FUMO_FEET yanchor 1.0
    xoffset 0 yoffset 0 zoom 1.0 xzoom 1.0 yzoom 1.0 rotate None
    block:
        ease 1.4 yzoom 1.012
        ease 1.4 yzoom 1.0
        repeat


################################################################################
## Fumo juice
################################################################################

## Speaking: snappy hop with squash-and-stretch, then back to breathing.
transform fumo_talk:
    subpixel True
    xoffset 0 yoffset 0 zoom 1.0 rotate None
    xzoom 1.04 yzoom 0.92
    parallel:
        easeout 0.08 yoffset -30
        easein 0.10 yoffset 0
    parallel:
        easeout 0.08 xzoom 0.97 yzoom 1.05
        easein 0.10 xzoom 1.03 yzoom 0.95
        easeout 0.12 xzoom 1.0 yzoom 1.0
    block:
        ease 1.4 yzoom 1.012
        ease 1.4 yzoom 1.0
        repeat

## Caught in a lie: rapid horizontal shake while lurching toward the camera.
transform fumo_shock:
    subpixel True
    xoffset 0 yoffset 0 rotate None xzoom 1.0 yzoom 1.0
    zoom 1.0
    parallel:
        easeout 0.07 zoom 1.12
        easein 0.30 zoom 1.06
    parallel:
        block:
            linear 0.025 xoffset -22
            linear 0.050 xoffset 22
            linear 0.025 xoffset 0
            repeat 5
        linear 0.04 xoffset 0

## Defeated by a verdict: squash, then a full 360 spin off the top-right.
## The anchor moves to the sprite's centre so the spin pivots there; the
## yoffset cancels that move so nothing jumps.
transform fumo_yeet:
    subpixel True
    zoom 1.0 xzoom 1.0 yzoom 1.0 xoffset 0
    anchor (0.5, 0.5) yoffset FUMO_CENTER_LIFT
    rotate 0
    easein 0.12 xzoom 1.12 yzoom 0.84
    parallel:
        easeout 0.9 yoffset -1050
    parallel:
        linear 0.9 xoffset 1350
    parallel:
        linear 0.9 rotate 360
    parallel:
        easeout 0.18 xzoom 1.0 yzoom 1.0

## Eiki's sermon. Apply to the camera so the whole court pushes in:
##     camera at eiki_lecture
## and reset afterwards with a plain `camera`.
transform eiki_lecture:
    subpixel True
    shader "fumo.vignette"
    u_vignette 0.0
    xanchor 0.5 xpos 0.5
    yanchor 0.34 ypos 0.34
    zoom 1.0
    easein 2.8 zoom 1.25 u_vignette 0.62


################################################################################
## Effects
################################################################################

## Full-screen flashes.
define flash = Fade(0.06, 0.0, 0.45, color="#FFFFFF")
define red_flash = Fade(0.05, 0.0, 0.35, color="#C41E3A")

## Ace Attorney style whip pans between the bench and the stand. Dict
## transitions only touch the master layer, so the HUD and text box hold still.
define whip_left = { "master" : PushMove(0.26, "pushleft") }
define whip_right = { "master" : PushMove(0.26, "pushright") }

## Gavel comes down hard. Pair with `with vpunch`.
transform gavel_slam:
    subpixel True
    xpos 1500 xanchor 0.5 ypos 560 yanchor 1.0
    alpha 0.0 rotate -34 yoffset -120
    easein 0.12 alpha 1.0
    easein 0.09 rotate 6 yoffset 8
    easeout 0.08 rotate 0 yoffset 0
    pause 0.9
    linear 0.25 alpha 0.0

## The verdict stamp drops onto the screen.
transform stamp_slam:
    subpixel True
    align (0.5, 0.42)
    alpha 0.0 zoom 3.2 rotate -16
    easein 0.16 alpha 1.0 zoom 1.16 rotate -8
    easeout 0.10 zoom 1.25

## Shout bubble (OBJECTION! / HOLD IT!).
transform shout_pop:
    subpixel True
    align (0.5, 0.45)
    alpha 0.0 zoom 0.35 rotate -8
    easeout 0.11 alpha 1.0 zoom 1.08 rotate -3
    easein 0.07 zoom 1.0
    block:
        linear 0.03 xoffset -4
        linear 0.03 xoffset 4
        repeat 4
    xoffset 0

transform shout_lines:
    align (0.5, 0.5)
    alpha 0.0
    linear 0.08 alpha 1.0
    block:
        linear 0.06 rotate 0.6
        linear 0.06 rotate -0.6
        repeat

## Text box click-to-continue marker.
transform ctc_bob:
    xpos 1702 ypos 896 anchor (0.5, 1.0)
    block:
        ease 0.45 yoffset -7
        ease 0.45 yoffset 0
        repeat

image ctc_marker = At("gui/ctc.svg", ctc_bob)


################################################################################
## UI animation
################################################################################

## HUD panels drop in from above.
transform hud_drop(delay=0.0):
    yoffset -140 alpha 0.0
    pause delay
    easeout 0.35 yoffset 0 alpha 1.0

## A spent magatama cracks, shakes and falls away.
transform magatama_break:
    subpixel True
    anchor (0.5, 0.5) pos (0.5, 0.5)
    block:
        linear 0.035 xoffset -5 rotate -10
        linear 0.035 xoffset 5 rotate 10
        repeat 5
    xoffset 0
    parallel:
        easein 0.45 yoffset 70
    parallel:
        linear 0.45 rotate 140
    parallel:
        linear 0.45 alpha 0.0

## Cross-examination / testimony banner sweeps in.
transform banner_sweep:
    xoffset -1300 alpha 0.0
    easeout 0.28 xoffset 0 alpha 1.0

## Testimony statements slide up when they change (used with showif).
transform statement_in:
    on appear, show:
        yoffset 14 alpha 0.0
        easeout 0.2 yoffset 0 alpha 1.0
    on hide:
        alpha 0.0

## Fallacy cards rise one after another.
transform card_rise(delay=0.0):
    yoffset 90 alpha 0.0
    pause delay
    easeout 0.28 yoffset 0 alpha 1.0

## Plaque buttons: lift on hover.
transform plaque_lift:
    on idle:
        easein 0.10 yoffset 0
    on hover:
        easeout 0.10 yoffset -6

## Generic quick fade for modal screens.
transform modal_fade:
    on show:
        alpha 0.0
        linear 0.18 alpha 1.0
    on hide:
        linear 0.14 alpha 0.0

## Title-screen fumos idle bob, offset so they don't move in sync.
transform title_bob(delay=0.0):
    subpixel True
    pause delay
    block:
        easein 0.9 yoffset -10
        easeout 0.9 yoffset 0
        repeat
