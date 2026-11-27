"""
Prepares a downloaded music track for game/audio/music/.

    python tools/build_music.py path/to/track.mp3 cirno_theme
    python tools/build_music.py track.flac cirno_theme --end 181.5 --fade 2.0

Trims the silence at both ends, optionally cuts the track at --start/--end,
fades the tail so the loop back to the top doesn't click, normalises loudness
to sit under the sound effects (two-pass EBU R128, -17 LUFS, -1.5 dBTP) and
encodes Ogg Vorbis at 44.1 kHz stereo.

Needs ffmpeg with libvorbis on PATH.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "audio", "music")

TARGET = "I=-17:TP=-1.5:LRA=11"


def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit("ffmpeg failed: " + " ".join(cmd))
    return proc.stderr


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        stdout=subprocess.PIPE, text=True, check=True).stdout
    return float(out.strip())


def silence_bounds(path, length):
    """First and last moment the track rises above -60 dBFS."""
    log = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
               "-af", "silencedetect=noise=-60dB:d=0.05", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    head = ends[0] if starts and starts[0] <= 0.01 and ends else 0.0
    tail = length
    if starts and (len(ends) < len(starts) or ends[-1] >= length - 0.05):
        tail = starts[-1]
    return max(0.0, head - 0.02), min(length, tail + 0.05)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("name", help="file stem, e.g. cirno_theme")
    ap.add_argument("--start", type=float, help="cut the track from here (seconds)")
    ap.add_argument("--end", type=float, help="cut the track here (seconds)")
    ap.add_argument("--fade", type=float, default=1.5, help="tail fade in seconds (default 1.5)")
    ap.add_argument("--quality", type=float, default=6.0, help="Vorbis quality (default 6)")
    args = ap.parse_args()

    length = duration(args.source)
    head, tail = silence_bounds(args.source, length)
    if args.start is not None:
        head = args.start
    if args.end is not None:
        tail = args.end
    if tail - head < 10:
        raise SystemExit("less than ten seconds left after trimming; check --start/--end")

    cut = "atrim=start={:.3f}:end={:.3f},asetpts=PTS-STARTPTS".format(head, tail)
    if args.fade > 0:
        cut += ",afade=t=out:st={:.3f}:d={:.3f}".format(tail - head - args.fade, args.fade)

    # Pass 1: measure.
    log = run(["ffmpeg", "-hide_banner", "-nostats", "-i", args.source,
               "-af", cut + ",loudnorm=" + TARGET + ":print_format=json", "-f", "null", "-"])
    stats = json.loads(log[log.rindex("{"):log.rindex("}") + 1])

    # Pass 2: apply as a single linear gain, then encode.
    norm = ("loudnorm=" + TARGET + ":linear=true"
            ":measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}"
            ":measured_thresh={input_thresh}:offset={target_offset}").format(**stats)

    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, args.name + ".ogg")
    run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", args.source,
         "-af", cut + "," + norm + ",aresample=44100",
         "-ac", "2", "-map_metadata", "-1", "-c:a", "libvorbis", "-q:a", str(args.quality), dest])

    print("{}: {:.1f}s (cut {:.2f}-{:.2f} of {:.1f}s), {:.1f} LUFS in, {} KB".format(
        os.path.relpath(dest, ROOT), duration(dest), head, tail, length,
        float(stats["input_i"]), os.path.getsize(dest) // 1024))


if __name__ == "__main__":
    main()
