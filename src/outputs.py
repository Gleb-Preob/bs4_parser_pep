import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import DT_FORMAT, RESULTS_DIR


def default_output(results, cli_args):
    """Печатаем список results построчно."""
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
    """Выводим таблицу в консоль."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table.get_string())


def file_output(results, cli_args):
    """Запись в файл"""
    RESULTS_DIR.mkdir(exist_ok=True)

    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DT_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = RESULTS_DIR / file_name

    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUT_TYPES = {
    'pretty': pretty_output,
    'file': file_output
}


def control_output(output):
    return OUTPUT_TYPES.get(output) or default_output
