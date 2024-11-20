import pytest
import csv
from unittest.mock import Mock
from .solution import fetch_animal_counts, save_to_csv

MOCK_HTML = """
<div class="mw-category-group">
    <ul>
        <li><a href="/wiki/Animal_A">Аист</a></li>
        <li><a href="/wiki/Animal_B">Белка</a></li>
        <li><a href="/wiki/Animal_A">Акула</a></li>
    </ul>
</div>
<a href="/wiki/Категория:Животные_по_алфавиту?page=2">Следующая страница</a>
"""

MOCK_HTML_NO_NEXT = """
<div class="mw-category-group">
    <ul>
        <li><a href="/wiki/Animal_C">Верблюд</a></li>
    </ul>
</div>
"""


@pytest.fixture
def mock_requests_get(mocker):
    """Фикстура для подмены requests.get,
    чтобы возвращать заранее подготовленные HTML-страницы.
    """
    return mocker.patch("requests.get")


def test_fetch_animal_counts_multiple_pages(mock_requests_get):
    """Тест парсинга нескольких страниц."""
    mock_requests_get.side_effect = [
        Mock(status_code=200, text=MOCK_HTML),
        Mock(status_code=200, text=MOCK_HTML_NO_NEXT),
    ]

    result = fetch_animal_counts("https://example.com")

    assert result == {"А": 2, "Б": 1, "В": 1}
    assert mock_requests_get.call_count == 2


def test_fetch_animal_counts_single_page(mock_requests_get):
    """Тест парсинга одной страницы."""
    mock_requests_get.return_value = Mock(
        status_code=200, text=MOCK_HTML_NO_NEXT
    )

    result = fetch_animal_counts("https://example.com")

    assert result == {"В": 1}
    assert mock_requests_get.call_count == 1


def test_save_to_csv(tmp_path):
    """Тест сохранения данных в CSV."""
    test_data = {"А": 2, "Б": 1}
    test_file = tmp_path / "test_beasts.csv"

    save_to_csv(test_data, test_file)

    assert test_file.exists()

    with open(test_file, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)

    assert data == [["Буква", "Количество"], ["А", "2"], ["Б", "1"]]
