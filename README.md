# Fumo Court: Shiki Eiki's Logic Trials

An *Ace Attorney*-style courtroom game made in Ren'Py 8.3. Yama Shiki Eiki puts Gensokyo's residents (as deadpan fumo plushies) on trial for petty crimes. You're her junior judge: press testimony, spot the **logical fallacy**, and object.

**Case 01: Cirno's Frosty Fallacy.** Cirno froze twenty frogs, they all thawed and hopped off, so she's decided freezing makes frogs immortal. Find the flaw.

All visuals are code: hand-written SVG shapes and Ren'Py styles. No AI-generated art.

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

## Swapping in real art

Every character is a single static sprite. Drop `eiki_fumo.png` or `cirno_fumo.png` (any size, transparent background, feet at the bottom) into `game/images/`. A PNG takes priority over the SVG placeholder automatically and is scaled into the same 480×500 slot, so staging and animations keep working.

## Repository layout

```
game/
  options.rpy      config, build settings
  gui.rpy          palette, fonts, CourtPanel (sharp gold/crimson frames)
  transforms.rpy   fumo_talk, fumo_shock, fumo_yeet, eiki_lecture, effects
  screens.rpy      courtroom HUD, cross-examination engine, menus
  script.rpy       Case 01
  images/          SVG sprites, background, gavel, scales
  gui/             SVG UI pieces, window icon
  fonts/           Shippori Mincho B1 subsets (SIL OFL 1.1)
tools/
  make_art.py      regenerates every SVG and icon
  build_fonts.py   rebuilds the font subsets
```

To add a case, write a new `Testimony(...)` in a script file (Case 01 in `script.rpy` is the template), then `call cross_examination("your_testimony")`.

## Credits and disclaimer

**Touhou Project** and all of its characters are the property of **Team Shanghai Alice (ZUN)**. *Fumo Court* is an unofficial, non-commercial fan work. It is not affiliated with, endorsed by, or produced by Team Shanghai Alice. Please support the official games.

Fumo is a plush line produced by Gift. This project is not affiliated with Gift.

- Engine: [Ren'Py](https://www.renpy.org) (MIT and other licenses)
- Font: [Shippori Mincho B1](https://github.com/fontdasu/ShipporiMincho) by FONTDASU, SIL Open Font License 1.1 (`game/fonts/OFL.txt`)
