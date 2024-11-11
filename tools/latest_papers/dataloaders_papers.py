# imports 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
from typing import Dict, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import sys
from database_manager import DatabaseManager



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
        SELENIUM WEB SCRAPER
"""

class WebScraper:
    def __init__(self, headless=True):
        """
        Initializes the WebScraper with specified WebDriver options.
        """
        self.driver = None
        self.headless = headless
        self.cookies_accepted_domains = set()

    def _initialize_driver(self):
        """
        Configures and initializes the WebDriver with options if not already done.
        """
        if self.driver is None:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-background-timer-throttling")
            if self.headless:
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(2)  # Implicit wait for all elements

    def accept_cookies(self):
        """
        Attempts to click the 'Accept All Cookies' button on the page if present.
        Only attempts once per domain to avoid redundancy.
        """
        domain = self.driver.current_url.split("/")[2]
        if domain not in self.cookies_accepted_domains:
            try:
                accept_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All Cookies') or contains(text(), 'Accept all cookies')]"))
                )
                accept_button.click()
                self.cookies_accepted_domains.add(domain)
            except Exception as e:
                print("Could not find or click the accept cookies button:", e)

    def get_page_source(self, url):
        """
        Retrieves the page source of the specified URL after attempting to accept cookies.
        """
        self._initialize_driver()
        self._navigate_to_url(url)
        self.accept_cookies()
        return self.driver.page_source

    def _navigate_to_url(self, url):
        """
        Navigates to the specified URL.
        """
        self.driver.get(url)

    def close(self):
        """
        Closes the webdriver if initialized.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None  # Ensure driver is set to None for re-initialization


"""
-------------------------------------------------------------------------------------------------
        JPORMGMT PARSER
"""

class JPMArticlesParser:
    BASE_URL = "https://www.pm-research.com"

    def __init__(self, html_source):
        """
        Initializes the JPMArticles class with HTML content and parses it.
        
        Parameters:
        - html_source: str, the HTML content to parse
        """
        self.soup = BeautifulSoup(html_source, "html.parser")
        self.articles = self.parse_articles()

    def parse_articles(self):
        """
        Parses articles from the HTML content and stores them in a list.
        """
        articles = {}
        item_list = self.soup.find("div", class_="item-list")
        if item_list:
            articles_html = item_list.find_all("article")
            for i, article_html in enumerate(articles_html):
                article_data = {
                    "date": self._get_date(article_html),
                    "title": self._get_title(article_html),
                    "author": self._get_authors(article_html),
                    "type": None,
                    "abstract": None,
                    "link": self._get_link(article_html),
                }
                articles[i] = article_data
        return articles

    def _get_title(self, article):
        """
        Extracts the title from an article.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The title of the article
        """
        title_tag = article.find("span", class_="field--highwire-content-title")
        return title_tag.text if title_tag else None

    def _get_authors(self, article):
        """
        Extracts the authors list from an article.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The authors of the article
        """
        authors_tag = article.find("ul", class_="contributor-list")
        return authors_tag.text.strip() if authors_tag else None

    def _get_date(self, article):
        """
        Extracts and formats the publication date from an article.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The publication date in 'YYYY-MM-DD' format
        """
        date_tag = next((x for x in article.find_all("span", class_="author-name") 
                         if "The Journal of Portfolio Management" in x.text), None)
        if date_tag:
            date_str = date_tag.text.split(" - ")[0]
            try:
                return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Error parsing date: {date_str}")
        return None

    def _get_link(self, article):
        """
        Extracts the article link.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The full URL to the article
        """
        link_tag = article.find("a", class_="latest-articles")
        return self.BASE_URL + link_tag.get("href") if link_tag else None

    def get_articles(self):
        """
        Returns the list of parsed articles.
        
        Returns:
        - list of dict: Each dictionary contains 'title', 'authors', 'date', and 'link' for an article
        """
        return self.articles


"""
-------------------------------------------------------------------------------------------------
        JOF PARSER
"""

class JOFArticlesParser:

    def __init__(self, html_source):
        """
        Initializes the JOFArticlesFetcher class with HTML content and parses it.
        
        Parameters:
        - html_source: str, the HTML content to parse
        """
        self.soup = BeautifulSoup(html_source, "html.parser")
        self.articles = self.parse_articles()

    def parse_articles(self):
        """
        Parses articles from the HTML content and stores them in a list.
        """
        articles = {}
        item_list = self.soup.find("section", {"data-ga": "journal-articles"})
        if item_list:
            articles_html = item_list.find_all("article", class_="app-card-open app-card-open--has-image")
            for i, article_html in enumerate(articles_html):
                article_data = {
                    "date": self._get_date(article_html),
                    "title": self._get_title(article_html),
                    "author": self._get_authors(article_html),
                    "type": self._get_type(article_html),
                    "abstract": None,
                    "link": self._get_link(article_html),
                }
                articles[i] = article_data
        return articles

    def _get_title(self, article):
        """
        Extracts the title from an article.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The title of the article
        """
        title_tag = article.find("h3", class_="app-card-open__heading")
        return title_tag.text.strip() if title_tag else None

    def _get_authors(self, article):
        """
        Extracts the authors list from an article.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The authors of the article
        """
        authors = (", ").join(x.text.strip() for x in article.find("div", class_="app-card-open__authors").find_all("li"))
        return authors if authors else None

    def _get_date(self, article):
        """
        Extracts and formats the publication date from an article.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The publication date in 'YYYY-MM-DD' format
        """
        date_tag = article.find("div", class_="app-card-open__meta").find_all("span", class_="c-meta__item")[-1]

        if date_tag:
            date_str = date_tag.text.strip()
            try:
                return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Error parsing date: {date_str}")
        return None

    def _get_link(self, article):
        """
        Extracts the article link.
        
        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The full URL to the article
        """
        link_tag = article.find("a", {"data-track": "select_article"})
        return link_tag.get("href") if link_tag else None
    
    def _get_type(self, article):
        """
        Extract article type

        Parameters:
        - article: BeautifulSoup element representing the article

        Returns:
        - str: The type of the article
        """
        type_tag = article.find("div", class_="app-card-open__meta").find_all("span", class_="c-meta__item")[0]
        return type_tag.text.strip() if type_tag else None

    def get_articles(self):
        """
        Returns the list of parsed articles.
        
        Returns:
        - list of dict: Each dictionary contains 'title', 'authors', 'date', and 'link' for an article
        """
        return self.articles


"""
-------------------------------------------------------------------------------------------------
        JDS FETCHER + PARSER
"""

class JDSArticleFetcher:
    def __init__(self, base_url: str = "https://jds-online.org/journal/JDS/to-appear"):
        self.base_url = base_url

    def fetch_articles(self) -> Dict[int, Dict[str, str]]:
        """Fetches and returns articles with details such as title, date, type, abstract, and link."""
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="row filtered-item")

        articles_dict = {}
        for i, article in tqdm(enumerate(articles), desc="Fetching articles"):
            article_data = self.extract_article_data(article)
            articles_dict[i] = article_data

        return articles_dict

    def extract_article_data(self, article) -> Dict[str, str]:
        """Extracts relevant data from an individual article."""
        title = article.get("data-title", "")
        date = datetime.strptime(article.get("data-published", ""), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        article_type = article.get("data-type", "")
        link_tag = article.find("a", class_="article-title")

        abstract, link = self.fetch_abstract(link_tag) if link_tag else ("", "")

        return {
            "date": date,
            "title": title,
            "author": None,
            "type": article_type,
            "abstract": abstract,
            "link": link
        }

    def fetch_abstract(self, link_tag) -> Tuple[str, str]:
        """Fetches the abstract of an article from its individual page."""
        url = link_tag.get("href", "")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        abstract_div = soup.find("div", class_="first para")
        abstract = abstract_div.text.strip() if abstract_div else "Abstract not found."

        return abstract, url


"""
-------------------------------------------------------------------------------------------------
"""
if __name__ == "__main__":

    jpm_url = "https://www.pm-research.com/content/iijpormgmt?implicit-login=true"
    jof_url = "https://link.springer.com/journal/10203/articles?gad_source=1&_gl=1*8mlr1g*_up*MQ..&gclid=Cj0KCQiA0MG5BhD1ARIsAEcZtwSrwV9bgzmFbL6dqx5l1d-7uBgQOEsOWdfAExgq9KOnkKVPeG1Ce0waAn0uEALw_wcB"
    jds_url = "https://jds-online.org/journal/JDS/to-appear"

    # start the scraper
    scraper = WebScraper(headless=True)

    # find the sources of jof and jpm pages
    jpm_page_source = scraper.get_page_source(jpm_url)
    jof_page_source = scraper.get_page_source(jof_url)

    # close scraper
    scraper.close()

    # parse data
    jpm_articles = JPMArticlesParser(jpm_page_source).get_articles()
    jof_articles = JOFArticlesParser(jof_page_source).get_articles()

    # find data for jds
    jds_fetcher = JDSArticleFetcher(base_url=jds_url)
    jds_articles = jds_fetcher.fetch_articles()


    # start db manager and save data
    db_manager = DatabaseManager()
    db_manager.store_article_if_not_exists("Journal of Portfolio Management", jpm_articles)
    db_manager.store_article_if_not_exists("Journal of Finance", jof_articles)
    db_manager.store_article_if_not_exists("Journal of Data Science", jds_articles)




"""
-------------------------------------------------------------------------------------------------
"""