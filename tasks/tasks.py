from url_scrapers.provider_a import ProviderAScraper
from url_scrapers.provider_b import ProviderBScraper
from url_scrapers.provider_c import ProviderCScraper
from course_info_scrapers.provider_a_detail import ProviderADetailScraper
from course_info_scrapers.provider_b_detail import ProviderBDetailScraper
from course_info_scrapers.provider_c_detail import ProviderCDetailScraper
         
def provider_a_scraper(db_manager):
    provider_a_scraper = ProviderAScraper(db_manager)
    provider_a_scraper.run("https://example.com/")

def provider_b_scraper(db_manager):
    provider_b_scraper =ProviderBScraper(db_manager)
    provider_b_scraper.run("https://example.com/")

def provider_c_scraper(db_manager):
    provider_c_scraper = ProviderCScraper(db_manager)
    provider_c_scraper.run("https://example.com/")

def provider_a_detail_scraper(db_manager):
    provider_a_detail_scraper = ProviderADetailScraper(db_manager)
    provider_a_detail_scraper.run()

def provider_b_detail_scraper(db_manager):
    provider_b_detail_scraper = ProviderBDetailScraper(db_manager)
    provider_b_detail_scraper.run()

def provider_c_detail_scraper(db_manager):
    provider_c_detail_scraper = ProviderCDetailScraper(db_manager)
    provider_c_detail_scraper.run()


TASKS = {
    "prov a": provider_a_scraper,
    "prov b": provider_b_scraper,
    "prov c": provider_c_scraper,
    "prov a detail": provider_a_detail_scraper,
    "prov b detail": provider_b_detail_scraper,
    "prov c detail": provider_c_detail_scraper,
}


    
      

