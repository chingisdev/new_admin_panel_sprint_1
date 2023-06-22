import sqlite3

from sqlite_to_postgres.models import FilmWork, GenreFilmwork, Genre, PersonFilmwork, Person


class SQLiteExtractor:
    def __init__(self, sqlite_connection: sqlite3.Connection):
        self.connection = sqlite_connection
        self.fetch_size = 100

    def _execute_select_query(self, table_name, model_class):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM {table};".format(table=table_name))
        # Получаем данные
        movie_batches: list[model_class] = []
        while data := cursor.fetchmany(self.fetch_size):
            converted_data = [model_class(**dict(movie)) for movie in data]
            movie_batches.extend(converted_data)
        return {table_name: movie_batches}

    def extract_movies(self):
        table_name = "film_work"
        return self._execute_select_query(table_name, model_class=FilmWork)

    def extract_genres(self):
        table_name = "genre"
        return self._execute_select_query(table_name, model_class=Genre)

    def extract_persons(self):
        table_name = "person"
        return self._execute_select_query(table_name, model_class=Person)

    def extract_person_movies(self):
        table_name = "person_film_work"
        return self._execute_select_query(table_name, model_class=PersonFilmwork)

    def extract_genre_movies(self):
        table_name = "genre_film_work"
        return self._execute_select_query(table_name, model_class=GenreFilmwork)
