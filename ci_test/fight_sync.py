"""
CI only. Builds the fight preview from the two recording passes.

    python3 fight_sync.py VIDEO AUDIO EVENTS GAME_DIR WARP OUT

VIDEO was recorded with RENPY_TIMEWARP=WARP (game time runs WARP times real
time). AUDIO is the real-time pass with the effects channel muted after the
sync gavel; it carries the music and the text blips. EVENTS lists each sound
effect the picture pass played, as "<game seconds after the sync flash>
<file>"; those files are mixed back in on the event channel's rules (a new
effect cuts off the one before), at the gain the gavel measured.
"""

import array
import subprocess
import sys

video, audio, events, game_dir, warp, out = sys.argv[1:7]
warp = float(warp)
LEAD = 0.6              # game seconds after the sync cue to start the output
VFPS = 15.0


def pcm(path, rate, extra=()):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path] + list(extra) +
                         ["-ac", "1", "-ar", str(rate), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h")
    a.frombytes(raw[:len(raw) // 2 * 2])
    return a


# The first white frame of the picture pass.
W, H = 32, 18
raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", video, "-vf", "fps=%g,scale=%d:%d,format=gray" % (VFPS, W, H),
     "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
n = W * H
vt = None
for i in range(len(raw) // n):
    if sum(raw[i * n:(i + 1) * n]) / n > 225:
        vt = i / VFPS
        break
if vt is None:
    sys.exit("no sync flash in the video")

# The gavel: the first loud 10 ms after the first long silence.
RATE = 8000
a = pcm(audio, RATE)
win = RATE // 100
quiet, armed, at = 0, False, None
for k, i in enumerate(range(0, len(a) - win, win)):
    lv = max(abs(x) for x in a[i:i + win])
    if lv < 300:
        quiet += 1
        armed = armed or quiet >= 60
    elif armed and lv > 3000:
        at = k * 0.01
        break
    else:
        quiet = 0
if at is None:
    sys.exit("no gavel in the audio")

# Effect gain: the recorded gavel against the gavel file.
rec = a[int(at * RATE):int((at + 0.6) * RATE)]
src = pcm(game_dir + "/audio/sfx/gavel.ogg", RATE)
gain = max(abs(x) for x in rec) / float(max(abs(x) for x in src))
print("flash at %.2fs of video, gavel at %.2fs of audio, effect gain %.3f" % (vt, at, gain))

ev = []
for line in open(events):
    t, fn = line.split(None, 1)
    ev.append((float(t), fn.strip()))
ev.sort()

inputs = ["-ss", "%.3f" % (vt + LEAD / warp), "-i", video,
          "-ss", "%.3f" % (at + LEAD), "-i", audio]
chains = ["[0:v]setpts=(PTS-STARTPTS)*%g,fps=30[v]" % warp,
          "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[m]"]
labels = ["[m]"]
for k, (t, fn) in enumerate(ev):
    nxt = ev[k + 1][0] if k + 1 < len(ev) else None
    start = t - LEAD
    if start < 0:
        continue
    inputs += ["-i", game_dir + "/" + fn]
    idx = 2 + len(labels) - 1
    f = "[%d:a]aformat=sample_rates=48000:channel_layouts=stereo" % idx
    if nxt is not None:
        d = max(0.03, nxt - t)
        f += ",atrim=0:%.3f,afade=t=out:st=%.3f:d=0.02" % (d, d - 0.02)
    ms = int(round(start * 1000))
    f += ",volume=%.4f,adelay=%d|%d[s%d]" % (gain, ms, ms, k)
    chains.append(f)
    labels.append("[s%d]" % k)
    print("  %6.2fs  %s" % (start, fn))
chains.append("%samix=inputs=%d:normalize=0:duration=first,alimiter=limit=0.97[a]" % ("".join(labels), len(labels)))

subprocess.run(
    ["ffmpeg", "-v", "error", "-y"] + inputs +
    ["-filter_complex", ";".join(chains), "-map", "[v]", "-map", "[a]",
     "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
    check=True)
