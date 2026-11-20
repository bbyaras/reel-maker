"""Kullanım:
  python -m reel_maker preview examples/fable52.py --out prev
  python -m reel_maker render  examples/fable52.py --ses ses --out reel.mp4
"""
import argparse, importlib.util, os, sys

from reel_maker.engine import Reel


def load_scenes(path):
    spec = importlib.util.spec_from_file_location("scenes_mod", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.SCENES


def main():
    ap = argparse.ArgumentParser(prog="reel_maker")
    ap.add_argument("cmd", choices=["preview", "render"])
    ap.add_argument("scenes", help="SCENES listesi içeren .py dosyası")
    ap.add_argument("--ses", default="ses", help="s0.mp3, s1.mp3... klip klasörü")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    sys.path.insert(0, os.getcwd())
    reel = Reel(load_scenes(a.scenes), a.ses)
    if a.cmd == "preview":
        reel.preview(a.out or "prev"); print("önizleme kareleri:", a.out or "prev")
    else:
        print("yazıldı:", reel.render(a.out or "reel.mp4"), f"({reel.total:.1f} sn)")


if __name__ == "__main__":
    main()
