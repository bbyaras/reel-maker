"""Örnek 2: Fable 5.2 hakkında 5 detay (7 sahne)."""
from reel_maker.engine import *


def sc_hook(s, t, D):
    s.pop(pill("CLAUDE · YENİ MODEL", AC, 36), 80, 330, t, .1)
    s.pop(txt("Fable 5.2\nhakkında\n5 detay", B, 128, lh=1.08), 80, 430, t, .3, .7, 60)
    labels = ["Fiyat", "Düşünme", "Effort", "Yedek model", "Hızlı mod"]
    for i, lb in enumerate(labels):
        st = 2.2 + i*.5; y = 1010 + i*104
        row = Image.new("RGBA", (920, 90), (0,0,0,0)); row.alpha_composite(shape(920, 90, 26, CARD+(255,), EDGE+(255,)), (0,0))
        row.alpha_composite(disc(52, AC), (22, 19)); ImageDraw.Draw(row).text((48, 44), str(i+1), font=font(B, 32), fill=(24,20,17), anchor="mm")
        ImageDraw.Draw(row).text((100, 44), lb, font=font(B, 40), fill=FG, anchor="lm")
        s.pop(row, 80, y, t, st, .5, 0, dx=-60)

def sc_price(s, t, D):
    header(s, t, 1, "DETAY 1", "FİYAT", "Daha yeni ama *daha ucuz*")
    rows = [("Fable 5.2", 8, 40, OK, 2.0), ("Fable 5.1", 10, 50, MUT, 6.4)]
    for k, (nm, i_, o_, col, st) in enumerate(rows):
        y = 640 + k*370
        s.pop(card(920, 330, col if col != MUT else EDGE, chrome=False), 80, y, t, st, .5)
        s.pop(txt(nm, B, 52, FG if col != MUT else MUT, maxw=600), 120, y+30, t, st+.1)
        s.pop(txt("Girdi", R, 34, MUT, maxw=140), 120, y+136, t, st+.2)
        s.pop(txt("Çıktı", R, 34, MUT, maxw=140), 120, y+226, t, st+.2)
        for j, v in enumerate((i_, o_)):
            full = 480 * (v/50.0); p = pr(t, st+.4+j*.2, .9)
            yy = y + (140 if j == 0 else 230)
            s.put(shape(max(10, int(full*p)), 34, 17, col+(255,)), 270, yy, pr(t, st+.4, .3))
            s.put(txt(f"${v}", B, 40, col, maxw=200), 270 + int(full*p) + 18, yy-10, pr(t, st+1.0, .3))
    s.pop(pill("−%20 · 1M token başına", OK, 38), 80, 1440, t, 8.6, .5)

def sc_think(s, t, D):
    header(s, t, 2, "DETAY 2", "DÜŞÜNME", "Düşünme *her zaman açık*")
    s.pop(card(920, 200, chrome=False), 80, 660, t, 1.0)
    s.put(code_img('thinking: {"type": "disabled"}', 36, 700, 99, MUT, False), 125, 745, pr(t, 1.2))
    s.pop(pill("400 hata", BAD), 760, 680, t, 1.6)
    s.pop(card(920, 200, OK, chrome=False), 80, 900, t, 3.6)
    s.put(code_img('thinking alanını boş bırak', 38, 700, 99, FG, False), 125, 985, pr(t, 3.8))
    s.pop(pill("çalışır", OK), 790, 920, t, 4.0)
    s.pop(txt("Derinliği şuradan ayarla:", B, 44, MUT), 80, 1180, t, 6.6)
    s.pop(card(920, 150, AC, chrome=False), 80, 1260, t, 7.0)
    s.put(code_img('output_config: {"effort": "high"}', 38, 800, 99, FG, False), 125, 1305, pr(t, 7.2))

def sc_effort(s, t, D):
    header(s, t, 3, "DETAY 3", "EFFORT", "*high* ile başla")
    lv = [("low", 90), ("medium", 180), ("high", 270), ("xhigh", 360), ("max", 450)]
    for i, (nm, h) in enumerate(lv):
        x = 80 + i*190; st = 1.0 + i*.45; p = pr(t, st, .7)
        hh = max(10, int(h*p)); col = AC if nm == "high" else EDGE
        s.put(shape(160, hh, 24, col+(255,)), x, 1150 - hh, pr(t, st, .2))
        s.put(txt(nm, B, 36, FG if nm == "high" else MUT, maxw=170, align="center"), x-5, 1170, pr(t, st+.3, .3))
    s.pop(pill("buradan başla", AC, 36), 80+2*190-20, 640, t, 3.2, .4, 20)
    s.pop(txt("*xhigh:* sadece kazancı ölçtüysen", B, 42, maxw=920), 80, 1270, t, 7.6)
    s.pop(txt("*max:* tavanı ölçmek için", B, 42, MUT, maxw=920), 80, 1350, t, 9.2)

def sc_fallback(s, t, D):
    header(s, t, 4, "DETAY 4", "YEDEK MODEL", "Reddedilirse *akış yarıda kalmaz*")
    nodes = [("İstek", EDGE, 1.0), ("Fable 5.2", EDGE, 2.2), ("Güvenlik reddi", BAD, 3.8), ("Yedek model", OK, 5.4), ("Yanıt", OK, 7.0)]
    for i, (nm, col, st) in enumerate(nodes):
        y = 650 + i*118
        s.pop(card(520, 92, col, chrome=False), 80, y, t, st, .45, 24)
        s.pop(txt(nm, B, 42, FG, maxw=480), 112, y+20, t, st+.1, .4, 24)
        if i < 4:
            s.pop(shape(6, 22, 3, MUT+(255,)), 330, y+95, t, st+.3, .3, 0)
    s.pop(card(920, 150, AC, chrome=False), 80, 1290, t, 8.6)
    s.put(code_img('fallbacks: "default"', 40, 800, 99, FG, False), 125, 1335, pr(t, 8.8))

def sc_fast(s, t, D):
    header(s, t, 5, "DETAY 5", "HIZLI MOD", "Aynı model, *2,5 kata kadar* hızlı")
    s.pop(txt("Çıktı hızı", B, 36, MUT), 80, 650, t, 1.6)
    s.put(txt("standart", B, 38, FG, maxw=300), 80, 720, pr(t, 2.0))
    s.put(shape(max(10, int(260*pr(t, 2.2, .8))), 40, 20, EDGE+(255,)), 80, 780, pr(t, 2.2, .2))
    p = pr(t, 4.2, 1.2)
    s.put(txt("hızlı mod", B, 38, AC, maxw=300), 80, 870, pr(t, 4.0))
    s.put(shape(max(10, int(920*0.9*p)), 40, 20, AC+(255,)), 80, 930, pr(t, 4.2, .2))
    s.pop(txt("2,5x'e kadar", B, 52, AC, maxw=500), 80, 990, t, 5.4)
    s.pop(card(920, 130, chrome=False), 80, 1130, t, 6.2)
    s.put(code_img('speed: "fast"', 42, 700, 99, FG, False), 125, 1165, pr(t, 6.4))
    s.pop(txt("Fiyat: *$16 girdi / $80 çıktı*", B, 48, maxw=920), 80, 1320, t, 7.8)

def sc_end(s, t, D):
    header(s, t, "check", "ÖZET", "KONTROL LİSTESİ", "Fable 5.2 *tek bakışta*")
    items = ["Ucuzladı: $8 / $40", "Düşünme hep açık", "Effort: high ile başla", "Yedek model hazır", "Hız lazımsa fast mode"]
    for i, it in enumerate(items):
        st = 1.2 + i*.8; p = back((t-st)/.45)
        y = 650 + i*128
        s.pop(card(920, 106, EDGE, chrome=False), 80, y, t, st, .4, 24)
        d = int(64*clamp(p))
        if d > 6: s.put(icon("check", d), 112+(64-d)//2, y+21+(64-d)//2, 1)
        s.pop(txt(it, B, 50, FG, maxw=700), 210, y+22, t, st+.1, .4, 24)
    b = shape(920, 120, 60, AC+(255,)).copy(); g = ImageDraw.Draw(b)
    g.polygon([(70,34),(70,86),(92,68),(114,86),(114,34)], fill=(24,20,17))
    g.text((150, 60), "Kaydet · geliştirirken bu listeye bak", font=font(B, 37), fill=(24,20,17), anchor="lm")
    s.pop(b, 80, 1360, t, 6.4, .6, 40)

SCENES = [
 (sc_hook, ["Fable beş nokta iki hakkında", "bilmen gereken beş ilginç detay."]),
 (sc_price, ["Bir: Daha yeni ama daha ucuz.", "Milyon token başına sekiz dolar girdi, kırk dolar çıktı.", "Fable beş nokta bir ise on ve elli dolardı."]),
 (sc_think, ["İki: Düşünme her zaman açık.", "Kapatmaya çalışırsan API hata verir.", "Derinliği effort ayarıyla belirliyorsun."]),
 (sc_effort, ["Üç: Effort'a high ile başla.", "Daha yüksek seviyeler her işte fark yaratmıyor.", "Ekstra high'ı sadece kazancı ölçtüğün yerde kullan."]),
 (sc_fallback, ["Dört: Güvenlik filtresi isteği reddederse,", "istek aynı çağrı içinde yedek modele geçebilir.", "Yani akışın yarıda kalmaz."]),
 (sc_fast, ["Beş: Hızlı mod.", "Aynı model, çıktı hızı iki buçuk katına kadar çıkıyor.", "Bedeli on altı dolar girdi, seksen dolar çıktı."]),
 (sc_end, ["Özetle: ucuzladı, hep düşünüyor,", "effort high ile başla, yedek modeli aç,", "hız lazımsa fast mode. Kaydet."]),
]

