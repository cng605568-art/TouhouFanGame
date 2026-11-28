# Fumo Court: Shiki Eiki's Logic Trials

An *Ace Attorney*-style courtroom game made in Ren'Py 8.3. Yama Shiki Eiki puts Gensokyo's residents (as deadpan fumo plushies) on trial for petty crimes. You're her junior judge: press testimony, spot the **logical fallacy**, and object.

Nine cases, played in order. Each witness hides one fallacy in their testimony:

- **Case 01: Cirno's Frosty Fallacy.** Cirno froze twenty frogs, they all thawed and hopped off, so she's decided freezing makes frogs immortal. *False Cause.*
- **Case 02: The Long-Term Loan.** Marisa "borrowed" forty-seven grimoires, and besides, Reimu pockets her own donation box. *Tu Quoque.*
- **Case 03: The Vanished Pudding.** Sakuya is sure the gatekeeper ate the pudding, because the only other suspect would never. *False Dilemma.*
- **Case 04: The Lunar Prescription.** Reisen's tonic makes villagers hear colours, but Master Eirin says it's safe. *Appeal to Authority.*
- **Case 05: The Unappealable Verdict.** The pudding from Case 03 turns up frozen at Misty Lake, and a judge can't hear her own appeal. You take the bench; Eiki takes the stand. *Circular Reasoning.*
- **Case 06: The Open Gate.** The mistress's parasol is gone, and Meiling knows the thief didn't use her gate: Marisa came in by a window once, so every thief does. *Hasty Generalization.*
- **Case 07: Strings Attached.** Alice tied Marisa to a tree over an insult Marisa never actually said. *Straw Man.*
- **Case 08: Fifty Satisfied Customers.** Reimu's lucky charms must work, because fifty villagers bought one. *Bandwagon.*
- **Case 09: The Five Impossible Chores.** Reisen finished all five of Kaguya's chores, so now there's a sixth: the moon. *Moving the Goalposts.* Someone with a thousand-year grudge has been waiting for Kaguya to lose.

How a trial works:

- **Press** every statement. Some presses make the witness add a new statement (TESTIMONY UPDATED), and the flaw is often the one they didn't want to say.
- **Object** with the fallacy card that names the flaw. On Normal and up, Eiki then asks you to **prove it** with an item from the **Court Record** (TAKE THAT!).
- Wrong objections cost a magatama of spirit. Run out and it's a mistrial.
- **Difficulty**, chosen on the Docket: *Easy* (seven magatama, the case's three cards, no proof), *Normal* (five, every fallacy met so far), *Hard* (four, a 30-second card timer) and *Lunatic* (three, fifteen seconds, every card from the start). Each case is ranked S to C by how many mistakes you made, and the Docket keeps your best.
- When a witness is cornered the pursuit theme kicks in, and each one breaks down in their own way.

CASE CLOSED leads straight into the next trial, and the fumo on the right of the title screen is always whoever testifies next. Begin Trial opens the Docket, where you pick a difficulty and replay closed cases.

The character sprites are photos of the official Fumo plushies, cut out with the open BiRefNet segmentation model and relit to match the courtroom. Every other visual is code: hand-written SVG shapes and Ren'Py styles. Nothing is AI-generated art.

## Play

Download the latest build from [Releases](../../releases):

- **`FumoCourt-x.y.z-win.zip`**: unzip it, then run `FumoCourt.exe`.
- **`FumoCourt-x.y.z-web.zip`**: an HTML5 build. Upload it to itch.io as an HTML game, or unzip it and serve the folder over HTTP. Opening `index.html` straight from disk won't work.
- **`FumoCourt-x.y.z-android.apk`**: for Android phones and tablets. Open it on the device and allow installing from your browser or file manager.

The game is in English, Japanese (日本語) and Simplified Chinese (简体中文); switch under **Settings → Language**.

| Action | Mouse | Keyboard |
|---|---|---|
| Next / previous statement | ◆ arrows | Right / Left |
| Press the witness | `PRESS` plaque | P |
| Object | `OBJECT!` plaque | O |
| Court Record | `COURT RECORD` | R |
| Withdraw an objection | `Withdraw` | Esc |

## Building

Builds run automatically on GitHub Actions (`.github/workflows/build.yml`).

**To publish a release:**

1. Set the version in `game/options.rpy`, for example `define config.version = "0.2.0"`.
2. Commit, then push a tag with the same number:
   ```
   git tag v0.2.0
   git push origin v0.2.0
   ```
3. The workflow downloads Ren'Py 8.3.7, lints the game, and attaches the Windows and web zips to a new GitHub Release.

**For a test build without a release:** go to **Actions → Build & Release → Run workflow**. The zips show up as a downloadable artifact on the run page. **Actions → Android → Run workflow** does the same for the APK.

**Android** (`.github/workflows/android.yml`) uses Ren'Py's RAPT with the runner's Android SDK and Java 21, and reads its settings from `.android.json` (package name, orientation) and the launcher icon from `android-icon_foreground.png` / `android-icon_background.png`. To sign every APK with the same key, so that a new version installs over the old one, run `sh tools/make_keystore.sh` once and save the printed text as a repository secret named `ANDROID_KEYSTORE` (Settings → Secrets and variables → Actions). Keep the `.keystore` file somewhere safe and never commit it. Without the secret each build is signed with a one-off key, and updating means uninstalling first.

**itch.io:** `itch/page.md` has the page text and project settings, `itch/cover.png` the cover and `itch/screenshots/` the screenshots. To upload tagged builds automatically, add a `BUTLER_API_KEY` secret (from itch.io → Settings → API keys) and an `ITCH_GAME` repository variable such as `yourname/fumo-court`; the workflows then push the Windows, web and Android builds to the `windows`, `html5` and `android` channels.

**To build locally**, use the [Ren'Py 8.3.7 SDK](https://www.renpy.org/release/8.3.7) plus its web support package:

```
renpy.sh launcher distribute path/to/TouhouFanGame --package win
renpy.sh launcher web_build path/to/TouhouFanGame
```

Or just open the folder as a project in the Ren'Py launcher.

## Character sprites

Every character is one static sprite, `game/images/<name>_fumo.png`, made from a plush photo in `art_src/`. Each sprite is scaled into the same 480×500 slot with its feet at the bottom, so any photo size works with the staging and animations.

**To add or replace a fumo:**

1. Put the photo in `art_src/`, named after the character, e.g. `art_src/reimu_fumo.jpg`. A plain or white backdrop works best.
2. Commit and push. The **Make fumo sprites** workflow runs on its own. You can also start it from **Actions → Make fumo sprites → Run workflow**.
3. Within a few minutes it commits `game/images/reimu_fumo.png`, plus a before/after preview in `art_src/previews/`. Pull to get them.

What the workflow does (`tools/fumo_sprite.py`):

- removes the background with BiRefNet, which only decides which pixels are plush and draws nothing;
- cleans the edges with alpha matting and strips backdrop colour out of edge pixels, so nothing grey or white fringes the plush;
- relights the plush for the courtroom: dimmer studio highlights, crimson-warm colour balance, red bounce light, a gold rim light from the mirror halo, and shading toward the cushion.

To skip the AI model, run it with `--model classic` (GrabCut or white-backdrop flood fill). If you delete a sprite PNG, the game falls back to the SVG placeholder of the same name.

## Sound effects

Every sound is named after the moment it plays at (`gavel.ogg`, `shout_objection.ogg`, `penalty.ogg`...) and lives in `game/audio/sfx/`. To change one, replace that file. A missing file is skipped silently. The full list of slots is at the top of `game/audio.rpy`.

The sounds come from Warsong's CC0 packs for the Touhou fan games *Petaldust* and *Nostalgiac Blues*. `game/audio/sfx/CREDITS.txt` lists which pack sound went where, and `tools/build_sfx.py` rebuilds them from the unzipped packs.

## Music

The title screen and each witness have a theme in `game/audio/music/`, listed in the `BGM` table in `game/audio.rpy`. A witness theme starts with the witness's testimony and carries through the cross-examination; when the witness is cornered the pursuit theme takes over, and the music cuts out when the case breaks open. Each title card slides in at the bottom right, the way a Touhou stage names its BGM.

Every piece is a chiptune arrangement by +TEK, released under CC BY 4.0: *Scarlet Beyond a Crimson Dream* on the title screen, then *Beloved Tomboyish Girl* (Cirno), *Love-coloured Master Spark* (Marisa), *Lunar Clock ~ Luna Dial* (Sakuya) and *Lunatic Eyes ~ Invisible Full Moon* (Reisen), *Reach for the Moon, Immortal Smoke* (Eiki in Case 05, and Mokou), *Shanghai Teahouse ~ Chinese Tea* (Meiling), *The Doll Maker of Bucuresti* (Alice), *Maiden's Capriccio ~ Dream Battle* (Reimu) and *Gensokyo Millenium ~ History of the Moon* (Kaguya), with *U.N. Owen Was Her S* as the pursuit theme. Nothing is extracted from the official games: ZUN's guidelines don't allow that, so every theme is a fan arrangement whose arranger allows game use.

To add or swap a theme, run `python tools/build_music.py track.flac <name> --find-loop`. Arrangements usually play the tune twice and then fade out. The tool finds where the second pass begins, cuts the file there and crossfades the cut, so the theme loops seamlessly for as long as the cross-examination lasts. It also matches the loudness to the sound effects and writes `game/audio/music/<name>.ogg`. Then add a `Theme` to `BGM` with the loop start the tool prints. Without `--find-loop` it just trims the silence and fades the tail.

## Repository layout

```
game/
  options.rpy      config, build settings
  audio.rpy        sound effect slots, per-speaker text blips, music
  gui.rpy          palette, fonts, CourtPanel (sharp gold/crimson frames)
  transforms.rpy   fumo_talk, fumo_shock, fumo_yeet, eiki_lecture, effects
  court.rpy        the trial engine: testimony, presses, hidden statements,
                   the Court Record, difficulty, spirit and ranks
  reactions.rpy    witness breakdowns, react() emotes and pose photos
  screens.rpy      courtroom HUD, cross-examination, fallacy and evidence picks, menus
  script.rpy       cast, camera shots, fallacy cards, Case 01
  case02-09.rpy    Cases 02 to 09
  docket.rpy       case list, progress, the Docket screen
  compendium.rpy   the Compendium of fallacies and practice mode
  translations.rpy language switching; the translations are in tl/japanese and tl/schinese
  images/          fumo sprites (PNG, with SVG fallbacks), shadow, background, gavel, scales
  gui/             SVG UI pieces, window icon
  fonts/           Shippori Mincho B1 subsets (SIL OFL 1.1)
  audio/sfx/       sound effects (CC0)
  audio/music/     title and witness themes (fan arrangements, see CREDITS.txt there)
tools/
  make_art.py      regenerates every SVG and icon
  fumo_sprite.py   photo -> cut-out, relit sprite PNG
  build_sfx.py     CC0 sound packs -> game/audio/sfx/
  build_music.py   downloaded track -> seamless loop, normalised .ogg
  build_fonts.py   rebuilds the font subsets
art_src/           plush photos the sprites are made from, plus previews
```

To add a case: put the witness's fumo photo in `art_src/`, copy `case02.rpy` as a template (evidence, testimony, presses, the case labels), and add a `Case(...)` to `CASES` in `docket.rpy`. In a `Statement`, `reveals="key"` makes pressing it add the hidden statement with that `key`; `proof` names the Court Record item that proves the objection. A new fallacy needs a `Fallacy(...)` in `script.rpy`, an icon from `tools/make_art.py`, a tip and practice lines in `compendium.rpy`, and a place in `FALLACY_ORDER` in `court.rpy`.

**Pose photos.** `react("cirno", "smug")` makes a fumo react with a little move and an emote. To give a character a real pose instead, add a photo named `art_src/cirno_fumo_smug.jpg` (or `_nervous`, `_angry`, `_shock`, `_gloom`); the sprite workflow turns it into `game/images/cirno_fumo_smug.png` with the same lighting, and the game uses it automatically.

**Translations.** Run `renpy.sh path/to/TouhouFanGame translate <language>` to add or update the files in `game/tl/<language>/`, translate the `new` lines, then run `tools/build_fonts.py` so the font subsets include every character used.

## Credits and disclaimer

**Touhou Project** and all of its characters are the property of **Team Shanghai Alice (ZUN)**. *Fumo Court* is an unofficial, non-commercial fan work. It is not affiliated with, endorsed by, or produced by Team Shanghai Alice. Please support the official games.

Fumo is a plush line produced by Gift. The sprite photos show Gift's official plushies. This project is not affiliated with Gift.

- Sound effects: Warsong's [Petaldust and Nostalgiac Blues sound packs](https://warsong.pages.dev/tags/touhou/) (CC0)
- Title theme: [*Scarlet Beyond a Crimson Dream*](https://plustek.bandcamp.com/track/scarlet-beyond-a-crimson-dream) by +TEK, from *Embodiment of Frequency Modulation* (2024), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of music by ZUN (Team Shanghai Alice).
- Cirno's theme: [*Beloved Tomboyish Girl*](https://plustek.bandcamp.com/track/beloved-tomboyish-girl) by +TEK, from *Story of Modulated Frequency* (2017), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of おてんば恋娘 by ZUN (Team Shanghai Alice).
- Marisa's theme: [*Love-coloured Master Spark*](https://plustek.bandcamp.com/track/love-coloured-master-spark), Sakuya's theme: [*Lunar Clock ~ Luna Dial*](https://plustek.bandcamp.com/track/lunar-clock-luna-dial) and Reisen's theme: [*Lunatic Eyes ~ Invisible Full Moon*](https://plustek.bandcamp.com/track/lunatic-eyes-invisible-full-moon), all by +TEK from *Embodiment of Frequency Modulation* (2024), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangements of ZUN's 恋色マスタースパーク, 月時計 ～ ルナ・ダイアル and 狂気の瞳 ～ Invisible Full Moon.
- Eiki's theme (Case 05): [*Reach for the Moon, Immortal Smoke*](https://plustek.bandcamp.com/track/reach-for-the-moon-immortal-smoke) by +TEK, from *Embodiment of Frequency Modulation* (2024), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of 月まで届け、不死の煙 by ZUN (Team Shanghai Alice).
- Meiling's theme (Case 06): [*Shanghai Teahouse ~ Chinese Tea*](https://plustek.bandcamp.com/track/shanghai-teahouse-chinese-tea) by +TEK, from *Story of Modulated Frequency* (2017), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of 上海紅茶館 ～ Chinese Tea by ZUN (Team Shanghai Alice).
- Alice's theme (Case 07): [*The Doll Maker of Bucuresti*](https://plustek.bandcamp.com/track/the-doll-maker-of-bucuresti) by +TEK, from *Phantasmagoria of F.M* (2020), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of ブクレシュティの人形師 by ZUN (Team Shanghai Alice).
- Reimu's theme (Case 08): [*Maiden's Capriccio ~ Dream Battle*](https://plustek.bandcamp.com/track/maidens-capriccio-dream-battle) by +TEK, from *Phantasmagoria of F.M* (2020), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of 少女綺想曲 ～ Dream Battle by ZUN (Team Shanghai Alice).
- Kaguya's theme (Case 09): [*Gensokyo Millenium ~ History of the Moon*](https://plustek.bandcamp.com/track/gensokyo-millenium-history-of-the-moon) by +TEK, from *Story of Modulated Frequency* (2017), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cut to loop seamlessly, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of 千年幻想郷 ～ History of the Moon by ZUN (Team Shanghai Alice).
- Pursuit theme: [*U.N. Owen Was Her S*](https://plustek.bandcamp.com/track/u-n-owen-was-her-s) by +TEK, from *Embodiment of Frequency Modulation* (2024), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Looped by hand at a repeated passage, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of U.N.オーエンは彼女なのか？ by ZUN (Team Shanghai Alice).
- Background removal: [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) (MIT) via [rembg](https://github.com/danielgatis/rembg)

- Engine: [Ren'Py](https://www.renpy.org) (MIT and other licenses)
- Fonts: [Shippori Mincho B1](https://github.com/fontdasu/ShipporiMincho) by FONTDASU and [Noto Serif SC](https://fonts.google.com/noto/specimen/Noto+Serif+SC) by Google, SIL Open Font License 1.1 (`game/fonts/OFL.txt`, `game/fonts/OFL-NotoSerifSC.txt`)
