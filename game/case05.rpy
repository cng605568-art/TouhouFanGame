################################################################################
## case05.rpy - Case 05: The Unappealable Verdict. Witness: Shiki Eiki.
## Circular reasoning. The finale: the pudding from Case 03 turns up at Misty
## Lake (Komachi mentions it at the end of Case 04), the mansion appeals, and
## a judge can't hear her own appeal. The Junior Judge takes the bench,
## Komachi clerks, and Eiki testifies.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_case3_verdict = Evidence("case3_verdict", _("Case 03 Verdict"),
    _("Hong Meiling: NOT GUILTY. The real thief: \"Undetermined.\" Signed, Shiki Eiki."), "gui/ev_document.svg")
define evidence_frozen_pudding = Evidence("frozen_pudding", _("Frozen Pudding Cup"),
    _("Found at Misty Lake inside a block of fairy ice. Bat crest on the cup. Half eaten."), "gui/ev_pudding.svg")

## The witness speaks in red ink, like every witness.
define eiki_t = Character(kind=eiki, what_color="#7A1C2A", what_size=40)

define testimony_eiki = Testimony(
    title=_("The Unappealable Verdict"),
    witness="eiki",
    judge="komachi",
    witness_shot="shot_eiki_stand",
    judge_shot="shot_bench",
    statements=[
        Statement(
            _("The pudding vanished from the mansion kitchen at three o'clock."),
            "press_eiki_1",
            _("The time's on the roster, Junior Judge. That part's solid.")),
        Statement(
            _("Hong Meiling was found not guilty. I reviewed every page of that trial."),
            "press_eiki_2",
            _("Meiling's acquittal checks out. You helped win it, remember?")),
        Statement(
            _("This appeal cannot succeed. My verdict stands."),
            "press_eiki_3",
            _("That's a claim, not a reason. Press her for the reason first."),
            reveals="circle"),
        Statement(
            _("My verdicts are correct because I gave them. And I only give correct verdicts."),
            "press_eiki_4",
            None,
            hidden=True, key="circle"),
        ],
    cards=[ fallacy_appeal_to_authority, fallacy_circular_reasoning, fallacy_false_dilemma ],
    flaw=3,
    answer="circular_reasoning",
    scolds={
        "appeal_to_authority" : _("Close. But she isn't leaning on someone else's name. She's leaning on her own conclusion."),
        "false_cause" : _("Nothing here happens before anything else. The reasoning goes around, not forward."),
        "ad_hominem" : _("She isn't attacking anyone. She's defending her verdict with her verdict."),
        "tu_quoque" : _("Nobody else is being blamed. Look at the reason, then look at the claim."),
        "false_dilemma" : _("No either-or here. Just one idea chasing its own tail."),
        "slippery_slope" : _("No chain of disasters. Just a circle."),
        },
    proof="frozen_pudding",
    proof_wrong=_("That still comes from her. Show something that doesn't depend on her word."))


## The Junior Judge's bench, empty but for the scales. Komachi speaks from
## beside it.
label shot_bench(trans=whip_right):
    camera
    scene bg_courtroom
    show judge_bench at stand_pos
    show scales at bench_scales
    with trans
    return

## Eiki at the witness stand.
label shot_eiki_stand(trans=whip_left):
    call shot_witness("eiki_fumo", trans)
    return

transform bench_scales:
    xpos 960 xanchor 0.5 ypos FUMO_FEET yanchor 1.0 zoom 0.9


label press_eiki_1:
    you "Who says it vanished at three?"
    eiki "Sakuya's roster, and Sakuya's pocket watch. The time is not in dispute."
    return

label press_eiki_2:
    you "If Meiling didn't take it, who did?"
    $ react("eiki", "nervous")
    eiki "Undetermined. Not every case needs a culprit. Some only need a verdict."
    call shot_bench
    komachi "That's... not a great sentence, boss."
    return

label press_eiki_3:
    you "Why can't the appeal succeed?"
    $ react("eiki", "smug")
    eiki "Because my verdicts are correct. Obviously."
    eiki "Enter that into my testimony, Junior Judge. In full."
    return

label press_eiki_4:
    you "How do you know your verdicts are correct?"
    eiki "Because I gave them. Were you not listening?"
    call shot_bench
    komachi "Boss, that's the reason and the answer. It's the same thing twice."
    return


label case5:

    call open_case("case5")

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Order. The Higan Court of Logic is in session."
    hide gavel
    eiki "Komachi. The defendant?"
    komachi "About that, boss. There isn't one. It's an appeal."
    eiki "An appeal of what?"
    komachi "The vanished pudding. The mansion says the thief was never found."
    komachi "And a cup turned up at Misty Lake. Frozen solid."
    eiki "That case is closed. I closed it."
    komachi "The appeal names your verdict, boss. A judge can't hear her own appeal."
    $ react("eiki", "shock")
    eiki "..."
    eiki "...Rules are rules. Even mine. Especially mine."
    eiki "Junior Judge. Take the bench. I will take the stand."

    call shot_eiki_stand
    eiki "Shiki Eiki, Yama of Paradise. I will explain why this appeal wastes everyone's afternoon."

    call shot_bench
    komachi "The bench is yours, Junior Judge. The gavel's heavier than it looks."
    komachi "The boss always says it: listen for where the reasons run in circles."

    ## Testimony.
    window hide
    call shot_eiki_stand
    $ bgm("eiki")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Unappealable Verdict"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    eiki_t "The pudding vanished from the mansion kitchen at three o'clock."
    eiki_t "Hong Meiling was found not guilty. I reviewed every page of that trial."
    eiki_t "This appeal cannot succeed. My verdict stands."

    hide screen court_tag
    call shot_bench
    komachi "Your witness. [spirit_Word!t] magatama of spirit, same as always. She'd want it fair."

    jump case5_cross


label case5_cross:

    call shot_eiki_stand
    $ bgm("eiki")
    call cross_examination("testimony_eiki")

    if _return == "mistrial":
        call mistrial
        call shot_bench(Dissolve(0.5))
        komachi "Deep breath, Junior Judge. Even the boss gets a second hearing."
        jump case5_cross

    jump case5_breakthrough


label case5_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "This cup came from the mansion and froze at Misty Lake. Your verdict says nothing about it."
    you "Your reason was your conclusion. Evidence breaks the circle. Your argument never left it."

    call breakdown("eiki")
    eiki "My scales... They tipped. They have never tipped."

    camera at eiki_lecture
    eiki "Circular reasoning. The conclusion hides inside the reason, so the argument only proves itself."
    eiki "\"I am right because I am never wrong.\" I have sentenced souls for less."
    camera
    with Dissolve(0.4)

    call shot_bench
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    you "In the matter of the vanished pudding, this court finds the appeal..."
    hide gavel

    window hide
    show screen verdict_stamp(_("UPHELD"), "再審")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    komachi "Case 03 is reopened. Which means we still need a thief."

    call shot_cirno
    cirno "Hey! Who dug up my ice block? I was keeping that pudding cold!"
    call shot_bench
    komachi "And there she is."
    call shot_cirno
    $ react("cirno", "smug")
    cirno "It was going to melt in that kitchen! I saved it. That makes me a hero."

    call shot_eiki_stand
    eiki "Cirno. Saving it would mean giving it back. Not eating half."
    eiki "...Junior Judge. This one is yours to sentence."

    call shot_bench
    you "Return what's left of the pudding. And write \"a verdict needs evidence\" fifty times."

    call shot_eiki_stand
    $ react("eiki", "gloom")
    eiki "Make it a hundred. I will write mine beside hers."
    komachi "Court's adjourned, then. First time I've seen the boss on that side of the stand."
    eiki "And the last, Komachi."
    komachi "Whatever you say, boss."

    call close_case("case5", fallacy_circular_reasoning)
    return
