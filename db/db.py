import os
from dotenv import load_dotenv

import psycopg2


load_dotenv()


class PostgreSQL:
    def __init__(self):
        self.con = psycopg2.connect(
            database=os.getenv('database'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            host=os.getenv('host'),
            port=os.getenv('port')
        )
        self.cursor = self.con.cursor()

    def insert(self, table, insert, value):
        text = f"INSERT INTO {table} ({insert}) VALUES ({value})"
        self.cursor.execute(text)
        self.con.commit()

    def select(self, request):
        self.cursor.execute(request)
        return self.cursor

    def update(self, table, set_1, set_2, where_1, where_2):
        text = f"UPDATE {table} SET {set_1} = {set_2} WHERE {where_1} = {where_2}"
        self.cursor.execute(text)
        self.con.commit()

    def delete(self, table, where_1, where_2):
        text = f"DELETE FROM {table} WHERE {where_1} = {where_2}"
        self.cursor.execute(text)
        self.con.commit()


if __name__ == '__main__':
    database = PostgreSQL()
    database.select("SELECT * FROM nike")

