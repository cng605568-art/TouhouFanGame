################################################################################
## screens.rpy - courtroom UI. The engine that drives it is in court.rpy.
##
##   3. Courtroom screens: HUD, banners, cross-exam, fallacy and evidence
##      cards, the Court Record, verdicts
##   4. Standard screens restyled: say, choice, quick menu, menus, save/load...
################################################################################

init offset = -1

init python:
    config.character_id_prefixes.append("namebox")


################################################################################
## 3. Courtroom screens
################################################################################

## Top HUD: case banner (left) and spirit gauge (right).
screen court_hud():
    zorder 40

    frame at hud_drop(0.0):
        style "hud_case"
        vbox:
            spacing 2
            text case_number style "hud_case_number"
            text case_title style "hud_case_title"

    frame at hud_drop(0.08):
        style "hud_spirit"
        hbox:
            spacing 10
            vbox:
                yalign 0.5
                spacing 0
                text _("SPIRIT") style "hud_spirit_label"
                text "霊力" style "hud_spirit_jp"
            null width 6
            for i in range(spirit_cap):
                fixed:
                    xysize (48, 60)
                    if i < spirit:
                        add "gui/magatama_full.svg"
                    else:
                        add "gui/magatama_empty.svg"
                        if i == spirit_broken:
                            add "gui/magatama_full.svg" at magatama_break

style hud_case is default:
    xpos 40 ypos 24
    background LacquerPanel(corners=False)
    padding (32, 14, 40, 16)

style hud_case_number is default:
    font FONT_HEAD
    size 22
    color GOLD
    kerning 4

style hud_case_title is default:
    font FONT_HEAD
    size 32
    color PARCHMENT

style hud_spirit is default:
    xanchor 1.0 xpos 1880 ypos 24
    background IndigoPanel(rule=GOLD_LO, rule_inset=7, rule_w=1)
    padding (28, 12, 28, 12)

style hud_spirit_label is default:
    font FONT_HEAD
    size 24
    color GOLD
    kerning 3

style hud_spirit_jp is default:
    size 20
    color PARCHMENT
    xalign 0.5


## Small ribbon at the top centre ("TESTIMONY").
screen court_tag(caption):
    zorder 41
    frame at banner_sweep:
        style "court_tag"
        text caption style "court_tag_text"

style court_tag is default:
    xalign 0.5 ypos 30
    background CourtPanel(fill=CRIMSON_DEEP, edge=GOLD, edge_w=3, rule=GOLD_LO, rule_inset=7, rule_w=1, shadow=5)
    padding (40, 12, 40, 12)

style court_tag_text is default:
    font FONT_HEAD
    size 28
    color GOLD_HI
    kerning 5


## Music title card, bottom right above the dialogue box, the way a Touhou
## stage names its BGM. Shown by bgm() in audio.rpy.
screen bgm_title(theme, delay=0.0):
    zorder 45
    frame at bgm_card(delay):
        style "bgm_card"
        hbox:
            spacing 18
            text u"♪" style "bgm_note"
            vbox:
                spacing 4
                hbox:
                    spacing 16
                    text theme.title style "bgm_name"
                    text theme.original style "bgm_original" yalign 0.5
                text theme.credit style "bgm_credit"
    timer (delay + 5.5) action Hide("bgm_title")

style bgm_card is default:
    xanchor 1.0 xpos (BOX_X + BOX_W - 40)
    yanchor 1.0 ypos (BOX_Y - 22)
    background IndigoPanel(rule=GOLD_LO, rule_inset=7, rule_w=1, shadow=4)
    padding (26, 12, 32, 14)

style bgm_note is default:
    font FONT_BODY
    size 44
    color GOLD
    yalign 0.5

style bgm_name is default:
    font FONT_HEAD
    size 28
    color PARCHMENT

style bgm_original is default:
    font FONT_BODY
    size 22
    color GOLD_HI

style bgm_credit is default:
    font FONT_BODY
    size 19
    color GOLD
    kerning 1


## Full-width title ribbon: "WITNESS TESTIMONY", "CROSS-EXAMINATION".
screen court_title(caption, jp, subtitle):
    zorder 70
    on "show" action Function(sfx, "banner")
    frame at banner_sweep:
        style "court_title"
        vbox:
            xalign 0.5
            spacing 6
            hbox:
                xalign 0.5
                spacing 26
                text jp style "court_title_jp" yalign 0.5
                text caption style "court_title_text" yalign 0.5
            add "gui/divider.svg" xalign 0.5
            text subtitle style "court_title_sub"

style court_title is default:
    xfill True
    yalign 0.42
    background CourtPanel(fill="#2B070DEE", edge=GOLD, edge_w=4, inner=CRIMSON, inner_w=3, rule=GOLD_LO, rule_inset=14, rule_w=1, line=None)
    padding (0, 34, 0, 34)

style court_title_text is default:
    font FONT_HEAD
    size 72
    color GOLD_HI
    kerning 6
    outlines [ (absolute(3), CRIMSON_DEEP, absolute(0), absolute(3)) ]

style court_title_jp is default:
    font FONT_HEAD
    size 56
    color PARCHMENT

style court_title_sub is default:
    font FONT_HEAD
    size 34
    color PARCHMENT
    xalign 0.5


## The cross-examination screen. Returns ("press", index) or ("object", index).
## Arrow buttons and keys change the statement in place.
screen cross_exam(tm_name):
    zorder 30
    modal True

    $ tm = testimony(tm_name)
    $ count = len(xexam_vis)
    $ stmt_no = xexam_index + 1

    ## Ribbon.
    frame at banner_sweep:
        style "court_tag"
        text _("CROSS-EXAMINATION") style "court_tag_text"

    ## Court Record, under the spirit gauge.
    textbutton _("COURT RECORD"):
        style "record_button"
        action Show("court_record")
        at hud_drop(0.12)

    ## Parchment box with the current statement.
    frame:
        style "say_window"

        window:
            style "namebox"
            background LacquerPanel(rule_inset=7, rule_w=1, shadow=4)
            text tm.witness_character.name style "say_label"

        text _("STATEMENT [stmt_no] / [count]"):
            style "xexam_counter"

        for n, i in enumerate(xexam_vis):
            showif n == xexam_index:
                text tm.statements[i].text style "testimony_text" at statement_in

    ## Statement arrows.
    imagebutton:
        idle "gui/nav_prev_idle.svg"
        hover "gui/nav_prev_hover.svg"
        xpos BOX_X - 96 ypos BOX_Y + (BOX_H - 76) // 2
        hover_sound SFX_HOVER
        activate_sound SFX_NAV
        action SetVariable("xexam_index", (xexam_index - 1) % count)
        alt _("Previous statement")

    imagebutton:
        idle "gui/nav_next_idle.svg"
        hover "gui/nav_next_hover.svg"
        xpos BOX_X + BOX_W + 20 ypos BOX_Y + (BOX_H - 76) // 2
        hover_sound SFX_HOVER
        activate_sound SFX_NAV
        action SetVariable("xexam_index", (xexam_index + 1) % count)
        alt _("Next statement")

    ## Plaques.
    use cross_exam_plaques

    key "K_LEFT" action [ SetVariable("xexam_index", (xexam_index - 1) % count), Function(sfx, "nav") ]
    key "K_RIGHT" action [ SetVariable("xexam_index", (xexam_index + 1) % count), Function(sfx, "nav") ]
    key "K_p" action [ Function(sfx, "ui_confirm"), Return(("press", xexam_index)) ]
    key "K_o" action [ Function(sfx, "ui_confirm"), Return(("object", xexam_index)) ]
    key "K_r" action [ Function(sfx, "ui_confirm"), Show("court_record") ]

style record_button is default:
    xanchor 1.0 xpos 1880 ypos 130
    background IndigoPanel(rule=GOLD_LO, rule_inset=6, rule_w=1, shadow=4)
    hover_background IndigoPanel(edge=GOLD_HI, rule=GOLD, rule_inset=6, rule_w=1, shadow=4)
    padding (26, 10, 26, 12)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM

style record_button_text is default:
    font FONT_HEAD
    size 22
    color GOLD
    hover_color GOLD_HI
    kerning 4

screen cross_exam_plaques():
    fixed:
        xysize (1920, 1080)

        button:
            style "plaque_button"
            xcenter 960 - 262
            idle_background "gui/plaque_press_idle.svg"
            hover_background "gui/plaque_press_hover.svg"
            action Return(("press", xexam_index))
            at card_rise(0.10), plaque_lift
            vbox:
                align (0.5, 0.5)
                spacing -2
                text _("PRESS") style "plaque_press_text"
                text "待った" style "plaque_press_sub"

        button:
            style "plaque_button"
            xcenter 960 + 262
            idle_background "gui/plaque_object_idle.svg"
            hover_background "gui/plaque_object_hover.svg"
            action Return(("object", xexam_index))
            at card_rise(0.16), plaque_lift
            vbox:
                align (0.5, 0.5)
                spacing -2
                text _("OBJECT!") style "plaque_object_text"
                text "異議あり" style "plaque_object_sub"

style plaque_button is default:
    xysize (460, 130)
    ypos PLAQUE_Y - 6
    padding (0, 0)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM

style plaque_press_text is default:
    font FONT_HEAD
    size 44
    color INDIGO
    kerning 6
    xalign 0.5

style plaque_press_sub is default:
    size 20
    color "#5C3A1C"
    kerning 8
    xalign 0.5

style plaque_object_text is plaque_press_text:
    color GOLD_HI
    outlines [ (absolute(2), CRIMSON_DEEP, absolute(0), absolute(2)) ]

style plaque_object_sub is plaque_press_sub:
    color PARCHMENT

style xexam_counter is default:
    font FONT_HEAD
    size 22
    color CRIMSON
    kerning 3
    xanchor 1.0 xpos BOX_W - 48
    ypos 26

style testimony_text is default:
    xpos BOX_PAD_X ypos BOX_PAD_TOP + 8
    xsize BOX_W - 2 * BOX_PAD_X
    size 40
    line_spacing 10
    color "#7A1C2A"


## Objection: pick the fallacy. Returns a Fallacy key, None to withdraw, or
## "timeout" when the clock runs out (Hard and Lunatic).
screen fallacy_pick(tm_name, index):
    zorder 60
    modal True

    $ tm = testimony(tm_name)
    $ cards = deck_for(tm)
    $ stmt_no = xexam_index + 1
    $ quote = tm.statements[index].text

    add Solid("#0A0205D9") at modal_fade

    vbox:
        at modal_fade
        xalign 0.5 ypos 54
        spacing 22

        frame:
            style "court_tag"
            xalign 0.5 ypos 0
            hbox:
                spacing 20
                text "誤謬" style "court_tag_text" color PARCHMENT
                text _("NAME THE FALLACY") style "court_tag_text"

        frame:
            style "fallacy_quote"
            text _("Statement [stmt_no]: “[quote!t]”") style "fallacy_quote_text"

    if len(cards) <= 3:
        hbox:
            xalign 0.5 ypos 318
            spacing 40
            for n, card in enumerate(cards):
                button:
                    style "fallacy_card"
                    action Return(card.key)
                    at card_rise(0.06 * n), plaque_lift
                    vbox:
                        xfill True
                        spacing 18
                        frame:
                            style "fallacy_card_head"
                            vbox:
                                xalign 0.5
                                text card.name style "fallacy_name"
                                text card.alias style "fallacy_alias"
                        add SVG(card.icon, 1.15) xalign 0.5
                        text card.blurb style "fallacy_blurb"
    else:
        ## A bigger deck: smaller cards in a grid.
        vpgrid:
            cols (3 if len(cards) <= 6 else 4)
            xalign 0.5 ypos 300
            spacing 26
            for n, card in enumerate(cards):
                button:
                    style "fallacy_card_small"
                    action Return(card.key)
                    at card_rise(0.04 * n), plaque_lift
                    vbox:
                        xfill True
                        spacing 8
                        frame:
                            style "fallacy_card_head"
                            padding (12, 10, 12, 12)
                            vbox:
                                xalign 0.5
                                text card.name style "fallacy_name" size 30
                                text card.alias style "fallacy_alias" size 20
                        add SVG(card.icon, 0.62) xalign 0.5
                        text card.blurb style "fallacy_blurb" size 21 xsize 344 line_spacing 2

    use pick_timer

    textbutton _("Withdraw"):
        style "menu_plaque"
        xalign 0.5 ypos 1000
        activate_sound SFX_CANCEL
        action Return(None)
        at modal_fade

    key "game_menu" action [ Function(sfx, "ui_cancel"), Return(None) ]

## On Hard and Lunatic, a shrinking vermilion bar; at zero the pick times out.
screen pick_timer():
    $ seconds = diff()["timer"]
    if seconds:
        timer seconds action Return("timeout")
        frame:
            style "pick_timer_frame"
            add Solid(VERMILION) xsize 1200 ysize 10 at timer_shrink(seconds)

style pick_timer_frame is default:
    xalign 0.5 ypos 286
    xsize 1212 ysize 22
    background Solid("#00000066")
    padding (6, 6, 6, 6)

style fallacy_quote is default:
    xalign 0.5
    xmaximum 1500
    background CourtPanel(fill=PARCHMENT, edge=GOLD, edge_w=3, shadow=5)
    padding (36, 16, 36, 18)

style fallacy_quote_text is default:
    size 30
    color "#7A1C2A"
    text_align 0.5
    xalign 0.5

style fallacy_card is default:
    xysize (500, 540)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM
    background ParchmentPanel(corner_size=36)
    hover_background ParchmentPanel(corner_size=36, edge=GOLD_HI, inner=VERMILION)
    padding (30, 30, 30, 30)

style fallacy_card_small is fallacy_card:
    xysize (400, 320)
    padding (22, 22, 22, 18)
    background ParchmentPanel(corner_size=28)
    hover_background ParchmentPanel(corner_size=28, edge=GOLD_HI, inner=VERMILION)

style fallacy_card_head is default:
    xfill True
    background CourtPanel(fill=CRIMSON, edge=GOLD, edge_w=2, shadow=0)
    padding (16, 16, 16, 18)

style fallacy_name is default:
    font FONT_HEAD
    size 40
    color GOLD_HI
    xalign 0.5
    text_align 0.5

style fallacy_alias is default:
    size 24
    color PARCHMENT
    xalign 0.5

style fallacy_blurb is default:
    size 29
    color INK
    text_align 0.5
    xalign 0.5
    xsize 420
    line_spacing 6


## Prove it: pick the evidence that backs the objection. Returns an Evidence
## key, None to withdraw, or "timeout".
screen evidence_pick(tm_name):
    zorder 60
    modal True

    add Solid("#0A0205D9") at modal_fade

    vbox:
        at modal_fade
        xalign 0.5 ypos 54
        spacing 22
        frame:
            style "court_tag"
            xalign 0.5 ypos 0
            hbox:
                spacing 20
                text "証拠" style "court_tag_text" color PARCHMENT
                text _("PRESENT EVIDENCE") style "court_tag_text"
        frame:
            style "fallacy_quote"
            text _("Which item proves your objection?") style "fallacy_quote_text"

    vpgrid:
        cols min(4, max(1, len(court_record)))
        xalign 0.5 ypos 300
        spacing 26
        for n, key in enumerate(court_record):
            $ ev = evidence(key)
            button:
                style "evidence_card"
                action Return(ev.key)
                at card_rise(0.05 * n), plaque_lift
                use evidence_face(ev)

    use pick_timer

    textbutton _("Withdraw"):
        style "menu_plaque"
        xalign 0.5 ypos 1000
        activate_sound SFX_CANCEL
        action Return(None)
        at modal_fade

    key "game_menu" action [ Function(sfx, "ui_cancel"), Return(None) ]

## One evidence card's contents.
screen evidence_face(ev):
    vbox:
        xfill True
        spacing 10
        frame:
            style "evidence_head"
            text ev.name style "evidence_name"
        add SVG(ev.icon, 0.62) xalign 0.5
        text ev.desc style "evidence_desc"

style evidence_card is fallacy_card_small:
    xysize (400, 340)

style evidence_head is default:
    xfill True
    background CourtPanel(fill=INDIGO, edge=GOLD, edge_w=2, shadow=0)
    padding (12, 12, 12, 14)

style evidence_name is default:
    font FONT_HEAD
    size 28
    color GOLD_HI
    xalign 0.5
    text_align 0.5

style evidence_desc is default:
    size 22
    color INK
    text_align 0.5
    xalign 0.5
    xsize 350
    line_spacing 3


## The Court Record: every item collected in this case. Opened from the
## cross-examination; closes back to it.
screen court_record():
    zorder 70
    modal True

    add Solid("#0A0205E6") at modal_fade

    frame:
        style "court_tag"
        xalign 0.5 ypos 54
        at modal_fade
        hbox:
            spacing 20
            text "法廷記録" style "court_tag_text" color PARCHMENT
            text _("COURT RECORD") style "court_tag_text"

    vpgrid:
        cols min(4, max(1, len(court_record)))
        xalign 0.5 ypos 190
        spacing 26
        for n, key in enumerate(court_record):
            frame:
                style "evidence_card"
                at card_rise(0.05 * n)
                use evidence_face(evidence(key))

    textbutton _("Close"):
        style "menu_plaque"
        xalign 0.5 ypos 1000
        activate_sound SFX_CANCEL
        action Hide("court_record")

    key "game_menu" action [ Function(sfx, "ui_cancel"), Hide("court_record") ]
    key "K_r" action [ Function(sfx, "ui_cancel"), Hide("court_record") ]


## "Added to the Court Record" card, top right, for a few seconds.
screen evidence_added(ev):
    zorder 90
    frame at bgm_card(0.0):
        style "evidence_added_frame"
        hbox:
            spacing 18
            add SVG(ev.icon, 0.42) yalign 0.5
            vbox:
                yalign 0.5
                spacing 2
                text _("ADDED TO THE COURT RECORD") style "evidence_added_label"
                text ev.name style "evidence_added_name"
    timer 3.2 action Hide("evidence_added")

style evidence_added_frame is default:
    xanchor 1.0 xpos 1880 ypos 200
    background IndigoPanel(rule=GOLD_LO, rule_inset=7, rule_w=1, shadow=4)
    padding (20, 12, 30, 14)

style evidence_added_label is default:
    font FONT_HEAD
    size 18
    color GOLD
    kerning 3

style evidence_added_name is default:
    font FONT_HEAD
    size 30
    color PARCHMENT


## OBJECTION! / HOLD IT! bubble over speed lines.
screen court_shout(kind):
    zorder 80
    on "show" action Function(sfx, "shout_" + ("objection" if kind == "takethat" else kind))

    if kind == "hold":
        $ main = _("HOLD IT!")
        $ jp = "待った！"
    elif kind == "takethat":
        $ main = _("TAKE THAT!")
        $ jp = "くらえ！"
    else:
        $ main = _("OBJECTION!")
        $ jp = "異議あり！"

    add "gui/speedlines.svg" at shout_lines

    fixed at shout_pop:
        xysize (1120, 600)
        add "gui/burst.svg"
        vbox:
            align (0.5, 0.5)
            spacing -6
            text main style "shout_text"
            text jp style "shout_sub"

style shout_text is default:
    font FONT_HEAD
    size 112
    color CRIMSON
    xalign 0.5
    outlines [ (absolute(6), GOLD, absolute(0), absolute(0)), (absolute(10), CRIMSON_DEEP, absolute(0), absolute(5)) ]

style shout_sub is default:
    font FONT_HEAD
    size 44
    color INDIGO
    xalign 0.5
    kerning 10


## Verdict stamp.
screen verdict_stamp(word, jp):
    zorder 85
    on "show" action Function(sfx, "stamp")
    add Solid("#0A0205B3") at modal_fade
    fixed at stamp_slam:
        xysize (600, 320)
        add "gui/stamp_frame.svg"
        vbox:
            align (0.5, 0.5)
            spacing -8
            text jp style "stamp_jp"
            text word style "stamp_word" size (78 if len(word) <= 7 else 58)

style stamp_word is default:
    font FONT_HEAD
    size 78
    color VERMILION
    kerning 12
    xalign 0.5

style stamp_jp is default:
    font FONT_HEAD
    size 64
    color VERMILION
    kerning 24
    xalign 0.5


## Case title card.
screen case_card(number, title, tagline):
    zorder 95
    add "bg_courtroom"
    add Solid("#12030AD9")
    vbox:
        align (0.5, 0.47)
        spacing 16
        add SVG("images/scales.svg", 0.5) xalign 0.5
        text number style "card_number"
        add "gui/divider.svg" xalign 0.5
        text title style "card_title"
        text tagline style "card_tagline"

style card_number is default:
    font FONT_HEAD
    size 34
    color GOLD
    kerning 12
    xalign 0.5

style card_title is default:
    font FONT_HEAD
    size 88
    color PARCHMENT
    xalign 0.5
    outlines [ (absolute(4), CRIMSON_DEEP, absolute(0), absolute(4)) ]

style card_tagline is default:
    size 32
    color GOLD_HI
    xalign 0.5


## Case closed: summary of the fallacy learned. Returns "next" to go straight
## on to `next_case` (a Case, or None after the last one) or "title".
screen case_closed(fallacy, next_case=None):
    zorder 95
    modal True
    on "show" action Function(sfx, "case_closed")

    add "bg_courtroom"
    add Solid("#12030AE0")

    vbox:
        align (0.5, 0.5)
        spacing 26

        hbox:
            xalign 0.5
            spacing 28
            text "閉廷" style "closed_jp" yalign 0.5
            text _("CASE CLOSED") style "closed_title" yalign 0.5

        add "gui/divider.svg" xalign 0.5

        frame:
            style "closed_panel"
            vbox:
                spacing 18
                text _("FALLACY RECORDED") style "closed_label"
                hbox:
                    spacing 30
                    add SVG(fallacy.icon, 0.9) yalign 0.5
                    vbox:
                        yalign 0.5
                        spacing 6
                        text fallacy.name style "closed_name"
                        text fallacy.alias style "closed_alias"
                text fallacy.blurb style "closed_blurb"
                null height 4
                hbox:
                    spacing 12
                    text _("SPIRIT REMAINING") style "closed_label" yalign 0.5
                    null width 8
                    for i in range(spirit_cap):
                        add ("gui/magatama_full.svg" if i < spirit else "gui/magatama_empty.svg")
                hbox:
                    spacing 18
                    text _("RANK") style "closed_label" yalign 0.5
                    text case_rank() style "closed_rank" yalign 0.5
                    text diff()["name"] style "closed_label" yalign 0.5 color GOLD_LO

        hbox:
            xalign 0.5
            spacing 36
            if next_case is not None:
                textbutton _("Next Case"):
                    style "menu_plaque"
                    action Return("next")
            textbutton _("Return to Title"):
                style "menu_plaque"
                action Return("title")

style closed_rank is default:
    font FONT_HEAD
    size 64
    color VERMILION
    outlines [ (absolute(2), CRIMSON_DEEP, absolute(0), absolute(2)) ]

style closed_title is default:
    font FONT_HEAD
    size 84
    color GOLD_HI
    kerning 8
    outlines [ (absolute(4), CRIMSON_DEEP, absolute(0), absolute(4)) ]

style closed_jp is closed_title:
    color PARCHMENT
    kerning 4

style closed_panel is default:
    xalign 0.5
    xsize 1100
    background ParchmentPanel()
    padding (64, 50, 64, 50)

style closed_label is default:
    font FONT_HEAD
    size 24
    color CRIMSON
    kerning 4

style closed_name is default:
    font FONT_HEAD
    size 54
    color INK

style closed_alias is default:
    size 30
    color "#7A1C2A"

style closed_blurb is default:
    size 32
    color INK
    line_spacing 6


## Game over.
screen mistrial_screen():
    zorder 95
    modal True
    on "show" action Function(sfx, "mistrial")

    add "bg_courtroom"
    add Solid("#0A0205E6")

    vbox:
        align (0.5, 0.46)
        spacing 26

        add SVG("gui/magatama_empty.svg", 2.4) xalign 0.5
        hbox:
            xalign 0.5
            spacing 28
            text "審理無効" style "closed_jp" yalign 0.5
            text _("MISTRIAL") style "closed_title" yalign 0.5
        add "gui/divider.svg" xalign 0.5
        text _("Your spirit is spent. The Yama has requested a smarter plush.") style "mistrial_text"
        null height 10
        hbox:
            xalign 0.5
            spacing 40
            textbutton _("Retry Cross-Examination"):
                style "menu_plaque"
                xsize 560
                action Return("retry")
            textbutton _("Return to Title"):
                style "menu_plaque"
                xsize 560
                action Return("title")

style mistrial_text is default:
    size 34
    color PARCHMENT
    xalign 0.5


################################################################################
## 4. Standard screens
################################################################################

## Say ##########################################################################

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

style say_window is default:
    xpos BOX_X ypos BOX_Y
    xsize BOX_W ysize BOX_H
    background ParchmentPanel()
    padding (0, 0)

style namebox is default:
    xpos 58 ypos -36
    xminimum 280 ysize 68
    padding (36, 0, 36, 0)
    background IndigoPanel(rule=GOLD_LO, rule_inset=7, rule_w=1, shadow=4)

style say_label is default:
    font FONT_HEAD
    size 34
    color PARCHMENT
    align (0.5, 0.5)
    kerning 2
    outlines [ (absolute(2), "#0B1020", absolute(0), absolute(1)) ]

style say_dialogue is default:
    xpos BOX_PAD_X ypos BOX_PAD_TOP
    xsize BOX_W - 2 * BOX_PAD_X
    size 38
    line_spacing 10
    color INK

style say_thought is say_dialogue


## Choice ######################################################################

screen choice(items):
    style_prefix "choice"
    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is default:
    xalign 0.5 yalign 0.4
    spacing 18

style choice_button is menu_plaque:
    xsize 900

style choice_button_text is menu_plaque_text


## Input #######################################################################

screen input(prompt):
    style_prefix "input"
    window:
        style "say_window"
        vbox:
            xpos BOX_PAD_X ypos BOX_PAD_TOP
            spacing 14
            text prompt style "say_dialogue" xpos 0 ypos 0
            input id "input"

style input is default:
    size 38
    color INDIGO


## Quick menu (under the text box during dialogue) #############################

screen quick_menu():
    zorder 100

    if quick_menu and renpy.get_screen("say"):
        hbox:
            style_prefix "quick"
            xalign 0.5 ypos 968
            spacing 34
            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu("history")
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu("save")
            textbutton _("Load") action ShowMenu("load")
            textbutton _("Settings") action ShowMenu("preferences")

init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default:
    padding (10, 6)
    activate_sound SFX_CONFIRM

style quick_button_text is default:
    font FONT_HEAD
    size 24
    color "#B79A5A"
    hover_color GOLD_HI
    selected_color GOLD_HI
    kerning 2


## Buttons used across menus #####################################################

style menu_plaque is default:
    xsize 480 ysize 74
    background CourtPanel(fill=CRIMSON, edge=GOLD, edge_w=3, rule=GOLD_LO, rule_inset=8, rule_w=1, shadow=6)
    hover_background CourtPanel(fill=GOLD, edge=GOLD_HI, edge_w=3, rule=CRIMSON, rule_inset=8, rule_w=1, shadow=6)
    selected_background CourtPanel(fill=INDIGO, edge=GOLD, edge_w=3, rule=GOLD, rule_inset=8, rule_w=1, shadow=6)
    insensitive_background CourtPanel(fill=CRIMSON_DEEP, edge=GOLD_LO, edge_w=3, shadow=6)
    padding (24, 0)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM

style menu_plaque_text is default:
    font FONT_HEAD
    size 32
    color PARCHMENT
    hover_color CRIMSON_DEEP
    selected_color GOLD_HI
    insensitive_color "#7d6a5e"
    align (0.5, 0.5)
    kerning 2


## Main menu ###################################################################

screen main_menu():
    tag menu

    add "bg_courtroom"
    add Solid("#0D02064D")

    ## Flanking fumos, grounded with soft shadows.
    add "fumo_shadow" xcenter 330 ycenter 1034 zoom 0.9
    add "fumo_shadow" xcenter 1590 ycenter 1034 zoom 0.9
    add "eiki_fumo":
        xcenter 330 yanchor 1.0 ypos 1040
        at title_bob(0.0)
    ## Whoever testifies next waits on the right.
    add title_witness():
        xcenter 1590 yanchor 1.0 ypos 1040
        at title_bob(0.45)

    vbox:
        xalign 0.5 ypos 28
        spacing 4

        add SVG("images/scales.svg", 0.32) xalign 0.5
        text _("FUMO COURT") style "title_logo"
        add "gui/divider.svg" xalign 0.5
        text _("Shiki Eiki's Logic Trials") style "title_sub"
        text "是非曲直庁・論理裁判" style "title_jp"

    vbox:
        style_prefix "main"
        xalign 0.5 ypos 566
        spacing 10

        textbutton _("Begin Trial") action BeginTrial()
        textbutton _("Continue") action ShowMenu("load")
        textbutton _("Settings") action ShowMenu("preferences")
        textbutton _("Controls") action ShowMenu("controls")
        textbutton _("About") action ShowMenu("about")
        if renpy.variant("pc"):
            textbutton _("Quit") action Quit(confirm=False)

    text _("A Touhou Project fan work. Not affiliated with Team Shanghai Alice."):
        style "title_footer"
        xpos 36 yanchor 1.0 ypos 1056
    text "v[config.version]":
        style "title_footer"
        xanchor 1.0 xpos 1884 yanchor 1.0 ypos 1056

style title_logo is default:
    font FONT_HEAD
    size 124
    color GOLD_HI
    kerning 10
    xalign 0.5
    outlines [ (absolute(5), CRIMSON_DEEP, absolute(0), absolute(0)), (absolute(5), "#00000099", absolute(0), absolute(7)) ]

style title_sub is default:
    font FONT_HEAD
    size 46
    color PARCHMENT
    xalign 0.5
    outlines [ (absolute(3), CRIMSON_DEEP, absolute(0), absolute(2)) ]

style title_jp is default:
    font FONT_HEAD
    size 28
    color GOLD
    kerning 8
    xalign 0.5

style title_footer is default:
    size 20
    color "#C9B48A"

style main_button is menu_plaque:
    xsize 440 ysize 64

style main_button_text is menu_plaque_text:
    size 30


## Game menu frame ##############################################################

screen game_menu(title, scroll=None, yinitial=0.0):

    add "bg_courtroom"
    add Solid("#0D0206C0")

    ## Navigation column.
    frame:
        style "cm_nav_frame"
        vbox:
            style_prefix "cm_nav"
            spacing 12

            if main_menu:
                textbutton _("Begin Trial") action BeginTrial()
            else:
                textbutton _("History") action ShowMenu("history")
                textbutton _("Save") action ShowMenu("save")

            textbutton _("Load") action ShowMenu("load")
            textbutton _("Settings") action ShowMenu("preferences")
            textbutton _("Controls") action ShowMenu("controls")
            textbutton _("About") action ShowMenu("about")

            if not main_menu:
                textbutton _("Main Menu") action MainMenu()

            if renpy.variant("pc"):
                textbutton _("Quit") action Quit(confirm=not main_menu)

            null height 24
            textbutton _("Return") action Return() activate_sound SFX_CANCEL

    ## Title.
    vbox:
        xpos 500 ypos 40
        spacing 6
        text title style "cm_title"
        add "gui/divider.svg" xpos -6

    ## Content.
    frame:
        style "cm_content"

        if scroll == "viewport":
            viewport:
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                side_yfill True
                vbox:
                    transclude
        elif scroll == "vpgrid":
            vpgrid:
                cols 1
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                side_yfill True
                transclude
        else:
            transclude

    key "game_menu" action Return()

style cm_nav_frame is default:
    xpos 60 ypos 160
    xsize 420
    background LacquerPanel(corners=False)
    padding (30, 34, 30, 34)

style cm_nav_button is menu_plaque:
    xsize 360 ysize 62

style cm_nav_button_text is menu_plaque_text:
    size 28

style cm_title is default:
    font FONT_HEAD
    size 64
    color GOLD_HI
    kerning 4
    outlines [ (absolute(3), CRIMSON_DEEP, absolute(0), absolute(3)) ]

style cm_content is default:
    xpos 500 ypos 160
    xsize 1380 ysize 880
    background ParchmentPanel()
    padding (50, 50, 50, 50)

style cm_text is default:
    size 32
    color INK
    line_spacing 8

style cm_heading is default:
    font FONT_HEAD
    size 32
    color CRIMSON
    kerning 3


## About ########################################################################

screen about():
    tag menu
    use game_menu(_("About"), scroll="viewport"):
        style_prefix "cm"
        vbox:
            spacing 22
            text _("[config.name!t]  ·  Version [config.version!t]") style "cm_heading"
            text gui.about style "cm_text"


## Controls #####################################################################

screen controls():
    tag menu
    use game_menu(_("Controls")):
        style_prefix "ctl"
        vbox:
            spacing 16
            text _("IN COURT") style "cm_heading"
            use control_row(_("Advance"), _("Click, Space or Enter"))
            use control_row(_("Previous / next statement"), _("◆ buttons or Left / Right arrows"))
            use control_row(_("Press the witness"), _("PRESS plaque or P"))
            use control_row(_("Object"), _("OBJECT! plaque or O"))
            use control_row(_("Withdraw an objection"), _("Withdraw or Esc"))
            null height 10
            text _("ANYWHERE") style "cm_heading"
            use control_row(_("Menu"), _("Esc or right-click"))
            use control_row(_("Roll back"), _("Mouse wheel up or Page Up"))
            use control_row(_("Skip"), _("Hold Ctrl"))
            use control_row(_("Hide the text box"), _("H or middle-click"))
            use control_row(_("Fullscreen"), _("F"))

screen control_row(what, how):
    hbox:
        spacing 20
        text what style "ctl_what"
        text how style "ctl_how"

style ctl_what is default:
    font FONT_HEAD
    size 30
    color INK
    xsize 520

style ctl_how is default:
    size 30
    color "#5A4A40"


## Save / load ###################################################################

screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:
            input:
                style "slot_page_name"
                value page_name_value

            grid 3 2:
                style_prefix "slot"
                xalign 0.5 ypos 56
                spacing 30

                for i in range(6):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        spacing 8

                        add FileScreenshot(slot, empty=Fixed(Solid("#00000014"), Text(_("Empty record"), style="slot_empty"), xysize=(config.thumbnail_width, config.thumbnail_height))):
                            xalign 0.5
                        text FileTime(slot, format=_("{#file_time}%b %d, %H:%M"), empty=_("—")) style "slot_time"
                        text FileSaveName(slot) style "slot_name"

                        key "save_delete" action FileDelete(slot)

            hbox:
                style_prefix "page"
                xalign 0.5 yalign 1.0
                spacing 6

                textbutton "‹" action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("A") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("Q") action FilePage("quick")
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)
                textbutton "›" action FilePageNext()

style slot_page_name is default:
    font FONT_HEAD
    size 30
    color CRIMSON
    xalign 0.5

style slot_button is default:
    xsize 400 ysize 300
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM
    background CourtPanel(fill=PARCHMENT_SHADE, edge=GOLD_LO, edge_w=2, shadow=4)
    hover_background CourtPanel(fill="#FFF8E6", edge=GOLD, edge_w=4, inner=CRIMSON, inner_w=2, shadow=4)
    padding (8, 8, 8, 10)

style slot_time is default:
    font FONT_HEAD
    size 24
    color CRIMSON
    xalign 0.5

style slot_name is default:
    size 22
    color INK
    xalign 0.5

style slot_empty is default:
    size 24
    color "#8A7A6A"
    align (0.5, 0.5)

style page_button is default:
    xysize (54, 50)
    activate_sound SFX_CONFIRM
    background CourtPanel(fill=CRIMSON, edge=GOLD, edge_w=2, shadow=3)
    hover_background CourtPanel(fill=GOLD, edge=GOLD_HI, edge_w=2, shadow=3)
    selected_background CourtPanel(fill=INDIGO, edge=GOLD_HI, edge_w=2, shadow=3)

style page_button_text is default:
    font FONT_HEAD
    size 26
    color PARCHMENT
    hover_color CRIMSON_DEEP
    selected_color GOLD_HI
    align (0.5, 0.5)


## Preferences ###################################################################

screen preferences():
    tag menu

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            spacing 44

            hbox:
                spacing 110

                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "pref"
                        text _("DISPLAY") style "cm_heading"
                        use pref_option(_("Window"), Preference("display", "window"))
                        use pref_option(_("Fullscreen"), Preference("display", "fullscreen"))

                vbox:
                    style_prefix "pref"
                    text _("SKIP") style "cm_heading"
                    use pref_option(_("Unseen Text"), Preference("skip", "toggle"))
                    use pref_option(_("After Choices"), Preference("after choices", "toggle"))
                    use pref_option(_("Transitions"), InvertSelected(Preference("transitions", "toggle")))

            hbox:
                spacing 90

                vbox:
                    spacing 18
                    text _("TEXT SPEED") style "cm_heading"
                    bar value Preference("text speed") style "slider"
                    null height 12
                    text _("AUTO-FORWARD TIME") style "cm_heading"
                    bar value Preference("auto-forward time") style "slider"

                vbox:
                    spacing 18
                    text _("MUSIC") style "cm_heading"
                    bar value Preference("music volume") style "slider" xsize 440
                    null height 12
                    text _("SOUND EFFECTS") style "cm_heading"
                    bar value Preference("sound volume") style "slider" xsize 440
                    null height 12
                    vbox:
                        style_prefix "pref"
                        use pref_option(_("Mute All"), Preference("all mute", "toggle"))

## A settings toggle: a diamond that fills in when selected, then the label.
screen pref_option(caption, action):
    button:
        style "pref_button"
        action action
        hbox:
            spacing 16
            text "◆" style "pref_diamond" yalign 0.5
            text caption style "pref_button_text" yalign 0.5

style pref_vbox is default:
    spacing 10

style pref_button is default:
    padding (4, 6, 12, 6)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM

style pref_button_text is default:
    font FONT_HEAD
    size 32
    color INK
    hover_color CRIMSON
    selected_color CRIMSON

style pref_diamond is default:
    font FONT_BODY
    size 28
    color "#00000000"
    outlines [ (absolute(2), GOLD_LO, 0, 0) ]
    hover_color "#D4AF3766"
    selected_color GOLD
    selected_outlines [ (absolute(2), CRIMSON_DEEP, 0, 0) ]


## History #######################################################################

screen history():
    tag menu
    predict False

    use game_menu(_("History"), scroll="vpgrid", yinitial=1.0):
        style_prefix "history"

        for h in _history_list:
            window:
                has vbox
                spacing 4
                if h.who:
                    text h.who style "history_who"
                text h.what:
                    style "history_what"
                    substitute False

        if not _history_list:
            text _("The court record is empty.") style "cm_text"

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }

style history_window is default:
    xfill True
    padding (0, 10, 30, 14)

style history_who is default:
    font FONT_HEAD
    size 26
    color CRIMSON
    kerning 2

style history_what is default:
    size 30
    color INK


## Confirm #######################################################################

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    add Solid("#0A0205CC")

    frame:
        style "confirm_frame"
        at modal_fade
        vbox:
            xalign 0.5
            spacing 40
            text _(message) style "confirm_text"
            hbox:
                xalign 0.5
                spacing 40
                textbutton _("Yes") style "menu_plaque" xsize 300 action yes_action
                textbutton _("No") style "menu_plaque" xsize 300 action no_action

    key "game_menu" action no_action

style confirm_frame is default:
    align (0.5, 0.5)
    xsize 980
    background ParchmentPanel()
    padding (70, 60, 70, 56)

style confirm_text is default:
    size 36
    color INK
    text_align 0.5
    xalign 0.5


## Skip indicator / notify #####################################################

screen skip_indicator():
    zorder 100
    frame:
        style "notify_frame"
        hbox:
            spacing 12
            text _("Skipping") style "notify_text"
            text "◆ ◆ ◆" style "notify_text" color GOLD

screen notify(message):
    zorder 100
    frame at modal_fade:
        style "notify_frame"
        text "[message!tq]" style "notify_text"
    timer 3.0 action Hide("notify")

style notify_frame is default:
    xpos 40 ypos 150
    background LacquerPanel(corners=False, shadow=4)
    padding (26, 12, 30, 14)

style notify_text is default:
    font FONT_HEAD
    size 26
    color PARCHMENT
