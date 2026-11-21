"""Tek parça anlatımı sahne kliplerine (s0.mp3, s1.mp3...) böler ve cümle zamanlarını (captions.json) çıkarır.

Yöntem: ffmpeg ile sessizlik aralıkları bulunur. Altyazıdaki cümleler sırayla bu aralıklara dinamik
programlamayla yerleştirilir: her cümlenin süresi karakter sayısıyla orantılı olmalı, cümle sonlarında
sessizlik uzun olmalı (sahne sonlarında daha da uzun). Böylece hem sahne kesimleri hem altyazı zamanları
cümle düzeyinde ses ile eşleşir.

  python tools/split_audio.py examples/fable52.py anlatim.mp3 ses
"""
import json, os, re, subprocess, sys
import imageio_ffmpeg

sys.path.insert(0, os.getcwd())
from reel_maker.__main__ import load_scenes

FF = imageio_ffmpeg.get_ffmpeg_exe()


def silences(mp3, noise="-30dB", min_gap=0.18):
    r = subprocess.run([FF, "-i", mp3, "-af", f"silencedetect=n={noise}:d={min_gap}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    total = int(d[1])*3600 + int(d[2])*60 + float(d[3])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return total, list(zip(st, en))


def align(sents, scene_end, total, sil, w_gap=3.0, w_scene=5.0):
    """sents: cümle listesi (düz); scene_end[k]: k. cümle bir sahnenin son cümlesi mi.
    Dönüş: cümle sınırı olarak seçilen sessizlik indeksleri (len(sents)-1 adet)."""
    n, m = len(sents), len(sil)
    chars = [len(x) + 8 for x in sents]
    rate = sum(chars) / total
    mid = [(a + b)/2 for a, b in sil]; gap = [b - a for a, b in sil]
    INF = float("inf")
    # best[j][c]: j. cümle sınırı c. sessizlikte iken en iyi maliyet
    best = [[INF]*m for _ in range(n-1)]; prev = [[-1]*m for _ in range(n-1)]
    def seg_cost(a, b, k):
        exp = chars[k] / rate; dur = b - a
        return (dur/exp - 1)**2
    for c in range(m):
        best[0][c] = seg_cost(0.0, mid[c], 0) - (w_gap + (w_scene if scene_end[0] else 0))*gap[c]
    for j in range(1, n-1):
        for c in range(m):
            for p in range(c):
                if best[j-1][p] == INF: continue
                v = best[j-1][p] + seg_cost(mid[p], mid[c], j) - (w_gap + (w_scene if scene_end[j] else 0))*gap[c]
                if v < best[j][c]: best[j][c], prev[j][c] = v, p
    tot, last = INF, -1
    for c in range(m):
        if best[n-2][c] == INF: continue
        v = best[n-2][c] + seg_cost(mid[c], total, n-1)
        if v < tot: tot, last = v, c
    idx = [last]
    for j in range(n-2, 0, -1): idx.append(prev[j][idx[-1]])
    return idx[::-1]


def main(scenes_py, mp3, outdir):
    scenes = load_scenes(scenes_py)
    total, sil = silences(mp3)
    sents, scene_end, owner = [], [], []
    for i, (_, sn) in enumerate(scenes):
        for k, x in enumerate(sn):
            sents.append(x); scene_end.append(k == len(sn)-1); owner.append(i)
    idx = align(sents, scene_end, total, sil)
    # cümle konuşma aralıkları: önceki sessizliğin bitişi -> sonraki sessizliğin başlangıcı
    speech = []
    for k in range(len(sents)):
        s0 = 0.0 if k == 0 else sil[idx[k-1]][1]
        e0 = total if k == len(sents)-1 else sil[idx[k]][0]
        speech.append((s0, e0))
    bounds = [0.0]
    for k in range(len(sents)-1):
        if scene_end[k]: bounds.append((sil[idx[k]][0] + sil[idx[k]][1]) / 2)
    bounds.append(total)
    os.makedirs(outdir, exist_ok=True)
    caps = [[] for _ in scenes]
    for k, (a, b) in enumerate(speech):
        i = owner[k]; caps[i].append([round(a - bounds[i], 3), round(b - bounds[i], 3)])
        print(f"s{i} {a:6.2f}-{b:6.2f}  {len(sents[k])/(b-a):4.1f} kar/sn  {sents[k][:44]}")
    for i in range(len(scenes)):
        subprocess.run([FF, "-y", "-i", mp3, "-ss", str(bounds[i]), "-to", str(bounds[i+1]),
                        "-c:a", "libmp3lame", "-q:a", "2", os.path.join(outdir, f"s{i}.mp3")],
                       capture_output=True, check=True)
    json.dump(caps, open(os.path.join(outdir, "captions.json"), "w"))
    print("sahne sınırları (sn):", [round(b, 2) for b in bounds])


if __name__ == "__main__":
    main(*sys.argv[1:4])
