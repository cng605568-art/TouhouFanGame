# Fumo Court: Shiki Eiki's Logic Trials

An *Ace Attorney*-style courtroom game made in Ren'Py 8.3. Yama Shiki Eiki puts Gensokyo's residents (as deadpan fumo plushies) on trial for petty crimes. You're her junior judge: press testimony, spot the **logical fallacy**, and object.

**Case 01: Cirno's Frosty Fallacy.** Cirno froze twenty frogs, they all thawed and hopped off, so she's decided freezing makes frogs immortal. Find the flaw.

The character sprites are photos of the official Fumo plushies, cut out with the open BiRefNet segmentation model and relit to match the courtroom. Every other visual is code: hand-written SVG shapes and Ren'Py styles. Nothing is AI-generated art.

## Play

Download the latest build from [Releases](../../releases):

- **`FumoCourt-x.y.z-win.zip`**: unzip it, then run `FumoCourt.exe`.
- **`FumoCourt-x.y.z-web.zip`**: an HTML5 build. Upload it to itch.io as an HTML game, or unzip it and serve the folder over HTTP. Opening `index.html` straight from disk won't work.

| Action | Mouse | Keyboard |
|---|---|---|
| Next / previous statement | ◆ arrows | Right / Left |
| Press the witness | `PRESS` plaque | P |
| Object | `OBJECT!` plaque | O |
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

**For a test build without a release:** go to **Actions → Build & Release → Run workflow**. The zips show up as a downloadable artifact on the run page.

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

Each witness has a theme in `game/audio/music/`, listed in the `BGM` table in `game/audio.rpy`. It starts with the witness's testimony, carries through the cross-examination and cuts out when the objection lands. Its title card slides in at the bottom right, the way a Touhou stage names its BGM.

Cirno testifies to *Beloved Tomboyish Girl*, +TEK's chiptune arrangement of ZUN's おてんば恋娘, released under CC BY 4.0. Nothing is extracted from the official games: ZUN's guidelines don't allow that, so every theme is a fan arrangement whose arranger allows game use.

To add or swap a theme, run `python tools/build_music.py track.mp3 <name>`. It trims the silence, fades the tail for a clean loop, matches the loudness to the sound effects and writes `game/audio/music/<name>.ogg`. Then add a `Theme` to `BGM`.

## Repository layout

```
game/
  options.rpy      config, build settings
  audio.rpy        sound effect slots, text blips, witness themes
  gui.rpy          palette, fonts, CourtPanel (sharp gold/crimson frames)
  transforms.rpy   fumo_talk, fumo_shock, fumo_yeet, eiki_lecture, effects
  screens.rpy      courtroom HUD, cross-examination engine, menus
  script.rpy       Case 01
  images/          fumo sprites (PNG, with SVG fallbacks), shadow, background, gavel, scales
  gui/             SVG UI pieces, window icon
  fonts/           Shippori Mincho B1 subsets (SIL OFL 1.1)
  audio/sfx/       sound effects (CC0)
  audio/music/     witness themes (fan arrangements, see CREDITS.txt there)
tools/
  make_art.py      regenerates every SVG and icon
  fumo_sprite.py   photo -> cut-out, relit sprite PNG
  build_sfx.py     CC0 sound packs -> game/audio/sfx/
  build_music.py   downloaded track -> trimmed, normalised .ogg
  build_fonts.py   rebuilds the font subsets
art_src/           plush photos the sprites are made from, plus previews
```

To add a case, write a new `Testimony(...)` in a script file (Case 01 in `script.rpy` is the template), then `call cross_examination("your_testimony")`.

## Credits and disclaimer

**Touhou Project** and all of its characters are the property of **Team Shanghai Alice (ZUN)**. *Fumo Court* is an unofficial, non-commercial fan work. It is not affiliated with, endorsed by, or produced by Team Shanghai Alice. Please support the official games.

Fumo is a plush line produced by Gift. The sprite photos show Gift's official plushies. This project is not affiliated with Gift.

- Sound effects: Warsong's [Petaldust and Nostalgiac Blues sound packs](https://warsong.pages.dev/tags/touhou/) (CC0)
- Cirno's theme: [*Beloved Tomboyish Girl*](https://plustek.bandcamp.com/track/beloved-tomboyish-girl) by +TEK, from *Story of Modulated Frequency* (2017), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Trimmed, loudness-normalised and re-encoded as Ogg Vorbis. Arrangement of おてんば恋娘 by ZUN (Team Shanghai Alice).
- Background removal: [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) (MIT) via [rembg](https://github.com/danielgatis/rembg)

- Engine: [Ren'Py](https://www.renpy.org) (MIT and other licenses)
- Font: [Shippori Mincho B1](https://github.com/fontdasu/ShipporiMincho) by FONTDASU, SIL Open Font License 1.1 (`game/fonts/OFL.txt`)
