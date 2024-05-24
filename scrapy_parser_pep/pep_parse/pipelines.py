import csv
import os
from datetime import datetime

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.counter = {}

    def process_item(self, item, spider):
        pep_status = item.get('status')
        self.counter[pep_status] = self.counter.get(pep_status, 0) + 1
        return item

    def close_spider(self, spider):
        os.makedirs(BASE_DIR, exist_ok=True)

        current_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"{BASE_DIR}/status_summary_{current_datetime}.csv"

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(
                [
                    ('Статус', 'Количество'),
                    *self.counter.items(),
                    ('Total', sum(self.counter.values()))
                ]
            )
            csv_writer.writerow()
