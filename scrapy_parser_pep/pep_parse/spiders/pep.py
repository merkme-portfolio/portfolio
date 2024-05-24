import scrapy

from pep_parse.items import PepParseItem
from pep_parse.utils import find_pep_number, get_pep_name
from pep_parse.settings import SPIDER_PEP_SETTINGS


class PepSpider(scrapy.Spider):
    name = SPIDER_PEP_SETTINGS['name']
    allowed_domains = [SPIDER_PEP_SETTINGS['allowed_domains']]
    start_urls = [SPIDER_PEP_SETTINGS['start_urls']]

    def parse(self, response):
        all_peps_link = response.css('#numerical-index a[href^="pep-"]')
        for pep_link in all_peps_link:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': find_pep_number(response.css('.page-title::text').get()),
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get(),
            'name': get_pep_name(response.css('.page-title::text').get()),
        }
        yield PepParseItem(data)
