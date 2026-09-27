from url_scrapers.base_scraper import BaseScraper

class ProviderBScraper(BaseScraper):
    temporary_urls : list[str]
    def __init__(self, db_manager):
        self.temporary_urls = []
        super().__init__(db_manager, "cursos_prov_b", "prov_b")

    def fetch(self) -> bool:
        self.page_counter += 1
        print(f"\nNavigating to page: {self.page_counter}\n")

        alt_main_div = self.page.locator("div.diplocursos")

        if alt_main_div.count() > 0:
            return self.alt_fetch(alt_main_div)

        main_div = self.page.locator("div.areas-listado")
        a_locators = main_div.locator("a")
    
        if main_div.count() < 1 or a_locators.count() < 1:
            return False
            
        a_elements = main_div.locator("a").all()
        
        valid_courses = 0
        
        for e in a_elements:
            course_name =e.inner_text().strip()
            url = e.get_attribute("href")
            self.process_information(course_name, url)
            valid_courses += 1
            self.temporary_urls.append(url)
        return valid_courses > 0

    def alt_fetch(self, alt_main_div) -> bool:
 
        item_divs = alt_main_div.locator("div.item").all()
               
        valid_courses = 0
        
        for div in item_divs:
            h5 = div.locator("h5")
            a = div.locator("a.download")

            if h5.count() < 1 or a.count() < 1:
                continue

            print(h5.inner_text())
            print(a.get_attribute("href"))

            course_name = h5.inner_text()
            url = a.get_attribute("href")
            self.process_information(course_name, url)
            valid_courses += 1
    
        return valid_courses > 0
           
    def get_next_page_locator(self):
        pass
    
    def navigate(self):
        if not self.temporary_urls:
            return False
        next_url = self.temporary_urls[0]
        self.temporary_urls.pop(0)
        self.page.goto(next_url)
        return True




        
    
      

