import csv
import logging
import os

from django.core.management import BaseCommand
from django.db import IntegrityError

from django.conf import settings
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

log_file = os.path.join(os.path.dirname(__file__), 'log.txt')

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s - %(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(
    logging.Formatter(
        '%(filename)s - %(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
logger.addHandler(file_handler)

FILES_CLASSES = {
    "category": Category,
    "genre": Genre,
    "titles": Title,
    "genre_title": GenreTitle,
    "users": User,
    "review": Review,
    "comments": Comment,
}

FIELDS = {
    "category": ("category", Category),
    "title_id": ("title", Title),
    "genre_id": ("genre", Genre),
    "author": ("author", User),
    "review_id": ("review", Review),
}


def open_csv_file(file_name):
    """Менеджер контекста для открытия csv-файлов."""
    csv_file = file_name + ".csv"
    csv_path = os.path.join(settings.CSV_FILES_DIR, csv_file)
    try:
        with open(csv_path, encoding="utf-8") as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f"Файл {csv_file} не найден.")
        return


def change_foreign_values(data_csv):
    """Изменяет значения."""
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            data_csv_copy[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value
            )
    return data_csv_copy


def load_csv(file_name, class_name):
    """Загрузка CSV-файлов."""
    table_not_loaded = f"Таблица {class_name.__name__} не загружена."
    table_loaded = f"Таблица {class_name.__name__} загружена."
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            logger.error(
                f"Ошибка в загруженных данных. {error}. {table_not_loaded}"
            )
            break
    logger.info(table_loaded)


class Command(BaseCommand):
    """Класс для загрузки тестовой базы данных."""

    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            logger.info(f"Загрузка таблицы {value.__name__}")
            load_csv(key, value)
