from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


base = Path(__file__).resolve().parent
pages = sorted(base.glob("meetai7-*.png"))
font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
thumb_w, thumb_h = 420, 594
pad, label_h = 24, 34

for sheet_index in range(0, len(pages), 4):
    selected = pages[sheet_index : sheet_index + 4]
    sheet = Image.new("RGB", (thumb_w * 2 + pad * 3, (thumb_h + label_h) * 2 + pad * 3), "#20283d")
    draw = ImageDraw.Draw(sheet)
    for slot, page_path in enumerate(selected):
        image = Image.open(page_path).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col, row = slot % 2, slot // 2
        x = pad + col * (thumb_w + pad)
        y = pad + row * (thumb_h + label_h + pad)
        draw.text((x, y), f"Page {sheet_index + slot + 1}", fill="white", font=font)
        sheet.paste(image, (x, y + label_h))
    output = base / f"qa-sheet-{sheet_index // 4 + 1}.png"
    sheet.save(output, quality=92)
    print(output)
