################################################################################
## case02.rpy - Case 02: The Long-Term Loan. Witness: Marisa. Tu quoque.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_library_ledger = Evidence("library_ledger", _("Library Ledger"),
    _("Forty-seven grimoires signed out to \"M. Kirisame.\" None returned."), "gui/ev_book.svg")
define evidence_donation_box = Evidence("donation_box", _("Shrine Donation Box"),
    _("Nearly empty. Contents: one leaf, one button."), "gui/ev_box.svg")
define evidence_reading_glasses = Evidence("reading_glasses", _("Patchouli's Spare Glasses"),
    _("Dusty. Found under a stack of unread books."), "gui/ev_glasses.svg")

define testimony_marisa = Testimony(
    title=_("The Forty-Seven Grimoires"),
    witness="marisa",
    judge="eiki",
    witness_shot="shot_marisa",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("I borrowed those books. I'll give 'em back when I die. That's a promise."),
            "press_marisa_1",
            _("A terrible promise is still a promise. Rude, yes. Illogical, no.")),
        Statement(
            _("Patchouli hasn't opened most of 'em in a hundred years. I checked the dust."),
            "press_marisa_2",
            _("Dust is evidence. Annoyingly good evidence. The bad step is somewhere else.")),
        Statement(
            _("And honestly? I'm not the only one around here with sticky fingers."),
            "press_marisa_3",
            _("That's a hint, not an argument. Press her and make her say it."),
            reveals="reimu"),
        Statement(
            _("Reimu pockets her own donation box! So who's the real thief here? Not me."),
            "press_marisa_4",
            None,
            hidden=True, key="reimu"),
        ],
    cards=[ fallacy_ad_hominem, fallacy_tu_quoque, fallacy_slippery_slope ],
    flaw=3,
    answer="tu_quoque",
    scolds={
        "ad_hominem" : _("Close. But she isn't insulting her accuser. She's hiding behind someone else's sins. There's a sharper name for that."),
        "slippery_slope" : _("Slippery Slope needs a chain of disasters. She predicted nothing. She just pointed at Reimu."),
        "false_cause" : _("Nobody is mistaking order for cause. She is pointing at Reimu to excuse herself."),
        },
    proof="library_ledger",
    proof_wrong=_("That has nothing to do with the forty-seven books. Show what she actually took."))


label press_marisa_1:
    you "And when exactly do you plan to die?"
    $ react("marisa", "smug")
    marisa "Not anytime soon. That's the beauty of it."
    call shot_eiki
    eiki "A loan with no due date. I will be writing to the Ministry."
    return

label press_marisa_2:
    you "You inspected the dust personally?"
    marisa "Wiped it off with my sleeve. Didn't want to steal the dust. That'd be wrong."
    return

label press_marisa_3:
    you "Not the only one? Who else?"
    marisa "Oh, nobody. Just a certain shrine maiden. With a certain donation box."
    marisa "You know what? Put it in the testimony."
    return

label press_marisa_4:
    you "What does Reimu's donation box have to do with your books?"
    $ react("marisa", "nervous")
    marisa "Everything! If the shrine maiden does it, it can't be that bad, right?"
    call shot_eiki
    eiki "Reimu's ledger is Reimu's problem. Yours is forty-seven books long."
    return


label case2:

    call open_case("case2")

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Order. The Higan Court of Logic is in session."
    hide gavel
    eiki "Komachi. The defendant?"
    komachi "Came in through the window, boss."
    eiki "We have a door."
    komachi "I mentioned that. She said doors are for people with time to spare."

    call shot_marisa
    marisa "Kirisame Marisa, ordinary magician. Let's keep this quick. I've got reading to do."

    call shot_eiki
    eiki "The charge: removal of forty-seven grimoires from the Scarlet Devil library."

    call shot_marisa
    $ react("marisa", "smug")
    marisa "Removal's a strong word. I prefer \"long-term borrowing.\""

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. Today's defendant won't deny what she did."
    eiki "So listen for the excuse instead. Excuses love to dress up as reasons."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_marisa
    $ bgm("marisa")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("The Forty-Seven Grimoires"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    marisa_t "I borrowed those books. I'll give 'em back when I die. That's a promise."
    marisa_t "Patchouli hasn't opened most of 'em in a hundred years. I checked the dust."
    marisa_t "And honestly? I'm not the only one around here with sticky fingers."

    hide screen court_tag
    call shot_eiki
    eiki "Your witness, Junior Judge. [spirit_Word!t] magatama of spirit, as always."

    jump case2_cross


label case2_cross:

    call shot_marisa
    $ bgm("marisa")
    call cross_examination("testimony_marisa")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. She'll still be here. Unfortunately."
        jump case2_cross

    jump case2_breakthrough


label case2_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Reimu's donation box isn't on trial today. Your forty-seven books are."
    you "Even if she's guilty, that doesn't return a single grimoire."

    call breakdown("marisa")
    marisa "Hey! I was making a comparison! A really convincing one!"

    call shot_eiki
    camera at eiki_lecture
    eiki "Tu quoque. \"You too.\""
    eiki "Another's wrongdoing does not make yours right. It only makes two."
    eiki "Two thieves do not add up to zero thieves."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Kirisame Marisa. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: return all forty-seven books. Alphabetised. While Patchouli watches."

    call shot_marisa
    marisa "Can I borrow a pen to sign that?"

    call shot_eiki
    eiki "Bailiff."
    komachi "On it, boss."

    window hide
    call shot_marisa
    show marisa_fumo at fumo_yeet
    show fumo_shadow at shadow_gone
    $ sfx("yeet")
    pause 1.15
    hide marisa_fumo

    call shot_eiki
    window auto
    eiki "...Through the window."
    komachi "She seemed to prefer it."
    eiki "Court is adjourned."

    call close_case("case2", fallacy_tu_quoque)
    return
