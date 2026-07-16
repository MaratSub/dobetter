from scrapling.fetchers import StealthyFetcher
import json

url = "https://www.apple.com/"

print("Открываю сайт Apple, подожди немного...")

page = StealthyFetcher.fetch(
    url=url,
    headless=True,
    timeout=60000,           # 60 секунд
    network_idle=True,
    disable_resources=False
)

# Извлекаем текст из тега <title>
page_title = page.css('title::text').get() or "Заголовок не найден"

print(f"Страница успешно загружена! Заголовок: {page_title}\n")

# Сбор блоков
blocks = []

selectors = ["header", "nav", "section", ".hero", "main", "footer"]

for sel in selectors:
    for el in page.css(sel):
        text = el.get_all_text(strip=True)
        if len(text) > 30:   # отбрасываем пустые блоки
            blocks.append({
                "tag": el.tag,
                "classes": el.attrib.get("class", "")[:120],
                "id": el.attrib.get("id", ""),
                "text_preview": text[:350]
            })

print(f"Найдено {len(blocks)} блоков для анализа.\n")

# Промпт для ИИ
prompt = f"""Ты — эксперт по веб-структуре. 
Проанализируй следующие блоки со страницы {url} и определи тип каждого:

{json.dumps(blocks, ensure_ascii=False, indent=2)}

Для каждого блока укажи:
- type: hero | header | navigation | main_content | product | footer | other
- short_description: 1-2 предложения о содержимом

Ответ строго в JSON формате."""

print("=== СКОПИРУЙ ВЕСЬ ТЕКСТ НИЖЕ И ВСТАВЬ В DEEPSEEK (или любой другой ИИ) ===\n")
print(prompt)
print("\n=== КОНЕЦ ПРОМПТА ===")