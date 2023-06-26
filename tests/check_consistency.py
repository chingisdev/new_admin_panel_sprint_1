from pathlib import Path

import pytest
from psycopg2.extras import DictCursor

from sqlite_to_postgres.database_contexts import (create_postgresql_connection,
                                                  create_sqlite_connection)
from sqlite_to_postgres.models import (FilmWork, Genre, GenreFilmwork, Person,
                                       PersonFilmwork)

BASE_DIR = Path(__file__).parent.parent.absolute() / 'sqlite_to_postgres'
SQLITE_DB_PATH = BASE_DIR / 'db.sqlite'

BATCH_SIZE = 100
POSTGRES_CREDENTIALS = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': '127.0.0.1',
    'port': 5432,
}
POSTGRES_CURSOR = DictCursor


def sort_data_by_id(data: list):
    return sorted(data, key=lambda x: x.id)


def extract_data(cursor, table_name, model_class):
    cursor.execute(f'SELECT * FROM {table_name};')
    batches: list[model_class] = []
    while data := cursor.fetchmany(BATCH_SIZE):
        converted_data = [model_class(**dict(item)) for item in data]
        batches.extend(converted_data)
    return sort_data_by_id(batches)


@pytest.fixture()
def sqlite_film_work():
    fixture_table = 'film_work'
    with create_sqlite_connection(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, FilmWork)


@pytest.fixture()
def sqlite_person():
    fixture_table = 'person'
    with create_sqlite_connection(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, Person)


@pytest.fixture()
def sqlite_genre():
    fixture_table = 'genre'
    with create_sqlite_connection(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, Genre)


@pytest.fixture()
def sqlite_genre_film_work():
    fixture_table = 'genre_film_work'
    with create_sqlite_connection(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, GenreFilmwork)


@pytest.fixture()
def sqlite_person_film_work():
    fixture_table = 'person_film_work'
    with create_sqlite_connection(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, PersonFilmwork)


@pytest.fixture()
def postgres_film_work():
    fixture_table = 'film_work'
    with create_postgresql_connection(POSTGRES_CREDENTIALS,
                                      POSTGRES_CURSOR) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, FilmWork)


@pytest.fixture()
def postgres_person():
    fixture_table = 'person'
    with create_postgresql_connection(POSTGRES_CREDENTIALS,
                                      POSTGRES_CURSOR) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, Person)


@pytest.fixture()
def postgres_genre():
    fixture_table = 'genre'
    with create_postgresql_connection(POSTGRES_CREDENTIALS,
                                      POSTGRES_CURSOR) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, Genre)


@pytest.fixture()
def postgres_genre_film_work():
    fixture_table = 'genre_film_work'
    with create_postgresql_connection(POSTGRES_CREDENTIALS,
                                      POSTGRES_CURSOR) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, GenreFilmwork)


@pytest.fixture()
def postgres_person_film_work():
    fixture_table = 'person_film_work'
    with create_postgresql_connection(POSTGRES_CREDENTIALS,
                                      POSTGRES_CURSOR) as conn:
        cursor = conn.cursor()
        return extract_data(cursor, fixture_table, PersonFilmwork)


def test_film_work_length(postgres_film_work, sqlite_film_work):
    assert len(postgres_film_work) == len(sqlite_film_work)


def test_person_length(postgres_person, sqlite_person):
    assert len(postgres_person) == len(sqlite_person)


def test_genre_length(postgres_genre, sqlite_genre):
    assert len(postgres_genre) == len(sqlite_genre)


def test_person_film_work_length(postgres_person_film_work,
                                 sqlite_person_film_work):
    assert len(postgres_person_film_work) == len(sqlite_person_film_work)


def test_genre_film_work_length(postgres_genre_film_work,
                                sqlite_genre_film_work):
    assert len(postgres_genre_film_work) == len(sqlite_genre_film_work)


def test_film_work_consistency(postgres_film_work, sqlite_film_work):
    assert postgres_film_work == sqlite_film_work


def test_person_consistency(postgres_person, sqlite_person):
    assert postgres_person == sqlite_person


def test_genre_consistency(postgres_genre, sqlite_genre):
    assert postgres_genre == sqlite_genre


def test_person_film_work_consistency(postgres_person_film_work,
                                      sqlite_person_film_work):
    assert postgres_person_film_work == sqlite_person_film_work


def test_genre_film_work_consistency(postgres_genre_film_work,
                                     sqlite_genre_film_work):
    assert postgres_genre_film_work == sqlite_genre_film_work
