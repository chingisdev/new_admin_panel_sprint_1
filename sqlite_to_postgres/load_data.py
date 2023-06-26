import sqlite3
from pathlib import Path

from database_contexts import (create_postgresql_connection,
                               create_sqlite_connection)
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_extractor import SQLiteExtractor


def load_from_sqlite(sqlite_connection: sqlite3.Connection,
                     postgres_connection: _connection):
    try:
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
    except IOError as e:
        print('An IOError occurred: %s' % e)


if __name__ == '__main__':
    dsl = {
        'dbname': 'movies_database',
        'user': 'app',
        'password': '123qwe',
        'host': '127.0.0.1',
        'port': 5432,
    }
    BASE_DIR = Path(__file__).parent.absolute()
    SQLITE_DB_PATH = BASE_DIR / 'db.sqlite'
    with create_sqlite_connection(SQLITE_DB_PATH) as sqlite_conn:
        with create_postgresql_connection(dsl, DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
