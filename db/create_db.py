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

    def create_nike(self):
        self.cursor.execute('''CREATE TABLE nike 
            (id SERIAL PRIMARY KEY,
            cloud_product_id VARCHAR(50) NOT NULL,
            title VARCHAR(100) NOT NULL,
            url VARCHAR(500) NOT NULL,
            product_type VARCHAR(100) NOT NULL,
            seller VARCHAR(100) NOT NULL,
            UNIQUE (cloud_product_id)
            );''')
        self.con.commit()
        print("Table 'nike' created successfully")

    def create_profile(self):
        self.cursor.execute('''CREATE TABLE profile
            (
            telegram_id INTEGER PRIMARY KEY,
            count_sub SMALLINT DEFAULT 0,
            max_sub SMALLINT DEFAULT 5
             );''')
        self.con.commit()
        print("Table 'profile' created successfully")

    def create_subscribers(self):
        self.cursor.execute('''CREATE TABLE subscribers
            (id SERIAL PRIMARY KEY,
            telegram_id SERIAL REFERENCES profile (telegram_id) NOT NULL,
            product_id VARCHAR(50) REFERENCES nike (cloud_product_id) NOT NULL,
            size VARCHAR(10) NOT NULL,
            price NUMERIC(7,2) NOT NULL
            );''')
        self.con.commit()
        print("Table 'subscribers' created successfully")

    def close_connect(self):
        self.con.close()


if __name__ == '__main__':
    database = PostgreSQL()

    database.create_nike()
    database.create_profile()
    database.create_subscribers()

    database.close_connect()
