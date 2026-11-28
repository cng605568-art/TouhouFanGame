"""
Builds game/audio/sfx/*.ogg from Warsong's CC0 sound packs.

    python tools/build_sfx.py path/to/petaldust path/to/nostalgiac [slot ...]

Name slots at the end to rebuild only those.

The packs (CC0, public domain) were made for the Touhou fan games Petaldust and
Nostalgiac Blues: https://warsong.pages.dev/tags/touhou/ (download
petaldust.zip and nostalgiac.zip, unzip, point this script at the folders).

Each slot below is one or more layers (pack, file, gain in dB, start offset in
seconds, and optionally a playback-rate ratio: 0.5 plays a layer an octave
lower and twice as long). Layers are mixed, slots listed in REVERB get a
room, trailing silence is trimmed, the tail gets a short fade, and the result
is peak-normalised so story beats sit above button sounds. Needs numpy,
scipy, soundfile and ffmpeg (with libvorbis).
"""

import os
import shutil
import subprocess
import sys
import tempfile

from fractions import Fraction

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "audio", "sfx")
RATE = 44100

# slot: (peak dBFS, max seconds or None, [(pack, file, gain dB, offset s), ...])
RECIPE = {
    # Buttons: quiet, short, chiptune.
    "ui_hover":        (-15, None, [("N", "goodblip.wav", 0, 0)]),
    "ui_confirm":      (-9,  None, [("N", "healthrestore.wav", 0, 0)]),
    "ui_cancel":       (-9,  None, [("N", "badblip.wav", 0, 0)]),
    "nav":             (-8,  None, [("P", "clothC.wav", 0, 0)]),          # paper rustle: turning to the next statement

    # Courtroom beats.
    "shout_objection": (-1,  None, [("N", "big damage.wav", 0, 0), ("P", "slashC.wav", -4, 0)]),
    "shout_hold":      (-2,  0.9,  [("N", "destroyed.wav", 0, 0), ("P", "slashB.wav", -4, 0)]),
    "gavel":           (-1,  None, [("P", "HeadCup.wav", 0, 0), ("N", "hurteffect.wav", -5, 0)]),   # wood knock + low thump
    "stamp":           (-2,  None, [("N", "hurteffect.wav", 0, 0), ("N", "landingsound.wav", -2, 0)]),
    "banner":          (-4,  None, [("P", "badbell.wav", 0, 0)]),         # court bell for the title ribbons
    "penalty":         (-2,  None, [("N", "breakeffect.wav", 0, 0)]),     # the magatama shatters
    "breakthrough":    (-2,  None, [("P", "success.wav", 0, 0)]),
    "shock":           (-2,  None, [("N", "cirnobullet.wav", 0, 0)]),     # Cirno's own ice shot
    "yeet":            (-2,  None, [("N", "faraway.wav", 0, 0)]),
    # The verdict: a gavel knock, the A-major arpeggio from "success" low then
    # high, and two bell tones retuned into the same chord (progress -> C#+E,
    # reconfirm -> A+C#) ringing out under it.
    "case_closed":     (-2,  None, [("P", "HeadCup.wav", 0, 0), ("N", "hurteffect.wav", -4, 0),
                                    ("P", "success.wav", -2, 0.03, 0.5),
                                    ("P", "success.wav", -4, 0.12),
                                    ("P", "reconfirm.wav", -7, 0.20, 0.943),
                                    ("P", "reconfirm.wav", -10, 0.20, 0.4715),
                                    ("P", "progress.wav", -7, 0.20, 0.792)]),
    "mistrial":        (-3,  None, [("P", "unexpectedoutcome.wav", 0, 0)]),

    # Breakdowns: each witness falls apart in their own way (reactions.rpy).
    "break_cirno":     (-2,  1.8,  [("N", "cirnodeatheffect.wav", 0, 0), ("N", "breakeffect2.wav", -5, 0)]),    # ice shatters
    "break_marisa":    (-2,  1.6,  [("N", "betterbullet.wav", 0, 0), ("N", "startbleep.wav", -4, 0.05)]),       # star burst
    "break_sakuya":    (-2,  1.8,  [("P", "blockberakhigh.wav", 0, 0), ("P", "progress.wav", -6, 0.05, 0.5)]),  # watch cracks, time drags
    "break_reisen":    (-2,  1.8,  [("P", "error resonance.wav", 0, 0), ("N", "weird.wav", -6, 0)]),            # lunatic ripple
    "break_eiki":      (-1,  2.0,  [("N", "big damage.wav", 0, 0), ("P", "HeadCup.wav", -2, 0),
                                    ("P", "badbell.wav", -6, 0.05, 0.5)]),                                      # the scales fall
    "break_meiling":   (-2,  1.6,  [("N", "big damage.wav", 0, 0), ("N", "good bloopy.wav", -6, 0.05, 1.25)]),  # rainbow scatters
    "break_alice":     (-2,  1.2,  [("P", "slashD.wav", 0, 0), ("P", "slashA.wav", -2, 0.08, 1.3),
                                    ("P", "slashB.wav", -4, 0.16, 1.6)]),                                       # strings snap
    "break_reimu":     (-2,  1.6,  [("P", "clothB.wav", 0, 0), ("N", "destroyed.wav", -4, 0.02)]),             # ofuda flutter out
    "break_kaguya":    (-2,  1.8,  [("P", "reconfirm.wav", -3, 0, 0.75), ("N", "breakeffect2.wav", 0, 0.04)]), # treasures scatter
    "mokou_burst":     (-1,  1.6,  [("N", "big damage.wav", 0, 0), ("N", "destroyed.wav", -2, 0.02, 0.8),
                                    ("P", "slashC.wav", -3, 0.0)]),                                             # Mokou barges in
    "break_mokou":     (-2,  1.8,  [("N", "destroyed.wav", 0, 0, 0.85), ("P", "slashC.wav", -3, 0.02), ("N", "big damage.wav", -5, 0.05, 0.7)]),  # she flares up
    "break_aya":       (-2,  1.6,  [("P", "HybridFoley.wav", 0, 0, 1.3), ("N", "bulletpuff.wav", -2, 0.04), ("P", "clothA.wav", -3, 0.08, 1.4),
                                    ("P", "clothC.wav", -5, 0.22, 1.2)]),                                       # a shutter, then feathers
    # Mokou lays into Kaguya: four quick hits, the last one heavy.
    "mokou_pummel":    (-1,  1.9,  [("N", "playerhurt.wav", 0, 0.00), ("P", "slashA.wav", -4, 0.00),
                                    ("N", "playerhurt.wav", -1, 0.28, 1.12), ("P", "slashB.wav", -4, 0.28),
                                    ("N", "playerhurt.wav", 0, 0.56, 0.94), ("P", "slashD.wav", -4, 0.56),
                                    ("N", "big damage.wav", 0, 0.86), ("N", "landingsound.wav", -3, 0.86, 0.8)]),

    # Text blips: built separately (one blip padded to a steady beat). Each
    # speaker has a pitch (audio.rpy): high and quick for fairies, low for
    # the judge.
    "blip":            (-17, None, [("N", "goodblip.wav", 0, 0)]),
    "blip_hi":         (-17, None, [("N", "goodblip.wav", 0, 0, 1.32)]),
    "blip_up":         (-17, None, [("N", "goodblip.wav", 0, 0, 1.16)]),
    "blip_dn":         (-17, None, [("N", "goodblip.wav", 0, 0, 0.92)]),
    "blip_lo":         (-16, None, [("N", "goodblip.wav", 0, 0, 0.84)]),
    "blip_deep":       (-15, None, [("N", "goodblip.wav", 0, 0, 0.72)]),
}

BLIP_PERIOD = 0.072   # seconds between blips while text types out

# slot: (wet level dB, reverb time s). A synthetic hall, so the moment rings
# out instead of stopping dead.
REVERB = {
    "case_closed": (-13, 2.0),
    "break_sakuya": (-12, 1.8),
    "break_eiki": (-12, 2.0),
    "break_kaguya": (-14, 1.6),
    "mokou_burst": (-15, 1.2),
    "mokou_pummel": (-17, 1.0),
}


def load(path):
    """Any wav -> float32 stereo at RATE, via ffmpeg for resampling."""
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "2", "-ar", str(RATE),
                    "-c:a", "pcm_f32le", tmp], check=True)
    data, _ = sf.read(tmp, dtype="float32", always_2d=True)
    os.remove(tmp)
    return data


def find(folder, name):
    """Finds a pack file wherever the zip put it inside `folder`."""
    for dirpath, _dirs, files in os.walk(folder):
        if name in files:
            return os.path.join(dirpath, name)
    sys.exit("%s not found in %s" % (name, folder))


def repitch(data, ratio):
    """Plays `data` at `ratio` times the speed (pitch and length change together)."""
    frac = Fraction(ratio).limit_denominator(64)
    return resample_poly(data, frac.denominator, frac.numerator, axis=0).astype(np.float32)


def hall(data, wet_db, seconds):
    """Adds a decorrelated stereo tail: filtered noise with an exponential decay."""
    rng = np.random.default_rng(9)
    n = int(seconds * RATE)
    t = np.arange(n) / float(RATE)
    decay = np.exp(-6.9 * t / seconds)
    ir = rng.standard_normal((n, 2)).astype(np.float32) * decay[:, None]
    # Darken the tail: a three-tap moving average, applied four times.
    for _ in range(4):
        ir = (ir + np.vstack([ir[:1], ir[:-1]]) + np.vstack([ir[:2], ir[:-2]])) / 3.0
    pre = np.zeros((int(0.025 * RATE), 2), np.float32)
    ir = np.concatenate([pre, ir])
    ir /= np.sqrt(np.sum(ir ** 2, axis=0))
    wet = np.stack([fftconvolve(data[:, ch], ir[:, ch]) for ch in range(2)], axis=1)
    out = np.zeros_like(wet)
    out[:len(data)] += data
    return out + wet * (10 ** (wet_db / 20.0))


def mix(layers, packs):
    tracks = []
    for layer in layers:
        pack, name, gain, offset = layer[:4]
        data = load(find(packs[pack], name)) * (10 ** (gain / 20.0))
        if len(layer) > 4:
            data = repitch(data, layer[4])
        pad = np.zeros((int(offset * RATE), 2), np.float32)
        tracks.append(np.concatenate([pad, data]))
    n = max(len(t) for t in tracks)
    out = np.zeros((n, 2), np.float32)
    for t in tracks:
        out[:len(t)] += t
    return out


def finish(data, peak_db, max_seconds):
    # Trim trailing silence (below -55 dB of the peak).
    level = np.abs(data).max(axis=1)
    loud = np.where(level > level.max() * 10 ** (-55 / 20.0))[0]
    data = data[: loud[-1] + 1] if len(loud) else data
    if max_seconds and len(data) > max_seconds * RATE:
        data = data[: int(max_seconds * RATE)]
        fade = int(0.12 * RATE)
    else:
        fade = int(0.015 * RATE)
    fade = min(fade, len(data))
    data[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return data * (10 ** (peak_db / 20.0) / (np.abs(data).max() + 1e-9))


def encode(data, dst):
    tmp = tempfile.mktemp(suffix=".wav")
    sf.write(tmp, data, RATE, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:a", "libvorbis", "-q:a", "5", dst], check=True)
    os.remove(tmp)


def main(petaldust, nostalgiac, only=()):
    packs = {"P": petaldust, "N": nostalgiac}
    os.makedirs(OUT, exist_ok=True)
    for slot, (peak, max_s, layers) in RECIPE.items():
        if only and slot not in only:
            continue
        data = mix(layers, packs)
        if slot in REVERB:
            data = hall(data, *REVERB[slot])
        if slot.startswith("blip"):
            data = finish(data, peak, None)
            beat = int(BLIP_PERIOD * RATE)
            data = np.concatenate([data[:beat], np.zeros((max(0, beat - len(data)), 2), np.float32)])
        else:
            data = finish(data, peak, max_s)
        dst = os.path.join(OUT, slot + ".ogg")
        encode(data, dst)
        print("%-16s %5.2fs  %s" % (slot, len(data) / float(RATE), " + ".join(l[1] for l in layers)))


if __name__ == "__main__":
    if len(sys.argv) < 3 or not shutil.which("ffmpeg"):
        sys.exit(__doc__)
    unknown = [s for s in sys.argv[3:] if s not in RECIPE]
    if unknown:
        sys.exit("unknown slot: " + ", ".join(unknown))
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
