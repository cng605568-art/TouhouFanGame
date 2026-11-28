################################################################################
## compendium.rpy - the Compendium of fallacies, and practice mode.
##
## Every fallacy you've caught in a trial gets a page: what it is, how to spot
## it, and the case that taught it. Practice (unlocked with two fallacies)
## puts five short statements in front of Eiki; name the fallacy in each.
################################################################################

init offset = 2

init python:

    # How to spot each fallacy, shown in the Compendium and after practice
    # answers. Kept here so the cards in script.rpy stay short.
    FALLACY_TIPS = {
        "false_cause": _("Ask what else could explain it. Coming first is not the same as causing."),
        "ad_hominem": _("Check whether the reply is about the claim, or about the person who made it."),
        "slippery_slope": _("Look for a chain of \"and then\" steps with no evidence for each link."),
        "tu_quoque": _("Someone else doing it doesn't make it right. Judge the act, not the accuser."),
        "false_dilemma": _("When you're offered two choices, ask where the third one went."),
        "appeal_to_authority": _("A name is not a test. Ask what evidence the expert actually has."),
        "circular_reasoning": _("Take the claim out of the reason. If nothing is left, it's a circle."),
        }

    for _k, _tip in FALLACY_TIPS.items():
        if hasattr(store, "fallacy_" + _k):
            getattr(store, "fallacy_" + _k).tip = _tip

    # Practice statements: (fallacy key, statement). Every line commits one
    # fallacy and only one.
    PRACTICE = [
        ("false_cause", _("I wore my lucky socks and passed the exam. The socks did it.")),
        ("false_cause", _("The rooster crowed, then the sun rose. Clearly the rooster raises the sun.")),
        ("false_cause", _("Since the shrine got a new bell, it rains more. Ring it less.")),
        ("ad_hominem", _("Why take magic safety advice from Marisa? She steals books.")),
        ("ad_hominem", _("Your sums are wrong because you're a fairy.")),
        ("ad_hominem", _("Reimu says the bridge is rotten, but she's lazy, so it's fine.")),
        ("slippery_slope", _("Let one youkai shop in the village, and soon they'll run the market.")),
        ("slippery_slope", _("Skip one practice and you'll quit for good, then lose everything.")),
        ("slippery_slope", _("Lend her one book and she'll want the whole library by spring.")),
        ("tu_quoque", _("Why should I stop being late? You were late last week.")),
        ("tu_quoque", _("You can't tell me to tidy up. Your room's a mess too.")),
        ("tu_quoque", _("Don't lecture me about naps. Meiling sleeps on duty every day.")),
        ("false_dilemma", _("Either you love summer, or you hate fun.")),
        ("false_dilemma", _("You agree with me, or you weren't listening.")),
        ("false_dilemma", _("We cancel the festival, or everyone gets soaked. Those are the choices.")),
        ("appeal_to_authority", _("A famous chef says the moon is cheese. Who are you to argue?")),
        ("appeal_to_authority", _("The village elder says frogs can't feel cold. That settles it.")),
        ("appeal_to_authority", _("A tengu reporter wrote it, so it must be true.")),
        ("circular_reasoning", _("This book is true, because the book says it's true.")),
        ("circular_reasoning", _("Cirno is the strongest because nobody is stronger than Cirno.")),
        ("circular_reasoning", _("I'm trustworthy. You can trust me on that.")),
        ]

    PRACTICE_LENGTH = 5

    def learned_fallacies():
        """The fallacy cards caught so far, in the deck's order."""
        return [ fallacy(k) for k in FALLACY_ORDER
                 if k in persistent.fallacies_learned and hasattr(store, "fallacy_" + k) ]

    def practice_unlocked():
        return len(learned_fallacies()) >= 2

    def practice_questions(n=PRACTICE_LENGTH):
        """n statements drawn from the fallacies learned so far, mixed up."""
        keys = [ f.key for f in learned_fallacies() ]
        pool = [ q for q in PRACTICE if q[0] in keys ]
        renpy.random.shuffle(pool)
        return pool[:n]

    def case_teaching(key):
        """The case whose testimony hides this fallacy, or None."""
        for case in CASES:
            if case.fallacy == key:
                return case
        return None

    def case_meeting(key):
        """The first case that offers this fallacy as a card, or None."""
        for case in CASES:
            if any(c.key == key for c in testimony(case.testimony).cards):
                return case
        return None


default persistent.practice_best = 0


################################################################################
## The Compendium screen
################################################################################

screen compendium():
    tag menu

    use game_menu(_("Compendium"), scroll="viewport"):
        vbox:
            spacing 16

            hbox:
                spacing 24
                textbutton _("Practice"):
                    style "docket_diff"
                    sensitive practice_unlocked() and main_menu
                    action Start("practice")
                if not main_menu:
                    text _("Practice starts from the title screen.") style "docket_tagline" yalign 0.5
                elif practice_unlocked():
                    text _("Five statements. Name the fallacy in each. Best: [persistent.practice_best] / 5.") style "docket_tagline" yalign 0.5
                else:
                    text _("Catch two fallacies in court to unlock practice.") style "docket_tagline" yalign 0.5
            null height 2

            for key in FALLACY_ORDER:
                if hasattr(store, "fallacy_" + key):
                    $ card = fallacy(key)
                    $ taught = case_teaching(key)
                    $ met = case_meeting(key)
                    if key in persistent.fallacies_learned:
                        frame:
                            style "compendium_row"
                            hbox:
                                spacing 28
                                add SVG(card.icon, 0.8) yalign 0.5
                                vbox:
                                    xsize 900
                                    spacing 6
                                    hbox:
                                        spacing 16
                                        text card.name style "docket_title"
                                        text card.alias style "docket_tagline" yalign 0.7
                                    text card.blurb style "compendium_blurb" xsize 900
                                    text _("How to spot it: [card.tip!t]") style "compendium_tip" xsize 900
                                    if taught:
                                        text _("Caught in [taught.number!t]: [taught.title!t]") style "docket_number"
                                    elif met:
                                        text _("Met in [met.number!t]: [met.title!t]") style "docket_number"
                    else:
                        frame:
                            style "compendium_row_sealed"
                            hbox:
                                spacing 28
                                text "封" style "docket_mark_jp" color GOLD_LO yalign 0.5
                                vbox:
                                    yalign 0.5
                                    spacing 4
                                    text "? ? ?" style "docket_title"
                                    if met:
                                        text _("Close [met.number!t] to add this page.") style "docket_title_sealed"

style compendium_row is default:
    xfill True
    padding (26, 18, 30, 18)
    background CourtPanel(fill=PARCHMENT, edge=GOLD, edge_w=2, shadow=3)

style compendium_row_sealed is compendium_row:
    ysize 120
    background CourtPanel(fill="#DCCFAE", edge=GOLD_LO, edge_w=2, shadow=0)

style compendium_blurb is default:
    size 26
    color INK

style compendium_tip is default:
    size 24
    color CRIMSON
    italic False


################################################################################
## Practice
################################################################################

## One question: the statement, and every learned card.
screen practice_pick(question, number):
    zorder 60
    modal True

    add Solid("#0A0205D9") at modal_fade

    $ deck = learned_fallacies()
    $ cols = 3 if len(deck) <= 6 else 4
    $ quote = question[1]

    vbox:
        at modal_fade
        xalign 0.5 ypos 40
        spacing 18
        frame:
            style "court_tag"
            xalign 0.5
            hbox:
                spacing 20
                text "練習" style "court_tag_text" color PARCHMENT
                text _("PRACTICE [number] / [PRACTICE_LENGTH]") style "court_tag_text"
        frame:
            style "fallacy_quote"
            xmaximum 1500
            text "“[quote!t]”" style "fallacy_quote_text"

    vpgrid:
        cols cols
        xalign 0.5 ypos 285
        spacing 22
        for n, card in enumerate(deck):
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
                    add SVG(card.icon, 0.5) xalign 0.5
                    text card.blurb style "fallacy_blurb" size 21 xsize 344 line_spacing 2

    textbutton _("Stop practice"):
        style "menu_plaque"
        xalign 0.5 ypos 1000
        activate_sound SFX_CANCEL
        action Return("withdraw")
        at modal_fade

    key "game_menu" action [ Function(sfx, "ui_cancel"), Return("withdraw") ]


label practice:
    $ practice_qs = practice_questions()
    $ practice_score = 0
    $ practice_n = 0

    call shot_eiki(Dissolve(0.5))
    eiki "Practice, Junior Judge. No defendants, no spirit to lose."
    eiki "I read a statement. You name the fallacy. Five times."

    while practice_n < len(practice_qs):
        $ practice_q = practice_qs[practice_n]
        $ practice_card = fallacy(practice_q[0])
        call screen practice_pick(practice_q, practice_n + 1)

        if _return in (None, True, "withdraw"):
            jump practice_done

        if _return == practice_card.key:
            $ practice_score += 1
            $ sfx("breakthrough")
            $ react("eiki", "smug")
            eiki "Correct. [practice_card.name!t]."
        else:
            $ sfx("penalty")
            $ react("eiki", "angry")
            $ practice_wrong = fallacy(_return)
            eiki "Not [practice_wrong.name!t]. That was [practice_card.name!t]."
        eiki "[practice_card.tip!t]"
        $ practice_n += 1

label practice_done:
    if practice_n == len(practice_qs):
        $ persistent.practice_best = max(persistent.practice_best, practice_score)
        if practice_score == len(practice_qs):
            eiki "[practice_score] of [practice_n]. Flawless. Do not let it go to your head."
        elif practice_score >= 3:
            eiki "[practice_score] of [practice_n]. Acceptable. The court will take it."
        else:
            eiki "[practice_score] of [practice_n]. Read the Compendium. Then try again."
    else:
        eiki "Practice adjourned."
    return


## Saves from before the Compendium only knew the fallacy each case taught:
## give them the other cards of every case they've closed too.
init 997 python:  # 999 with this file's init offset of 2
    for _case in CASES:
        if _case.key in persistent.cases_cleared:
            persistent.fallacies_learned.add(_case.fallacy)
            persistent.fallacies_learned.update(c.key for c in testimony(_case.testimony).cards)
