# -*- coding: utf-8 -*-
"""회차별 QR 발급 스크립트.
회차 폴더명 = URL 경로. 새 회차 추가 시 ROUNDS에 (폴더명, 라벨) 추가 후 실행.
출력: qr/<폴더명>.png (여백에 라벨 캡션 포함)
"""
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE = "https://winnywin21-design.github.io/nqi"
ROUNDS = [
    ("대수_1회", "대수 · 제1회 모의평가"),
]

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr")
os.makedirs(OUT_DIR, exist_ok=True)


def load_font(size):
    for path in (r"C:\Windows\Fonts\malgun.ttf", r"C:\Windows\Fonts\gulim.ttc"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make(folder, label):
    url = f"{BASE}/{folder}/"
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # 하단 캡션 여백 추가
    cap_h = 70
    canvas = Image.new("RGB", (img.width, img.height + cap_h), "white")
    canvas.paste(img, (0, 0))
    draw = ImageDraw.Draw(canvas)
    font = load_font(30)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((canvas.width - tw) // 2, img.height + 12), label, fill="black", font=font)

    out = os.path.join(OUT_DIR, f"{folder}.png")
    canvas.save(out)
    print(f"OK  {out}\n    -> {url}")


if __name__ == "__main__":
    for folder, label in ROUNDS:
        make(folder, label)
