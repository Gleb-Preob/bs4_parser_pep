# Проект парсинга pep
Проект bs4_parser_pep способен обрабатывать информацию с главных страниц документации Python и PEP

## Технологии:
- Python 3.7
- Beautiful Soup
- Request-Cache
- PrettyTable

## Возможности

Парсер может работать в четырёх режимах:

1. `whats-new` - Со [страницы о нововведениях в Python](https://docs.python.org/3/whatsnew/) собирает список ссылок на статьи с описанием нововведений каждой версии Python, с указанием Автора/Редактора
2. `latest-versions` - С [главной страницы документации Python](https://docs.python.org/3/) собирает список ссылок на документацию всех версий Python, с указанием номера версии и статусом.
3. `download` - сохраняет с [адреса актуальной документации](https://docs.python.org/3/download.html) архив с документацией последней версии Python в директорию проекта.
4. `pep` - собирает список используемых статусов документов PEP и подсчитывает число  документов в каждом статусе.

Варианты вывода результата:
- В консоль без разметки
- В консоль, в виде таблицы
- Запись в файл .csv

## Запуск локально

Достаточно склонировать репозиторий, развернуть виртуальное окружение, и установить зависимости из файла:

```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Парсер запускается из внутренней директории `src`.

Информация из команды --help:
```
$ python src/main.py -h
"2024-06-19_02-51-02 - [INFO] - Парсер запущен!"
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

