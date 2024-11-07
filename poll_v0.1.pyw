import os
import time
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tkinter as tk
from pandastable import Table
import customtkinter
from tkinter import messagebox, Canvas, Frame
from tkinter.ttk import Scrollbar

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Load environment variables
load_dotenv()
EMAIL = os.getenv("email")
PASSWORD = os.getenv("password")

class WebScraper:
    """Handles browser interactions and page scraping."""
    def __init__(self):
        # Set up Chrome options for headless mode
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Initialize the WebDriver with options
        self.driver = webdriver.Chrome(options=options)

    def login(self, url):
        """Logs into the specified URL using credentials from .env."""
        try:
            self.driver.get(url)
            email_input = self.driver.find_element(By.NAME, "email")
            password_input = self.driver.find_element(By.NAME, "password")
            email_input.send_keys(EMAIL)
            password_input.send_keys(PASSWORD)
            
            # Click the login button
            login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error during login: {e}")
            return False
        return True

    def navigate_and_scrape(self, url):
        """Navigates to the specified URL and returns the page source."""
        try:
            self.driver.get(url)
            time.sleep(2)
            return self.driver.page_source
        except Exception as e:
            print(f"Error during navigation or scraping: {e}")
            return None

    def close(self):
        """Closes the web driver."""
        self.driver.quit()


class DataParser:
    """Parses HTML content to extract specific data into a DataFrame."""
    def parse(self, html_content):
        """Extracts data from HTML content and returns it as a DataFrame."""
        soup = BeautifulSoup(html_content, 'html.parser')
        events = soup.find_all('div', class_='object-list events')
        
        data = []
        for event in events:
            date = event.find('div', class_="date").get_text(strip=True) if event.find('div', class_="date") else ''
            question = event.find('div', style='word-break: break-word;').get_text(strip=True)
            data.append({'Date': date, 'Question': question})
        
        return pd.DataFrame(data)


class App:
    """Tkinter application for displaying data."""
    def __init__(self, root):
        self.parser = DataParser()

        self.url_login = "https://app.zigpoll.com/log-in"
        self.url_data = "https://app.zigpoll.com/responses/a/2wvckJDJQEbjfzW8E/p/2wvckk3ydDJSZSjGj"

        # Set up the Tkinter UI
        self.root = root
        self.root.title("Data Viewer")
        self.root.geometry("800x600")  # Set initial window size

        # Create a scrollable canvas
        self.canvas = Canvas(self.root, bg="#2B2B2B", highlightthickness=0)  # Dark background for the canvas
        self.canvas.pack(fill="both", expand=True)

        # Add a scrollbar
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame within the canvas to hold the bubbles
        self.bubble_container = customtkinter.CTkFrame(self.canvas, fg_color="transparent", width=550)
        self.bubble_container.place(relx=0.5, rely=0.4, anchor="center")
        self.bubble_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a window within the canvas to hold the bubble_container frame
        self.canvas.create_window((0, 0), window=self.bubble_container, anchor="nw")

        # Refresh button
        refresh_button = customtkinter.CTkButton(
            master=self.root,
            text="Refresh",
            command=self.refresh_data,
            width=120,
            height=40,
            corner_radius=8
        )
        refresh_button.pack(pady=10)

        # Automatically load data on startup
        self.refresh_data()

    def refresh_data(self):
        """Fetches, parses, and displays data in the table."""

        self.scraper = WebScraper()
        if self.scraper.login(self.url_login):
            html_content = self.scraper.navigate_and_scrape(self.url_data)
            if html_content:
                df = self.parser.parse(html_content)
                self.display_data_as_bubbles(df)
            else:
                messagebox.showerror("Error", "Failed to load data.")
        else:
            messagebox.showerror("Login Failed", "Check your credentials in the .env file.")

    def display_data_as_bubbles(self, df):
        """Displays DataFrame in the Tkinter table."""
        # Clear previous table
        for widget in self.bubble_container.winfo_children():
            widget.destroy()

        bubble_width = 700

        # display data
        for _, row in df.iterrows():
            # Each bubble frame
            bubble = customtkinter.CTkFrame(
                master=self.bubble_container,
                corner_radius=10,
                width=bubble_width - 50,
                # height=100,
                fg_color="#3A3A3A"  # Slightly lighter dark gray for contrast
            )
            # bubble.pack_propagate(False)
            bubble.pack(padx=10, pady=10, anchor="center")  # Fill the width of the container with some padding


            # Display row content in the bubble
            content = "\n".join(f"{col}: {row[col]}" for col in df.columns)
            label = customtkinter.CTkLabel(
                bubble,
                text=content,
                justify="left",
                width=bubble_width - 70,  # Fixed width for label within bubble
                wraplength=bubble_width - 90  # Match wraplength to label width
            )
            label.pack(padx=5, pady=5)


    def on_closing(self):
        """Handles application close event."""
        self.scraper.close()
        self.root.destroy()


# Run the application
if __name__ == "__main__":
    root = customtkinter.CTk()
    scraper = WebScraper()
    parser = DataParser()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
