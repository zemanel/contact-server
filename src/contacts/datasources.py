import codecs
import csv
import logging

import requests

log = logging.getLogger('contacts.datasources')


class DatasourceError(Exception):
    pass


class CSVDatasource:
    @staticmethod
    def import_csv(url):
        if url:
            try:
                with requests.Session() as session:
                    r = session.get(url, stream=True)
                    r.raise_for_status()  # raise exception for HTTP errors
                    csvfile = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
                    items = [line for line in csvfile]
            except requests.exceptions.RequestException:
                log.exception('Error reading datasource')
                raise DatasourceError('Error reading datasource')
            return items
        else:
            raise DatasourceError('Error reading datasource')
