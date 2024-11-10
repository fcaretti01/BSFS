# imports 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton
from database_manager import DatabaseManager
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView

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
    Window
"""

# Journal Tab Widget for displaying multiple articles
class JournalTab(QWidget):
    def __init__(self, journal_name, fetch_article_func):
        super().__init__()
        self.journal_name = journal_name
        self.fetch_article_func = fetch_article_func

        # Layout and UI elements
        self.layout = QVBoxLayout()
        
        # Table to display articles
        self.article_table = QTableWidget()
        self.article_table.setColumnCount(6)
        self.article_table.setHorizontalHeaderLabels(["Date", "Author", "Title", "Type", "Abstract", "Link"])
        self.article_table.setWordWrap(True)  # Enable word wrapping

        # Adjust the title and link columns to fit content and extend their lengths
        header = self.article_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  # Resize all columns to contents
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Ensure the title column stretches
        header.setSectionResizeMode(5, QHeaderView.Stretch)  # Ensure the link column stretches

        # Set maximum width for the title and link columns for better readability
        self.article_table.setColumnWidth(1, 400)  # Set title column width
        self.article_table.setColumnWidth(5, 400)  # Set link column width

        # Set a fixed width for the abstract column and prevent resizing
        self.article_table.setColumnWidth(4, 200)  # Fixed width for abstract column
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Fixed resize mode for the abstract column
        
        # Fetch Articles Button
        self.refresh_button = QPushButton("Fetch Articles")
        self.refresh_button.clicked.connect(self.load_articles)
        
        # Add widgets to layout
        self.layout.addWidget(self.article_table)
        self.layout.addWidget(self.refresh_button)
        self.setLayout(self.layout)
        
        # Load articles on initialization
        self.load_articles()

    def load_articles(self):
        articles = self.fetch_article_func()
        self.article_table.setRowCount(len(articles))  # Set number of rows based on articles count

        for row, article in enumerate(articles):
            self.article_table.setItem(row, 0, QTableWidgetItem(article.get('date')))
            
            # Create wrapped item for title
            title_item = QTableWidgetItem(article['author'])
            title_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            title_item.setFlags(title_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            title_item.setSizeHint(title_item.sizeHint())  # Ensure wrapping
            self.article_table.setItem(row, 1, title_item)
            
            # Set other items
            self.article_table.setItem(row, 2, QTableWidgetItem(article.get('title')))
            self.article_table.setItem(row, 3, QTableWidgetItem(article.get('type')))
            self.article_table.setItem(row, 4, QTableWidgetItem(article.get('abstract')))
            # self.article_table.setItem(row, 5, QTableWidgetItem(article.get('link')))
            
            
            # Create wrapped item for link
            link_item = QTableWidgetItem(article['link'])
            link_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            link_item.setFlags(link_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            link_item.setSizeHint(link_item.sizeHint())
            self.article_table.setItem(row, 5, link_item)

        # Resize columns based on content after loading
        # self.article_table.resizeColumnsToContents()
"""
-------------------------------------------------------------------------------------------------
    Window
"""


# Main Application Window
class ArticleTrackerApp(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Article Tracker")
        self.setGeometry(100, 100, 1200, 700)  # Increased window width to better fit content
        
        # Main widget and layout
        self.tabs = QTabWidget()
        
        # Journal Tabs with different fetch functions for each journal
        self.tabs.addTab(JournalTab("Journal of Portfolio Management", lambda: db_manager.fetch_articles("Journal of Portfolio Management")), "JPM")
        self.tabs.addTab(JournalTab("Journal of Finance", lambda: db_manager.fetch_articles("Journal of Finance")), "JoF")
        self.tabs.addTab(JournalTab("Journal of Data Science", lambda: db_manager.fetch_articles("Journal of Data Science")), "JDS")
        
        self.setCentralWidget(self.tabs)


"""
-------------------------------------------------------------------------------------------------
    USAGE
"""

# Run the application

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = ArticleTrackerApp(db_manager)
    window.show()
    sys.exit(app.exec_())   