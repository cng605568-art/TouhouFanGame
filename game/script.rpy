################################################################################
## script.rpy - cast, camera shots, fallacies, and Case 01.
##
## Cases 02-04 live in case02.rpy, case03.rpy and case04.rpy; the list of
## cases and the Docket are in docket.rpy.
################################################################################


################################################################################
## Sprites
################################################################################

## Each fumo is one static sprite in a fixed 480x500 slot, feet at the bottom.
## The <name>_fumo.png sprites are made from the photos in art_src/ by
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
    # A pose photo, images/<name>_fumo_<pose>.*, becomes "<name>_fumo <pose>"
    # (see react() in reactions.rpy).
    def register_fumo_sprites():
        import os
        names = set()
        for fn in renpy.list_files():
            base, ext = os.path.splitext(os.path.basename(fn))
            if fn.startswith("images/") and "_fumo" in base and ext.lower() in (".png", ".webp", ".svg"):
                names.add(base.lower())
        for name in sorted(names):
            char, _, pose = name.partition("_fumo")
            if not pose:
                renpy.image(name, fumo_sprite(name))
            elif pose.startswith("_") and len(pose) > 1:
                renpy.image((char + "_fumo", pose[1:]), fumo_sprite(name))

    register_fumo_sprites()


################################################################################
## Characters
################################################################################

init python:

    class FumoHop(object):
        """
        Character callback: the speaker's fumo hops at the start of each line,
        unless it is mid-reaction (shocked, broken down, or being yeeted).
        """

        def __init__(self, tag):
            self.tag = tag

        def __call__(self, event, interact=True, **kwargs):
            if event != "begin" or not interact:
                return
            if not renpy.showing(self.tag):
                return
            # Mid-fight poses (fight.rpy) hold until the fight is over.
            if self.tag in store.fumo_freeze:
                return
            # A reaction from react() or a breakdown holds for one line.
            hold, store.fumo_hold = store.fumo_hold, None
            if hold == self.tag:
                return
            for t in renpy.get_at_list(self.tag) or [ ]:
                if t is fumo_shock or t is fumo_yeet or any(t is s for s in FUMO_STAY):
                    return
            renpy.show(self.tag, at_list=[ fumo_talk ])

## Every speaker shares the bobbing click-to-continue magatama.
define adv = Character(kind=adv, ctc="ctc_marker", ctc_position="fixed")
define narrator = Character(None, kind=adv, callback=TextBlip("blip"))

define eiki = Character("Shiki Eiki",
    image="eiki_fumo",
    callback=Callbacks(FumoHop("eiki_fumo"), TextBlip("blip_lo")))

define cirno = Character("Cirno",
    image="cirno_fumo",
    callback=Callbacks(FumoHop("cirno_fumo"), TextBlip("blip_hi")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define marisa = Character("Marisa",
    image="marisa_fumo",
    callback=Callbacks(FumoHop("marisa_fumo"), TextBlip("blip")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define sakuya = Character("Sakuya",
    image="sakuya_fumo",
    callback=Callbacks(FumoHop("sakuya_fumo"), TextBlip("blip_dn")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define reisen = Character("Reisen",
    image="reisen_fumo",
    callback=Callbacks(FumoHop("reisen_fumo"), TextBlip("blip_up")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define meiling = Character("Meiling",
    image="meiling_fumo",
    callback=Callbacks(FumoHop("meiling_fumo"), TextBlip("blip")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define alice = Character("Alice",
    image="alice_fumo",
    callback=Callbacks(FumoHop("alice_fumo"), TextBlip("blip_up")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define reimu = Character("Reimu",
    image="reimu_fumo",
    callback=Callbacks(FumoHop("reimu_fumo"), TextBlip("blip")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define kaguya = Character("Kaguya",
    image="kaguya_fumo",
    callback=Callbacks(FumoHop("kaguya_fumo"), TextBlip("blip_dn")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define mokou = Character("Mokou",
    image="mokou_fumo",
    callback=Callbacks(FumoHop("mokou_fumo"), TextBlip("blip_lo")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

define aya = Character("Aya",
    image="aya_fumo",
    callback=Callbacks(FumoHop("aya_fumo"), TextBlip("blip_hi")),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

## Testimony is written in red ink.
define cirno_t = Character(kind=cirno, what_color="#7A1C2A", what_size=40)
define marisa_t = Character(kind=marisa, what_color="#7A1C2A", what_size=40)
define sakuya_t = Character(kind=sakuya, what_color="#7A1C2A", what_size=40)
define reisen_t = Character(kind=reisen, what_color="#7A1C2A", what_size=40)
define meiling_t = Character(kind=meiling, what_color="#7A1C2A", what_size=40)
define alice_t = Character(kind=alice, what_color="#7A1C2A", what_size=40)
define reimu_t = Character(kind=reimu, what_color="#7A1C2A", what_size=40)
define kaguya_t = Character(kind=kaguya, what_color="#7A1C2A", what_size=40)
define mokou_t = Character(kind=mokou, what_color="#7A1C2A", what_size=40)
define aya_t = Character(kind=aya, what_color="#7A1C2A", what_size=40)

define komachi = Character("Komachi",
    callback=TextBlip("blip_deep"),
    namebox_background=LacquerPanel(rule_inset=7, rule_w=1, shadow=4))

## The player.
define you = Character("Junior Judge",
    callback=TextBlip("blip_dn"),
    namebox_background=CourtPanel(fill=GOLD, edge=GOLD_HI, edge_w=3, rule=CRIMSON, rule_inset=7, rule_w=1, shadow=4),
    who_color=CRIMSON_DEEP,
    who_outlines=[ ])


################################################################################
## Shots
################################################################################

## Camera set-ups. Call with the transition to use for the cut.

label shot_eiki(trans=whip_right):
    camera
    hide screen emote
    scene bg_courtroom
    show judge_bench at stand_pos
    show fumo_shadow at shadow_pos
    show eiki_fumo at on_stand
    with trans
    return

## Witness stand. Each witness has a one-line shot so testimony data can name
## it ("shot_marisa") and the engine can cut back to it after a press.
label shot_witness(fumo, trans=whip_left):
    camera
    hide screen emote
    scene bg_courtroom
    show witness_stand at stand_pos
    show fumo_shadow at shadow_pos
    $ renpy.show(fumo, at_list=[ on_stand ])
    with trans
    return

label shot_cirno(trans=whip_left):
    call shot_witness("cirno_fumo", trans)
    return

label shot_marisa(trans=whip_left):
    call shot_witness("marisa_fumo", trans)
    return

label shot_sakuya(trans=whip_left):
    call shot_witness("sakuya_fumo", trans)
    return

label shot_reisen(trans=whip_left):
    call shot_witness("reisen_fumo", trans)
    return

label shot_meiling(trans=whip_left):
    call shot_witness("meiling_fumo", trans)
    return

label shot_alice(trans=whip_left):
    call shot_witness("alice_fumo", trans)
    return

label shot_reimu(trans=whip_left):
    call shot_witness("reimu_fumo", trans)
    return

label shot_kaguya(trans=whip_left):
    call shot_witness("kaguya_fumo", trans)
    return

label shot_mokou(trans=whip_left):
    call shot_witness("mokou_fumo", trans)
    return

label shot_aya(trans=whip_left):
    call shot_witness("aya_fumo", trans)
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

define fallacy_tu_quoque = Fallacy(
    "tu_quoque",
    _("Tu Quoque"),
    _("(You Too!)"),
    _("Excusing a wrong by pointing out that someone else does it too."),
    "gui/fallacy_tu_quoque.svg")

define fallacy_false_dilemma = Fallacy(
    "false_dilemma",
    _("False Dilemma"),
    _("(Only Two Doors)"),
    _("Offering two options as the only ones, when others exist."),
    "gui/fallacy_false_dilemma.svg")

define fallacy_appeal_to_authority = Fallacy(
    "appeal_to_authority",
    _("Appeal to Authority"),
    _("(Because They Said So)"),
    _("Treating a famous name as proof instead of checking the evidence."),
    "gui/fallacy_appeal_to_authority.svg")

define fallacy_hasty_generalization = Fallacy(
    "hasty_generalization",
    _("Hasty Generalization"),
    _("(A Sample of One)"),
    _("Drawing a rule about everything from one or two examples."),
    "gui/fallacy_hasty_generalization.svg")

define fallacy_straw_man = Fallacy(
    "straw_man",
    _("Straw Man"),
    _("(Scarecrow Argument)"),
    _("Attacking a twisted, weaker version of what someone actually said."),
    "gui/fallacy_straw_man.svg")

define fallacy_bandwagon = Fallacy(
    "bandwagon",
    _("Bandwagon"),
    _("(Everyone Says So)"),
    _("Treating a claim as true because lots of people believe it."),
    "gui/fallacy_bandwagon.svg")

define fallacy_moving_goalposts = Fallacy(
    "moving_goalposts",
    _("Moving the Goalposts"),
    _("(The Finish Line Moves)"),
    _("Changing the test after it has been passed, so no answer is ever enough."),
    "gui/fallacy_moving_goalposts.svg")

define fallacy_red_herring = Fallacy(
    "red_herring",
    _("Red Herring"),
    _("(Change the Subject)"),
    _("Dragging in something else, so nobody notices the question was never answered."),
    "gui/fallacy_red_herring.svg")

define fallacy_cherry_picking = Fallacy(
    "cherry_picking",
    _("Cherry Picking"),
    _("(Only the Ripe Ones)"),
    _("Showing only the evidence that agrees, and hiding the rest."),
    "gui/fallacy_cherry_picking.svg")

define fallacy_circular_reasoning = Fallacy(
    "circular_reasoning",
    _("Circular Reasoning"),
    _("(Begging the Question)"),
    _("Using the conclusion as its own reason, so the argument proves nothing."),
    "gui/fallacy_circular_reasoning.svg")

## Case 01 evidence.
define evidence_frog_census = Evidence("frog_census", _("Frog Census"),
    _("Twenty frogs, all accounted for. All mildly annoyed."), "gui/ev_document.svg")
define evidence_weather_log = Evidence("weather_log", _("Misty Lake Weather Log"),
    _("Clear skies all day. Thirty-one degrees by noon."), "gui/ev_sun.svg")
define evidence_cirno_ice = Evidence("cirno_ice", _("Cirno's Ice"),
    _("Ordinary ice. Melts in the sun, like all ice."), "gui/ev_ice.svg")

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
        "tu_quoque" : _("She isn't excusing herself by pointing at anyone. She's crediting the ice with the sun's work."),
        "false_dilemma" : _("Nobody offered two doors. She saw two events in a row and crowned the first one."),
        "appeal_to_authority" : _("She cites no famous name. Only herself, which is not the same thing."),
        "circular_reasoning" : _("Her logic doesn't loop back on itself. It just trips over the word \"then.\""),
        },
    proof="weather_log",
    proof_wrong=_("That doesn't explain the thawing. What actually warmed those frogs?"))


################################################################################
## Press conversations
################################################################################

label press_cirno_1:
    you "Twenty exactly? How did you count them?"
    $ react("cirno", "smug")
    cirno "On my fingers! I ran out, so I counted my fingers again."
    call shot_eiki
    eiki "...That is correct arithmetic. I am as surprised as you are."
    return

label press_cirno_2:
    you "What was the weather like at noon?"
    cirno "Hot! The sun was showing off all day. Rude, honestly."
    $ react("cirno", "angry")
    cirno "Stop changing the subject. The subject is me being amazing."
    return

label press_cirno_3:
    you "How exactly does freezing make a frog immortal?"
    cirno "Easy! First, ice. Then, frog is alive. So the ice did the alive part!"
    $ react("cirno", "smug")
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

    call open_case("case1")

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
    if diff()["proof"]:
        eiki "Then prove it. Everything this court knows sits in the Court Record."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_cirno
    $ bgm("cirno")
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
    eiki "When a statement fails, object. You have [spirit_word!t] magatama of spirit. Spend them wisely."

    jump case1_cross


label case1_cross:

    call shot_cirno
    $ bgm("cirno")
    call cross_examination("testimony_cirno")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. From the top. Slower, for everyone's sake."
        jump case1_cross

    jump case1_breakthrough


label case1_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Plenty of frogs freeze in winter and thaw in spring. They manage it without you."
    you "The ice didn't save them. The noon sun thawed them. You just happened to be first."

    call breakdown("cirno")
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

    call close_case("case1", fallacy_false_cause)
    return
