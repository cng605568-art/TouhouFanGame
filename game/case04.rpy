################################################################################
## case04.rpy - Case 04: The Lunar Prescription. Witness: Reisen.
## Appeal to authority. The last case on the docket.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_tonic_bottle = Evidence("tonic_bottle", _("Miracle Tonic"),
    _("Label: \"Perfectly safe! —Eirin.\" Smells faintly of blueberries."), "gui/ev_bottle.svg")
define evidence_eirin_diploma = Evidence("eirin_diploma", _("Eirin's Diploma"),
    _("Lunar Academy of Medicine. Top of her class, ten thousand years running."), "gui/ev_diploma.svg")
define evidence_lab_notebook = Evidence("lab_notebook", _("Eientei Lab Notebook"),
    _("\"Miracle Tonic. Tests run: none yet. Selling anyway (Reisen).\""), "gui/ev_book.svg")

define testimony_reisen = Testimony(
    title=_("Eientei's Miracle Tonic"),
    witness="reisen",
    judge="eiki",
    witness_shot="shot_reisen",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("I sold the tonic in the Human Village yesterday. Everyone paid in full."),
            "press_reisen_1",
            _("A sales record is not an argument. Though the receipts are very neat.")),
        Statement(
            _("This morning, three customers said they could hear colours. Mostly blue."),
            "press_reisen_2",
            _("That is a symptom, not a syllogism. Find the place where she reasons.")),
        Statement(
            _("But the tonic was cleared before I sold a single bottle."),
            "press_reisen_3",
            _("Cleared by whom? Press her before you object."),
            reveals="eirin"),
        Statement(
            _("Master Eirin says it's perfectly safe. So it can't be the tonic."),
            "press_reisen_4",
            None,
            hidden=True, key="eirin"),
        ],
    cards=[ fallacy_ad_hominem, fallacy_false_dilemma, fallacy_appeal_to_authority ],
    flaw=3,
    answer="appeal_to_authority",
    scolds={
        "ad_hominem" : _("That's the mirror image. Ad Hominem rejects a claim because of who made it. She's accepting one."),
        "false_dilemma" : _("Nobody is offering two doors here. She's leaning on one very famous name."),
        "false_cause" : _("Order isn't her mistake. She's treating a name as if it were a test."),
        "tu_quoque" : _("She isn't pointing at anyone else's sins. She's hiding behind her teacher's title."),
        "slippery_slope" : _("No chain of disasters predicted. Just one reputation, doing all the work."),
        },
    proof="lab_notebook",
    proof_wrong=_("That's a reputation, not a result. Show whether anyone actually tested it."))


label press_reisen_1:
    you "What exactly is in the tonic?"
    $ react("reisen", "nervous")
    reisen "Moon herbs, honey, and something Master told me not to ask about."
    return

label press_reisen_2:
    you "Is hearing colours a known side effect?"
    $ react("reisen", "shock")
    reisen "Define \"known.\" On the moon, we... never mind. No. It isn't."
    return

label press_reisen_3:
    you "Cleared by whom, exactly?"
    $ react("reisen", "smug")
    reisen "By the greatest pharmacist in Gensokyo! My master!"
    reisen "Add that to my testimony. It settles everything."
    return

label press_reisen_4:
    you "Did Eirin actually test the tonic?"
    $ react("reisen", "smug")
    reisen "She didn't need to. She's a genius. Geniuses just know things."
    call shot_eiki
    eiki "Her teacher's reputation is doing all of her arguing for her."
    return


label case4:

    call open_case("case4")

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Order. The Higan Court of Logic is in session. Last case of the day."
    hide gavel
    eiki "Komachi."
    komachi "Defendant's here, boss. Brought free samples."
    eiki "Confiscate them."
    komachi "Already drank one. Is purple supposed to sound like that?"

    call shot_reisen
    reisen "Reisen Udongein Inaba, assistant to Eientei's pharmacist. This is all a misunderstanding."

    call shot_eiki
    eiki "The charge: selling an untested tonic in the Human Village."

    call shot_reisen
    reisen "It's tested! Well. It's approved. By someone very qualified."

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. Respect your elders. Respect experts."
    eiki "But respect is not evidence. Remember which one you are weighing."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_reisen
    $ bgm("reisen")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("Eientei's Miracle Tonic"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    reisen_t "I sold the tonic in the Human Village yesterday. Everyone paid in full."
    reisen_t "This morning, three customers said they could hear colours. Mostly blue."
    reisen_t "But the tonic was cleared before I sold a single bottle."

    hide screen court_tag
    call shot_eiki
    eiki "The floor is yours, Junior Judge. Do not drink anything she offers you."

    jump case4_cross


label case4_cross:

    call shot_reisen
    $ bgm("reisen")
    call cross_examination("testimony_reisen")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. And Komachi, put the samples down."
        jump case4_cross

    jump case4_breakthrough


label case4_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Eirin's genius doesn't change what happened to your customers."
    you "Three villagers hear colours. A reputation can't outvote three witnesses."

    call breakdown("reisen")
    reisen "B-but Master is never wrong! ...She's rarely wrong. She's wrong sometimes."

    call shot_eiki
    camera at eiki_lecture
    eiki "An appeal to authority. A famous name is not a test result."
    eiki "Experts deserve a hearing. They do not deserve a free pass."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Reisen Udongein Inaba. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: recall every bottle, and bring this court a written test report. Signed."

    call shot_reisen
    reisen "Can Master sign it?"

    call shot_eiki
    eiki "Only if she runs the test first. Bailiff."
    komachi "On it, boss."

    window hide
    call shot_reisen
    show reisen_fumo at fumo_yeet
    show fumo_shadow at shadow_gone
    $ sfx("yeet")
    pause 1.15
    hide reisen_fumo

    call shot_eiki
    window auto
    eiki "I keep saying \"escort.\""
    komachi "And I keep escorting, boss. Very efficiently."
    eiki "That clears today's docket. Junior Judge, your work was... acceptable."
    komachi "That's her highest praise, by the way."
    eiki "Komachi."
    komachi "Escorting myself out."

    call close_case("case4", fallacy_appeal_to_authority)
    return
