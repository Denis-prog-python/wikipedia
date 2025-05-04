import wikipedia
from typing import List, Optional

# Устанавливаем язык Википедии (можно изменить)
wikipedia.set_lang("ru")


def get_page_content(page_title: str) -> Optional[str]:
    """Получает содержимое страницы Википедии."""
    try:
        page = wikipedia.page(page_title)
        return page.content
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Уточните запрос. Возможные варианты: {e.options[:5]}")
        return None
    except wikipedia.exceptions.PageError:
        print("Страница не найдена.")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def get_paragraphs(content: str) -> List[str]:
    """Разбивает содержимое страницы на параграфы."""
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    return paragraphs


def browse_paragraphs(paragraphs: List[str]):
    """Позволяет пользователю листать параграфы статьи."""
    current_idx = 0
    while True:
        print(f"\nПараграф {current_idx + 1}/{len(paragraphs)}:")
        print(paragraphs[current_idx])

        action = input("\nДействие: [Следующий (→), Предыдущий (←), Выйти (q)] ").strip().lower()
        if action in ('→', 'next', 'n', ''):
            current_idx = min(current_idx + 1, len(paragraphs) - 1)
        elif action in ('←', 'prev', 'p'):
            current_idx = max(current_idx - 1, 0)
        elif action in ('q', 'exit', 'quit'):
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


def get_links(page_title: str) -> Optional[List[str]]:
    """Получает список связанных страниц."""
    try:
        page = wikipedia.page(page_title)
        return page.links
    except Exception as e:
        print(f"Ошибка при получении ссылок: {e}")
        return None


def browse_links(links: List[str], current_page: str):
    """Позволяет пользователю переходить по связанным страницам."""
    while True:
        print("\nСвязанные страницы:")
        for i, link in enumerate(links[:20], 1):  # Показываем первые 20 ссылок
            print(f"{i}. {link}")

        choice = input("\nВыберите страницу (номер), 'q' для выхода: ").strip()
        if choice.lower() in ('q', 'exit', 'quit'):
            break

        try:
            selected_idx = int(choice) - 1
            if 0 <= selected_idx < len(links):
                selected_page = links[selected_idx]
                print(f"\nПереход на страницу: {selected_page}")
                article_content = get_page_content(selected_page)
                if article_content:
                    paragraphs = get_paragraphs(article_content)
                    browse_article(selected_page, paragraphs)
            else:
                print("Некорректный номер. Попробуйте снова.")
        except ValueError:
            print("Введите число или 'q' для выхода.")


def browse_article(page_title: str, paragraphs: List[str]):
    """Основной цикл взаимодействия с одной статьей."""
    while True:
        print(f"\nТекущая страница: {page_title}")
        print("1. Листать параграфы статьи")
        print("2. Перейти на связанную страницу")
        print("3. Выйти в меню")

        choice = input("Выберите действие (1-3): ").strip()

        if choice == '1':
            browse_paragraphs(paragraphs)
        elif choice == '2':
            links = get_links(page_title)
            if links:
                browse_links(links, page_title)
        elif choice == '3':
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


def main():
    print("Поиск в Википедии")

    while True:
        query = input("\nВведите поисковый запрос (или 'q' для выхода): ").strip()
        if query.lower() in ('q', 'exit', 'quit'):
            break

        article_content = get_page_content(query)
        if article_content:
            paragraphs = get_paragraphs(article_content)
            browse_article(query, paragraphs)


if __name__ == "__main__":
    main()