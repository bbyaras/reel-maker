"""Örnek 1: Claude skill'lerini doğru kullanma (7 sahne)."""
from reel_maker.engine import *

def sc_hook(s, t, D):
    s.pop(pill("CLAUDE SKILL", AC, 36), 80, 330, t, .1)
    s.pop(txt("Skill'in\nçalışmıyor mu?", B, 128, lh=1.1), 80, 430, t, .3, .7, 60)
    s.pop(txt("*Sorun skill'de değil.*", B, 82), 80, 760, t, 2.4, .6)
    labels = ["Description", "SKILL.md", "Tek iş", "Örnek", "Test"]
    for i, lb in enumerate(labels):
        st = 4.0 + i*.55; y = 1010 + i*104
        row = Image.new("RGBA", (920, 90), (0,0,0,0)); row.alpha_composite(shape(920, 90, 26, CARD+(255,), EDGE+(255,)), (0,0))
        row.alpha_composite(disc(52, AC), (22, 19)); ImageDraw.Draw(row).text((48, 44), str(i+1), font=font(B, 32), fill=(24,20,17), anchor="mm")
        ImageDraw.Draw(row).text((100, 44), lb, font=font(B, 40), fill=FG, anchor="lm")
        s.pop(row, 80, y, t, st, .5, 0, dx=-60)
    s.pop(txt("5 hata, 5 çözüm", B, 40, MUT), 80, 940, t, 3.6)

def sc_desc(s, t, D):
    header(s, t, 1, "HATA 1", "DESCRIPTION", "Claude skill'i *description'a* bakıp seçer")
    s.pop(card(920, 200), 80, 660, t, 1.0)
    s.pop(pill("Belirsiz", BAD), 740, 735, t, 1.2)
    s.put(code_img("description: PDF aracı", 38, 600, 99, MUT), 125, 745, pr(t, 1.2))
    s.pop(icon("cross", 56), 912, 732, t, 1.4, .4, 0)
    h = 70 + code_h("description: PDF'den metin çıkarır, birleştirir, böler. \"PDF\" veya \"formu doldur\" denince kullan.", 38, 760) + 40
    s.pop(card(920, h, OK), 80, 900, t, 2.2)
    s.pop(pill("Net", OK), 830, 925, t, 2.4)
    txt_good = "description: PDF'den metin çıkarır, birleştirir, böler. \"PDF\" veya \"formu doldur\" denince kullan."
    shown = int((t-3.0)*34) if t > 3.0 else 0
    s.put(code_img(txt_good, 38, 760, shown), 125, 985, pr(t, 2.9))
    y2 = 900 + h + 50
    s.pop(txt("Formül", B, 34, MUT), 80, y2, t, 6.0)
    s.pop(pill("Ne yapar", OK, 40), 80, y2+60, t, 6.2)
    s.pop(txt("+", B, 56, MUT), 330, y2+54, t, 6.4)
    s.pop(pill("Ne zaman", AC, 40), 390, y2+60, t, 6.6)

def sc_bloat(s, t, D):
    header(s, t, 2, "HATA 2", "ŞİŞKİN SKILL.MD", "Her şeyi tek dosyaya *doldurma*")
    s.pop(card(920, 560), 80, 660, t, .9)
    rows = [("skill/", None, 0, MUT, ""), ("SKILL.md", OK, 90, OK, "kısa"), ("reference.md", MUT, 250, MUT, "detay"), ("scripts/", MUT, 150, MUT, "kesin işler")]
    for i, (nm, col, blen, bc, lab) in enumerate(rows):
        st = 1.5 + i*.8; y = 760 + i*105; ind = 0 if i == 0 else 50
        dim = 1.0 if i < 2 else (1 - .5*pr(t, 6.0, .6))
        p = pr(t, st, .5)
        s.put(txt(nm, M, 44, FG if i else MUT), 125+ind, y, p*dim)
        if blen:
            bp = pr(t, st+.3, .9)
            bar = shape(max(8, int(blen*bp)), 26, 13, bc+(255,))
            s.put(bar, 500, y+14, p*dim)
            if bp > .95: s.put(txt(lab, B, 32, bc, maxw=300), 500+blen+16, y+4, pr(t, st+1.1, .3)*dim)
    s.pop(txt("Claude detayı *sadece gerekince* okur", B, 54, maxw=920), 80, 1310, t, 5.8, .6)
    a = pr(t, 6.4, .5)
    if a > 0:
        s.put(pill("gerekince → reference.md", AC, 34), 80, 1440, a)

def sc_one(s, t, D):
    header(s, t, 3, "HATA 3", "TEK İŞ", "Bir skill = *bir iş*")
    s.pop(card(920, 340, BAD), 80, 520, t, .9) if False else None
    s.pop(card(920, 370, chrome=False), 80, 560, t, .9)
    s.pop(icon("cross", 56), 912, 584, t, 1.0, .4, 0)
    s.pop(txt("super-skill", M, 44, BAD), 125, 592, t, 1.1)
    chips = ["PDF", "Mail", "Excel", "Kod", "Tweet", "Özet", "Rapor", "Çeviri"]
    pos = [(125,690),(300,720),(470,680),(630,725),(180,790),(380,810),(580,795),(740,780)]
    for i, (c, (x, y)) in enumerate(zip(chips, pos)):
        s.pop(pill(c, MUT, 34), x, y, t, 1.8 + i*.18, .35, 12)
    s.pop(txt("karışık, tetiklenmesi zor", B, 36, MUT), 125, 870, t, 3.6)
    names = ["pdf-oku", "özet-yaz", "rapor-çiz"]
    for i, nm in enumerate(names):
        x = 80 + i*320; st = 4.4 + i*.6
        s.pop(card(280, 250, OK, chrome=False), x, 1030, t, st)
        s.pop(icon("check", 56), x+26, 1060, t, st+.1, .4, 0)
        s.pop(txt(nm, M, 36, FG, maxw=240), x+26, 1160, t, st+.2)
        s.pop(txt("tek iş", B, 30, OK, maxw=240), x+26, 1210, t, st+.3)
    s.pop(txt("Küçük, net, birbirini tamamlayan skill'ler", B, 44, MUT), 80, 1330, t, 6.4)

def sc_example(s, t, D):
    header(s, t, 4, "HATA 4", "BELİRSİZ TALİMAT", "\"Güzel yaz\" değil, *örnek ver*")
    s.pop(card(920, 170, chrome=False), 80, 640, t, .9)
    s.pop(icon("cross", 56), 112, 697, t, 1.0, .4, 0)
    s.put(code_img("Profesyonel bir özet yaz.", 40, 700, 99, MUT, False), 190, 700, pr(t, 1.1))
    gt = "3 madde, en fazla 15 kelime.\nÖrnek: \"Gelir %12 arttı.\""
    s.pop(card(920, 260, OK, chrome=False), 80, 850, t, 2.0)
    s.pop(icon("check", 56), 112, 902, t, 2.1, .4, 0)
    s.put(code_img(gt, 40, 700, int(max(0, t-2.8)*30), FG, False), 190, 905, pr(t, 2.7))
    s.pop(txt("Çıktı", B, 34, MUT), 80, 1170, t, 5.0)
    outs = ["Gelir %12 arttı.", "Maliyet %4 düştü.", "340 yeni müşteri."]
    for i, o in enumerate(outs):
        s.pop(card(920, 90, EDGE, chrome=False), 80, 1230+i*105, t, 5.3 + i*.5, .45, 30)
        s.put(disc(16, AC), 120, 1230+i*105+37, pr(t, 5.4+i*.5)) if True else None
        s.pop(txt(o, B, 40, FG, maxw=700), 160, 1230+i*105+18, t, 5.4 + i*.5, .45, 30)

def sc_test(s, t, D):
    header(s, t, 5, "HATA 5", "TEST ETMEMEK", "Yaz → *gerçek istemle dene* → düzelt", 76)
    nodes = [("Yaz", 80), ("Dene", 410), ("Düzelt", 740)]
    for i, (nm, x) in enumerate(nodes):
        st = 1.0 + i*.7; p = back((t-st)/.5)
        d = int(260*clamp(p)) if p > 0 else 0
        if d > 20:
            cx = x+130; cy = 860
            s.put(disc(d, CARD), cx-d//2, cy-d//2, 1)
            s.put(ring(d, 1, EDGE, 6), cx-d//2, cy-d//2, 1)
            s.put(txt(nm, B, 54, FG, maxw=260, align="center"), x, cy-34, pr(t, st+.2, .3))
    for i in range(2):
        s.pop(arrow(70, MUT), 325+i*330, 836, t, 1.7+i*.7, .4, 0)
    # çalışan döngü halkası
    if t > 4.0:
        ph = ((t-4.0)/2.4) % 3; idx = int(ph); frac = ph - idx; x = nodes[idx][1]
        s.put(ring(260, clamp(frac*1.15), AC, 12), x, 730, 1)
    s.pop(card(920, 150, chrome=False), 80, 1090, t, 3.4)
    s.pop(txt("Tetiklenmedi mi?", B, 38, MUT, maxw=340), 118, 1130, t, 3.5)
    s.pop(arrow(60, AC), 465, 1117, t, 3.7, .3, 0)
    s.pop(txt("Description'ı *düzelt*", B, 38, maxw=420), 540, 1130, t, 3.8)
    s.pop(card(920, 150, chrome=False), 80, 1270, t, 5.0)
    s.pop(txt("Yanlış çıktı mı?", B, 38, MUT, maxw=340), 118, 1310, t, 5.1)
    s.pop(arrow(60, AC), 465, 1297, t, 5.3, .3, 0)
    s.pop(txt("Talimatı *netleştir*", B, 38, maxw=420), 540, 1310, t, 5.4)
    s.pop(pill("/skill-adı ile elle çağır", OK, 38), 80, 1470, t, 7.4)

def sc_end(s, t, D):
    header(s, t, "check", "ÖZET", "KONTROL LİSTESİ", "5 maddede *doğru skill*")
    items = ["Description net", "SKILL.md kısa", "Tek iş", "Örnek var", "Test edildi"]
    for i, it in enumerate(items):
        st = 1.2 + i*.75; p = back((t-st)/.45)
        y = 650 + i*128
        s.pop(card(920, 106, EDGE, chrome=False), 80, y, t, st, .4, 24)
        d = int(64*clamp(p))
        if d > 6: s.put(icon("check", d), 112+(64-d)//2, y+21+(64-d)//2, 1)
        s.pop(txt(it, B, 52, FG, maxw=700), 210, y+22, t, st+.1, .4, 24)
    b = shape(920, 120, 60, AC+(255,)).copy(); g = ImageDraw.Draw(b)
    g.polygon([(70,34),(70,86),(92,68),(114,86),(114,34)], fill=(24,20,17))
    g.text((150, 60), "Kaydet · sonraki skill'ini bu listeyle yaz", font=font(B, 37), fill=(24,20,17), anchor="lm")
    s.pop(b, 80, 1360, t, 6.0, .6, 40)

SCENES = [
 (sc_hook, ["Claude skill'in çalışmıyor mu?", "Sorun büyük ihtimalle skill'de değil.", "Çoğu kişi aynı beş hatayı yapıyor."]),
 (sc_desc, ["Bir: Description.", "Claude hangi skill'i kullanacağını description'a bakarak seçer.", "\"PDF aracı\" yazma.", "Ne yaptığını ve ne zaman devreye gireceğini yaz."]),
 (sc_bloat, ["İki: Şişkin skill md dosyası.", "Her şeyi tek dosyaya doldurma.", "Skill md dosyası kısa kalsın,", "detayları ayrı dosyalara, kesin işleri script'e koy."]),
 (sc_one, ["Üç: Bir skill, bir iş.", "Her şeyi yapan süper skill yerine", "küçük ve net skill'ler yaz."]),
 (sc_example, ["Dört: Belirsiz talimat.", "\"Profesyonel özet yaz\" yerine", "formatı ve bir örnek ver:", "üç madde, en fazla on beş kelime."]),
 (sc_test, ["Beş: Test etmemek.", "Gerçek isteminle dene.", "Tetiklenmediyse description'ı,", "yanlış çıktıysa talimatı düzelt.", "Gerekirse slash ile elle çağır."]),
 (sc_end, ["Description net, skill md dosyası kısa,", "tek iş, örnek var, test edildi.", "Kaydet, bir sonraki skill'ini bu listeyle yaz."]),
]

