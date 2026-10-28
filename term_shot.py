from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).parent
shots = root / "screenshots"
shots.mkdir(exist_ok=True)

log = (root / "behave_log.txt").read_text(encoding="utf-8-sig").strip().splitlines()
log = [line.rstrip() for line in log if line.strip()]

cmd1 = (
    r"PS C:\...\Агенты> .\.venv\Scripts\python.exe -m behave "
    r"-f allure_behave.formatter:AllureFormatter -o allure-results features"
)
log = [cmd1] + [line for line in log if line != "USING RUNNER: behave.runner:Runner"]
cmd2 = r"PS C:\...\Агенты> .\.venv\Scripts\python.exe db_check.py"

font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 20)

lines = [(line, font) for line in log]
lines.append(("", font))
lines.append((cmd2, font))
lines.append(("OK", font))

pad = 28
line_h = 30
width = max(int(font.getlength(t)) for t, _ in lines) + 2 * pad
height = len(lines) * line_h + 2 * pad

img = Image.new("RGB", (width, height), "#1e1e1e")
draw = ImageDraw.Draw(img)
y = pad
for text, f in lines:
    color = "#7ee787" if text.startswith("PS ") else "#d4d4d4"
    if "passed" in text or text == "OK" and y > line_h * 8:
        color = "#d4d4d4"
    draw.text((pad, y), text, font=f, fill=color)
    y += line_h

img.save(shots / "behave_output.png")
print("terminal shot ok", img.size)
