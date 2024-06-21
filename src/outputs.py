import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DT_FORMAT


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
    # тесты требуют создавать переменную с путём results_dir здесь
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)

    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DT_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name

    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUT_TYPES = {
    'pretty': pretty_output,
    'file': file_output
}


def control_output(results, args):
    called_func = OUTPUT_TYPES.get(args.output) or default_output
    return called_func(results, args)
