################################################################################
## docket.rpy - the list of cases, progress, and the Docket screen.
##
## Cases are played in order. Clearing one unlocks the next, and the title
## screen's right-hand fumo is always the witness waiting on the next case.
## Begin Trial opens the Docket: choose a difficulty, then the next case or
## any closed one to replay. Sealed cases show only a silhouette, and closed
## ones their best rank.
################################################################################

init -1 python:

    class Case(object):
        """One trial: where it starts, who testifies, what it teaches."""

        def __init__(self, key, number, title, tagline, witness, fallacy, testimony, record):
            self.key = key              # also the label the case starts at
            self.number = number
            self.title = title
            self.tagline = tagline
            self.witness = witness      # image tag prefix: <witness>_fumo
            self.fallacy = fallacy      # key of the fallacy it teaches
            self.testimony = testimony  # name of its Testimony
            self.record = record        # evidence keys in the Court Record at the start

        @property
        def label(self):
            return self.key

        @property
        def fumo(self):
            return self.witness + "_fumo"

        @property
        def fallacy_card(self):
            return getattr(store, "fallacy_" + self.fallacy)


    def case_state(case):
        """'closed', 'next' (playable, not yet cleared) or 'sealed'."""
        if case.key in persistent.cases_cleared:
            return "closed"
        if case is next_case():
            return "next"
        return "sealed"

    def next_case():
        """The first case not yet cleared, or None once all are."""
        for case in CASES:
            if case.key not in persistent.cases_cleared:
                return case
        return None

    def case_after(key):
        keys = [ c.key for c in CASES ]
        i = keys.index(key) + 1
        return CASES[i] if i < len(CASES) else None

    def title_witness():
        """
        The fumo on the right of the title screen: whoever testifies next.
        Once every case is closed, the pudding thief from Case 05 takes the
        spot.
        """
        case = next_case()
        return case.fumo if case else "cirno_fumo"

    def BeginTrial():
        """Begin Trial opens the Docket: pick a difficulty, then a case."""
        return ShowMenu("docket")


define CASES = [
    Case("case1", _("CASE 01"), _("Cirno's Frosty Fallacy"),
         _("The Ministry of Right and Wrong v. One Ice Fairy"), "cirno", "false_cause",
         "testimony_cirno", [ "frog_census", "weather_log", "cirno_ice" ]),
    Case("case2", _("CASE 02"), _("The Long-Term Loan"),
         _("The Scarlet Devil Library v. One Ordinary Magician"), "marisa", "tu_quoque",
         "testimony_marisa", [ "library_ledger", "donation_box", "reading_glasses" ]),
    Case("case3", _("CASE 03"), _("The Vanished Pudding"),
         _("The Scarlet Devil Mansion v. One Sleeping Gatekeeper"), "sakuya", "false_dilemma",
         "testimony_sakuya", [ "empty_plate", "pudding_recipe" ]),
    Case("case4", _("CASE 04"), _("The Lunar Prescription"),
         _("The Human Village v. One Moon Rabbit"), "reisen", "appeal_to_authority",
         "testimony_reisen", [ "tonic_bottle", "eirin_diploma", "lab_notebook" ]),
    Case("case5", _("CASE 05"), _("The Unappealable Verdict"),
         _("The Scarlet Devil Mansion v. The Verdict in Case 03"), "eiki", "circular_reasoning",
         "testimony_eiki", [ "case3_verdict", "staff_roster", "frozen_pudding" ]),
    ]

default persistent.cases_cleared = set()


## Called at the end of every case. Records the win, shows CASE CLOSED and
## either moves straight on to the next case or ends the game (back to title).
label close_case(key, fallacy):
    $ persistent.cases_cleared.add(key)
    $ persistent.fallacies_learned.add(fallacy.key)
    $ record_rank(key, case_rank())
    $ close_next = case_after(key)

    hide screen court_hud
    with Dissolve(0.3)
    call screen case_closed(fallacy, close_next)

    if _return == "next":
        $ renpy.pop_call()
        jump expression close_next.label
    return


## Opening shared by every case: stops the title theme, refills spirit and
## shows the case card.
label open_case(key):
    $ bgm_stop(1.0)
    $ difficulty = persistent.difficulty
    $ spirit_reset()
    $ case_penalties = 0
    $ case_mistrial = False
    $ open_this = [ c for c in CASES if c.key == key ][0]
    $ court_record = list(open_this.record)
    $ case_number = open_this.number
    $ case_title = open_this.title

    scene black
    show screen case_card(open_this.number, open_this.title, open_this.tagline)
    with Dissolve(0.6)
    pause 2.4

    call shot_eiki(None)
    hide screen case_card
    show screen court_hud
    with Dissolve(0.6)
    return


################################################################################
## The Docket
################################################################################

screen docket():
    tag menu

    use game_menu(_("Docket"), scroll="viewport"):
        vbox:
            spacing 16

            ## Difficulty, remembered between sessions.
            hbox:
                spacing 14
                text _("DIFFICULTY") style "docket_number" yalign 0.5
                null width 6
                for d in DIFFICULTY_ORDER:
                    textbutton DIFFICULTY[d]["name"]:
                        style "docket_diff"
                        action SetField(persistent, "difficulty", d)
            text DIFFICULTY[persistent.difficulty]["blurb"] style "docket_tagline"
            null height 4

            for case in CASES:
                $ state = case_state(case)

                button:
                    style "docket_row"
                    sensitive state != "sealed"
                    action Start(case.label)

                    hbox:
                        spacing 30

                        fixed:
                            xysize (150, 150)
                            if state == "sealed":
                                add Transform(case.fumo, zoom=0.3, matrixcolor=BrightnessMatrix(-1.0), alpha=0.75):
                                    xalign 0.5 yalign 1.0
                            else:
                                add Transform(case.fumo, zoom=0.3):
                                    xalign 0.5 yalign 1.0

                        vbox:
                            yalign 0.5
                            xsize 720
                            spacing 4
                            text case.number style "docket_number"
                            if state == "sealed":
                                text _("Sealed until the case before it is closed.") style "docket_title_sealed"
                            else:
                                text case.title style "docket_title"
                                text case.tagline style "docket_tagline"

                        frame:
                            style "docket_mark"
                            if state == "closed":
                                $ best = best_rank(case.key)
                                vbox:
                                    xalign 0.5
                                    text "閉廷" style "docket_mark_jp"
                                    text case.fallacy_card.name style "docket_mark_text"
                                    if best:
                                        $ best_letter, best_diff = best[0], DIFFICULTY[best[1]]["name"]
                                        text _("Rank [best_letter] · [best_diff!t]") style "docket_mark_text" color VERMILION
                            elif state == "next":
                                vbox:
                                    xalign 0.5
                                    text "開廷" style "docket_mark_jp" color VERMILION
                                    text _("NEXT") style "docket_mark_text" color VERMILION
                            else:
                                text "封" style "docket_mark_jp" color GOLD_LO

style docket_diff is default:
    xminimum 150
    padding (18, 8, 18, 10)
    background CourtPanel(fill=PARCHMENT_SHADE, edge=GOLD_LO, edge_w=2, shadow=2)
    hover_background CourtPanel(fill=PARCHMENT, edge=GOLD, edge_w=2, shadow=2)
    selected_background CourtPanel(fill=CRIMSON, edge=GOLD, edge_w=2, shadow=2)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM

style docket_diff_text is default:
    font FONT_HEAD
    size 24
    color INK
    selected_color GOLD_HI
    xalign 0.5

style docket_row is default:
    xfill True
    ysize 172
    padding (26, 10, 30, 10)
    background CourtPanel(fill=PARCHMENT_SHADE, edge=GOLD_LO, edge_w=2, shadow=3)
    hover_background CourtPanel(fill=PARCHMENT, edge=GOLD, edge_w=3, inner=VERMILION, inner_w=2, shadow=3)
    insensitive_background CourtPanel(fill="#DCCFAE", edge=GOLD_LO, edge_w=2, shadow=0)
    hover_sound SFX_HOVER
    activate_sound SFX_CONFIRM

style docket_number is default:
    font FONT_HEAD
    size 22
    color CRIMSON
    kerning 4

style docket_title is default:
    font FONT_HEAD
    size 40
    color INK

style docket_title_sealed is default:
    size 28
    color "#7D6B4E"

style docket_tagline is default:
    size 24
    color "#6B5536"

style docket_mark is default:
    xsize 230
    yalign 0.5
    background None

style docket_mark_jp is default:
    font FONT_HEAD
    size 46
    color CRIMSON
    kerning 6
    xalign 0.5

style docket_mark_text is default:
    font FONT_HEAD
    size 22
    color CRIMSON
    kerning 2
    xalign 0.5
    text_align 0.5
