"""Собирает наглядный HTML-отчёт из JSON-вывода behave (без Allure).

Использование:
    python make_html_report.py reports/behave.json reports/behave-report.html
"""

import json
import sys
from datetime import datetime
from html import escape
from pathlib import Path

STATUS_RU = {"passed": "пройден", "failed": "упал", "skipped": "пропущен", "untested": "не запускался"}


def fmt_duration(seconds):
    seconds = seconds or 0
    if seconds < 1:
        return f"{seconds * 1000:.0f} мс"
    return f"{seconds:.2f} с"


def build(data):
    scenarios = []
    for feature in data:
        for element in feature.get("elements", []):
            if element.get("type") not in ("scenario", "scenario_outline"):
                continue
            steps = element.get("steps", [])
            duration = sum(s.get("result", {}).get("duration", 0) or 0 for s in steps)
            scenarios.append(
                {
                    "feature": feature.get("name", ""),
                    "name": element.get("name", ""),
                    "status": element.get("status", "untested"),
                    "duration": duration,
                    "steps": [
                        (
                            f"{s.get('keyword', '').strip()} {s.get('name', '')}",
                            s.get("result", {}).get("status", "untested"),
                            s.get("result", {}).get("duration", 0) or 0,
                        )
                        for s in steps
                    ],
                }
            )

    total = len(scenarios)
    passed = sum(1 for s in scenarios if s["status"] == "passed")
    failed = sum(1 for s in scenarios if s["status"] == "failed")
    total_steps = sum(len(s["steps"]) for s in scenarios)
    passed_steps = sum(1 for s in scenarios for st in s["steps"] if st[1] == "passed")
    total_time = sum(s["duration"] for s in scenarios)
    percent = round(passed / total * 100) if total else 0

    rows = []
    details = []
    for i, scenario in enumerate(scenarios, start=1):
        color = "#1a7f37" if scenario["status"] == "passed" else "#cf222e"
        rows.append(
            f"<tr><td>{i}</td><td>{escape(scenario['name'])}</td>"
            f"<td>{escape(scenario['feature'])}</td>"
            f"<td style='color:{color};font-weight:600'>{STATUS_RU.get(scenario['status'], scenario['status'])}</td>"
            f"<td>{fmt_duration(scenario['duration'])}</td></tr>"
        )
        step_html = "".join(
            f"<li class='{status}'><span>{escape(name)}</span>"
            f"<em>{STATUS_RU.get(status, status)} · {fmt_duration(dur)}</em></li>"
            for name, status, dur in scenario["steps"]
        )
        details.append(
            f"<details{' open' if scenario['status'] != 'passed' else ''}>"
            f"<summary><b>{i}. {escape(scenario['name'])}</b>"
            f"<span class='badge {scenario['status']}'>{STATUS_RU.get(scenario['status'], scenario['status'])}</span></summary>"
            f"<ul class='steps'>{step_html}</ul></details>"
        )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Отчёт о тестировании — перевод между счетами</title>
<style>
  body {{ font-family: "Segoe UI", Arial, sans-serif; margin: 0; background: #f6f8fa; color: #1f2328; }}
  .wrap {{ max-width: 1000px; margin: 0 auto; padding: 32px 24px 64px; }}
  h1 {{ font-size: 26px; margin: 0 0 4px; }}
  .sub {{ color: #59636e; margin-bottom: 24px; }}
  .cards {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 28px; }}
  .card {{ background: #fff; border: 1px solid #d1d9e0; border-radius: 12px; padding: 16px 22px; min-width: 150px; }}
  .card .num {{ font-size: 28px; font-weight: 700; }}
  .card .lbl {{ color: #59636e; font-size: 13px; }}
  .ok {{ color: #1a7f37; }} .bad {{ color: #cf222e; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d1d9e0; border-radius: 12px; overflow: hidden; }}
  th, td {{ padding: 10px 12px; border-bottom: 1px solid #eaeef2; text-align: left; font-size: 14px; }}
  th {{ background: #f6f8fa; font-weight: 600; }}
  h2 {{ margin: 32px 0 12px; font-size: 19px; }}
  details {{ background: #fff; border: 1px solid #d1d9e0; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; }}
  summary {{ cursor: pointer; display: flex; justify-content: space-between; gap: 12px; align-items: center; }}
  .badge {{ font-size: 12px; padding: 2px 10px; border-radius: 999px; color: #fff; }}
  .badge.passed {{ background: #1a7f37; }} .badge.failed {{ background: #cf222e; }}
  ul.steps {{ list-style: none; padding: 12px 0 0; margin: 0; }}
  ul.steps li {{ display: flex; justify-content: space-between; gap: 12px; padding: 6px 10px; border-left: 3px solid #d1d9e0; margin-bottom: 6px; background: #f6f8fa; font-size: 14px; }}
  ul.steps li.passed {{ border-left-color: #1a7f37; }} ul.steps li.failed {{ border-left-color: #cf222e; }}
  ul.steps em {{ color: #59636e; font-style: normal; white-space: nowrap; }}
  footer {{ color: #59636e; font-size: 12px; margin-top: 32px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Отчёт о тестировании</h1>
  <div class="sub">Форма «Перевод между своими счетами» · сформирован {datetime.now():%d.%m.%Y %H:%M}</div>

  <div class="cards">
    <div class="card"><div class="num">{total}</div><div class="lbl">сценариев</div></div>
    <div class="card"><div class="num ok">{passed}</div><div class="lbl">пройдено</div></div>
    <div class="card"><div class="num bad">{failed}</div><div class="lbl">упало</div></div>
    <div class="card"><div class="num">{percent}%</div><div class="lbl">успешных</div></div>
    <div class="card"><div class="num">{passed_steps}/{total_steps}</div><div class="lbl">шагов пройдено</div></div>
    <div class="card"><div class="num">{fmt_duration(total_time)}</div><div class="lbl">время прогона</div></div>
  </div>

  <h2>Сценарии</h2>
  <table>
    <tr><th>№</th><th>Сценарий</th><th>Функционал</th><th>Статус</th><th>Время</th></tr>
    {''.join(rows)}
  </table>

  <h2>Шаги</h2>
  {''.join(details)}

  <footer>Отчёт сформирован скриптом make_html_report.py из результатов behave.</footer>
</div>
</body>
</html>
"""


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "reports/behave.json")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "reports/behave-report.html")
    data = json.loads(src.read_text(encoding="utf-8"))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(build(data), encoding="utf-8")
    print(f"Отчёт: {dst}")


if __name__ == "__main__":
    main()
