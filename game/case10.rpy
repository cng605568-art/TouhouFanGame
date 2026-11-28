################################################################################
## case10.rpy - Case 10: Back by Dinner. Witness: Fujiwara no Mokou.
## A short trial. Red herring, and the docket's first bad argument with a
## true conclusion: Mokou's reasoning is a dodge, but the answer she dodged
## clears her. Ends by summoning the reporter behind every headline so far.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_scorched_bench = Evidence("scorched_bench", _("Scorched Bench"),
    _("The witness bench from Case 09. Still smoking. Smells faintly of bamboo."), "gui/ev_scorch.svg")
define evidence_bunbunmaru_extra = Evidence("bunbunmaru_extra", _("Bunbunmaru Extra"),
    _("\"PRINCESS KIDNAPPED IN COURT!\" One blurry photo. Printed before it happened."), "gui/ev_newspaper.svg")
define evidence_kaguya_letter = Evidence("kaguya_letter", _("Kaguya's Letter"),
    _("\"Mokou: come and get me after my trial. Loser does the dishes. —K\""), "gui/ev_letter.svg")

define testimony_mokou = Testimony(
    title=_("Custody"),
    witness="mokou",
    judge="eiki",
    witness_shot="shot_mokou",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("Kidnapping? I carried her out the door. She hardly struggled."),
            "press_mokou_1",
            _("Carrying someone out is the charge, not a fallacy. Find where she argues.")),
        Statement(
            _("And what about what her family did to mine, a thousand years ago? Ask about that."),
            "press_mokou_2",
            None),
        ],
    cards=[ fallacy_red_herring, fallacy_tu_quoque, fallacy_ad_hominem ],
    flaw=1,
    answer="red_herring",
    scolds={
        "tu_quoque" : _("Close. But she isn't saying Kaguya does it too. She's leaving the question behind entirely."),
        "ad_hominem" : _("She isn't attacking Kaguya to refute a claim. She's leading the court away from the question."),
        "straw_man" : _("Nobody's words are twisted. The question is simply abandoned."),
        "false_dilemma" : _("No either-or. Just a thousand-year-old fish, dragged across the trail."),
        "circular_reasoning" : _("No circle. Her answer is about something else altogether."),
        },
    proof="kaguya_letter",
    proof_wrong=_("That doesn't answer the question she dodged. Did Kaguya go against her will?"),
    after_wrong="mokou_flare")

## Mokou is hot-headed: every wrong objection, something catches fire.
define MOKOU_FLARES = [
    _("Boss, the bench is on fire again."),
    _("That was the railing, boss. Was."),
    _("Boss, your hat is fine. Mostly."),
    ]

label mokou_flare:
    call shot_mokou
    $ react("mokou", "angry")
    $ sfx("mokou_burst")
    show screen mokou_fire
    with vpunch
    $ flare = renpy.random.choice(MOKOU_FLARES)
    komachi "[flare!t]"
    return


label press_mokou_1:
    you "Hardly struggled?"
    $ react("mokou", "smug")
    mokou "She laughed the whole way. Then she handed me this."
    $ add_evidence("kaguya_letter")
    call shot_eiki
    eiki "...Laughed."
    return

label press_mokou_2:
    you "What does a thousand-year-old feud have to do with yesterday?"
    $ react("mokou", "angry")
    mokou "Everything! ...Mostly. Some of it."
    call shot_eiki
    eiki "None of it."
    return


label case10:

    call open_case("case10")

    komachi "Boss. They're back. Both of them. It's dinner time."
    eiki "As predicted."
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "A short session. The charge is kidnapping, and the defendant is hungry."
    hide gavel

    call shot_mokou
    mokou "Fujiwara no Mokou. Let's make it quick. There's a pot of dishes waiting for somebody."

    call shot_eiki
    eiki "The charge: carrying the defendant of Case 09 out of this court. By force. On fire."
    kaguya "I'm a witness too, you know. Nobody asked me."
    eiki "Later."

    camera at eiki_lecture
    eiki "Junior Judge. A bad argument is not the same as a false conclusion."
    eiki "Today, catch the fallacy. Then ask whether the answer was right anyway."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_mokou
    $ bgm("mokou")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("Custody"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    mokou_t "Kidnapping? I carried her out the door. She hardly struggled."
    mokou_t "And what about what her family did to mine, a thousand years ago? Ask about that."

    hide screen court_tag
    call shot_eiki
    eiki "Quickly, Junior Judge. Before she sets anything else alight."

    jump case10_cross


label case10_cross:

    call shot_mokou
    $ bgm("mokou")
    call cross_examination("testimony_mokou")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. Komachi, fetch a bucket."
        jump case10_cross

    jump case10_breakthrough


label case10_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "A thousand-year-old feud says nothing about yesterday. That's a red herring."
    you "But this letter answers the question you dodged. Kaguya asked you to come and get her."

    call breakdown("mokou")
    mokou "...You read her letter? Out loud? In court?"

    call shot_eiki
    camera at eiki_lecture
    eiki "A red herring. Drag a smelly fish across the trail, and the hounds forget the fox."
    eiki "Her reasoning was a red herring. Her conclusion, however, was correct."
    eiki "No one can kidnap a princess who wrote the invitation."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Fujiwara no Mokou. On the charge of kidnapping, this court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("NOT GUILTY"), "無罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "On the matter of the bench, however: you will build this court a new one."

    call shot_mokou
    mokou "Fine. I'm good with wood. Better with fire."

    call shot_kaguya
    $ react("kaguya", "smug")
    kaguya "For the record, I won. She's doing the dishes."
    mokou "You did NOT win."

    call shot_eiki
    komachi "Bailiff time, boss? ...Wait. She was acquitted."
    eiki "She was."
    komachi "Can I throw someone anyway? It's a habit."
    eiki "No."

    komachi "Boss. The Bunbunmaru printed this before the trial even started."
    eiki "\"PRINCESS KIDNAPPED IN COURT.\" One blurry photo, and not one word from the princess."
    eiki "That tengu has written about every case on this docket."
    eiki "Komachi. Summon her. Tomorrow, she writes from the witness stand."
    komachi "On it, boss."

    call close_case("case10", fallacy_red_herring)
    return
