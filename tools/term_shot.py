from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
shots = root / "screenshots"
shots.mkdir(exist_ok=True)

log = [line.rstrip() for line in (root / "tools" / "behave_log.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
log = [line for line in log if not line.startswith("USING RUNNER")]

cmd1 = (
    r"PS C:\...\Агенты> .\.venv\Scripts\python.exe -m behave "
    r"-f json -o reports\behave.json features"
)
cmd2 = r"PS C:\...\Агенты> .\.venv\Scripts\python.exe make_html_report.py reports\behave.json reports\behave-report.html"
cmd3 = r"PS C:\...\Агенты> .\.venv\Scripts\python.exe db_check.py"

font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
lines = [(cmd1, font)] + [(line, font) for line in log]
lines += [("", font), (cmd2, font), ("Отчёт: reports\\behave-report.html", font)]
lines += [("", font), (cmd3, font), ("OK", font)]

pad = 28
line_h = 30
width = max(int(font.getlength(t)) for t, _ in lines) + 2 * pad
height = len(lines) * line_h + 2 * pad

img = Image.new("RGB", (width, height), "#1e1e1e")
draw = ImageDraw.Draw(img)
y = pad
for text, f in lines:
    draw.text((pad, y), text, font=f, fill="#7ee787" if text.startswith("PS ") else "#d4d4d4")
    y += line_h

img.save(shots / "behave_output.png")
print("terminal shot ok", img.size)

