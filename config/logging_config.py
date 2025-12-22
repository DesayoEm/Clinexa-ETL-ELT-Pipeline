
import os
from pathlib import Path
from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG
from copy import deepcopy


LOGGING_CONFIG = deepcopy(DEFAULT_LOGGING_CONFIG)

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')
LOG_DIR = Path(AIRFLOW_HOME) / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG['formatters']['json'] = {
    '()': 'log_formatter.MyJSONFormatter',
    'fmt_keys': {
        'level': 'levelname',
        'message': 'message',
        'timestamp': 'timestamp',
        'logger': 'name',
        'module': 'module',
        'function': 'funcName',
        'line': 'lineno',
        'dag_id': 'dag_id',
        'task_id': 'task_id',
        'execution_date': 'execution_date',
        'try_number': 'try_number'
    }
}


LOGGING_CONFIG['handlers']['task'] = {
    'class': 'airflow.utils.log.file_task_handler.FileTaskHandler',
    'formatter': 'json',
    'base_log_folder': os.path.join(AIRFLOW_HOME, 'logs'),
    'filename_template': '{{ ts }}/ {{ ti.dag_id }}/{{ ti.task_id }}/{{ try_number }}.log',
}

LOGGING_CONFIG['handlers']['main_file'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'formatter': 'json',
    'filename': os.path.join(LOG_DIR, 'main.log'),
    'maxBytes': 10_000_000,
    'backupCount': 30,
    'level': 'DEBUG'
}

LOGGING_CONFIG['handlers']['error_file'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'formatter': 'json',
    'filename': os.path.join(LOG_DIR, 'errors.log'),
    'maxBytes': 5_000_000,
    'backupCount': 30,
    'level': 'ERROR'
}


LOGGING_CONFIG['loggers']['airflow.task'] = {
    'handlers': ['task', 'main_file', 'error_file'],
    'level': 'INFO',
    'propagate': False
}

LOGGING_CONFIG['loggers']['airflow.processor'] = {
    'handlers': ['processor', 'main_file', 'error_file'],
    'level': 'INFO',
    'propagate': False
}

LOGGING_CONFIG['root'] = {
    'handlers': ['console', 'main_file', 'error_file'],
    'level': 'INFO'
}