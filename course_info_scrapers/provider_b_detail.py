from course_info_scrapers.base_detail_scraper import BaseDetailScraper

class ProviderBDetailScraper(BaseDetailScraper):
    def __init__(self, db_manager):
        super().__init__(db_manager, "cursos_prov_b", "prov_b")
    
    def fetch(self, course_dict: dict[str, str]) -> str | None:
        main_div = self.page.locator("div.content-duoc-uc")
            
        if main_div.count() < 1:
            print("There is currently no available information for this course.")
            return None
        
        course_data = ""
        texts = []
        elements = main_div.locator("h5, p").all()
        for e in elements:
            text = e.inner_text().strip()
            if text != "":
                texts.append(text) 
        
        course_data = "\n\n".join(texts)
        print(course_data)
        return course_data
 
         
