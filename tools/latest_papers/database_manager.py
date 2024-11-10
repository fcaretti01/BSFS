# imports
import sys, os, sqlite3

"""
-------------------------------------------------------------------------------------------------
        SET DIRECTORY
"""

# Get the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

# Add the script's directory to the Python path
sys.path.insert(0, script_dir)


"""
-------------------------------------------------------------------------------------------------
    DATABASE MANAGER
"""

class DatabaseManager:
    def __init__(self, db_name="articles.db"):
        """
        Initializes the DatabaseManager with the specified database name.
        
        Parameters:
        - db_name: str, the name of the SQLite database file
        """
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """
        Initializes the database and creates the articles table if it doesn't exist.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                                journal TEXT, 
                                date TEXT,
                                title TEXT,
                                author TEXT,
                                type TEXT,
                                abstract TEXT, 
                                link TEXT)''')
            conn.commit()

    def store_articles(self, journal, articles_data):
        """
        Stores multiple articles in the database.

        Parameters:
        - journal: str, the name of the journal
        - articles_data: dict, a dictionary where each key represents an article ID and 
          the value is another dictionary with 'title', 'description', and 'link' keys
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            for article_id, article in articles_data.items():
                cursor.execute("INSERT INTO articles (journal, date, title, author, type, abstract, link) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (journal, article.get('date'), article.get('title'), article.get('author'), article.get('type'), article.get('abstract'), article.get('link')))
            conn.commit()

    def store_article_if_not_exists(self, journal, articles):
        """
        Stores a single article in the database only if it does not already exist.
        
        Parameters:
        - journal: str, the name of the journal
        - article: dict, a dictionary with 'date', 'title', 'author', 'type', 'abstract', and 'link' keys
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Check if an article with the same journal and title already exists
            for article_id, article in articles.items():
                cursor.execute("SELECT 1 FROM articles WHERE journal = ? AND title = ?", (journal, article.get('title')))
                exists = cursor.fetchone()
                if not exists:
                    # Insert the article if it doesn't exist
                    cursor.execute("INSERT INTO articles (journal, date, title, author, type, abstract, link) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (journal, article.get('date'), article.get('title'), article.get('author'), article.get('type'), article.get('abstract'), article.get('link')))
                    conn.commit()       

    def fetch_articles(self, journal=None):
        """
        Retrieves articles from the database, optionally filtered by journal.

        Parameters:
        - journal: str, the name of the journal to filter by (default: None, which means no filtering)

        Returns:
        - list of dict: A list where each dictionary represents an article
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if journal:
                cursor.execute("SELECT journal, date, title, author, type, abstract, link FROM articles WHERE journal = ?", (journal,))
            else:
                cursor.execute("SELECT journal, date, title, author, type, abstract, link FROM articles")
            rows = cursor.fetchall()
            return [
                {
                    "journal": row[0],
                    "date": row[1],
                    "title": row[2],
                    "author": row[3],
                    "type": row[4],
                    "abstract": row[5],
                    "link": row[6]
                }
                for row in rows
            ]

    def clear_articles(self):
        """
        Clears all articles from the database.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM articles")
            conn.commit()