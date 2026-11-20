"""Örnek 3: Prompt caching, 5 kural (7 sahne)."""
from reel_maker.engine import *


def sc_hook(s, t, D):
    s.pop(pill("CLAUDE API", AC, 36), 80, 330, t, .1)
    s.pop(txt("Prompt\ncaching:\n5 kural", B, 128, lh=1.08), 80, 430, t, .3, .7, 60)
    labels = ["Baştan eşleşir", "Değişeni sona koy", "Tek satırla başla", "Fiyatı bil", "Sonucu ölç"]
    for i, lb in enumerate(labels):
        st = 2.6 + i*.5; y = 1010 + i*104
        row = Image.new("RGBA", (920, 90), (0,0,0,0)); row.alpha_composite(shape(920, 90, 26, CARD+(255,), EDGE+(255,)), (0,0))
        row.alpha_composite(disc(52, AC), (22, 19)); ImageDraw.Draw(row).text((48, 44), str(i+1), font=font(B, 32), fill=(24,20,17), anchor="mm")
        ImageDraw.Draw(row).text((100, 44), lb, font=font(B, 40), fill=FG, anchor="lm")
        s.pop(row, 80, y, t, st, .5, 0, dx=-60)


def sc_prefix(s, t, D):
    header(s, t, 1, "KURAL 1", "PREFIX EŞLEŞME", "Önbellek *baştan eşleşir*")
    blocks = [("tools", 1.2), ("system", 2.2), ("messages", 3.2)]
    changed = t > 6.4
    for i, (nm, st) in enumerate(blocks):
        y = 650 + i*170
        bad = changed and nm != "tools"
        col = BAD if bad else OK
        label = ("yeniden hesaplanır" if nm == "messages" else "değişti") if bad else "önbellekte"
        s.pop(card(920, 130, col, chrome=False), 80, y, t, st, .5)
        s.pop(txt(nm, M, 46, FG, maxw=400), 120, y+38, t, st+.1)
        pl = pill(label, col, 34)
        s.pop(pl, 1000 - 30 - pl.width, y+40, t, st+.2)
        if i < 2: s.pop(shape(6, 40, 3, MUT+(255,)), 538, y+130, t, st+.3, .3, 0)
    s.pop(txt("Bir bayt değişir: sonrası *yeniden yazılır*", B, 46, maxw=920), 80, 1210, t, 7.0, .6)


def sc_order(s, t, D):
    header(s, t, 2, "KURAL 2", "SIRALAMA", "Sabiti başa, *değişeni sona*")
    s.pop(card(920, 230, BAD, chrome=False), 80, 650, t, 1.4)
    s.pop(pill("her istekte değişir", BAD, 32), 650, 680, t, 1.7)
    s.put(code_img('system: "Saat 14:03:11.\nUzman asistansın..."', 36, 760, 99, FG, False), 120, 750, pr(t, 1.6))
    s.pop(card(920, 330, OK, chrome=False), 80, 930, t, 6.6)
    s.pop(pill("sabit, önbellekte", OK, 32), 650, 960, t, 6.9)
    s.put(code_img('system: "Uzman asistansın..."\nuser: "Saat 14:03:11.\nSoru..."', 36, 760, 99, FG, False), 120, 1030, pr(t, 6.8))
    s.pop(txt("Saat, kimlik gibi şeyler *user mesajına*", B, 44, MUT, maxw=920), 80, 1330, t, 8.4)


def sc_oneline(s, t, D):
    header(s, t, 3, "KURAL 3", "TEK SATIR", "*Tek satırla* başla")
    code = 'client.messages.create(\n    model="...",\n    cache_control={"type": "ephemeral"},\n    messages=[...],\n)'
    s.pop(card(920, 420), 80, 650, t, 1.0)
    s.put(shape(800, 48, 10, AC+(70,)), 108, 735+2*51-6, pr(t, 5.0, .4))
    s.put(code_img(code, 34, 800, int(max(0, t-1.6)*34), FG, False), 120, 735, pr(t, 1.5))
    s.pop(txt("Son önbelleğe alınabilir blok *otomatik* önbelleğe alınır", B, 44, maxw=920), 80, 1130, t, 7.0, .6)
    s.pop(pill("çok kısa istem önbelleğe girmez", BAD, 36), 80, 1330, t, 11.0)
    s.pop(txt("alt sınır modele göre 512 – 4096 token", B, 40, MUT, maxw=920), 80, 1410, t, 12.0)


def sc_cost(s, t, D):
    header(s, t, 4, "KURAL 4", "FİYAT ÇARPANLARI", "Önbellek *okuması ~10 kat ucuz*")
    rows = [("Normal", 1.0, MUT, "1x", 1.2), ("Yazma", 1.25, AC, "~1,25x", 4.0), ("Okuma", 0.1, OK, "~0,1x", 6.6)]
    for i, (nm, mult, col, lab, st) in enumerate(rows):
        y = 680 + i*190
        s.pop(card(920, 150, col if col != MUT else EDGE, chrome=False), 80, y, t, st, .5)
        s.pop(txt(nm, B, 46, FG if col != MUT else MUT, maxw=260), 120, y+44, t, st+.1)
        full = int(520*mult/1.25); p = pr(t, st+.3, .9)
        s.put(shape(max(10, int(full*p)), 40, 20, col+(255,)), 330, y+55, pr(t, st+.3, .3))
        s.put(txt(lab, B, 38, col, maxw=200), 330 + int(full*p) + 16, y+46, pr(t, st+1.0, .3))
    s.pop(pill("tekrar eden bağlamda %90'a kadar tasarruf", OK, 36), 80, 1300, t, 10.2, .5)


def sc_verify(s, t, D):
    header(s, t, 5, "KURAL 5", "DOĞRULA", "Sonucu *ölç*")
    s.pop(card(920, 140, chrome=False), 80, 650, t, 1.2)
    s.put(code_img("usage.cache_read_input_tokens", 38, 800, 99, FG, False), 125, 705, pr(t, 1.4))
    s.pop(txt("0 ise: *sessiz bir bozucu var*", B, 50, maxw=920), 80, 860, t, 3.6, .6)
    rows = ["datetime.now() sistem promptunda", "sıralanmamış json.dumps()", "değişen araç listesi"]
    for i, r in enumerate(rows):
        st = 6.4 + i*1.3; y = 1000 + i*110
        s.pop(card(920, 92, BAD, chrome=False), 80, y, t, st, .45, 24)
        s.pop(icon("cross", 52), 110, y+20, t, st+.1, .4, 0)
        s.pop(txt(r, M, 36, FG, maxw=700), 190, y+26, t, st+.15, .4, 24)


def sc_end(s, t, D):
    header(s, t, "check", "ÖZET", "KONTROL LİSTESİ", "Caching *tek bakışta*")
    items = ["Baştan eşleşir", "Değişeni sona koy", "Tek satırla başla", "Okuma ~0,1x fiyat", "usage ile ölç"]
    for i, it in enumerate(items):
        st = 1.2 + i*.8; p = back((t-st)/.45)
        y = 650 + i*128
        s.pop(card(920, 106, EDGE, chrome=False), 80, y, t, st, .4, 24)
        d = int(64*clamp(p))
        if d > 6: s.put(icon("check", d), 112+(64-d)//2, y+21+(64-d)//2, 1)
        s.pop(txt(it, B, 50, FG, maxw=700), 210, y+22, t, st+.1, .4, 24)
    b = shape(920, 120, 60, AC+(255,)).copy(); g = ImageDraw.Draw(b)
    g.polygon([(70,34),(70,86),(92,68),(114,86),(114,34)], fill=(24,20,17))
    g.text((150, 60), "Kaydet · API'ye yazmadan önce bak", font=font(B, 37), fill=(24,20,17), anchor="lm")
    s.pop(b, 80, 1360, t, 6.4, .6, 40)


SCENES = [
    (sc_hook, ["Claude API faturanı düşürmenin en kolay yolu prompt caching.", "İşte bilmen gereken beş kural."]),
    (sc_prefix, ["Bir: Önbellek baştan eşleşir.", "Araçlar, sistem, sonra mesajlar sırasıyla.", "Tek bir bayt değişirse, ondan sonraki her şey yeniden hesaplanır."]),
    (sc_order, ["İki: Sabit olanı başa, değişeni sona koy.", "Sistem promptuna saat ya da rastgele kimlik yazma.", "Onları kullanıcı mesajına ekle."]),
    (sc_oneline, ["Üç: Tek satırla başla.", "Üst seviye cache control parametresi, son önbelleğe alınabilir bloğu otomatik önbelleğe alır.", "Çok kısa istemler önbelleğe girmez.", "Alt sınır modele göre beş yüz on iki ile dört bin doksan altı token arası."]),
    (sc_cost, ["Dört: Fiyat çarpanlarını bil.", "Önbelleğe yazmak yaklaşık yüzde yirmi beş pahalı, önbellekten okumak yaklaşık onda biri.", "Tekrar eden bağlamda tasarruf yüzde doksana kadar çıkar."]),
    (sc_verify, ["Beş: Sonucu ölç.", "Cache read input tokens sıfırsa, sessiz bir bozucu var.", "Sistem promptunda saat, sıralanmamış JSON ya da değişen araç listesi."]),
    (sc_end, ["Özetle: baştan eşleşir, değişeni sona koy,", "tek satırla başla, fiyatı bil, sonucu ölç.", "Kaydet."]),
]
