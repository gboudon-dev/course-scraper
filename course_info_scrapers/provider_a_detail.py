from course_info_scrapers.base_detail_scraper import BaseDetailScraper

class ProviderADetailScraper(BaseDetailScraper):

    def __init__(self, db_manager):
        super().__init__(db_manager, table_name="cursos_prov_a", cft_name="prov_a" )

    def fetch(self, course_dict: dict[str, str]) -> str | None:
        general_info_div = self.page.locator("div:has-text('Acerca del programa')")
        
        if general_info_div.count() < 1:
            print("There is currently no available information for this course.")
            return None
        
        general_info_elements = general_info_div.locator("h2, p, h3").all_inner_texts()
        details = self.page.locator("section.detalle-programa").all_inner_texts()
        units = self.page.locator("div.editor__contenido").all_inner_texts()
        elements_list = general_info_elements + details + units
        course_information = self.process_text(elements_list, course_dict)
        print(course_information)
        return course_information
  