from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
shots = root / "screenshots"
shots.mkdir(exist_ok=True)

W, H = 1500, 1150
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

title_f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
box_f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
small_f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)

d.text((60, 35), "Схема: от репозитория с тестами до отчёта", font=title_f, fill="#1f2937")

boxes = [
    ("1. Репозиторий с тестами (GitHub)", "features/*.feature, шаги, environment.py", "#dbeafe"),
    ("2. Сервер CI — GitHub Actions", "на каждый push запускает пайплайн tests.yml", "#e0e7ff"),
    ("3. Машина runner (Linux VM, Docker)", "ставит зависимости и Chromium", "#ede9fe"),
    ("4. Запуск тестов параллельно", "behave + Allure, несколько сценариев сразу", "#f3e8ff"),
    ("5. reports/behave.json", "сырые результаты каждого шага", "#fae8ff"),
    ("6. reports/behave-report.html", "HTML-отчёт: «3 из 3 пройдено, 100 % успеха»", "#fce7f3"),
    ("7. Артефакт / публикация", "ссылка на отчёт для QA, владельцев продукта, демо", "#ffe4e6"),
]

x, y = 150, 110
bw, bh, gap = 1200, 110, 34
centers = []
for i, (head, sub, color) in enumerate(boxes):
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=18, fill=color, outline="#94a3b8", width=2)
    d.text((x + 26, y + 22), head, font=box_f, fill="#111827")
    d.text((x + 26, y + 62), sub, font=small_f, fill="#374151")
    centers.append(y + bh)
    y += bh + gap

for i in range(len(boxes) - 1):
    top = centers[i] + 4
    bottom = centers[i] + gap - 8
    cx = x + bw // 2
    d.line([cx, top, cx, bottom], fill="#475569", width=3)
    d.polygon([(cx - 9, bottom - 10), (cx + 9, bottom - 10), (cx, bottom + 2)], fill="#475569")

# Боковой блок про тестовый стенд и БД
bx, by = 150, y - 4
d.rounded_rectangle([bx, by, bx + 1200, by + 96], radius=18, fill="#f1f5f9", outline="#94a3b8", width=2)
d.text((bx + 26, by + 16), "Отдельно: тестовый стенд «Вега-Банка» и тестовая БД", font=box_f, fill="#111827")
d.text(
    (bx + 26, by + 56),
    "UI-тесты открывают форму в браузере, тесты БД проверяют остатки через SQLAlchemy/psycopg2",
    font=small_f,
    fill="#374151",
)

img.save(shots / "schema.png")
print("schema ok", img.size)

