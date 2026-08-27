#!/usr/bin/env python3
"""Pobiera legalne zdjęcia stock (Pexels / Unsplash — darmowa licencja) i konwertuje do WebP."""

from __future__ import annotations

import io
import json
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "public" / "assets" / "images"
UA = "SDAUTOS-demo/1.0 (local demo; attribution in CREDITS.md)"

# Źródła: Pexels License / Unsplash License — darmowe użycie komercyjne
DOWNLOADS = [
    # Hero — lakiernik / kabina (Pexels)
    {
        "url": "https://images.pexels.com/photos/3807329/pexels-photo-3807329.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "out": "hero/hero-workshop.webp",
        "size": (1920, 1080),
        "credit": "Pexels — person spray painting (photo 3807329)",
    },
    # Galeria
    {
        "url": "https://images.pexels.com/photos/3807517/pexels-photo-3807517.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "gallery/before-01.webp",
        "size": (1200, 900),
        "credit": "Pexels — car body repair (photo 3807517)",
    },
    {
        "url": "https://images.pexels.com/photos/3806249/pexels-photo-3806249.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "gallery/after-01.webp",
        "size": (1200, 900),
        "credit": "Pexels — polished car paint (photo 3806249)",
    },
    {
        "url": "https://images.pexels.com/photos/4489749/pexels-photo-4489749.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "gallery/part-01.webp",
        "size": (1200, 900),
        "credit": "Pexels — car part / spray work (photo 4489749)",
    },
    {
        "url": "https://images.pexels.com/photos/4489702/pexels-photo-4489702.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "gallery/process-01.webp",
        "size": (1200, 900),
        "credit": "Pexels — auto body process (photo 4489702)",
    },
    {
        "url": "https://images.pexels.com/photos/6870313/pexels-photo-6870313.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "gallery/polish-01.webp",
        "size": (1200, 900),
        "credit": "Pexels — car polishing (photo 6870313)",
    },
    {
        "url": "https://images.pexels.com/photos/3807277/pexels-photo-3807277.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "gallery/booth-01.webp",
        "size": (1200, 900),
        "credit": "Pexels — workshop paint work (photo 3807277)",
    },
    # Produkty / materiały
    {
        "url": "https://images.pexels.com/photos/5898101/pexels-photo-5898101.jpeg?auto=compress&cs=tinysrgb&w=800",
        "out": "products/paint-cans.webp",
        "size": (800, 600),
        "credit": "Pexels — paint materials (photo 5898101)",
    },
    {
        "url": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&q=80&fm=jpg",
        "out": "products/tools.webp",
        "size": (800, 600),
        "credit": "Unsplash — workshop tools (photo-1581094794329-c8112a89af12)",
    },
    {
        "url": "https://images.pexels.com/photos/4489733/pexels-photo-4489733.jpeg?auto=compress&cs=tinysrgb&w=800",
        "out": "products/spray-gun.webp",
        "size": (800, 600),
        "credit": "Pexels — spray equipment (photo 4489733)",
    },
    {
        "url": "https://images.pexels.com/photos/3807315/pexels-photo-3807315.jpeg?auto=compress&cs=tinysrgb&w=800",
        "out": "products/abrasive.webp",
        "size": (800, 600),
        "credit": "Pexels — sanding / prep (photo 3807315)",
    },
    {
        "url": "https://images.pexels.com/photos/6871880/pexels-photo-6871880.jpeg?auto=compress&cs=tinysrgb&w=800",
        "out": "products/polish.webp",
        "size": (800, 600),
        "credit": "Pexels — polishing compound context (photo 6871880)",
    },
    # OG
    {
        "url": "https://images.pexels.com/photos/3807329/pexels-photo-3807329.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "out": "og-default.webp",
        "size": (1200, 630),
        "credit": "Pexels — OG image base (photo 3807329)",
        "crop": "center",
    },
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def to_webp(data: bytes, out: Path, size: tuple[int, int], crop: str | None = None) -> None:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    tw, th = size
    if crop == "center":
        src_ratio = img.width / img.height
        dst_ratio = tw / th
        if src_ratio > dst_ratio:
            new_w = int(img.height * dst_ratio)
            left = (img.width - new_w) // 2
            img = img.crop((left, 0, left + new_w, img.height))
        else:
            new_h = int(img.width / dst_ratio)
            top = (img.height - new_h) // 2
            img = img.crop((0, top, img.width, top + new_h))
        img = img.resize((tw, th), Image.Resampling.LANCZOS)
    else:
        img.thumbnail((tw, th), Image.Resampling.LANCZOS)
        # Dopełnij do docelowego aspect przez letterbox ciemny (unikamy CLS przy stałych wymiary w HTML)
        canvas = Image.new("RGB", (tw, th), (15, 20, 25))
        x = (tw - img.width) // 2
        y = (th - img.height) // 2
        canvas.paste(img, (x, y))
        img = canvas
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "WEBP", quality=82, method=6)


def main() -> None:
    credits = []
    for item in DOWNLOADS:
        out = ROOT / item["out"]
        print(f"Pobieram {item['out']} …")
        try:
            data = fetch(item["url"])
            to_webp(data, out, tuple(item["size"]), item.get("crop"))
            print(f"  OK {out.stat().st_size // 1024} KB")
            credits.append({"file": item["out"], "credit": item["credit"], "source_url": item["url"].split("?")[0]})
        except Exception as exc:  # noqa: BLE001
            print(f"  BŁĄD: {exc}")

    credits_path = ROOT / "CREDITS.json"
    credits_path.write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Zapisano {credits_path}")


if __name__ == "__main__":
    main()
