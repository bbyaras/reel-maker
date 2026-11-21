"""Reel motoru: ortak çizim yardımcıları + Reel sınıfı (önizleme, render, ses karıştırma)."""
import sys, math, re, subprocess, functools, os, json
import numpy as np, imageio.v2 as imageio, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FG, MUT, AC = (246,240,231), (158,148,136), (217,119,87)
OK, BAD, CARD, EDGE, DARK = (111,198,134), (236,100,92), (38,34,30), (66,59,51), (22,19,17)
import font_roboto  # pip: font-roboto (Apache-2.0, Türkçe karakter destekli)
_RD = os.path.join(os.path.dirname(font_roboto.__file__), "files")
B, R = os.path.join(_RD, "Roboto-Bold.ttf"), os.path.join(_RD, "Roboto-Regular.ttf")

def _find_mono():
    """Kod yazısı için monospace font: REEL_MONO_FONT, sonra yaygın sistem/paket yolları, yoksa Roboto."""
    cands = [os.environ.get("REEL_MONO_FONT", "")]
    try:
        import matplotlib; cands.append(os.path.join(matplotlib.get_data_path(), "fonts/ttf/DejaVuSansMono.ttf"))
    except ImportError: pass
    cands += ["C:/Windows/Fonts/consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "/Library/Fonts/Courier New.ttf", "/System/Library/Fonts/Supplemental/Courier New.ttf"]
    return next((p for p in cands if p and os.path.exists(p)), R)
M = _find_mono()

@functools.lru_cache(None)
def font(n, s): return ImageFont.truetype(n, s)
def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def pr(t, s, d=.5): return ease((t - s) / d)
def back(x):  # hafif taşan giriş
    x = clamp(x); c = 1.7; return 1 + (c+1)*(x-1)**3 + c*(x-1)**2

# ---------- şekiller (2x supersample) ----------
@functools.lru_cache(None)
def shape(w, h, r, fill, outline=None, ow=2):
    k = 2; im = Image.new("RGBA", (w*k, h*k), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,w*k-1,h*k-1), r*k, fill=fill, outline=outline, width=ow*k)
    return im.resize((w, h), Image.LANCZOS)

@functools.lru_cache(None)
def card(w, h, edge=EDGE, chrome=True, fill=CARD):
    im = shape(w, h, 34, fill+(255,), edge+(255,), 2).copy(); d = ImageDraw.Draw(im)
    if chrome:
        for i, c in enumerate([(236,106,94),(244,191,79),(98,197,84)]):
            d.ellipse((34+i*30, 30, 34+i*30+16, 46), fill=c+(200,))
    return im

@functools.lru_cache(None)
def pill(text, col, size=34):
    f = font(B, size); tw = int(f.getlength(text)); w, h = tw+52, size+30
    im = shape(w, h, h//2, col+(46,), col+(200,), 2).copy()
    ImageDraw.Draw(im).text((26, 13), text, font=f, fill=col)
    return im

@functools.lru_cache(None)
def icon(kind, d, col=None):
    k = 4; col = col or (OK if kind == "check" else BAD)
    im = Image.new("RGBA", (d*k, d*k), (0,0,0,0)); g = ImageDraw.Draw(im)
    g.ellipse((0,0,d*k-1,d*k-1), fill=col+(255,))
    wd = int(d*k*.1); s = d*k
    if kind == "check":
        pts = [(.28*s,.52*s),(.44*s,.68*s),(.73*s,.34*s)]
        g.line(pts, fill=(18,16,14), width=wd, joint="curve")
        for p in (pts[0], pts[-1]): g.ellipse((p[0]-wd/2,p[1]-wd/2,p[0]+wd/2,p[1]+wd/2), fill=(18,16,14))
    else:
        g.line((.32*s,.32*s,.68*s,.68*s), fill=(18,16,14), width=wd); g.line((.68*s,.32*s,.32*s,.68*s), fill=(18,16,14), width=wd)
        for p in ((.32,.32),(.68,.68),(.68,.32),(.32,.68)): g.ellipse((p[0]*s-wd/2,p[1]*s-wd/2,p[0]*s+wd/2,p[1]*s+wd/2), fill=(18,16,14))
    return im.resize((d, d), Image.LANCZOS)

@functools.lru_cache(None)
def arrow(L, col=MUT, wd=7):
    k = 3; im = Image.new("RGBA", (L*k, 50*k), (0,0,0,0)); g = ImageDraw.Draw(im)
    y = 25*k; g.line((6*k, y, (L-10)*k, y), fill=col+(255,), width=wd*k)
    g.polygon([((L-4)*k, y), ((L-26)*k, y-15*k), ((L-26)*k, y+15*k)], fill=col+(255,))
    return im.resize((L, 50), Image.LANCZOS)

def ring(d, p, col, wd=10):
    k = 2; im = Image.new("RGBA", (d*k, d*k), (0,0,0,0)); g = ImageDraw.Draw(im)
    if p > 0: g.arc((wd*k, wd*k, d*k-wd*k, d*k-wd*k), -90, -90+360*p, fill=col+(255,), width=wd*k)
    return im.resize((d, d), Image.LANCZOS)

@functools.lru_cache(None)
def disc(d, col, alpha=255):
    k = 2; im = Image.new("RGBA", (d*k, d*k), (0,0,0,0))
    ImageDraw.Draw(im).ellipse((0,0,d*k-1,d*k-1), fill=col+(alpha,))
    return im.resize((d, d), Image.LANCZOS)

# ---------- metin ----------
@functools.lru_cache(None)
def txt(text, fn, size, col=FG, maxw=920, align="left", lh=1.22, acc=AC):
    f = font(fn, size); sp = f.getlength(" "); lines = []
    for raw in text.split("\n"):
        cur, x, on, prev = [], 0, False, " "
        for part in raw.split("*"):
            first = True
            for w in part.split(" "):
                if not w: continue
                if first and cur and prev != " " and not part.startswith(" "): x -= sp  # vurgu sınırında boşluk yoksa yapıştır
                first = False
                wl = f.getlength(w)
                if cur and x + wl > maxw: lines.append((cur, x-sp)); cur, x = [], 0
                cur.append((w, acc if on else col, x)); x += wl + sp
            if part: prev = part[-1]
            on = not on
        lines.append((cur, x-sp))
    h = int(size*lh); im = Image.new("RGBA", (maxw, h*len(lines)+int(size*.35)), (0,0,0,0)); d = ImageDraw.Draw(im)
    for i, (ws, lw) in enumerate(lines):
        off = 0 if align == "left" else (maxw-lw)/2
        for w, c, x in ws: d.text((off+x, i*h), w, font=f, fill=c)
    return im

@functools.lru_cache(None)
def wrap_code(text, size, maxw):
    f = font(M, size); out = []
    for raw in text.split("\n"):
        cur = ""
        for w in raw.split(" "):
            t = (cur+" "+w) if cur else w
            if cur and f.getlength(t) > maxw: out.append(cur); cur = w
            else: cur = t
        out.append(cur)
    return out

def code_img(text, size, maxw, shown, col=FG, key=True):
    lines = wrap_code(text, size, maxw); lh = int(size*1.5)
    im = Image.new("RGBA", (maxw+10, lh*len(lines)+10), (0,0,0,0)); d = ImageDraw.Draw(im); f = font(M, size); left = shown
    for i, ln in enumerate(lines):
        part = ln[:max(0, left)]; left -= len(ln)+1
        if not part: continue
        if key and i == 0 and part.startswith("description:"):
            d.text((0, i*lh), "description:", font=f, fill=AC); kw = f.getlength("description:")
            d.text((kw, i*lh), part[len("description:"):], font=f, fill=col)
        else: d.text((0, i*lh), part, font=f, fill=col)
    return im

def code_h(text, size, maxw): return int(size*1.5)*len(wrap_code(text, size, maxw)) + 10

# ---------- arka plan ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None, None]
    a = np.array((30,27,24), float); b = np.array((16,14,12), float)
    arr = (a*(1-y) + b*y) * np.ones((1, W, 1))
    im = Image.fromarray(arr.astype("uint8"), "RGB"); d = ImageDraw.Draw(im)
    for gx in range(40, W, 60):
        for gy in range(40, H, 60): d.ellipse((gx-1, gy-1, gx+1, gy+1), fill=(46,41,36))
    return im
BG = make_bg()
def make_glow(d=1500):
    yy, xx = np.mgrid[0:d, 0:d]; r = np.sqrt((xx-d/2)**2 + (yy-d/2)**2)/(d/2)
    a = (np.clip(1-r, 0, 1)**2*62).astype("uint8")
    return Image.fromarray(a, "L")
GLOW = make_glow(); GLOWC = Image.new("RGB", GLOW.size, AC)

# ---------- sahne içeriği ----------
class S:
    def __init__(s, fr, ga): s.fr, s.ga = fr, ga
    def put(s, layer, x, y, a=1.0):
        a *= s.ga
        if a <= .004: return
        m = layer.getchannel("A")
        if a < 1: m = m.point(lambda v: int(v*a))
        s.fr.paste(layer, (int(x), int(y)), m)
    def pop(s, layer, x, y, t, st, d=.5, slide=44, dx=0):
        p = pr(t, st, d); s.put(layer, x + (1-p)*dx, y + (1-p)*slide, p)

def header(s, t, num, tag, sub, title, tsize=84):
    if num == "check": b = icon("check", 104, AC)
    else:
        b = disc(104, AC).copy(); ImageDraw.Draw(b).text((52, 50), str(num), font=font(B, 62), fill=(24,20,17), anchor="mm")
    s.pop(b, 80, 150, t, .05, .5, 0)
    s.pop(txt(tag, B, 44, AC), 210, 143, t, .15, .5, 20)
    s.pop(txt(sub, B, 32, MUT), 210, 200, t, .25, .5, 20)
    s.pop(txt(title, B, tsize), 80, 300, t, .4, .6, 40)


# ---------- süre / altyazı / render ----------
def mp3_dur(p):
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", p], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); return int(m[1])*3600 + int(m[2])*60 + float(m[3])


class Reel:
    """scenes: [(sahne_fonksiyonu(s, t, D), [altyazı cümleleri]), ...]
    ses_dir: s0.mp3, s1.mp3, ... (sahne başına bir klip). Klip yoksa süre, cümle uzunluğundan tahmin edilir."""

    def __init__(self, scenes, ses_dir, lead=0.35, tail=0.6, cps=12.5):
        self.scenes, self.ses, self.lead = scenes, ses_dir, lead
        self.n = len(scenes)
        self.clips = [os.path.join(ses_dir, f"s{i}.mp3") for i in range(self.n)]
        self.aud = [mp3_dur(p) if os.path.exists(p) else sum(len(x) for x in sn)/cps
                    for p, (_, sn) in zip(self.clips, scenes)]
        capf = os.path.join(ses_dir, "captions.json")  # tools/split_audio.py çıktısı: cümle zamanları
        self.caps = json.load(open(capf)) if os.path.exists(capf) else None
        self.durs = [a + lead + tail for a in self.aud]
        self.starts = [sum(self.durs[:i]) for i in range(self.n)]
        self.total = sum(self.durs)

    def cues(self, i):
        """i. sahnenin cümle başlangıçları (sahne saniyesi). Sahne fonksiyonları animasyonu bunlara bağlayabilir: s.cues[k]."""
        sents = self.scenes[i][1]; tot = sum(len(x) for x in sents); acc = 0; out = []
        for k, sn in enumerate(sents):
            out.append(self.lead + (self.caps[i][k][0] if self.caps else self.aud[i]*acc/tot)); acc += len(sn)
        return out

    def caption(self, s, t, i):
        sents = self.scenes[i][1]; tot = sum(len(x) for x in sents); acc = 0
        for k, sn in enumerate(sents):
            if self.caps:  # ölçülmüş cümle zamanları
                st, en = self.lead + self.caps[i][k][0], self.lead + self.caps[i][k][1]
            else:  # tahmin: karakter oranı
                st = self.lead + self.aud[i]*acc/tot; en = self.lead + self.aud[i]*(acc+len(sn))/tot; acc += len(sn)
            if st-.05 <= t < en+.05:
                im = txt(sn, B, 58, FG, 860, "center", 1.2)
                h = im.height + 60
                box = shape(920, h, 36, (10,9,8,205), (80,72,63,255), 2).copy(); box.alpha_composite(im, (30, 26))
                p = pr(t, st, .25); s.put(box, 80, 1700 - h//2 + (1-p)*20 - 40, p * (1 - pr(t, en-.08, .12)))
                return

    def frame_at(self, i, t):
        gt = self.starts[i] + t; fr = BG.copy()
        gx = 540 - 750 + 80*math.sin(gt*.35); gy = 250 + 60*math.cos(gt*.28)
        fr.paste(GLOWC, (int(gx), int(gy)), GLOW)
        D = self.durs[i]; ga = 1 - ease((t-(D-.35))/.35)
        s = S(fr, ga); s.cues = self.cues(i)
        self.scenes[i][0](s, t, D)
        self.caption(s, t, i)
        d = ImageDraw.Draw(fr); seg = (920 - (self.n-1)*10)/self.n
        for k in range(self.n):
            x0 = 80 + k*(seg+10); fill = clamp((gt - self.starts[k])/self.durs[k])
            d.rounded_rectangle((x0, 62, x0+seg, 70), 4, fill=(54,48,42))
            if fill > 0: d.rounded_rectangle((x0, 62, x0+max(8, seg*fill), 70), 4, fill=AC)
        return fr

    def preview(self, outdir, points=None):
        """Her sahneden sahne sonuna yakın bir kare kaydeder (points: [(sahne, saniye), ...])."""
        os.makedirs(outdir, exist_ok=True)
        points = points or [(i, self.durs[i] - 1.0) for i in range(self.n)]
        for n, (i, t) in enumerate(points):
            self.frame_at(i, min(t, self.durs[i] - .5)).save(os.path.join(outdir, f"p{n}.png"))

    def render(self, out):
        missing = [p for p in self.clips if not os.path.exists(p)]
        if missing: raise SystemExit("Eksik ses klipleri: " + ", ".join(missing))
        silent = out + ".sessiz.mp4"
        w = imageio.get_writer(silent, fps=FPS, codec="libx264", quality=9, macro_block_size=None)
        for i in range(self.n):
            for f in range(round(self.durs[i]*FPS)): w.append_data(np.asarray(self.frame_at(i, f/FPS)))
        w.close()
        cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-i", silent] + sum([["-i", p] for p in self.clips], [])
        fl = ";".join(f"[{i+1}:a]aresample=44100,adelay={int((self.starts[i]+self.lead)*1000)}:all=1[a{i}]" for i in range(self.n))
        fl += ";" + "".join(f"[a{i}]" for i in range(self.n)) + f"amix=inputs={self.n}:normalize=0,alimiter=limit=0.95[aout]"
        cmd += ["-filter_complex", fl, "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{self.total:.2f}", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode: raise SystemExit(r.stderr[-800:])
        os.remove(silent)
        return out
