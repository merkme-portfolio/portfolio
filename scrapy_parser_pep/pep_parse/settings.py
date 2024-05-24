BOT_NAME = 'pep_parse'

SPIDER_PEP_SETTINGS = {
    'name': 'pep',
    'allowed_domains': 'peps.python.org',
    'start_urls': 'https://peps.python.org/'
}

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True


BASE_DIR = "results"

FEEDS = {
    f'{BASE_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}
ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
