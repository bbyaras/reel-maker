# reel-maker

Python ile 9:16 (1080x1920) Instagram Reel üretir: animasyonlu sahneler, ses ile eşleşen altyazı, ilerleme çubuğu ve sesli final MP4. Tarayıcı veya ekran kaydı gerekmez.

*English: renders animated vertical reels (scenes, synced captions, voiceover mix) from plain Python scene functions using Pillow + ffmpeg.*

## Kurulum

```bash
pip install -r requirements.txt
```

Metin fontu `font-roboto` paketinden gelir (Türkçe karakterler dahil), ek bir şey gerekmez. Kod yazısı için sırayla şunlar aranır: `REEL_MONO_FONT` ortam değişkeni, matplotlib'in DejaVu Sans Mono'su, Windows'ta Consolas, Linux'ta DejaVu Sans Mono, macOS'ta Courier New. Hiçbiri yoksa Roboto kullanılır. İstediğiniz monospace fontu vermek için:

```bash
export REEL_MONO_FONT=/yol/font.ttf
```

## Nasıl çalışır

Bir reel, `SCENES` listesidir. Her eleman bir sahne fonksiyonu ve o sahnenin altyazı cümleleridir:

```python
from reel_maker.engine import *

def sc_ornek(s, t, D):                      # s: çizim yüzeyi, t: sahne saniyesi, D: sahne süresi
    header(s, t, 1, "DETAY 1", "FİYAT", "Daha yeni ama *daha ucuz*")
    s.pop(card(920, 200), 80, 660, t, 1.0)  # 1. saniyede kayarak gelen kart

SCENES = [(sc_ornek, ["Bir: Daha yeni ama daha ucuz.", "..."])]
```

Hazır yapı taşları: `card`, `pill`, `icon` (check/cross), `txt` (`*vurgu*` söz dizimi), `shape`, `code_img` (yazılma efektli kod), `arrow`, `ring`, `header`.
Sahne süresi = ses klibi süresi + 0,95 sn. Altyazılar cümle uzunluğuna göre ses süresine dağıtılır.

## Adımlar

1. **Önizleme** (ses gerekmez, süreler cümle uzunluğundan tahmin edilir):
   ```bash
   python -m reel_maker preview examples/fable52.py --out prev
   ```
2. **Anlatımı üret.** Altyazı cümlelerini sahne sahne, sahneler arası boş satırla tek parça seslendirin (ElevenLabs, VidIQ vb.) ve `anlatim.mp3` olarak kaydedin.
3. **Sahnelere böl** (paragraf aralarındaki sessizliklerden):
   ```bash
   python tools/split_audio.py examples/fable52.py anlatim.mp3 ses
   ```
   `ses/s0.mp3 … s6.mp3` oluşur. Sınırlar yanlışsa komutu `noise` değerini değiştirerek tekrar çalıştırın veya klipleri elle düzeltin.
4. **Render + ses karıştırma:**
   ```bash
   python -m reel_maker render examples/fable52.py --ses ses --out reel.mp4
   ```

## Örnekler

- [`examples/claude_skills.py`](examples/claude_skills.py): Claude skill'lerini doğru kullanma, 5 hata.
- [`examples/fable52.py`](examples/fable52.py): Fable 5.2 hakkında 5 detay.

## Notlar

- Türkçe karakterler Roboto ile test edildi (ç, ğ, ı, İ, ö, ş, ü).
- `ffmpeg`, `imageio-ffmpeg` paketiyle birlikte gelir; ayrıca kurmanız gerekmez.
- Üretilen MP4 ve ses dosyaları `.gitignore` ile repoya girmez.
