"""
Prepares a downloaded music track for game/audio/music/.

    python tools/build_music.py path/to/track.flac cirno_theme --find-loop
    python tools/build_music.py track.mp3 cirno_theme --loop 4.8 89.1
    python tools/build_music.py track.mp3 cirno_theme --end 181.5

Arrangements usually play the tune twice and fade out. With --find-loop the
tool finds where the second pass repeats the first, cuts the file there and
prints the loop start for the Theme in game/audio.rpy, so the game loops the
tune forever instead of replaying the intro and the fade. The last moments
before the cut are crossfaded into the moments before the loop start, so the
jump back is seamless even when the two passes differ slightly. --loop START
END sets the points by hand.

Without a loop the tool trims the silence at both ends and fades the tail.

Either way the result is loudness-normalised to sit under the sound effects
(EBU R128, -17 LUFS) and encoded as Ogg Vorbis, 44.1 kHz stereo.

Needs ffmpeg (with libvorbis) on PATH, and numpy.
"""

import argparse
import os
import re
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "audio", "music")

SR = 44100
TARGET_LUFS = -17.0
PEAK_CEILING = 10 ** (-1.5 / 20)


# Audio in and out #############################################################

def decode(path):
    """The first audio stream as float32 stereo at 44.1 kHz, shape (n, 2)."""
    raw = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-map", "0:a:0",
         "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
        stdout=subprocess.PIPE, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def loudness(audio):
    """Integrated loudness (LUFS) of a stereo buffer, measured by ffmpeg."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2",
         "-i", "-", "-af", "ebur128", "-f", "null", "-"],
        input=audio.astype(np.float32).tobytes(), stderr=subprocess.PIPE, check=True)
    found = re.findall(r"I:\s+(-?[\d.]+) LUFS", proc.stderr.decode("utf-8", "replace"))
    return float(found[-1])


def encode(audio, dest, quality):
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR),
         "-ac", "2", "-i", "-", "-c:a", "libvorbis", "-q:a", str(quality), dest],
        input=audio.astype(np.float32).tobytes(), check=True)


# Trimming #####################################################################

def silence_bounds(audio, floor_db=-60.0):
    """First and last sample louder than floor_db."""
    level = np.abs(audio).max(axis=1)
    loud = np.nonzero(level > 10 ** (floor_db / 20))[0]
    if len(loud) == 0:
        raise SystemExit("the track is silent")
    return max(0, loud[0] - SR // 50), min(len(audio), loud[-1] + SR // 20)


def fade_tail(audio, seconds):
    n = min(len(audio), int(seconds * SR))
    if n:
        audio[-n:] *= np.linspace(1.0, 0.0, n, dtype=np.float32)[:, None]
    return audio


# Loop finding #################################################################

def spectrogram(mono, n=2048, hop=512):
    frames = np.lib.stride_tricks.sliding_window_view(mono, n)[::hop] * np.hanning(n)
    # Lower half of the spectrum, pooled into 128 bands: plenty to tell
    # passages apart, and quick to compare.
    mag = np.abs(np.fft.rfft(frames, axis=1))[:, : n // 4]
    spec = np.log1p(mag.reshape(len(mag), 128, -1).mean(axis=2))
    spec -= spec.mean(axis=1, keepdims=True)
    spec /= np.linalg.norm(spec, axis=1, keepdims=True) + 1e-9
    return spec, SR / hop


def find_repeat(mono, usable_end):
    """
    The lag (seconds) at which the track best repeats itself, and the span
    (start, end, in seconds) over which the repeat holds.
    """
    spec, fps = spectrogram(mono)
    last = int(usable_end * fps)
    best = (-1.0, 0)
    for lag in range(int(20 * fps), last - int(20 * fps)):
        span = last - lag
        score = float(np.mean(np.sum(spec[:span] * spec[lag:lag + span], axis=1)))
        if score > best[0]:
            best = (score, lag)
    score, lag = best
    if score < 0.75:
        raise SystemExit("no clear repeat found (best match {:.2f}); use --loop START END".format(score))

    sim = np.sum(spec[: last - lag] * spec[lag:last], axis=1)
    per_sec = [float(sim[int(s * fps):int((s + 1) * fps)].mean()) for s in range(int(len(sim) / fps))]
    good = [s for s, v in enumerate(per_sec) if v > 0.85]
    return lag / fps, float(good[0]), float(good[-1] + 1), score


def refine_lag(mono, lag_s, start_s, end_s):
    """
    Sample-accurate lag. Checks windows along the span and keeps the lag where
    the two passes match best; the passes can differ in places (a varied
    melody, a new drum fill), so a strong match anywhere wins over the median.
    """
    lag0 = int(round(lag_s * SR))
    search = int(0.03 * SR)
    picks = []
    for t in np.linspace(start_s + 0.5, end_s - 1.5, 24):
        a = mono[int(t * SR):int(t * SR) + SR // 2]
        b = mono[int(t * SR) + lag0 - search:int(t * SR) + lag0 + search + SR // 2]
        if len(b) < len(a) + 2 * search:
            continue
        corr = np.correlate(b, a, mode="valid")
        energy = np.sqrt(np.convolve(b ** 2, np.ones(len(a)), mode="valid")) * np.linalg.norm(a) + 1e-12
        k = int(np.argmax(corr / energy))
        picks.append((float(corr[k] / energy[k]), lag0 - search + k))
    best = max(c for c, _ in picks)
    close = [lag for c, lag in picks if c > best - 0.02]
    return int(np.median(close)), best


def matching_run(mono, lag, start_s, end_s, need=3.0, threshold=0.9):
    """
    The first stretch of at least `need` seconds where the second pass matches
    the first sample for sample (waveform correlation above `threshold`).
    Returns (start, end) in seconds, or None.
    """
    step = 0.25
    run = None
    t = start_s
    while t + step <= end_s:
        a = mono[int(t * SR):int((t + step) * SR)]
        b = mono[int(t * SR) + lag:int((t + step) * SR) + lag]
        c = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
        if c > threshold:
            run = (run[0], t + step) if run else (t, t + step)
            if run[1] - run[0] >= need:
                return run
        else:
            run = None
        t += step
    return None


def snap_to_onset(mono, t, reach=0.35):
    """Moves t onto the nearest note attack, a few ms before it."""
    hop = SR // 200
    lo, hi = int((t - reach) * SR), int((t + reach) * SR)
    seg = mono[lo:hi]
    energy = np.array([np.sum(seg[i:i + hop] ** 2) for i in range(0, len(seg) - hop, hop)])
    rise = np.diff(np.log(energy + 1e-9))
    return lo + int(np.argmax(rise) + 1) * hop - int(0.004 * SR)


def bake_loop(audio, loop_start, loop_end, xfade_s):
    """
    Cuts at loop_end and crossfades the samples before it into the samples
    before loop_start, so jumping from the end back to loop_start is seamless.
    """
    n = int(xfade_s * SR)
    out = audio[:loop_end].copy()
    ramp = np.linspace(0.0, 1.0, n, dtype=np.float32)[:, None]
    out[loop_end - n:] = (1 - ramp) * audio[loop_end - n:loop_end] + ramp * audio[loop_start - n:loop_start]
    return out


# Main #########################################################################

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("name", help="file stem, e.g. cirno_theme")
    ap.add_argument("--find-loop", action="store_true", help="find a seamless loop automatically")
    ap.add_argument("--loop", nargs=2, type=float, metavar=("START", "END"), help="loop points in seconds")
    ap.add_argument("--xfade", type=float, default=0.12, help="loop crossfade in seconds (default 0.12)")
    ap.add_argument("--start", type=float, help="without a loop: cut the track from here (seconds)")
    ap.add_argument("--end", type=float, help="without a loop: cut the track here (seconds)")
    ap.add_argument("--fade", type=float, default=1.5, help="without a loop: tail fade (default 1.5)")
    ap.add_argument("--quality", type=float, default=6.0, help="Vorbis quality (default 6)")
    args = ap.parse_args()

    audio = decode(args.source)
    length = len(audio) / SR
    head, tail = silence_bounds(audio)
    loop_note = None

    if args.find_loop or args.loop:
        # Loop points are measured from the first sound, after leading silence.
        audio = audio[head:].copy()
        mono = audio.mean(axis=1)
        if args.loop:
            loop_start = int(args.loop[0] * SR) - head
            loop_end = int(args.loop[1] * SR) - head
        else:
            # Stop looking before the closing fade: the last point still within
            # 6 dB of the track's typical level.
            hop = SR // 2
            levels = np.array([np.sqrt(np.mean(mono[i:i + hop] ** 2)) for i in range(0, len(mono) - hop, hop)])
            typical = np.median(levels)
            usable_end = (np.nonzero(levels > typical / 2)[0][-1] + 1) * 0.5
            lag_s, rep_start, rep_end, score = find_repeat(mono, usable_end)
            lag, wave = refine_lag(mono, lag_s, rep_start, rep_end)
            # Loop inside a stretch where the passes match exactly, so the
            # crossfade blends two copies of the same audio.
            run = matching_run(mono, lag, rep_start, usable_end - lag / SR)
            if run is None:
                print("warning: the two passes never match exactly; the loop relies on the crossfade")
                run = (rep_start, rep_start + 2.0)
            loop_start = snap_to_onset(mono, run[0] + args.xfade + 0.5, reach=0.3)
            loop_end = loop_start + lag
            if loop_end > usable_end * SR:
                raise SystemExit("the repeat runs into the fade; use --loop START END")
            print("repeat every {:.4f}s (spectral match {:.2f}, waveform {:.2f}); exact from {:.1f}s".format(
                lag / SR, score, wave, run[0]))
        audio = bake_loop(audio, loop_start, loop_end, args.xfade)
        loop_note = loop_start / SR
    else:
        if args.start is not None:
            head = int(args.start * SR)
        if args.end is not None:
            tail = int(args.end * SR)
        if (tail - head) / SR < 10:
            raise SystemExit("less than ten seconds left after trimming; check --start/--end")
        audio = fade_tail(audio[head:tail].copy(), args.fade)

    gain = 10 ** ((TARGET_LUFS - loudness(audio)) / 20)
    audio *= gain
    peak = float(np.abs(audio).max())
    if peak > PEAK_CEILING:
        audio *= PEAK_CEILING / peak

    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, args.name + ".ogg")
    encode(audio, dest, args.quality)

    print("{}: {:.2f}s of {:.1f}s, gain {:+.1f} dB, {} KB".format(
        os.path.relpath(dest, ROOT), len(audio) / SR, length, 20 * np.log10(gain),
        os.path.getsize(dest) // 1024))
    if loop_note is not None:
        print("loop start: {:.6f}  ->  Theme(..., loop={:.6f})".format(loop_note, loop_note))


if __name__ == "__main__":
    main()
