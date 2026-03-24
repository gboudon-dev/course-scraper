from playwright.sync_api import sync_playwright, Page
from typing import Optional
from urllib.parse import urljoin
from abc import ABC, abstractmethod
import time
from database.db_manager import DbManager

class BaseScraper(ABC):

    courses : list[tuple[str, str]]
    page_counter : int
    page : Optional[Page]
    table_name : str

    def __init__(self, db_manager : DbManager, table_name : str, cft_name : str):
        self.db_manager = db_manager
        self.table_name = table_name
        self.courses = []
        self.page_counter = 0
        self.page = None
        self.cft_name = cft_name
    
    def run(self, first_url):

        print(f"Starting url scraping process for {self.cft_name}")
        with sync_playwright() as playwright:
            chromium = playwright.chromium
            browser = chromium.launch()
            self.page = browser.new_page()
            self.page.goto(first_url)

            while True:
                self.page.wait_for_load_state()
                if not self.fetch():
                    print(f"Process for {self.cft_name} url scraping finished\n")
                    break
                self.db_manager.db_update(self.courses, self.table_name)
                self.courses = []
                if not self.navigate():
                    print(f"Process for {self.cft_name} url scraping finished\n")
                    break    

    def process_information(self, course_name : str, url : str) -> None:
        course = (course_name, url)
        self.courses.append(course)
    
    def navigate(self) -> bool:
        nav_locator = self.get_next_page_locator()

        if nav_locator.count() < 1:
            print("There are no more pages left")
            return False
        time.sleep(2.5)
     
        try:
            href = nav_locator.get_attribute("href")
            if not href:
                return False
            next_url = urljoin(self.page.url, href)
            if self.page.url == next_url:
                return False
            self.page.goto(next_url)
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    @abstractmethod
    def fetch(self) -> bool:
        pass
    @abstractmethod
    def get_next_page_locator(self):
        pass
