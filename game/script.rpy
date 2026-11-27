################################################################################
## script.rpy - Case 01: Cirno's Frosty Fallacy.
################################################################################


################################################################################
## Sprites
################################################################################

## Each fumo is one static sprite in a fixed 480x500 slot, feet at the bottom.
## eiki_fumo.png / cirno_fumo.png are made from the photos in art_src/ by
## tools/fumo_sprite.py (the "Make fumo sprites" workflow runs it). A PNG or
## WebP wins over the SVG placeholder of the same name and is scaled to fit
## the slot, so staging and animations keep working with any image size.

init -1 python:

    def fumo_sprite(name):
        for ext in (".png", ".webp", ".svg"):
            filename = "images/" + name + ext
            if renpy.loadable(filename):
                break

        return Fixed(
            Transform(filename, fit="contain", xysize=(480, 500), xalign=0.5, yalign=1.0),
            xysize=(480, 500),
            )

    # Every images/<name>_fumo.* becomes the image <name>_fumo, in its slot.
    # New characters from art_src/ work with `show reimu_fumo at on_stand`.
    def register_fumo_sprites():
        import os
        names = set()
        for fn in renpy.list_files():
            base, ext = os.path.splitext(os.path.basename(fn))
            if fn.startswith("images/") and base.endswith("_fumo") and ext.lower() in (".png", ".webp", ".svg"):
                names.add(base.lower())
        for name in sorted(names):
            renpy.image(name, fumo_sprite(name))

    register_fumo_sprites()


################################################################################
## Characters
################################################################################

init python:

    class FumoHop(object):
        """
        Character callback: the speaker's fumo hops at the start of each line,
        unless it is mid-reaction (shocked or being yeeted).
        """

        def __init__(self, tag):
            self.tag = tag

        def __call__(self, event, interact=True, **kwargs):
            if event != "begin" or not interact:
                return
            if not renpy.showing(self.tag):
                return
            for t in renpy.get_at_list(self.tag) or [ ]:
                if t is fumo_shock or t is fumo_yeet:
                    return
            renpy.show(self.tag, at_list=[ fumo_talk ])

## Every speaker shares the bobbing click-to-continue magatama.
define adv = Character(kind=adv, ctc="ctc_marker", ctc_position="fixed")
define narrator = Character(None, kind=adv)

define eiki = Character("Shiki Eiki",
    image="eiki_fumo",
    callback=FumoHop("eiki_fumo"))

define cirno = Character("Cirno",
    image="cirno_fumo",
    callback=FumoHop("cirno_fumo"),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

## Testimony is written in red ink.
define cirno_t = Character(kind=cirno, what_color="#7A1C2A", what_size=40)

define komachi = Character("Komachi",
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

## The player.
define you = Character("Junior Judge",
    namebox_background=CourtPanel(fill=GOLD, edge=GOLD_HI, edge_w=3, rule=CRIMSON, rule_inset=7, rule_w=1, shadow=4),
    who_color=CRIMSON_DEEP,
    who_outlines=[ ])


################################################################################
## Shots
################################################################################

## Camera set-ups. Call with the transition to use for the cut.

label shot_eiki(trans=whip_right):
    scene bg_courtroom
    show judge_bench at stand_pos
    show fumo_shadow at shadow_pos
    show eiki_fumo at on_stand
    with trans
    return

label shot_cirno(trans=whip_left):
    scene bg_courtroom
    show witness_stand at stand_pos
    show fumo_shadow at shadow_pos
    show cirno_fumo at on_stand
    with trans
    return


################################################################################
## Fallacies and testimony
################################################################################

define fallacy_false_cause = Fallacy(
    "false_cause",
    _("False Cause"),
    _("(Correlation ≠ Causation)"),
    _("Assuming that because B happened after A, A must have caused B."),
    "gui/fallacy_false_cause.svg")

define fallacy_ad_hominem = Fallacy(
    "ad_hominem",
    _("Ad Hominem"),
    _("(Attack the Speaker)"),
    _("Rejecting a claim by attacking the person who made it."),
    "gui/fallacy_ad_hominem.svg")

define fallacy_slippery_slope = Fallacy(
    "slippery_slope",
    _("Slippery Slope"),
    _("(Chain of Doom)"),
    _("Insisting one small step must snowball into disaster, with no proof."),
    "gui/fallacy_slippery_slope.svg")

define testimony_cirno = Testimony(
    title=_("The Frog Incident"),
    witness="cirno",
    judge="eiki",
    witness_shot="shot_cirno",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("I froze twenty frogs by Misty Lake this morning!"),
            "press_cirno_1",
            _("She froze twenty frogs. We have sworn statements from the frogs. That part is simply true.")),
        Statement(
            _("Every single one of them thawed out by noon and hopped away!"),
            "press_cirno_2",
            _("Frogs thawing in the noon sun is a fact, not a fallacy. Object to reasoning, not weather.")),
        Statement(
            _("Therefore, freezing frogs makes them immortal! I'm basically a lifesaver!"),
            "press_cirno_3",
            None),
        ],
    cards=[ fallacy_ad_hominem, fallacy_false_cause, fallacy_slippery_slope ],
    flaw=2,
    answer="false_cause",
    scolds={
        "ad_hominem" : _("Ad Hominem means attacking the speaker. Nobody insulted anyone. Except, arguably, the frogs."),
        "slippery_slope" : _("Slippery Slope predicts a chain of disasters. She predicted one immortal frog. Look again."),
        })


################################################################################
## Press conversations
################################################################################

label press_cirno_1:
    you "Twenty exactly? How did you count them?"
    cirno "On my fingers! I ran out, so I counted my fingers again."
    call shot_eiki
    eiki "...That is correct arithmetic. I am as surprised as you are."
    return

label press_cirno_2:
    you "What was the weather like at noon?"
    cirno "Hot! The sun was showing off all day. Rude, honestly."
    cirno "Stop changing the subject. The subject is me being amazing."
    return

label press_cirno_3:
    you "How exactly does freezing make a frog immortal?"
    cirno "Easy! First, ice. Then, frog is alive. So the ice did the alive part!"
    cirno "That's called science. I'm basically a scientist. A cold one."
    call shot_eiki
    eiki "Her entire argument is balanced on the word \"then.\""
    return


################################################################################
## Case 01
################################################################################

label start:
    jump case1


label case1:

    $ spirit_reset()
    $ case_number = _("CASE 01")
    $ case_title = _("Cirno's Frosty Fallacy")

    scene black
    show screen case_card(_("CASE 01"), _("Cirno's Frosty Fallacy"), _("The Ministry of Right and Wrong v. One Ice Fairy"))
    with Dissolve(0.6)
    pause 2.4

    call shot_eiki(None)
    hide screen case_card
    show screen court_hud
    with Dissolve(0.6)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Order. The Higan Court of Logic is now in session."
    hide gavel
    eiki "Komachi. Bring in the defendant."
    komachi "She's already here, boss. Tried to freeze the bailiff on the way in."
    eiki "You are the bailiff."
    komachi "Yep. Little chilly."
    eiki "Junior Judge, you will cross-examine today. Try not to embarrass the Ministry."

    call shot_cirno
    cirno "I'm Cirno! Strongest fairy in Gensokyo! Do I win now?"

    call shot_eiki
    eiki "The charge: unlicensed refrigeration of twenty frogs at Misty Lake."
    eiki "Defendant. How do you plead?"

    call shot_cirno
    cirno "Super innocent! Also, you're welcome."

    call shot_eiki
    camera at eiki_lecture
    eiki "Listen well, Junior Judge. A liar is easy to catch."
    eiki "Bad logic is slipperier. It hides between true facts and dresses up as common sense."
    eiki "Find the step that doesn't follow. Then object, and name the fallacy."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_cirno
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Frog Incident"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    cirno_t "I froze twenty frogs by Misty Lake this morning!"
    cirno_t "Every single one of them thawed out by noon and hopped away!"
    cirno_t "Therefore, freezing frogs makes them immortal! I'm basically a lifesaver!"

    hide screen court_tag
    call shot_eiki
    eiki "The floor is yours, Junior Judge. Press her for details."
    eiki "When a statement fails, object. You have five magatama of spirit. Spend them wisely."

    jump case1_cross


label case1_cross:

    call shot_cirno
    call cross_examination("testimony_cirno")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. From the top. Slower, for everyone's sake."
        jump case1_cross

    jump case1_breakthrough


label case1_breakthrough:

    $ sfx("breakthrough")
    with flash
    you "Plenty of frogs freeze in winter and thaw in spring. They manage it without you."
    you "The ice didn't save them. The noon sun thawed them. You just happened to be first."

    show cirno_fumo at fumo_shock
    $ sfx("shock")
    with vpunch
    cirno "B-but the ice came first! First means it did it!"

    call shot_eiki
    camera at eiki_lecture
    eiki "Post hoc, ergo propter hoc. \"After this, therefore because of this.\""
    eiki "Two events line up in time, and you crown the first one the cause."
    eiki "The rooster crows, then the sun rises. Nobody thanks the rooster."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Cirno. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: one hundred hours explaining causation to the frogs."

    call shot_cirno
    cirno "Can I freeze them while I explain?"

    call shot_eiki
    eiki "Bailiff."
    komachi "On it, boss."

    window hide
    call shot_cirno
    show cirno_fumo at fumo_yeet
    show fumo_shadow at shadow_gone
    $ sfx("yeet")
    pause 1.15
    hide cirno_fumo

    call shot_eiki
    window auto
    eiki "...I said escort."
    komachi "She's escorted. Very far."
    eiki "Court is adjourned. Adequate work, Junior Judge."

    $ persistent.fallacies_learned.add("false_cause")

    hide screen court_hud
    with Dissolve(0.3)
    call screen case_closed(fallacy_false_cause)

    return
