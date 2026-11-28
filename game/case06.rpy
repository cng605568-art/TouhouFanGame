################################################################################
## case06.rpy - Case 06: The Open Gate. Witness: Hong Meiling.
## Hasty generalization. The first case of the second docket: Eiki is back on
## the bench, and the gatekeeper from Case 03 is awake for once.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_library_window = Evidence("library_window", _("Library Window"),
    _("Replaced after Marisa's last visit. Locked from the inside. Not a scratch on it."), "gui/ev_window.svg")
define evidence_gate_footprints = Evidence("gate_footprints", _("Footprints at the Gate"),
    _("Tengu geta prints, from the front gate straight to the hall. Muddy. Fresh."), "gui/ev_footprints.svg")
define evidence_parasol_note = Evidence("parasol_note", _("Note on the Parasol Stand"),
    _("\"Borrowed for a photo shoot. Back soon! —A.S.\""), "gui/ev_document.svg")

define testimony_meiling = Testimony(
    title=_("The Window Theory"),
    witness="meiling",
    judge="eiki",
    witness_shot="shot_meiling",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("Yesterday at noon I rested my eyes. Briefly. My mind stayed on duty."),
            "press_meiling_1",
            _("A nap is a confession, not a fallacy. Find where she reasons.")),
        Statement(
            _("While I was resting, the mistress's parasol vanished from the hall."),
            "press_meiling_2",
            _("That is simply what happened. Look for where she draws a conclusion.")),
        Statement(
            _("But the thief didn't come through my gate. Thieves never do."),
            "press_meiling_3",
            _("\"Never\" is a big word. Press her on it before you object."),
            reveals="window"),
        Statement(
            _("Marisa broke in through the library window. So every thief uses the windows!"),
            "press_meiling_4",
            None,
            hidden=True, key="window"),
        ],
    cards=[ fallacy_false_cause, fallacy_hasty_generalization, fallacy_slippery_slope ],
    flaw=3,
    answer="hasty_generalization",
    scolds={
        "false_cause" : _("She isn't saying one event caused another. She's building a rule out of one example."),
        "slippery_slope" : _("No chain of disasters here. Just one break-in, stretched over every thief alive."),
        "false_dilemma" : _("Nobody is offering two doors. Count how many thieves her rule is built on."),
        "ad_hominem" : _("She isn't attacking anyone. She's turning one burglar into all of them."),
        "tu_quoque" : _("She isn't excusing herself with Marisa's sins. She's using Marisa as a sample of one."),
        "appeal_to_authority" : _("No famous name here. Just one memory doing the work of a survey."),
        "circular_reasoning" : _("Her conclusion isn't hiding in her reason. Her reason is simply far too small."),
        },
    proof="gate_footprints",
    proof_wrong=_("That doesn't show how this thief got in. Find out which way they came."))


label press_meiling_1:
    you "How brief was this rest?"
    $ react("meiling", "nervous")
    meiling "Two hours. For a youkai, that's barely a blink."
    return

label press_meiling_2:
    you "Did you hear anything while you rested?"
    meiling "Birds. The breeze. Someone humming. Ordinary gate sounds."
    call shot_eiki
    eiki "Humming."
    return

label press_meiling_3:
    you "Never? How can you be so sure?"
    $ react("meiling", "smug")
    meiling "Because I've seen how thieves get in! Write this down."
    meiling "Put it in my testimony. Exactly as I say it."
    return

label press_meiling_4:
    you "How many thieves have you actually seen break in?"
    meiling "One. Marisa. But she was very thorough about it."
    call shot_eiki
    eiki "One thief, and from her a law for every thief alive."
    return


label case6:

    call open_case("case6")

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Order. The Higan Court of Logic is in session."
    hide gavel
    komachi "Back on the bench, boss?"
    eiki "Where I belong. Komachi, the defendant?"
    komachi "Awake, boss. I checked twice."
    eiki "A first. Bring her in."

    call shot_meiling
    meiling "Hong Meiling, gatekeeper of the Scarlet Devil Mansion. I was awake. Mostly."

    call shot_eiki
    eiki "The charge: napping at the gate while a thief walked off with the mistress's parasol."

    call shot_meiling
    meiling "Nobody gets past my gate. Everyone knows that."

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. One example is a story. It is not a rule."
    eiki "Watch for a witness who turns one story into everyone's."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_meiling
    $ bgm("meiling")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Window Theory"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    meiling_t "Yesterday at noon I rested my eyes. Briefly. My mind stayed on duty."
    meiling_t "While I was resting, the mistress's parasol vanished from the hall."
    meiling_t "But the thief didn't come through my gate. Thieves never do."

    hide screen court_tag
    call shot_eiki
    eiki "Your witness, Junior Judge. Try to keep her awake."

    jump case6_cross


label case6_cross:

    call shot_meiling
    $ bgm("meiling")
    call cross_examination("testimony_meiling")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. Komachi, nudge the witness."
        jump case6_cross

    jump case6_breakthrough


label case6_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "One break-in through one window doesn't tell us how every thief gets in."
    you "These geta prints come straight through your front gate. Someone walked right past you."

    call breakdown("meiling")
    meiling "...Tengu sandals. I'd know them anywhere. I usually see them while I'm asleep."

    call shot_eiki
    camera at eiki_lecture
    eiki "A hasty generalization. One example, stretched into a law."
    eiki "One swallow does not make a summer. One window does not make every thief."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Hong Meiling. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: one week at the gate. Awake. Komachi will check on you."
    komachi "Me? Boss, I'm the court's leading expert on naps."
    eiki "Exactly. It takes one to know one."

    call shot_meiling
    meiling "And the parasol?"

    call shot_eiki
    eiki "The note is signed \"A.S.\" A certain reporter will be hearing from this court."
    eiki "Bailiff."
    komachi "On it, boss."

    window hide
    call shot_meiling
    show meiling_fumo at fumo_yeet
    show fumo_shadow at shadow_gone
    $ sfx("yeet")
    pause 1.15
    hide meiling_fumo

    call shot_eiki
    window auto
    eiki "Over the wall. Of course."
    komachi "Gatekeepers never use gates, boss. Everyone knows that."
    eiki "Komachi, that is exactly the fallacy we just..."
    eiki "Never mind. Court is adjourned."

    call close_case("case6", fallacy_hasty_generalization)
    return
