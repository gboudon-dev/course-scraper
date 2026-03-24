from url_scrapers.base_scraper import BaseScraper


class ProviderCScraper(BaseScraper):
    def __init__(self, db_manager):
        super().__init__(db_manager, "cursos_prov_c", "prov_c")

    
    def fetch(self) -> bool:
        self.page_counter += 1
        print(f"\nNavigating to page: {self.page_counter}\n") 
        locator = self.page.locator("h3.simple-prog__title")
        if locator.count() < 1:
            return False
        h3s = locator.all()
        valid_courses = 0
        for h3 in h3s:
            a = h3.locator("a")
            if a.count() < 1:
                continue
            
            course_name = h3.inner_text()
            url = a.get_attribute("href")

            self.process_information(course_name, url)
            valid_courses += 1
        return valid_courses > 0
        
    def get_next_page_locator(self):
        nav_locator = self.page.locator("a[title='Página siguiente']")
        return nav_locator
