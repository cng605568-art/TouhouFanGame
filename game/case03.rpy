################################################################################
## case03.rpy - Case 03: The Vanished Pudding. Witness: Sakuya. False dilemma.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_empty_plate = Evidence("empty_plate", _("Empty Plate"),
    _("One spoon, licked clean. No fingerprints, just custard."), "gui/ev_plate.svg")
define evidence_pudding_recipe = Evidence("pudding_recipe", _("Pudding Recipe"),
    _("Eggs, milk, sugar. \"For the mistress only\" piped in caramel."), "gui/ev_document.svg")
define evidence_staff_roster = Evidence("staff_roster", _("Mansion Roster, 3 PM"),
    _("Present: the mistress, her sister, Patchouli, forty fairy maids, one uninvited magician."), "gui/ev_list.svg")

define testimony_sakuya = Testimony(
    title=_("The Three O'Clock Pudding"),
    witness="sakuya",
    judge="eiki",
    witness_shot="shot_sakuya",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("At three o'clock, the mistress's pudding was in the kitchen. I placed it there myself."),
            "press_sakuya_1",
            _("A maid placing a pudding is a fact. A very precise fact. Look further.")),
        Statement(
            _("At five past three, the plate was empty. Only the spoon remained."),
            "press_sakuya_2",
            _("An empty plate is evidence, not reasoning. Object to how she gets from the plate to the culprit."),
            reveals="inside"),
        Statement(
            _("Five minutes is too quick for anyone outside to reach the kitchen. So it was someone in the mansion."),
            "press_sakuya_trap",
            _("That one holds. Five minutes is too short for an outsider. Her mistake is in who she counts as inside."),
            hidden=True, key="inside"),
        Statement(
            _("Either Meiling ate it, or the mistress ate her own pudding. The mistress would never. So: Meiling."),
            "press_sakuya_4",
            None),
        ],
    cards=[ fallacy_false_cause, fallacy_false_dilemma, fallacy_tu_quoque ],
    flaw=3,
    answer="false_dilemma",
    scolds={
        "false_cause" : _("Nothing here mistakes order for cause. The trouble is her menu. Count the dishes."),
        "tu_quoque" : _("Nobody is excusing themselves by pointing elsewhere. Count her suspects. Then count the mansion."),
        "ad_hominem" : _("She isn't attacking Meiling's character. She's offering the court only two doors."),
        "slippery_slope" : _("No chain of disasters here. Just a list of suspects that is suspiciously short."),
        },
    proof="staff_roster",
    proof_wrong=_("That says nothing about who else was home. Ask her who was in the mansion."))


label press_sakuya_1:
    you "How can you be certain of the time?"
    $ react("sakuya", "smug")
    sakuya "I stop it every day. I always know exactly where I left it."
    return

label press_sakuya_2:
    you "Who else was in the mansion at three?"
    $ react("sakuya", "angry")
    sakuya "The mistress, her sister, Patchouli, forty fairy maids, and a certain magician. Uninvited."
    $ add_evidence("staff_roster")
    call shot_eiki
    eiki "...The window again, I assume."
    call shot_sakuya
    sakuya "And note the timing, Junior Judge. Put this in my testimony."
    return

label press_sakuya_trap:
    you "Couldn't someone have come in from outside?"
    $ react("sakuya", "smug")
    sakuya "Through these halls? I make them longer when I'm annoyed. Nobody outside gets in that fast."
    call shot_eiki
    eiki "That much is sound. Keep your objections for the parts that aren't."
    return

label press_sakuya_4:
    you "Why are those the only two suspects?"
    $ react("sakuya", "nervous")
    sakuya "Because they're the two I considered. That makes the list complete."
    call shot_eiki
    eiki "A list is complete when it holds everyone, not when you stop writing."
    return


label case3:

    call open_case("case3")

    komachi "Witness is already here, boss. She was here before me. Before you, even."
    eiki "Head maids."
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Court is in session. The defendant, Hong Meiling, stands accused of eating the mistress's pudding."
    hide gavel
    komachi "Defendant's asleep at the gate, boss. Seemed rude to wake her."
    eiki "...We will proceed without her. The witness, please."

    call shot_sakuya
    sakuya "Izayoi Sakuya, head maid. I'll be brief. I have a mansion to run."

    call shot_eiki
    eiki "You accuse your own gatekeeper?"

    call shot_sakuya
    sakuya "I accuse whoever the facts accuse. Today, the facts are very sleepy."

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. A tidy witness gives tidy answers."
    eiki "Tidy is not the same as complete. Listen for what she leaves out."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_sakuya
    $ bgm("sakuya")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Three O'Clock Pudding"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    sakuya_t "At three o'clock, the mistress's pudding was in the kitchen. I placed it there myself."
    sakuya_t "At five past three, the plate was empty. Only the spoon remained."
    sakuya_t "Either Meiling ate it, or the mistress ate her own pudding. The mistress would never. So: Meiling."

    hide screen court_tag
    call shot_eiki
    eiki "Cross-examine, Junior Judge. Quickly. She has already checked her watch twice."

    jump case3_cross


label case3_cross:

    call shot_sakuya
    $ bgm("sakuya")
    call cross_examination("testimony_sakuya")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. The pudding is not getting any less eaten."
        jump case3_cross

    jump case3_breakthrough


label case3_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Your mansion holds dozens of people. You offered the court exactly two."
    you "Fairy maids, the mistress's sister, a certain magician. Any of them could have eaten it."

    call breakdown("sakuya")
    sakuya "...Forty fairy maids. I didn't count the fairy maids."

    call shot_eiki
    camera at eiki_lecture
    eiki "A false dilemma. Two doors painted on a wall, and you are told to pick one."
    eiki "When someone offers only two choices, ask who took away the others."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "In the matter of Hong Meiling and the vanished pudding, this court finds the defendant..."
    hide gavel

    window hide
    show screen verdict_stamp(_("NOT GUILTY"), "無罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "The pudding remains at large."

    call shot_sakuya
    sakuya "I'll find the real culprit. I have all the time in the world. Literally."

    window hide
    hide sakuya_fumo
    show fumo_shadow at shadow_gone
    with flash
    pause 0.4

    call shot_eiki
    window auto
    komachi "...She does that."
    eiki "Court is adjourned. Someone wake the defendant and tell her she won."

    call close_case("case3", fallacy_false_dilemma)
    return
