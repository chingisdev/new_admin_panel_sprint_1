import sqlite3
import psycopg2

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_extractor import SQLiteExtractor
from pathlib import Path


def load_from_sqlite(sqlite_connection: sqlite3.Connection, postgres_connection: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(postgres_connection)
    sqlite_extractor = SQLiteExtractor(sqlite_connection)

    movies_data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(movies_data)

    genres_data = sqlite_extractor.extract_genres()
    postgres_saver.save_all_data(genres_data)

    persons_data = sqlite_extractor.extract_persons()
    postgres_saver.save_all_data(persons_data)

    genre_filmwork = sqlite_extractor.extract_genre_movies()
    postgres_saver.save_all_data(genre_filmwork)

    persons_filmwork = sqlite_extractor.extract_person_movies()
    postgres_saver.save_all_data(persons_filmwork)


@contextmanager
def create_sqlite_connection(database_path: Path):
    sqlite_connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_COLNAMES)
    sqlite_connection.row_factory = sqlite3.Row
    yield sqlite_connection
    sqlite_connection.close()


@contextmanager
def create_postgresql_connection(credentials: dict, cursor_class):
    pg_connection = psycopg2.connect(**credentials, cursor_factory=cursor_class)
    yield pg_connection
    pg_connection.close()


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    BASE_DIR = Path(__file__).absolute()
    SQLITE_DB_PATH = BASE_DIR / "db.sqlite"
    with create_sqlite_connection(SQLITE_DB_PATH) as sqlite_conn, create_postgresql_connection(dsl,
                                                                                               DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
