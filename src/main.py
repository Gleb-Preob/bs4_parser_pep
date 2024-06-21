import logging
import re
from urllib.parse import urljoin

import requests_cache
from requests import RequestException
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, MAIN_PEP_URL
from exceptions import EmptyResponseException, ParserFindTagException
from outputs import control_output
from utils import find_tag, make_soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')

    soup = make_soup(session, whats_new_url)

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    exception_info = []
    for section in tqdm(sections_by_python):
        version_link = urljoin(whats_new_url, section.find('a')['href'])

        try:
            soup = make_soup(session, version_link)
        except EmptyResponseException as e:
            exception_info.append(e)
            continue

        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))

    if exception_info:
        logging.exception(*exception_info, stack_info=True)
    return results


def latest_versions(session):
    soup = make_soup(session, MAIN_DOC_URL)

    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise ParserFindTagException('В списке не найдено тэгов "a"')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')

    soup = make_soup(session, downloads_url)

    # container_tag= soup.find('div', {'class': 'responsive-table__container'})
    # table_tag = main_tag.find('table', {'class': 'docutils'})
    table_tag = find_tag(soup, 'table')
    pattern = r'.+pdf-a4\.zip$'
    pdf_a4_tag = find_tag(table_tag, 'a', {'href': re.compile(pattern)})

    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    # тесты требуют создавать переменную с путём download_dir здесь
    download_dir = BASE_DIR / 'downloads'
    download_dir.mkdir(exist_ok=True)
    archive_path = download_dir / filename

    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):

    soup = make_soup(session, MAIN_PEP_URL)

    table_by_numerical = find_tag(soup, 'section', {'id': 'numerical-index'})
    table_body = find_tag(table_by_numerical, 'tbody')
    table_entries = table_body.find_all('tr')

    results = []
    discrepancy_info = []
    pep8_counter = {}
    for entry in tqdm(table_entries):
        preview_status = find_tag(entry, 'td').text[1:]
        real_status = ''
        exception_info = []
        entry_url = urljoin(MAIN_PEP_URL, find_tag(entry, 'a')['href'])

        try:
            entry_soup = make_soup(session, entry_url)
        except EmptyResponseException as e:
            exception_info.append(e)
            continue

        dl_tag = find_tag(entry_soup, 'dl')

        # Не могу понять, по какой причине не работает такая запись:
        # dt_status = dl_tag.find('dt', string=re.compile('Status'))
        # в документации 'beautiful-soup' описано, что по такому запросу
        # должен возвращаться объект тега, а возвращает None
        # real_status = dt_status.find_next_sibling('dd').string

        dt_tags = dl_tag.find_all('dt')
        for dt in dt_tags:
            if dt.text == 'Status:':
                real_status = str(dt.find_next_sibling('dd').string)
                break

        pep8_counter[real_status] = pep8_counter.get(real_status, 0) + 1
        if real_status not in EXPECTED_STATUS[preview_status]:
            discrepancy_info.append(
                f'\nРазличия в статусе для документа:\n{entry_url}\nВ '
                f'индивидуальном документе прописан статус: {real_status}'
                f'\nОжидаемые статусы: {EXPECTED_STATUS[preview_status]}'
            )
    if exception_info:
        logging.exception(*exception_info, stack_info=True)
    if discrepancy_info:
        logging.info(*discrepancy_info)

    results.extend(pep8_counter.items())
    results.append(('Total', len(table_entries)))

    return [('Статус', 'Количество')] + results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    try:
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(f'Аргументы командной строки: {args}')

        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)

    except RequestException as e:
        logging.exception(
            e,
            stack_info=True
        )
    except Exception as e:
        logging.exception(
            f'Возникла ошибка: {e}',
            stack_info=True
        )

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
