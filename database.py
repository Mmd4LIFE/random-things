import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS random_sentences (
                    id SERIAL PRIMARY KEY,
                    sentence TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        self.conn.commit()

    def save_sentence(self, sentence):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO random_sentences (sentence) VALUES (%s) RETURNING id",
                (sentence,)
            )
            self.conn.commit()
            return cur.fetchone()[0]

    def get_all_sentences(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT sentence FROM random_sentences")
            return [row[0] for row in cur.fetchall()]

    def sentence_exists(self, sentence):
        with self.conn.cursor() as cur:
            cur.execute("SELECT EXISTS(SELECT 1 FROM random_sentences WHERE sentence = %s)", (sentence,))
            return cur.fetchone()[0]
