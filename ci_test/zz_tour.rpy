## CI-only screenshot tour. Lives on the scratch branch, never in the game.

init python:
    import os

    def shot(name):
        d = os.environ.get("FUMO_SHOTS", "/tmp/shots")
        if not os.path.isdir(d):
            os.makedirs(d)
        ok = renpy.screenshot(os.path.join(d, name + ".png"))
        print("SHOT", name, ok)

    import time

    # Auto-shots: when one of these screens has been up for the given time,
    # screenshot it once. Lets the case run click freely and still capture
    # banners, cards, stamps and the case-closed panel.
    WATCH = {"case_card": 0.9, "bgm_title": 2.7, "fallacy_pick": 1.0, "verdict_stamp": 0.3,
             "case_closed": 1.2, "docket": 0.8, "main_menu": 1.5, "evidence_pick": 0.9,
             "court_record": 0.6, "breakdown_fx": 0.3, "emote": 0.25, "evidence_added": 0.5,
             "court_title": 0.45, "court_shout": 0.2}
    _seen = {}
    _count = {}

    def autoshot():
        if not os.environ.get("FUMO_AUTOSHOT"):
            return
        now = time.time()
        for name, delay in WATCH.items():
            if renpy.get_screen(name):
                t0 = _seen.get(name)
                if t0 is None:
                    _seen[name] = now
                elif t0 >= 0 and now - t0 >= delay:
                    _count[name] = _count.get(name, 0) + 1
                    shot("auto_%s_%d" % (name, _count[name]))
                    _seen[name] = -1.0
            else:
                _seen.pop(name, None)

    config.periodic_callbacks.append(autoshot)

    # Trace the trial engine's labels, so a stuck run shows where it went.
    def _trace(name, abnormal):
        if name in ("prove_it", "court_penalty", "cross_examination", "testimony_updated",
                    "breakdown", "mistrial", "close_case", "practice", "practice_done"):
            print("LABEL", name, "stmt", getattr(store, "xexam_stmt", None), "pick",
                  getattr(store, "xexam_pick", None), "index", getattr(store, "xexam_index", None),
                  "return", getattr(store, "_return", None))
    config.label_callbacks.append(_trace)

    # Give up instead of hanging until the runner kills X.
    _t0 = time.time()
    def _deadline():
        limit = float(os.environ.get("FUMO_MAX", "0") or 0)
        if limit and time.time() - _t0 > limit:
            print("DEADLINE reached; quitting")
            renpy.quit()
    config.periodic_callbacks.append(_deadline)

    def focus_dump(tag):
        out = []
        for f in renpy.display.focus.focus_list:
            try:
                t = f.widget._tts_all()[:24]
            except Exception:
                t = "?"
            out.append((t, f.x, f.y, f.w, f.h))
        print("FOCUS", tag, out)
        print("MOUSE", tag, renpy.get_mouse_pos())

    def mus(tag):
        print("MUSIC", tag, renpy.music.get_playing("music"),
              "card" if renpy.get_screen("bgm_title") else "no-card")

testcase pngswap:
    pause 3.0
    $ shot("40_png_swap_title")
    $ renpy.quit()

testcase tour:
    $ preferences.text_cps = 0
    $ preferences.afm_enable = False
    pause 3.0
    $ shot("01_title")
    $ mus("01_title")
    "Begin Trial"
    pause 1.0
    $ shot("02_docket")
    "Lunatic"
    pause 0.4
    $ shot("03_docket_lunatic")
    "Normal"
    pause 0.3
    "Cirno's Frosty Fallacy"
    pause 1.4
    $ shot("04_case_card")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("05_xexam_s1")
    $ print("STATE spirit", spirit, spirit_cap, difficulty, court_record)
    "待った"
    pause 1.3
    $ shot("06_press")
    click pos (40, 540)
    pause 0.35
    $ shot("07_press_smug")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("08_xexam_s2")
    "異議あり"
    pause 1.0
    $ shot("09_cards")
    "False Cause"
    move (40, 540)
    pause 2.4
    $ shot("10_penalty_wrong_statement")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    "Next statement"
    pause 0.5
    $ shot("11_flaw")
    "異議あり"
    pause 0.9
    "Ad Hominem"
    move (40, 540)
    pause 2.4
    $ shot("12_scold")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    "異議あり"
    pause 0.9
    "False Cause"
    move (40, 540)
    pause 2.0
    $ shot("13_prove_it")
    pause 2.5
    click pos (40, 540)
    pause 0.9
    pause 0.8
    $ shot("14_evidence_pick")
    "Frog Census"
    move (40, 540)
    pause 2.2
    $ shot("15_wrong_evidence")
    click pos (40, 540) until move (0.5, 0.5) pattern "COURT RECORD"
    pause 0.5
    $ shot("16_after_wrong_evidence")
    $ print("STATE spirit", spirit, "penalties", case_penalties)
    "COURT RECORD"
    pause 0.8
    $ shot("17_court_record")
    "Close"
    pause 0.4
    "異議あり"
    pause 0.9
    "False Cause"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    pause 0.5
    "Weather Log"
    move (40, 540)
    pause 0.35
    $ shot("18_take_that")
    click pos (40, 540)
    pause 0.5
    click pos (40, 540)
    pause 0.5
    click pos (40, 540)
    pause 0.6
    $ shot("19_breakthrough")
    click pos (40, 540)
    pause 0.15
    $ shot("20_breakdown_cirno")
    pause 0.4
    $ shot("21_breakdown_cirno_b")
    click pos (40, 540) until move (0.5, 0.5) pattern "Return to Title"
    pause 0.4
    $ shot("22_case_closed_rank")
    $ print("STATE rank", case_rank(), persistent.best_ranks)
    "Return to Title"
    pause 2.5
    $ shot("23_title_marisa")
    "Begin Trial"
    pause 1.0
    $ shot("24_docket_after_case1")
    "Return"
    pause 0.6
    "Settings"
    pause 0.8
    $ shot("25_settings")
    "Return"
    pause 0.6
    "About"
    pause 0.8
    $ shot("26_about")
    "Return"
    pause 0.5
    "Compendium"
    pause 0.8
    $ shot("27_compendium_one")
    "Return"
    pause 0.5
    "Settings"
    pause 0.8
    $ shot("27b_settings_language")
    "Return"
    pause 0.5
    $ renpy.change_language("japanese")
    pause 1.5
    $ shot("28_title_ja")
    "裁判を始める"
    pause 1.0
    $ shot("29_docket_ja")
    "チルノの凍てつく誤謬"
    pause 1.5
    click pos (40, 540) until move (0.5, 0.5) pattern "次の発言"
    pause 0.6
    $ shot("30_xexam_ja")
    "異議あり"
    pause 1.0
    $ shot("31_cards_ja")
    "取り下げる"
    pause 0.6
    $ renpy.change_language("schinese")
    pause 1.0
    $ shot("32_xexam_zh")
    "异议"
    pause 1.0
    $ shot("33_cards_zh")
    "撤回"
    pause 0.6
    $ renpy.change_language(None)
    pause 0.5
    $ renpy.quit()

testcase sfxcheck:
    pause 2.0
    $ print('SFXCHECK styles', SFX_HOVER, SFX_CONFIRM, SFX_CANCEL, SFX_NAV)
    $ sfx('ui_hover')
    pause 0.15
    $ print('SFXCHECK', 'ui_hover', sfx_file('ui_hover'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('ui_confirm')
    pause 0.15
    $ print('SFXCHECK', 'ui_confirm', sfx_file('ui_confirm'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('ui_cancel')
    pause 0.15
    $ print('SFXCHECK', 'ui_cancel', sfx_file('ui_cancel'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('nav')
    pause 0.15
    $ print('SFXCHECK', 'nav', sfx_file('nav'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('shout_objection')
    pause 0.15
    $ print('SFXCHECK', 'shout_objection', sfx_file('shout_objection'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('shout_hold')
    pause 0.15
    $ print('SFXCHECK', 'shout_hold', sfx_file('shout_hold'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('gavel')
    pause 0.15
    $ print('SFXCHECK', 'gavel', sfx_file('gavel'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('stamp')
    pause 0.15
    $ print('SFXCHECK', 'stamp', sfx_file('stamp'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('banner')
    pause 0.15
    $ print('SFXCHECK', 'banner', sfx_file('banner'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('penalty')
    pause 0.15
    $ print('SFXCHECK', 'penalty', sfx_file('penalty'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('breakthrough')
    pause 0.15
    $ print('SFXCHECK', 'breakthrough', sfx_file('breakthrough'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('shock')
    pause 0.15
    $ print('SFXCHECK', 'shock', sfx_file('shock'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('yeet')
    pause 0.15
    $ print('SFXCHECK', 'yeet', sfx_file('yeet'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('case_closed')
    pause 0.15
    $ print('SFXCHECK', 'case_closed', sfx_file('case_closed'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('mistrial')
    pause 0.15
    $ print('SFXCHECK', 'mistrial', sfx_file('mistrial'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('blip')
    pause 0.15
    $ print('SFXCHECK', 'blip', sfx_file('blip'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('blip_hi')
    pause 0.15
    $ print('SFXCHECK', 'blip_hi', sfx_file('blip_hi'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('blip_up')
    pause 0.15
    $ print('SFXCHECK', 'blip_up', sfx_file('blip_up'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('blip_dn')
    pause 0.15
    $ print('SFXCHECK', 'blip_dn', sfx_file('blip_dn'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('blip_lo')
    pause 0.15
    $ print('SFXCHECK', 'blip_lo', sfx_file('blip_lo'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('blip_deep')
    pause 0.15
    $ print('SFXCHECK', 'blip_deep', sfx_file('blip_deep'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('break_cirno')
    pause 0.15
    $ print('SFXCHECK', 'break_cirno', sfx_file('break_cirno'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('break_marisa')
    pause 0.15
    $ print('SFXCHECK', 'break_marisa', sfx_file('break_marisa'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('break_sakuya')
    pause 0.15
    $ print('SFXCHECK', 'break_sakuya', sfx_file('break_sakuya'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('break_reisen')
    pause 0.15
    $ print('SFXCHECK', 'break_reisen', sfx_file('break_reisen'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ sfx('break_eiki')
    pause 0.15
    $ print('SFXCHECK', 'break_eiki', sfx_file('break_eiki'), renpy.music.get_playing('event'), renpy.music.get_pos('event'))
    $ renpy.quit()

testcase musicloop:
    pause 2.0
    $ print("LOOPCHECK file", BGM["cirno"].filename)
    $ renpy.music.play("<from 86.5 loop 3.875488>audio/music/cirno_theme.ogg", channel="music", loop=True)
    pause 0.5
    $ print("LOOPCHECK before end", renpy.music.get_pos("music"), renpy.music.get_duration("music"))
    pause 3.0
    $ print("LOOPCHECK after wrap", renpy.music.get_pos("music"), renpy.music.get_playing("music"))
    pause 2.0
    $ print("LOOPCHECK later", renpy.music.get_pos("music"))
    $ renpy.quit()



testcase cases:
    $ preferences.text_cps = 0
    $ preferences.afm_enable = False
    pause 3.0
    $ shot("c00_title")
    "Begin Trial"
    pause 1.0
    "The Long-Term Loan"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c02_hidden_statement")
    "異議あり"
    pause 1.0
    "Tu Quoque"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    pause 0.4
    "Library Ledger"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.15
    $ shot("c02_breakdown")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    "Next statement"
    pause 0.3
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c03_trap")
    $ print("STATE record", court_record)
    "Next statement"
    pause 0.3
    $ shot("c03_dilemma_visible")
    "異議あり"
    pause 1.2
    "False Dilemma"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    $ shot("c03_evidence")
    "Mansion Roster"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c03_breakdown")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c04_trap")
    "Next statement"
    pause 0.3
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c04_hidden_statement")
    "異議あり"
    pause 1.2
    "Appeal to Authority"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    "Lab Notebook"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c04_breakdown")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c05_eiki_stand")
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c05_review")
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c05_hidden_statement")
    "異議あり"
    pause 1.2
    "Circular Reasoning"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    pause 0.6
    $ shot("c05_evidence")
    "Frozen Pudding"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c05_breakdown")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c06_meiling_stand")
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c06_dozing")
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c06_sleeptalk")
    "Next statement"
    pause 0.3
    "異議あり"
    pause 1.2
    "Hasty Generalization"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    $ shot("c06_counter")
    "Tengu geta prints run from the front gate"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c06_breakdown")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c07_alice_stand")
    "異議あり"
    pause 1.2
    "Ad Hominem"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c07_heckle")
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "異議あり"
    pause 1.2
    "Ad Hominem"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c07_second_testimony")
    "Next statement"
    pause 0.3
    "異議あり"
    pause 1.2
    "Straw Man"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    $ shot("c07_evidence")
    "Bunbunmaru Clipping"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c07_breakdown")
    click pos (40, 540)
    pause 0.5
    click pos (40, 540)
    pause 0.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c08_reimu_stand")
    "異議あり"
    pause 1.2
    "Bandwagon"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c08_charm_offer")
    "Take the charm"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c08_after_bribe")
    $ print("STATE bribe", case_bribed, spirit)
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c08_hidden_statement")
    "異議あり"
    pause 1.2
    "Bandwagon"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    $ shot("c08_pair_pick")
    "Donation Box (Full)"
    pause 0.4
    "Village Complaint List"
    pause 0.4
    $ shot("c08_pair_chosen")
    "Present these two"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c08_breakdown")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_01")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_02")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_03")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_04")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_05")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_06")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_07")
    click pos (40, 540)
    pause 0.45
    $ shot("c08e_08")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c09_kaguya_stand")
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "異議あり"
    pause 1.2
    "Moving the Goalposts"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c09_too_early")
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c09_shift_1")
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c09_shift_2")
    "Next statement"
    pause 0.3
    $ shot("c09_moon")
    "異議あり"
    pause 1.2
    "Moving the Goalposts"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    "Signed Chore List"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.9
    $ shot("c09_point")
    "then a week off"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c09_breakdown")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_01")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_02")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_03")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_04")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_05")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_06")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_07")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_08")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_09")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_10")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_11")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_12")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_13")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_14")
    click pos (40, 540)
    pause 0.45
    $ shot("c09m_15")
    click pos (40, 540)
    pause 0.45
    click pos (40, 540)
    pause 0.45
    click pos (40, 540)
    pause 0.45
    click pos (40, 540)
    pause 0.45
    click pos (40, 540)
    pause 0.3
    $ shot("c09p_01")
    pause 0.3
    $ shot("c09p_02")
    pause 0.3
    $ shot("c09p_03")
    pause 0.3
    $ shot("c09p_04")
    pause 0.3
    $ shot("c09p_05")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c10_mokou_stand")
    "異議あり"
    pause 1.2
    "Red Herring"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c10_flare")
    "待った"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.6
    $ shot("c10_letter")
    "異議あり"
    pause 1.2
    "Red Herring"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    "Kaguya's Letter"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c10_breakdown")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_01")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_02")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_03")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_04")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_05")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_06")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_07")
    click pos (40, 540)
    pause 0.45
    $ shot("c10e_08")
    click pos (40, 540) until move (0.5, 0.5) pattern "Next Case"
    pause 0.4
    "Next Case"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ shot("c11_speed_a")
    pause 4.2
    $ shot("c11_speed_b")
    $ print("STATE speed", xexam_index)
    $ gimmick_speed = 1000.0
    $ xexam_index = 2
    $ renpy.restart_interaction()
    pause 0.5
    "異議あり"
    pause 1.2
    "Bandwagon"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "The Bunbunmaru office"
    pause 0.4
    $ shot("c11_recess")
    "The Bunbunmaru office"
    click pos (40, 540) until move (0.5, 0.5) pattern "The court archive"
    pause 0.4
    "The court archive"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c11_second_testimony")
    $ print("STATE record", court_record)
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "異議あり"
    pause 1.2
    "Cherry Picking"
    move (40, 540)
    pause 2.5
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.5
    $ shot("c11_trap")
    "Next statement"
    pause 0.3
    "Next statement"
    pause 0.3
    "異議あり"
    pause 1.2
    "Cherry Picking"
    move (40, 540)
    pause 2.5
    click pos (40, 540)
    pause 0.9
    "Own Docket"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.9
    $ shot("c11_point")
    "Meiling, not guilty"
    move (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.4
    click pos (40, 540)
    pause 0.25
    $ shot("c11_breakdown")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_01")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_02")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_03")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_04")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_05")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_06")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_07")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_08")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_09")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_10")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_11")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_12")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_13")
    click pos (40, 540)
    pause 0.45
    $ shot("c11e_14")
    click pos (40, 540) until move (0.5, 0.5) pattern "Return to Title"
    pause 0.5
    $ print("STATE ranks", persistent.best_ranks)
    "Return to Title"
    pause 2.5
    $ shot("c12_title_end_aya")
    "Compendium"
    pause 0.8
    $ shot("c09a_compendium")
    "Practice"
    pause 1.5
    click pos (40, 540)
    pause 0.6
    click pos (40, 540)
    pause 0.9
    pause 0.8
    $ shot("c09b_practice_q1")
    "False Cause"
    move (40, 540)
    pause 1.5
    click pos (40, 540)
    pause 0.6
    click pos (40, 540)
    pause 0.9
    "Circular Reasoning"
    move (40, 540)
    pause 1.5
    click pos (40, 540)
    pause 0.6
    click pos (40, 540)
    pause 0.9
    "Tu Quoque"
    move (40, 540)
    pause 1.5
    click pos (40, 540)
    pause 0.6
    click pos (40, 540)
    pause 0.9
    "False Dilemma"
    move (40, 540)
    pause 1.5
    click pos (40, 540)
    pause 0.6
    click pos (40, 540)
    pause 0.9
    "Ad Hominem"
    move (40, 540)
    pause 1.0
    $ shot("c09c_practice_feedback")
    click pos (40, 540) until move (0.5, 0.5) pattern "Begin Trial"
    pause 1.0
    $ print("STATE practice", persistent.practice_best)
    "Begin Trial"
    pause 1.0
    $ shot("c10_docket_all_closed")
    "Lunatic"
    pause 0.3
    "Cirno's Frosty Fallacy"
    click pos (40, 540) until move (0.5, 0.5) pattern "Next statement"
    pause 0.4
    $ print("STATE lunatic", spirit, spirit_cap, difficulty)
    "異議あり"
    pause 1.2
    $ shot("c11_lunatic_deck")
    $ renpy.change_language("japanese")
    pause 1.0
    $ shot("c11b_lunatic_deck_ja")
    $ renpy.change_language("schinese")
    pause 1.0
    $ shot("c11c_lunatic_deck_zh")
    $ renpy.change_language(None)
    pause 2.0
    pause 4.0
    $ shot("c12_lunatic_timer")
    pause 4.0
    pause 4.5
    $ shot("c13_timeout")
    $ renpy.quit()
