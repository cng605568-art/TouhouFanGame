################################################################################
## case11.rpy - Case 11: The Scoop. Witness: Aya Shameimaru.
## The finale, in two parts. Bunbunmaru News accuses the Higan Court itself of
## convicting everyone, so the Junior Judge takes the bench again (as in Case
## 05) and Eiki sits as the defendant. Part one: Aya talks too fast and leans
## on a crowd (bandwagon). A recess, where Komachi investigates. Part two: her
## headline picks only the verdicts that suit it (cherry picking). Her film
## roll also answers Case 06: the parasol was "borrowed for a photo shoot".
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_bunbunmaru_headline = Evidence("bunbunmaru_headline", _("Bunbunmaru, Today's Edition"),
    _("\"HIGAN COURT FINDS EVERYONE GUILTY!\" Seven verdicts. Seven photos."), "gui/ev_newspaper.svg")
define evidence_court_docket = Evidence("court_docket", _("The Court's Own Docket"),
    _("Every verdict, Cases 01 to 10, in Eiki's own hand. Some of them say NOT GUILTY."), "gui/ev_book.svg")
define evidence_film_roll = Evidence("film_roll", _("Aya's Film Roll"),
    _("Thirty-six frames. Seven printed. The rest: acquittals, a parasol, a sleeping gatekeeper."), "gui/ev_film.svg")
define evidence_mistress_parasol = Evidence("mistress_parasol", _("The Mistress's Parasol"),
    _("From the Bunbunmaru props cupboard. Missing since Case 06."), "gui/ev_parasol.svg")

## Part one: the interviews.
define testimony_aya_first = Testimony(
    title=_("What the Defendants Say"),
    witness="aya",
    judge="komachi",
    witness_shot="shot_aya",
    judge_shot="shot_bench",
    statements=[
        Statement(
            _("Aya Shameimaru, Bunbunmaru News. Fastest reporter in Gensokyo. I've covered every case in this court."),
            "press_aya_1",
            _("Introductions aren't arguments, Junior Judge. Even fast ones.")),
        Statement(
            _("I interviewed seven of your defendants. Every one of them says this court is unfair."),
            "press_aya_2",
            _("That's what she was told. Object to what she makes of it.")),
        Statement(
            _("Seven defendants can't all be wrong. The Higan Court is unfair."),
            "press_aya_3",
            None),
        ],
    cards=[ fallacy_bandwagon, fallacy_cherry_picking, fallacy_appeal_to_authority ],
    flaw=2,
    answer="bandwagon",
    scolds={
        "cherry_picking" : _("Maybe later. Right now she isn't hiding anything. She's leaning on a headcount."),
        "appeal_to_authority" : _("No expert here, Junior Judge. Just seven unhappy voices, counted as proof."),
        "hasty_generalization" : _("She has seven examples, not one. The trouble is she counts votes instead of checking verdicts."),
        "ad_hominem" : _("She isn't attacking the boss. She's counting complaints."),
        },
    gimmick="speed")

## Part two: the headline.
define testimony_aya = Testimony(
    title=_("The Photo Never Lies"),
    witness="aya",
    judge="komachi",
    witness_shot="shot_aya",
    judge_shot="shot_bench",
    statements=[
        Statement(
            _("Here are this court's verdicts, as printed in today's Bunbunmaru."),
            "press_aya_4",
            _("A newspaper is a fact, Junior Judge. What she prints in it is the question.")),
        Statement(
            _("Cirno, Marisa, Reisen, Meiling, Alice, Reimu, Kaguya: guilty, every one. This court convicts everyone!"),
            "press_aya_5",
            None),
        Statement(
            _("The photo never lies. Every verdict I printed is real."),
            "press_aya_6",
            _("She's right. Every verdict she printed is real. The trouble is the ones she didn't print.")),
        ],
    cards=[ fallacy_cherry_picking, fallacy_bandwagon, fallacy_hasty_generalization ],
    flaw=1,
    answer="cherry_picking",
    scolds={
        "hasty_generalization" : _("Close. But she has more examples than she shows. She picked the ones that fit."),
        "bandwagon" : _("Not a crowd this time. A selection. Ask what she left out."),
        "straw_man" : _("Nobody's words are twisted. The verdicts are real. Just not all of them."),
        "false_cause" : _("Nothing's mistaken for a cause. Something's missing from the list."),
        "appeal_to_authority" : _("She isn't citing an expert. She's choosing her evidence."),
        },
    proof="court_docket",
    proof_wrong=_("That doesn't show what her headline left out. Find the court's full record."),
    proof_kind="line",
    proof_data=dict(
        phrases=[
            _("Case 01: Cirno, guilty."),
            _("Case 03: Meiling, not guilty."),
            _("Case 06: Meiling, guilty."),
            _("Case 09: Kaguya, guilty."),
            ],
        answer=1,
        wrong=_("That one's already in her headline. Find a verdict she left out.")))


label press_aya_1:
    you "Every case?"
    $ react("aya", "smug")
    aya "Every single one. I printed Case 10 before it happened. That's how fast I am."
    call shot_bench
    komachi "That's not how news works."
    return

label press_aya_2:
    you "Which seven defendants?"
    aya "Cirno, Marisa, Reisen, Meiling, Alice, Reimu and Kaguya. Very quotable, all of them."
    call shot_bench
    komachi "Funny. Every one of them was found guilty."
    return

label press_aya_3:
    you "Did you ask anyone who was found not guilty?"
    $ react("aya", "nervous")
    aya "Why would I? They're happy. Happy doesn't sell papers."
    return

label press_aya_4:
    you "Today's edition. Printed when?"
    aya "Last week. I like to get ahead of things."
    return

label press_aya_5:
    you "Seven verdicts. How many cases has this court heard?"
    $ react("aya", "nervous")
    aya "Seven! ...Seven that matter. Seven that photograph well."
    call shot_bench
    komachi "The boss keeps the docket, Junior Judge. Have a look at it."
    return

label press_aya_6:
    you "Every printed verdict is real. What about the ones you didn't print?"
    aya "Unprinted news isn't news. That's practically the first rule of journalism."
    return


label case11:

    call open_case("case11")

    call shot_bench
    komachi "Junior Judge. The boss can't sit today. She's the defendant."
    eiki "Bunbunmaru News accuses this court of convicting everyone. A judge cannot hear her own case."
    eiki "So the bench is yours again. I will sit where the defendants sit. It is educational."
    komachi "Gavel's yours, Junior Judge. Same as last time. It's still heavy."
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    you "Court is in session."
    hide gavel

    call shot_aya
    $ react("aya", "smug")
    aya "Aya Shameimaru! Bunbunmaru News! Big fan! Mind if I take your picture? Thanks!"
    $ sfx("ui_confirm")
    with flash

    call shot_bench
    komachi "She talks fast, Junior Judge. Watch her statements. They won't wait for you."
    eiki "A crowd, a headline, a photograph. None of them is a verdict. Ask what each one leaves out."

    ## Part one.
    window hide
    call shot_aya
    $ bgm("aya")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("What the Defendants Say"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    aya_t "Aya Shameimaru, Bunbunmaru News. Fastest reporter in Gensokyo. I've covered every case in this court."
    aya_t "I interviewed seven of your defendants. Every one of them says this court is unfair."
    aya_t "Seven defendants can't all be wrong. The Higan Court is unfair."

    hide screen court_tag
    jump case11_cross


label case11_cross:

    call shot_aya
    $ bgm("aya")
    call cross_examination("testimony_aya_first")

    if _return == "mistrial":
        call mistrial
        call shot_bench(Dissolve(0.5))
        komachi "Deep breath, Junior Judge. She talks fast. You don't have to."
        jump case11_cross

    $ sfx("breakthrough")
    with flash
    you "How many defendants complain doesn't make a verdict unfair. And every one you asked was found guilty."
    call shot_bench
    komachi "Bandwagon. Sustained. ...I've always wanted to say that."

    call shot_aya
    $ react("aya", "nervous")
    aya "Fine! Forget the interviews. I have something better. The verdicts themselves."
    aya "Front page. Printed and everything. I just need a moment to fetch it."
    call shot_bench
    komachi "Court will take a short recess!"
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    hide gavel

    jump case11_recess


## The recess: Komachi investigates while Aya fetches her paper.
default aya_seen_office = False
default aya_seen_archive = False

label case11_recess:

    $ bgm_stop(1.0)
    window hide
    scene black
    show screen court_title(_("RECESS"), "休廷", _("The Scoop"))
    with Dissolve(0.4)
    pause 1.4
    hide screen court_title
    call shot_bench(Dissolve(0.5))
    window auto

    eiki "A defendant may not investigate her own case, Junior Judge. But a bailiff may run errands."
    komachi "Where to, Junior Judge? I'm fast when I want to be. I almost never want to be."

    $ aya_seen_office = False
    $ aya_seen_archive = False

label case11_recess_menu:

    menu:
        "The Bunbunmaru office" if not aya_seen_office:
            $ aya_seen_office = True
            komachi "Back. Her desk is a mess. But look: her film roll."
            $ add_evidence("film_roll")
            komachi "Thirty-six photos on this roll, Junior Judge. She printed seven."
            komachi "And this was in her props cupboard."
            $ add_evidence("mistress_parasol")
            eiki "The mistress's parasol. Case 06 is not as closed as I thought."

        "The court archive" if not aya_seen_archive:
            $ aya_seen_archive = True
            komachi "Got it. The boss's docket. Every verdict, in her handwriting."
            $ add_evidence("court_docket")
            eiki "All of them. Including the ones that don't photograph well."

        "Ask Aya for a comment":
            call shot_aya
            aya "No comment! ...Okay, one comment. The photo never lies."
            call shot_bench

    if not (aya_seen_office and aya_seen_archive):
        jump case11_recess_menu

    komachi "She's back, Junior Judge. With a newspaper the size of a door."

    ## Part two.
    window hide
    call shot_aya
    $ bgm("aya")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Photo Never Lies"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    aya_t "Here are this court's verdicts, as printed in today's Bunbunmaru."
    aya_t "Cirno, Marisa, Reisen, Meiling, Alice, Reimu, Kaguya: guilty, every one. This court convicts everyone!"
    aya_t "The photo never lies. Every verdict I printed is real."

    hide screen court_tag
    call shot_bench
    komachi "Your witness, Junior Judge. Slower this time, at least."

    jump case11_cross2


label case11_cross2:

    call shot_aya
    $ bgm_pursuit()
    call cross_examination("testimony_aya")

    if _return == "mistrial":
        call mistrial
        call shot_bench(Dissolve(0.5))
        komachi "Again, Junior Judge. Her headline isn't going anywhere."
        jump case11_cross2

    jump case11_breakthrough


label case11_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Your headline prints seven guilty verdicts. This docket has ten cases. You left out every acquittal."
    you "Meiling, not guilty. Mokou, not guilty. Your film roll has their photos. You just didn't print them."

    call breakdown("aya")
    aya "...They weren't exciting! Nobody buys a paper that says \"Court Mostly Fair\"!"

    call shot_bench
    komachi "Cherry picking, Junior Judge. Pick the ripe ones, hide the rest."
    eiki "A handful of true facts, chosen to tell a false story. That is still a lie, Miss Shameimaru."

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    you "In the matter of Bunbunmaru News against the Higan Court, this court finds the defendant..."
    hide gavel

    window hide
    show screen verdict_stamp(_("NOT GUILTY"), "無罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Thank you, Junior Judge. And now, a separate matter. Komachi, the parasol."
    komachi "From her props cupboard, boss."

    call shot_aya
    $ react("aya", "shock")
    aya "Borrowed! For a photo shoot! I left a note!"
    call shot_bench
    eiki "Signed \"A.S.\" I remember. Case 06 is reopened. Bailiff."
    komachi "On it, boss."

    ## She's the fastest in Gensokyo. The bailiff never stood a chance.
    window hide
    call shot_aya
    $ sfx("yeet")
    hide aya_fumo
    show fumo_shadow at shadow_gone
    with Dissolve(0.08)
    pause 0.3
    $ sfx("ui_confirm")
    with flash
    window auto
    komachi "...She's gone, boss. Before I even swung."
    aya "Got the shot! \"Bailiff Misses!\" Front page tomorrow!"

    window hide
    $ sfx("break_sakuya")
    with flash
    call shot_sakuya
    window auto
    sakuya "I'll take the parasol, thank you. And the tengu. She's in my other hand."
    aya "How did she— I'm the fastest in—"
    sakuya "You are. I simply don't use time the way you do."

    window hide
    hide sakuya_fumo
    show fumo_shadow at shadow_gone
    with flash
    pause 0.4

    call shot_eiki
    window auto
    komachi "...She does that."
    eiki "Eleven cases, Junior Judge."
    eiki "You caught every fallacy on this docket. And twice, you found the truth behind a bad argument."
    eiki "Junior Judge. Your work was... more than acceptable."
    komachi "She's never said that before. Not once."
    eiki "Komachi."
    komachi "Escorting myself out."
    eiki "Court is adjourned."

    $ bgm_stop(2.0)
    call close_case("case11", fallacy_cherry_picking)
    return
