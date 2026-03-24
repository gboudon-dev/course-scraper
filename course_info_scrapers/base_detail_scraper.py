from playwright.sync_api import sync_playwright, Page
from typing import Optional
from abc import ABC, abstractmethod
import time
import random


class BaseDetailScraper(ABC):
    page : Optional[Page]
    table_name : str

    def __init__(self, db_manager, table_name, cft_name):
        self.db_manager = db_manager
        self.table_name = table_name
        self.page = None
        self.cft_name = cft_name

    def run(self):
        print(f"Starting course-info scraping process for {self.cft_name}")
        with sync_playwright() as playwright:
            chromium = playwright.chromium
            browser = chromium.launch()
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            self.page = context.new_page()

            courses = self.db_manager.read_db(self.table_name)
            
            for course in courses:
                course_dict = {
                "informacion" : "",
                "url" : course[1],
                "curso" : course[0]
                }

                print(f"Browsing to {course_dict['url']}")
                self.page.goto(course_dict["url"])
                self.page.wait_for_load_state()
                course_information = self.fetch(course_dict)
                if not course_information:
                    self.db_manager.update_course_info(course_dict, self.table_name)
                    continue
                
                course_dict["informacion"] = course_information
                self.db_manager.update_course_info(course_dict, self.table_name)
                random_value = random.uniform(1.5, 3)
                time.sleep(random_value)

            print(f"Process for {self.cft_name} course-info scraping finished\n")
    
    @abstractmethod
    def fetch(self, course_dict : dict[str, str]) -> str | None:
        pass

    def process_text(self, elements_list : list[str], course_dict : dict[str, str]) -> str:
        complete_text = ""

        try:
            complete_text = f"{course_dict['curso']}\n\n"
            for text in elements_list:
                complete_text += f"{text.strip()}\n"
            return complete_text
        except Exception as e:
            print(f"Error while obtaining course information in {course_dict['url']} {e}")
        