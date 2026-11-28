################################################################################
## case09.rpy - Case 09: The Five Impossible Chores. Witness: Kaguya Houraisan.
## Moving the goalposts. The last case of the second docket, and the one that
## ends with Mokou barging in to settle a thousand-year-old score.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_chore_list = Evidence("chore_list", _("Signed Chore List"),
    _("\"Five chores, then a week off.\" Signed: Kaguya Houraisan. All five ticked."), "gui/ev_list.svg")
define evidence_five_treasures = Evidence("five_treasures", _("The Five Treasures"),
    _("A dragon's jewel, a fire-rat robe, a stone bowl, a jewelled branch, a swallow's shell."), "gui/ev_jewel.svg")
define evidence_new_chore_list = Evidence("new_chore_list", _("New Chore List"),
    _("Written this morning, unsigned: \"Also: the moon. Bring it here.\""), "gui/ev_document.svg")

## Kaguya's testimony rewrites itself: every press moves her statements on
## to their next version, and the goalposts only finish moving at the end.
define testimony_kaguya = Testimony(
    title=_("The Five Impossible Chores"),
    witness="kaguya",
    judge="eiki",
    witness_shot="shot_kaguya",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("I told Reisen she could take a week off if she finished five chores."),
            "press_kaguya_1",
            _("An offer is not an argument. Look for where she reasons."),
            variants=[ _("I told Reisen she might take a week off. If she finished five chores. Roughly.") ]),
        Statement(
            _("Yesterday she brought me all five. I admit I was surprised."),
            "press_kaguya_2",
            _("Even the defendant admits the chores were done. Keep going.")),
        Statement(
            _("But she still hasn't earned her week off."),
            "press_kaguya_3",
            None,
            variants=[
                _("A week off is a privilege. Privileges must be earned properly."),
                _("Now she must also bring me the moon. Then the week off is hers. Probably."),
                ]),
        ],
    cards=[ fallacy_false_dilemma, fallacy_moving_goalposts, fallacy_circular_reasoning ],
    flaw=2,
    answer="moving_goalposts",
    scolds={
        "false_dilemma" : _("No either-or here. Just a finish line that keeps sliding away."),
        "circular_reasoning" : _("Her reason isn't her conclusion. Her rules simply change every time Reisen meets them."),
        "straw_man" : _("She isn't misquoting Reisen. She's rewriting her own deal."),
        "hasty_generalization" : _("No rule built from one example. Just a promise with a brand-new clause."),
        "bandwagon" : _("No crowd involved. Just one princess and an ever-growing chore list."),
        "false_cause" : _("Nothing here is mistaken for a cause. The test itself moved."),
        "ad_hominem" : _("She isn't attacking Reisen. She's attacking the finish line."),
        "tu_quoque" : _("Nobody's blaming anyone back. She just keeps adding chores."),
        "slippery_slope" : _("No chain of disasters predicted. Only a chain of chores."),
        "appeal_to_authority" : _("She isn't citing an expert. She's changing her own rules."),
        },
    proof="chore_list",
    proof_wrong=_("That doesn't show what was agreed. Find the deal as it was first made."),
    proof_kind="line",
    proof_data=dict(
        phrases=[
            _("\"Five chores, then a week off.\""),
            _("Signed: Kaguya Houraisan."),
            _("All five ticked."),
            ],
        answer=0,
        wrong=_("True, but that isn't where the finish line was drawn. Point to the deal itself.")),
    gimmick="shift",
    shift_early=_("Not yet. She's stalling, not moving anything. Press her and watch the line move."))


label press_kaguya_1:
    you "Which five chores?"
    kaguya "Little things. A dragon's jewel, a fire-rat robe. The usual."
    call shot_eiki
    eiki "The usual for whom?"
    return

label press_kaguya_2:
    you "Surprised? Why?"
    $ react("kaguya", "smug")
    kaguya "Nobody has finished my list in a thousand years. It's been a while."
    return

label press_kaguya_3:
    if xexam_shift == 0:
        you "Why not? She finished all five."
        kaguya "Ah, but finishing was never really the point. Let me rephrase."
    elif xexam_shift == 1:
        you "Earned properly how?"
        $ react("kaguya", "smug")
        kaguya "Oh, you'll see. Let me rephrase again."
    else:
        you "The moon wasn't on the list. When did you add it?"
        $ react("kaguya", "nervous")
        kaguya "This morning. After she finished the other five. Obviously."
        call shot_eiki
        eiki "So the finish line moved the moment she reached it."
    return


label case9:

    call open_case("case9")

    komachi "Boss, the defendant sent word. She'll arrive when she feels like it."
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Bring her in. Now."
    hide gavel
    komachi "...She feels like it now."

    call shot_kaguya
    kaguya "Kaguya Houraisan, princess of Eientei. How charming. A courtroom."

    call shot_eiki
    eiki "The charge: refusing your assistant, Reisen, the week off you promised her."

    call shot_kaguya
    kaguya "Promised? I set her a few little tasks. She simply hasn't finished them."

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. A fair test keeps its rules from start to finish."
    eiki "When the finish line moves every time someone reaches it, the race was never fair."
    eiki "And watch her testimony closely. With this one, it tends to change while you read it."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_kaguya
    $ bgm("kaguya")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Five Impossible Chores"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    kaguya_t "I told Reisen she could take a week off if she finished five chores."
    kaguya_t "Yesterday she brought me all five. I admit I was surprised."
    kaguya_t "But she still hasn't earned her week off."

    hide screen court_tag
    call shot_eiki
    eiki "Your witness, Junior Judge. She has had a thousand years of practice."

    jump case9_cross


label case9_cross:

    call shot_kaguya
    $ bgm("kaguya")
    call cross_examination("testimony_kaguya")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. The princess has time. So, apparently, do we."
        jump case9_cross

    jump case9_breakthrough


label case9_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "This list has your signature. Five chores, then a week off. All five are ticked."
    you "Reisen reached the line you drew. You moved it the moment she got there."

    call breakdown("kaguya")
    kaguya "...My signature. In ink. How very unlike me."

    call shot_eiki
    camera at eiki_lecture
    eiki "Moving the goalposts. Change the test as soon as it is passed, and no answer is ever enough."
    eiki "A promise judged by new rules is not a promise. It is a trap."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Kaguya Houraisan. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: Reisen takes her week off, starting today. You will do her chores."

    call shot_kaguya
    kaguya "Me? Chores? ...Do I have to fetch my own tea?"

    call shot_eiki
    eiki "Every cup. Bailiff."
    komachi "On it, boss."

    ## Before Komachi can get there, Mokou gets there first. The fight is
    ## staged in fight.rpy.
    window hide
    call shot_kaguya
    $ bgm("mokou", fadein=0.3, card_delay=2.4, fadeout=0.2)
    call mokou_entrance
    window auto

    mokou "KAGUYAAA!"
    kaguya "Oh no. Not now. Not in court."
    mokou "Fujiwara no Mokou. The Bunbunmaru says you lost. They printed it an hour before your verdict."
    mokou "Thought I'd help you lose some more."
    eiki "This is a courtroom. The defendant is in this court's custody."
    mokou "Great. I'll take custody."

    window hide
    call fight_faceoff
    call fight_rush
    call fight_finisher
    window auto
    kaguya "Ow! Ow! My face is priceless!"
    mokou "So's this. Free of charge."

    window hide
    call fight_dash_exit
    window auto
    kaguya "Eirin! Somebody! Bailiff!"

    call fight_cleanup
    call shot_eiki
    komachi "...Want me to chase them, boss?"
    eiki "No. They have been doing this for a thousand years. They will be back by dinner."
    eiki "Reisen's week off begins regardless. Court is adjourned."
    komachi "That's the docket, boss."
    eiki "Not quite. Keep the court open. They will be back by dinner."
    komachi "...You're keeping the court open for dinner?"
    eiki "Komachi."
    komachi "Escorting myself out."

    $ bgm_stop(2.0)
    call close_case("case9", fallacy_moving_goalposts)
    return
