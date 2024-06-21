from pathlib import Path

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / 'results'
DOWNLOAD_DIR = BASE_DIR / 'downloads'
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

# Формат логов: Время записи – Уровень сообщения – Cообщение
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
