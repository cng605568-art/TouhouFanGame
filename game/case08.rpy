################################################################################
## case08.rpy - Case 08: Fifty Satisfied Customers. Witness: Reimu Hakurei.
## Bandwagon. The donation box from Case 02 is finally full, for all the
## wrong reasons.
################################################################################

## Runs after script.rpy, which defines the cast and the fallacy cards.
init offset = 1

define evidence_lucky_charm = Evidence("lucky_charm", _("Hakurei Lucky Charm"),
    _("A red pouch. Inside, a slip of paper with one word on it: \"luck.\""), "gui/ev_charm.svg")
define evidence_full_donation_box = Evidence("full_donation_box", _("Donation Box (Full)"),
    _("Heavy, for once. Five thousand yen and a button."), "gui/ev_box.svg")
define evidence_complaint_list = Evidence("complaint_list", _("Village Complaint List"),
    _("Charm owners this week: 12 tripped, 9 rained on, 3 bitten by fairies. Lucky: none."), "gui/ev_list.svg")

image donation_box_prop = "gui/ev_box.svg"

define testimony_reimu = Testimony(
    title=_("Fifty Satisfied Customers"),
    witness="reimu",
    judge="eiki",
    witness_shot="shot_reimu",
    judge_shot="shot_eiki",
    statements=[
        Statement(
            _("Last week I started selling Hakurei Lucky Charms. One hundred yen each."),
            "press_reimu_1",
            _("A price list is not an argument. Though it is an expensive one."),
            reveals="crowd"),
        Statement(
            _("Fifty people bought one. Fifty people can't all be wrong."),
            "press_reimu_4",
            None,
            hidden=True, key="crowd"),
        Statement(
            _("Fifty villagers have bought one already. The rest are on a waiting list."),
            "press_reimu_2",
            _("Sales are a fact. Look for what she concludes from them.")),
        Statement(
            _("So there's no question about it. The charms work."),
            "press_reimu_3",
            _("That's her conclusion. Object to the reason she gives for it."),
            reveals="advert"),
        Statement(
            _("The Bunbunmaru even ran an advert for them. I paid that tengu five hundred yen."),
            "press_reimu_advert",
            _("An advert is a fact, not an argument. Though it tells us who has been watching this court."),
            hidden=True, key="advert"),
        ],
    cards=[ fallacy_appeal_to_authority, fallacy_bandwagon, fallacy_hasty_generalization ],
    flaw=1,
    answer="bandwagon",
    scolds={
        "appeal_to_authority" : _("Close. But she isn't leaning on one expert. She's leaning on a crowd."),
        "hasty_generalization" : _("That would be one example turned into a rule. She has fifty examples of buying, and none of testing."),
        "false_cause" : _("She isn't mixing up order and cause. She's counting customers as if they were results."),
        "ad_hominem" : _("She isn't attacking anyone. She's hiding behind a headcount."),
        "tu_quoque" : _("Nobody's being blamed in return. The crowd itself is her argument."),
        "slippery_slope" : _("No chain of disasters. Just fifty people and one bad conclusion."),
        "false_dilemma" : _("No either-or here. Just a popularity contest pretending to be proof."),
        "circular_reasoning" : _("Her reason isn't her conclusion. Her reason is the size of the queue."),
        "straw_man" : _("She isn't twisting anyone's words. She's counting heads instead of results."),
        },
    proof_kind="pair",
    proof_data=dict(
        items=("full_donation_box", "complaint_list"),
        wrong=_("Show what the crowd bought, and what happened to the crowd. Both.")),
    gimmick="bribe",
    bribe_label="reimu_bribe")


label reimu_bribe:
    call shot_reimu
    $ react("reimu", "smug")
    reimu "Smart judge. That one's on the house. Stay lucky."
    call shot_eiki
    $ react("eiki", "angry")
    eiki "...I saw that, Junior Judge. This court remembers."
    return

label press_reimu_1:
    you "What exactly do the charms do?"
    reimu "Luck. General luck. All-purpose, everyday luck."
    call shot_eiki
    eiki "That is not a specification."
    call shot_reimu
    reimu "It's the best-selling charm in Gensokyo. Put that in my testimony."
    return

label press_reimu_2:
    you "Fifty? Who's counting?"
    $ react("reimu", "smug")
    reimu "The donation box. It has never been this heavy."
    return

label press_reimu_3:
    you "How do you know they work?"
    reimu "Weren't you listening? Fifty customers! And it was in the paper. Write that down too."
    return

label press_reimu_advert:
    you "You advertised in the Bunbunmaru?"
    reimu "That tengu wouldn't stop following me. Taking pictures. Asking about my donation box."
    call shot_eiki
    eiki "That tengu has been following a great many of our defendants."
    return

label press_reimu_4:
    you "Did anyone check whether the charm owners actually got luckier?"
    $ react("reimu", "nervous")
    reimu "Why would I check? Fifty people already checked. By paying."
    call shot_eiki
    eiki "Paying is not checking."
    return


label case8:

    call open_case("case8")

    komachi "Boss! Lucky charms, one hundred yen. Want one?"
    eiki "Komachi. Where did you get those?"
    komachi "The defendant. She's selling them in the waiting room."
    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Confiscate them. Court is in session."
    hide gavel
    komachi "Bought three. Is my luck supposed to feel this ordinary?"

    call shot_reimu
    reimu "Reimu Hakurei, shrine maiden. Make it quick. The donation box doesn't fill itself."

    call shot_eiki
    eiki "The charge: selling lucky charms that do not work to half the Human Village."

    call shot_reimu
    reimu "They work. Ask anyone. Ask everyone."

    call shot_eiki
    camera at eiki_lecture
    eiki "Junior Judge. A crowd can be loud. That does not make it right."
    eiki "Count the votes if you like. Then go and check the facts anyway."
    eiki "And whatever she offers you on the stand, Junior Judge, do not take it."
    camera
    with Dissolve(0.4)

    ## Testimony.
    window hide
    call shot_reimu
    $ bgm("reimu")
    show screen court_title(_("WITNESS TESTIMONY"), "証言", _("Fifty Satisfied Customers"))
    with Dissolve(0.2)
    pause 1.6
    hide screen court_title
    show screen court_tag(_("TESTIMONY"))
    with Dissolve(0.2)
    window auto

    reimu_t "Last week I started selling Hakurei Lucky Charms. One hundred yen each."
    reimu_t "Fifty villagers have bought one already. The rest are on a waiting list."
    reimu_t "So there's no question about it. The charms work."

    hide screen court_tag
    call shot_eiki
    eiki "Your witness, Junior Judge. Keep your wallet in your pocket."

    jump case8_cross


label case8_cross:

    call shot_reimu
    $ bgm("reimu")
    call cross_examination("testimony_reimu")

    if _return == "mistrial":
        call mistrial
        call shot_eiki(Dissolve(0.5))
        eiki "Again. Komachi, stop buying charms."
        jump case8_cross

    jump case8_breakthrough


label case8_breakthrough:

    $ bgm_stop(0.15)
    $ sfx("breakthrough")
    with flash
    you "Five thousand yen in the box: fifty charms sold. And this list: not one owner got any luckier."
    you "A crowd buying something proves it sells. It doesn't prove it works."

    call breakdown("reimu")
    reimu "...Twelve tripped? Nine got rained on? ...Do I have to give the money back?"

    call shot_eiki
    camera at eiki_lecture
    eiki "Bandwagon. An appeal to popularity. A crowd of believers does not make a claim true."
    eiki "Everyone once agreed the earth was flat. The earth did not take a vote."
    camera
    with Dissolve(0.4)

    show gavel at gavel_slam
    $ sfx("gavel")
    with vpunch
    eiki "Defendant Reimu Hakurei. This court finds you..."
    hide gavel

    window hide
    show screen verdict_stamp(_("GUILTY"), "有罪")
    with vpunch
    pause 1.4
    hide screen verdict_stamp
    with Dissolve(0.25)
    window auto

    eiki "Sentence: refund every charm. From the donation box."

    call shot_reimu
    reimu "The donation box?! That's the cruellest sentence this court has ever passed."

    call shot_eiki
    komachi "Can I keep mine, boss? I've grown attached."
    eiki "Bailiff."
    komachi "On it, boss."

    window hide
    call shot_reimu
    show reimu_fumo at fumo_hover
    pause 0.9
    window auto
    reimu "Nice try. Shrine maiden. I fly."
    komachi "...She flies, boss."
    call shot_eiki
    eiki "Then throw the donation box."
    call shot_reimu
    $ react("reimu", "shock")
    reimu "You wouldn't."

    window hide
    show donation_box_prop at item_yeet
    $ sfx("yeet")
    pause 0.5
    show reimu_fumo at fumo_yeet
    show fumo_shadow at shadow_gone
    pause 1.15
    hide reimu_fumo
    hide donation_box_prop

    call shot_eiki
    window auto
    komachi "She dived after it, boss. Didn't even hesitate."
    eiki "The shrine maiden of paradise, on a refund schedule. Court is adjourned."
    komachi "A first for the Hakurei Shrine, boss. Money going out."

    call close_case("case8", fallacy_bandwagon)
    return
