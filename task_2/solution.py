import requests
from bs4 import BeautifulSoup
import csv

URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"


def fetch_animal_counts(url):
    """
    Функция для сбора количества животных.
    """
    counts = {}
    page_number = 1

    while url:

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for animal in soup.select(".mw-category-group > ul > li > a"):
            name = animal.text.strip()

            if name and 'Подкатегория:' not in animal['href']:
                first_letter = name[0].upper()
                counts[first_letter] = counts.get(first_letter, 0) + 1

        next_page = soup.find('a', string='Следующая страница')

        if next_page and 'href' in next_page.attrs:
            url = f"https://ru.wikipedia.org{next_page['href']}"
        else:
            url = None

        print(f"Обработана страница {page_number}")
        page_number += 1

    return counts


def save_to_csv(data, filename="beasts.csv"):
    """
    Функция для сохранения данных в CSV-файл.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Буква", "Количество"])
        writer.writerows(data.items())

    print(f"Данные успешно сохранены в файл {filename}")


if __name__ == "__main__":
    print("Начинаем сбор данных...")
    animal_counts = fetch_animal_counts(URL)
    print("Сбор данных завершён. Сохраняем результаты...")
    save_to_csv(animal_counts)
    print("Готово!")
