################################################################################
## court.rpy - the cross-examination engine.
##
##   1. Data: Statement, Fallacy, Evidence, Testimony
##   2. Difficulty, spirit, ranks and the fallacy deck
##   3. The Court Record
##   4. Engine labels: cross_examination, prove_it, court_shout,
##      court_penalty, mistrial
##
## A cross-examination runs until the player objects to the flawed statement
## with the right fallacy (and, above Easy, presents the evidence that proves
## it), or runs out of spirit. Some statements are hidden until the player
## presses the statement that leads to them.
################################################################################

init offset = -1


################################################################################
## 1. Data
################################################################################

init -1 python:

    class Statement(object):
        """
        One line of testimony.

        `text`     what the witness says.
        `press`    label played when the player presses this statement.
        `wrong`    the judge's scolding for objecting to it when it isn't
                   the flawed statement.
        `hidden`   True if it only appears once revealed.
        `key`      name of a hidden statement.
        `reveals`  key of the hidden statement that pressing this one adds.
        """

        def __init__(self, text, press, wrong, hidden=False, key=None, reveals=None):
            self.text = text
            self.press = press
            self.wrong = wrong
            self.hidden = hidden
            self.key = key
            self.reveals = reveals


    class Fallacy(object):
        """A logical fallacy card. `tip` is the Compendium's how-to-spot-it."""

        def __init__(self, key, name, alias, blurb, icon, tip=""):
            self.key = key
            self.name = name
            self.alias = alias
            self.blurb = blurb
            self.icon = icon
            self.tip = tip


    class Evidence(object):
        """An item in the Court Record."""

        def __init__(self, key, name, desc, icon):
            self.key = key
            self.name = name
            self.desc = desc
            self.icon = icon


    class Testimony(object):
        """
        Everything the cross-examination engine needs for one witness.

        Characters and shots are stored by name so save files stay small and
        survive edits to the script.

        `flaw`     index in `statements` of the one that contains the fallacy.
        `answer`   key of the correct Fallacy.
        `cards`    the three cards offered on Easy; harder levels show every
                   fallacy met so far (see deck_for).
        `scolds`   {fallacy key: line} for the right statement with the wrong
                   fallacy.
        `proof`    key of the Evidence that proves the objection.
        `proof_wrong`  the judge's line for presenting anything else.
        """

        def __init__(self, title, witness, judge, witness_shot, judge_shot,
                     statements, cards, flaw, answer, scolds,
                     proof=None, proof_wrong=None):
            self.title = title
            self.witness = witness
            self.judge = judge
            self.witness_shot = witness_shot
            self.judge_shot = judge_shot
            self.statements = statements
            self.cards = cards
            self.flaw = flaw
            self.answer = answer
            self.scolds = scolds
            self.proof = proof
            self.proof_wrong = proof_wrong

        @property
        def witness_character(self):
            return getattr(store, self.witness)

        @property
        def judge_character(self):
            return getattr(store, self.judge)

        def visible(self, revealed):
            """Indices of the statements on show, given the revealed keys."""
            return [ i for i, s in enumerate(self.statements)
                     if not s.hidden or s.key in revealed ]


    def testimony(name):
        return getattr(store, name)

    def fallacy(key):
        return getattr(store, "fallacy_" + key)

    def evidence(key):
        return getattr(store, "evidence_" + key)


################################################################################
## 2. Difficulty, spirit, ranks and the deck
################################################################################

init -1 python:

    # Touhou's four difficulties. `timer` is seconds to pick a card (None:
    # no limit); `proof` is whether a correct objection must be backed with
    # evidence; `deck` is "hand" (the case's three cards), "met" (every
    # fallacy met so far) or "all".
    DIFFICULTY = {
        "easy":    dict(name=_("Easy"),    spirit=7, timer=None, proof=False, deck="hand",
                        blurb=_("Seven magatama. Three cards. No evidence needed.")),
        "normal":  dict(name=_("Normal"),  spirit=5, timer=None, proof=True,  deck="met",
                        blurb=_("Five magatama. Every fallacy you've met. Prove each objection.")),
        "hard":    dict(name=_("Hard"),    spirit=4, timer=30,   proof=True,  deck="met",
                        blurb=_("Four magatama and thirty seconds to choose.")),
        "lunatic": dict(name=_("Lunatic"), spirit=3, timer=15,   proof=True,  deck="all",
                        blurb=_("Three magatama, fifteen seconds, and every card from the start.")),
        }
    DIFFICULTY_ORDER = [ "easy", "normal", "hard", "lunatic" ]

    # Canonical order of the cards, so they always sit in the same places.
    FALLACY_ORDER = [ "false_cause", "ad_hominem", "slippery_slope", "tu_quoque",
                      "false_dilemma", "appeal_to_authority", "circular_reasoning" ]

    RANKS = [ "S", "A", "B", "C" ]

    def diff():
        return DIFFICULTY[store.difficulty]

    def spirit_lose():
        store.spirit = max(0, store.spirit - 1)
        store.spirit_broken = store.spirit
        store.case_penalties += 1

    # Spirit counts in words, for Eiki's lines ("[spirit_word!t] magatama").
    SPIRIT_WORDS = {3: (_("three"), _("Three")), 4: (_("four"), _("Four")),
                    5: (_("five"), _("Five")), 7: (_("seven"), _("Seven"))}

    def spirit_reset():
        store.spirit_cap = diff()["spirit"]
        store.spirit_word, store.spirit_Word = SPIRIT_WORDS.get(store.spirit_cap, (str(store.spirit_cap),) * 2)
        store.spirit = store.spirit_cap
        store.spirit_broken = -1

    def deck_for(tm):
        """The fallacy cards offered for this testimony at this difficulty."""
        mode = diff()["deck"]
        if mode == "hand":
            return list(tm.cards)
        if mode == "all":
            keys = set(k for k in FALLACY_ORDER if hasattr(store, "fallacy_" + k))
        else:
            keys = set()
            for case in CASES:
                case_tm = testimony(case.testimony)
                keys.update(c.key for c in case_tm.cards)
                if case_tm is tm:
                    break
        return [ fallacy(k) for k in FALLACY_ORDER if k in keys ]

    def case_rank():
        """S for a clean case, then A, B, C; a mistrial caps it at C."""
        if store.case_mistrial:
            return "C"
        return RANKS[min(store.case_penalties, 3)]

    def record_rank(key, rank):
        slot = "%s:%s" % (key, store.difficulty)
        old = persistent.best_ranks.get(slot)
        if old is None or RANKS.index(rank) < RANKS.index(old):
            persistent.best_ranks[slot] = rank

    def best_rank(key):
        """(rank, difficulty key) of the best clear of a case, or None."""
        best = None
        for d in reversed(DIFFICULTY_ORDER):
            r = persistent.best_ranks.get("%s:%s" % (key, d))
            if r is not None and (best is None or RANKS.index(r) < RANKS.index(best[0])):
                best = (r, d)
        return best


default difficulty = "normal"
default persistent.difficulty = "normal"
default persistent.best_ranks = { }
default persistent.fallacies_learned = set()

default spirit_word = "five"
default spirit_Word = "Five"
default spirit_cap = 5
default spirit = 5
default spirit_broken = -1
default case_penalties = 0
default case_mistrial = False
default case_number = ""
default case_title = ""

default xexam_index = 0
default xexam_act = None
default xexam_pick = None
default xexam_line = ""
default xexam_stmt = 0
default xexam_revealed = set()
default xexam_vis = [ ]


################################################################################
## 3. The Court Record
################################################################################

default court_record = [ ]

init -1 python:

    def add_evidence(key, announce=True):
        """Adds an item to the Court Record, with a short card unless told not to."""
        if key in store.court_record:
            return
        store.court_record.append(key)
        if announce:
            sfx("ui_confirm")
            renpy.show_screen("evidence_added", evidence(key))


################################################################################
## 4. Engine labels
################################################################################

## Runs a cross-examination. Returns "solved" or "mistrial".
label cross_examination(tm_name):

    $ tm = testimony(tm_name)
    $ xexam_revealed = set()
    $ xexam_index = 0

    window hide
    show screen court_title(_("CROSS-EXAMINATION"), "反対尋問", tm.title)
    with Dissolve(0.2)
    pause 1.5
    hide screen court_title
    with Dissolve(0.2)
    window auto

    while True:

        $ xexam_vis = tm.visible(xexam_revealed)
        $ xexam_index = min(xexam_index, len(xexam_vis) - 1)
        call screen cross_exam(tm_name)
        $ xexam_act, xexam_index = _return
        $ xexam_stmt = xexam_vis[xexam_index]

        if xexam_act == "press":

            call court_shout("hold")
            call expression tm.statements[xexam_stmt].press
            $ xexam_new = tm.statements[xexam_stmt].reveals

            if xexam_new and xexam_new not in xexam_revealed:
                $ xexam_revealed.add(xexam_new)
                call expression tm.witness_shot
                $ bgm("pursuit", fadein=0.2, card_delay=1.7, fadeout=0.3)
                call testimony_updated(tm.title)
                $ xexam_vis = tm.visible(xexam_revealed)
                $ xexam_index = [ tm.statements[i].key for i in xexam_vis ].index(xexam_new)
            else:
                $ xexam_index = (xexam_index + 1) % len(xexam_vis)
                call expression tm.witness_shot

        elif xexam_act == "object":

            call screen fallacy_pick(tm_name, xexam_stmt)
            $ xexam_pick = _return

            if xexam_pick is None:
                pass

            elif xexam_pick == "timeout":
                call court_penalty(tm_name, _("Time's up. This court does not wait for the undecided."))

            else:
                call court_shout("objection")

                if xexam_stmt == tm.flaw and xexam_pick == tm.answer:

                    if not (diff()["proof"] and tm.proof):
                        return "solved"

                    call prove_it(tm_name)
                    if _return == "proved":
                        return "solved"

                elif xexam_stmt != tm.flaw:
                    call court_penalty(tm_name, tm.statements[xexam_stmt].wrong)

                else:
                    call court_penalty(tm_name, tm.scolds.get(xexam_pick,
                        _("Right statement. Wrong fallacy. Look again at how the reasoning fails.")))

            if spirit <= 0:
                return "mistrial"

            if xexam_pick is not None:
                call expression tm.witness_shot


## After the right fallacy: present the evidence that proves it. Returns
## "proved", "wrong" (penalty given) or "withdrawn".
label prove_it(tm_name):
    $ tm = testimony(tm_name)
    $ bgm("pursuit", fadein=0.2, card_delay=0.6, fadeout=0.3)
    call expression tm.judge_shot
    $ renpy.say(tm.judge_character, _("A fair objection. Now prove it. What in the Court Record backs you up?"))
    call screen evidence_pick(tm_name)

    if _return is None:
        return "withdrawn"

    if _return == tm.proof:
        call court_shout("takethat")
        return "proved"

    if _return == "timeout":
        call court_penalty(tm_name, _("Time's up. An objection without proof is just noise."))
    else:
        call court_penalty(tm_name, tm.proof_wrong or _("That proves nothing about this statement."))
    return "wrong"


## "TESTIMONY UPDATED" after a press adds a statement.
label testimony_updated(title):
    window hide
    show screen court_title(_("TESTIMONY UPDATED"), "証言追加", title)
    with Dissolve(0.2)
    pause 1.3
    hide screen court_title
    with Dissolve(0.2)
    window auto
    return


## A shout bubble: "objection", "hold" or "takethat".
label court_shout(kind):
    show screen court_shout(kind)
    with vpunch
    pause 0.8
    hide screen court_shout
    with Dissolve(0.12)
    return


## Cut to the judge, flash red, scold, and crack a magatama.
label court_penalty(tm_name, line):
    $ tm = testimony(tm_name)
    call expression tm.judge_shot
    with red_flash
    $ react(tm.judge_shot[len("shot_"):], "angry")
    $ renpy.say(tm.judge_character, line)
    $ spirit_lose()
    $ sfx("penalty")
    with hpunch
    pause 0.7
    $ renpy.block_rollback()
    return


## Game over. Returns to the caller to retry, or restarts to the title.
label mistrial:
    $ bgm_stop(1.2)
    $ case_mistrial = True
    hide screen court_hud
    call screen mistrial_screen
    if _return == "retry":
        $ spirit_reset()
        show screen court_hud
        return
    $ renpy.full_restart()
