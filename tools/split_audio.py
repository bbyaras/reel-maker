"""Tek parça anlatımı, sessizlik aralıklarından sahne klipleri (s0.mp3, s1.mp3...) olarak böler.

Sahne sınırı tahmini: her sahnenin altyazı cümlelerinin karakter oranı. Her sınır için tahmine yakın ve uzun
sessizlik aralığının ortası seçilir.

  python tools/split_audio.py examples/fable52.py anlatim.mp3 ses
"""
import os, re, subprocess, sys
import imageio_ffmpeg

sys.path.insert(0, os.getcwd())
from reel_maker.__main__ import load_scenes

FF = imageio_ffmpeg.get_ffmpeg_exe()


def main(scenes_py, mp3, outdir, noise="-30dB", min_gap=0.18):
    scenes = load_scenes(scenes_py)
    r = subprocess.run([FF, "-i", mp3, "-af", f"silencedetect=n={noise}:d={min_gap}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    total = int(dur[1])*3600 + int(dur[2])*60 + float(dur[3])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    mids = [((a + b)/2, b - a) for a, b in zip(st, en)]
    chars = [sum(len(x) for x in sn) for _, sn in scenes]
    bounds, acc = [0.0], 0
    for c in chars[:-1]:
        acc += c; want = total*acc/sum(chars)
        bounds.append(min(mids, key=lambda m: abs(m[0] - want) - 4*m[1])[0] if mids else want)
    bounds.append(total)
    os.makedirs(outdir, exist_ok=True)
    for i in range(len(scenes)):
        subprocess.run([FF, "-y", "-i", mp3, "-ss", str(bounds[i]), "-to", str(bounds[i+1]),
                        "-c:a", "libmp3lame", "-q:a", "2", os.path.join(outdir, f"s{i}.mp3")],
                       capture_output=True, check=True)
    print("sınırlar (sn):", [round(b, 2) for b in bounds])


if __name__ == "__main__":
    main(*sys.argv[1:4])
