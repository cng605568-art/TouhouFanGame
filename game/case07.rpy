################################################################################
## case07.rpy - Case 07: Strings Attached. Witness: Alice Margatroid.
## Straw man: Alice answers an insult Marisa never made.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_newest_doll = Evidence("newest_doll", _("Alice's Newest Doll"),
    _("Hand-stitched over three months. Beautiful. One button still missing."), "gui/ev_doll.svg")
define evidence_doll_string = Evidence("doll_string", _("Doll String"),
    _("Six metres, enchanted. Found knotted around a tree, very, very tightly."), "gui/ev_thread.svg")
define evidence_bunbunmaru_clipping = Evidence("bunbunmaru_clipping", _("Bunbunmaru Clipping"),
    _("Yesterday's quote: \"Alice's dolls are really good. They just take forever to make.\" —M. Kirisame"), "gui/ev_newspaper.svg")

## First round: Alice attacks the speaker instead of the comment.
define testimony_alice_first = Testimony(
    title=_("The Puppeteer's Pride"),
    witness="alice",
    judge="eiki",
    witness_shot="shot_alice",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("Yesterday Marisa came to my house. Uninvited, as always."),
            "press_alice_1",
            _("Uninvited, yes. Illogical, no. Keep looking.")),
        Statement(
            _("She looked at my newest doll and made a comment about it."),
            "press_alice_2",
            _("A comment is a fact. What she makes of it is the question.")),
        Statement(
            _("Marisa steals books and lies about borrowing them. Nothing she says about my dolls can be trusted."),
            "press_alice_thief",
            None),
        ],
    cards=[ fallacy_ad_hominem, fallacy_straw_man, fallacy_tu_quoque ],
    flaw=2,
    answer="ad_hominem",
    scolds={
        "straw_man" : _("Not yet. She hasn't quoted Marisa at all. She's dismissing the speaker."),
        "tu_quoque" : _("She isn't saying Marisa does it too. She's saying Marisa doesn't count, because of who Marisa is."),
        "hasty_generalization" : _("No rule built from one example. Just a comment thrown out because of who made it."),
        "false_cause" : _("Nothing is mistaken for a cause. She's judging the speaker instead of the words."),
        },
    after_wrong="alice_doll_heckle")

## Second round: told to quote Marisa exactly, Alice misquotes her.
define testimony_alice = Testimony(
    title=_("Word for Word"),
    witness="alice",
    judge="eiki",
    witness_shot="shot_alice",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("Fine. My counsel insists I quote Marisa exactly. So I will."),
            "press_alice_exact",
            _("Quoting is allowed. Misquoting is the question. Read on.")),
        Statement(
            _("She called my dolls worthless junk and said I should quit. So she deserved the string."),
            "press_alice_4",
            None),
        Statement(
            _("So I defended my life's work. Anyone would have."),
            "press_alice_3",
            _("Defending your work isn't a fallacy. What she says she defended it from is.")),
        ],
    cards=[ fallacy_ad_hominem, fallacy_straw_man, fallacy_tu_quoque ],
    flaw=1,
    answer="straw_man",
    scolds={
        "ad_hominem" : _("Close cousin. But she isn't attacking Marisa's character. She's attacking words Marisa never said."),
        "tu_quoque" : _("She isn't saying \"you do it too.\" She's rewriting what Marisa said."),
        "slippery_slope" : _("No chain of disasters predicted. Just a quote, quietly rewritten."),
        "false_cause" : _("Order isn't the issue. The issue is whether Marisa said that at all."),
        "hasty_generalization" : _("She isn't generalising from one example. She's replacing the real comment with a crueller one."),
        "false_dilemma" : _("No either-or. Just a comment that grew teeth between Marisa's mouth and this court."),
        "appeal_to_authority" : _("No famous name cited. Just a quote, misquoted."),
        "circular_reasoning" : _("Her reason isn't her conclusion. Her reason is a quote nobody said."),
        },
    proof="bunbunmaru_clipping",
    proof_wrong=_("That doesn't tell us what Marisa actually said. Find her real words."),
    after_wrong="alice_doll_heckle")

## The doll lawyer can't speak, so Alice passes on its remarks.
define DOLL_HECKLES = [
    _("My counsel says that was embarrassing."),
    _("My counsel is laughing. Silently."),
    _("My counsel would like that struck from the record. And from your memory."),
    _("My counsel asks whether the Junior Judge is new. ...She is? That explains it."),
    ]

label alice_doll_heckle:
    call shot_alice
    $ react("alice", "smug")
    $ heckle = renpy.random.choice(DOLL_HECKLES)
    alice "[heckle!t]"
    return


label press_alice_1:
    you "How did she get in?"
    alice "Through the window. She has never once used a door."
    call shot_eiki
    eiki "A pattern is emerging."
    return

label press_alice_2:
    you "What was the comment, exactly?"
    $ react("alice", "angry")
    alice "Something rude. The details don't matter."
    call shot_eiki
    eiki "The details are the entire case."
    return

label press_alice_thief:
    you "What does her borrowing have to do with your dolls?"
    $ react("alice", "smug")
    alice "Everything. A thief's opinion is worthless."
    call shot_eiki
    eiki "A thief can still be right about a doll."
    return

label press_alice_exact:
    you "Exactly? Word for word?"
    alice "I have a perfect memory for insults. Every puppeteer does."
    return

label press_alice_3:
    you "Defended it from what?"
    alice "From her insult, obviously. I just told you what she said."
    return

label press_alice_4:
    you "Are those her exact words? \"Worthless junk\"?"
    $ react("alice", "nervous")
    alice "Close enough. It's what she meant. I could tell by her face."
    call shot_eiki
    eiki "A face is not a quote."
    return


label case7:

    call open_case("case7")

    komachi "Defendant's here, boss. She brought a lawyer."
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "This court does not allow—"
    komachi "It's a doll, boss. It's very quiet."

    call shot_alice
    alice "Alice Margatroid, puppeteer of the Forest of Magic. I'll be brief. I had every right."

    call shot_eiki
    eiki "The charge: tying Kirisame Marisa to a tree with doll string. For six hours."

    call shot_alice
    $ react("alice", "smug")
    alice "Seven. She wriggled."

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. Before you weigh an argument, make sure it is the one actually made."
    eiki "Anyone can knock down a scarecrow. Check that it isn't one."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_alice
    $ bgm("alice")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Puppeteer's Pride"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    alice_t "Yesterday Marisa came to my house. Uninvited, as always."
    alice_t "She looked at my newest doll and made a comment about it."
    alice_t "Marisa steals books and lies about borrowing them. Nothing she says about my dolls can be trusted."

    hide screen court_tag
    call shot_eiki
    eiki "The floor is yours, Junior Judge. Mind the strings."

    jump case7_cross


label case7_cross:

    call shot_alice
    $ bgm("alice")
    call cross_examination("testimony_alice_first")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. And Komachi, give the lawyer back."
        jump case7_cross

    ## The first objection lands, and the doll lawyer intervenes.
    $ sfx("breakthrough")
    with flash
    you "Marisa's habits don't decide whether her comment was fair. That's an attack on the speaker."
    call shot_eiki
    eiki "Ad hominem. A thief can still be right about a doll. Sustained."

    call shot_alice
    show screen court_shout("objection")
    with vpunch
    pause 0.8
    hide screen court_shout
    with Dissolve(0.12)
    $ react("alice", "nervous")
    alice "...My counsel objects. To me."
    alice "She says I should stop talking about Marisa, and quote Marisa instead."
    call shot_eiki
    eiki "Your counsel is wiser than you. A second testimony, then. Word for word."

    window hide
    call shot_alice
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("Word for Word"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    alice_t "Fine. My counsel insists I quote Marisa exactly. So I will."
    alice_t "She called my dolls worthless junk and said I should quit. So she deserved the string."
    alice_t "So I defended my life's work. Anyone would have."

    hide screen court_tag
    jump case7_cross2


label case7_cross2:

    call shot_alice
    $ bgm_pursuit()
    call cross_examination("testimony_alice")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. Her second story, from the top."
        jump case7_cross2

    jump case7_breakthrough


label case7_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Marisa never called your dolls junk. She said they're really good, and take forever to make."
    you "You argued against the insult you imagined, not the comment she made."

    call breakdown("alice")
    alice "...She said they were really good? In the newspaper? In print?"

    call shot_eiki
    camera at eiki_lecture
    eiki "A straw man. Rebuild someone's words into something weaker, then knock that down instead."
    eiki "Answer what was said. Not what you wish had been said."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Alice Margatroid. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: untie Marisa. Then apologise. In person."

    call shot_alice
    alice "...She's still tied to the tree?"

    call shot_eiki
    komachi "Since yesterday, boss. She asked me to bring snacks."
    eiki "Then bring snacks. And escort the defendant to the tree. Bailiff."
    komachi "On it, boss."

    window hide
    call shot_alice
    show alice_fumo at fumo_yeet_caught
    show fumo_shadow at shadow_gone
    $ sfx("yeet")
    pause 2.2
    hide alice_fumo

    call shot_eiki
    window auto
    komachi "...Her dolls caught her, boss. They're carrying her out. Gently."
    eiki "Show-off."
    eiki "Court is adjourned. Someone take that magician a sandwich."
    komachi "Already packed two, boss. One's for me."

    call close_case("case7", fallacy_straw_man)
    return
