# Standard library imports
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class Database:
    """
    A class to handle all PostgreSQL database operations for the Dark Thoughts Bot.
    
    This class manages the connection to the PostgreSQL database and provides methods
    for creating tables, saving sentences, and checking for duplicates.
    """

    def __init__(self):
        """
        Initialize database connection using credentials from config.
        Establishes connection and creates required table if it doesn't exist.
        """
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.create_table()

    def create_table(self):
        """
        Create the random_sentences table if it doesn't exist.
        
        Table Schema:
        - id: Auto-incrementing primary key
        - sentence: The actual text content
        - created_at: Timestamp of sentence creation
        """
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
        """
        Save a new sentence to the database.

        Args:
            sentence (str): The sentence to be saved

        Returns:
            int: The ID of the newly inserted sentence
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO random_sentences (sentence) VALUES (%s) RETURNING id",
                (sentence,)
            )
            self.conn.commit()
            return cur.fetchone()[0]

    def get_all_sentences(self):
        """
        Retrieve all sentences from the database.

        Returns:
            list: A list of all sentences stored in the database
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT sentence FROM random_sentences")
            return [row[0] for row in cur.fetchall()]

    def sentence_exists(self, sentence):
        """
        Check if a sentence already exists in the database.

        Args:
            sentence (str): The sentence to check for duplicates

        Returns:
            bool: True if the sentence exists, False otherwise
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT EXISTS(SELECT 1 FROM random_sentences WHERE sentence = %s)", (sentence,))
            return cur.fetchone()[0]
