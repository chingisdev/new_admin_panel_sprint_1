from dataclasses import astuple, fields

from psycopg2.extensions import connection as _connection


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.connection = pg_conn

    def save_all_data(self, data):
        cursor = self.connection.cursor()
        table_name = list(data.keys())[0]
        data_to_save = data[table_name]
        if data_to_save:
            # clear database before pasting
            cursor.execute("TRUNCATE content.{table} CASCADE".format(table=table_name))

            column_names = [field.name for field in fields(data_to_save[0])]
            column_counts = ', '.join(['%s'] * len(column_names))
            data_tuples = (astuple(item) for item in data_to_save)
            query_values = [cursor.mogrify("({})".format(column_counts), item).decode("utf-8") for item in data_tuples]
            bind_values = ','.join(query_values)
            cursor.execute("""
                INSERT INTO content.{table} ({columns})
                VALUES {values}
                ON CONFLICT (id) DO NOTHING
                """.format(table=table_name, columns=','.join(column_names), values=bind_values))
            self.connection.commit()
