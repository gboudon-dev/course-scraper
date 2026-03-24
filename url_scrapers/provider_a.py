from url_scrapers.base_scraper import BaseScraper
     
class ProviderAScraper(BaseScraper):
    def __init__(self, db_manager):
        super().__init__(db_manager, "cursos_prov_a", "prov_a")
    
    def fetch(self):
        self.page_counter += 1
        print(f"\nNavigating to page: {self.page_counter}\n") 

        
        locator = self.page.locator("div.tarjeta__contenido")
        
        if locator.count() < 1:
            return False
        divs = locator.all()

        valid_courses = 0
        for div in divs:

            a = div.locator("a.tarjeta__titulo")
            
            if a.count() < 1:
                continue

            url = a.get_attribute("href")
            course_name = a.inner_text().strip()

            print(course_name)
            self.process_information(course_name, url)
            valid_courses += 1
        return valid_courses > 0
    
    def get_next_page_locator(self):
        nav_locator = self.page.locator("a.next")
        return nav_locator
