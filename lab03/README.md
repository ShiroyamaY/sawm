# Лабораторная №3 — Предотвращение XSS в Django (uv + SQLite)

## Запуск
1. Установите/активируйте окружение uv:
   - Windows PowerShell:
     ```bash
     uv venv
     .\.venv\Scripts\Activate.ps1
     uv pip install django
     ```
2. Миграции и запуск:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Страницы
- Безопасная: `/` — экранирование вывода, валидация, строгая CSP.
- Уязвимая (демо XSS): `/vulnerable/` — преднамеренно небезопасный вывод.

## Демонстрация XSS
На странице `/vulnerable/` введите в поле «Сообщение» любой из вариантов:
- `<script>location.href='https://example.com'</script>` — редирект.
- `<img src=x onerror=alert('XSS')>` — выполнение JS при ошибке загрузки.

На странице `/` те же payload‑ы выводятся как текст (не выполняются).

## Что сделано против XSS
- По умолчанию Django экранирует `{{ переменные }}` в шаблонах.
- Удалён небезопасный фильтр `|safe` в «безопасной» версии.
- Серверная валидация email и обязательных полей.
- CSP для безопасной страницы: `default-src 'self'` (без `'unsafe-inline'`).

## Модель
`guests.models.Guest(user, e_mail, text_message, data_time_message)` хранит записи.


