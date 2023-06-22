import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_extractor import SQLiteExtractor


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

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
def connection_context(sqlite_path, pg_credentials, pg_cursor_factory):
    sqlite_connection = sqlite3.connect(sqlite_path)
    sqlite_connection.row_factory = sqlite3.Row
    pg_connection = psycopg2.connect(**pg_credentials, cursor_factory=pg_cursor_factory)
    yield {'sqlite': sqlite_connection, 'postgres': pg_connection}
    sqlite_connection.close()
    pg_connection.close()


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with connection_context('db.sqlite', dsl, DictCursor) as connections:
        sqlite_conn = connections['sqlite']
        pg_conn = connections['postgres']
        load_from_sqlite(sqlite_conn, pg_conn)
