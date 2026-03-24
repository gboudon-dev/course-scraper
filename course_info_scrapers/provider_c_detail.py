from course_info_scrapers.base_detail_scraper import BaseDetailScraper

class ProviderCDetailScraper(BaseDetailScraper):
    def __init__(self, db_manager):
        super().__init__(db_manager, "cursos_prov_c", "prov_c")
    
    def fetch(self, course_dict: dict[str, str]) -> str | None:
        main_div = self.page.locator("div.single__content")
        
        if main_div.count() < 1:
            print("There is currently no available information for this course.")
            return None
        
        elements = main_div.locator("h1, h2, h3, p, li").all_inner_texts()
        course_information = self.process_text(elements, course_dict)
        print(course_information)
        return course_information


 
         
