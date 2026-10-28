# Практическая работа: организация автоматизации тестирования (Python)

**Выполнил:** Лисевич Арсений
**Группа:** Исп/п23-09.2
**Дисциплина:** Поддержка и тестирование программных модулей
**Кейс:** «Вега-Банк» — онлайн-банк для физических лиц

## Что внутри

| Файл / папка | Назначение |
|---|---|
| `transfer.html` | учебная форма перевода между счетами с атрибутами `data-test-id` |
| `features/transfer.feature` | сценарии на Gherkin (успешный перевод, недостаточно средств, нулевая сумма) |
| `features/steps/transfer_steps.py` | реализация шагов на Python + Playwright |
| `features/environment.py` | запуск браузера, настройка поиска по `data-test-id` |
| `db_check.py` | работа с БД через `sqlite3`: `get_balance`, `transfer` в одной транзакции |
| `make_html_report.py` | сборка HTML-отчёта из JSON-результатов behave |
| `requirements.txt` | зависимости проекта |
| `.github/workflows/tests.yml` | CI: установка зависимостей, прогон тестов, публикация отчёта |
| `reports/` | `behave.json` и `behave-report.html` (создаются при прогоне) |
| `docs/` | `index.html` — отчёт, который публикуется на GitHub Pages |
| `screenshots/` | скриншоты с GitHub для отчёта |
| `Отчёт_....docx` | отчёт по заданиям 1–6 и контрольным вопросам |

## Запуск

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

behave -f json -o reports/behave.json features
python make_html_report.py reports/behave.json reports/behave-report.html

python db_check.py
```

Ожидаемый результат: `3 scenarios passed`, `18 steps passed`, `OK` в конце.

После прогона отчёт открывается двойным щелчком: `reports\behave-report.html`.

## Ссылки

- Репозиторий: https://github.com/scifki/vega-bank-qa
- HTML-отчёт (GitHub Pages): https://scifki.github.io/vega-bank-qa/
- Прогоны CI: https://github.com/scifki/vega-bank-qa/actions

## Результаты

- 3 сценария / 18 шагов — все пройдены
- HTML-отчёт: 100 % успешных тестов
- CI GitHub Actions: зелёный прогон, `behave-report.html` публикуется артефактом
