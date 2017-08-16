import codecs
import csv
import logging
from PIL import Image
import requests
from django.core.files.storage import default_storage

log = logging.getLogger('contacts.datasources')


class DatasourceError(Exception):
    pass


class CSVDatasource:
    """
    Read data from CSV URL. If the `image_height` or `image_height` options are passed,
    images will be resized and uploaded to media storage.
    Currently using default django file storage but s3 storage is possible.
    The goal is to serve resized images from a CDN.
    """
    def __init__(self, url, opts):
        self.url = url
        self.opts = opts

    def import_csv(self):
        try:
            with requests.Session() as session:
                r = session.get(self.url, stream=True)
                r.raise_for_status()  # raise exception for HTTP errors
                csvfile = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
                items = [self.process_item(line) for line in csvfile]
        except requests.exceptions.RequestException:
            log.exception('Error reading datasource')
            raise DatasourceError('Error reading datasource')
        except Exception:
            log.exception('Error processing datasource')

        return items

    def should_process_image(self):
        return self.opts['image_width'] or self.opts['image_height']

    def process_item(self, item):
        if 'image' in item and len(item['image']) > 0 and self.should_process_image():
            item['image'] = self.process_image(item['image'])
        return item

    def process_image(self, url):
        """
        Resize image and return url.
        :return:
        """
        log.info('Processing image from url: {}'.format(url))
        from io import BytesIO
        try:
            with requests.Session() as session:
                r = session.get(url)
                r.raise_for_status()  # raise exception for HTTP errors

                filename = url.split('/')[-1]
                name, extension = filename.split('.')

                fh = BytesIO(r.content)
                fh_out = BytesIO()
                # resize image with Pillow
                im = Image.open(fh)
                im.thumbnail((100, 100))
                im.save(fh_out, extension)

                # resize image with Pillow
                filename = default_storage.save(filename, fh_out)
                # import shutil
                return default_storage.url(filename)
        except Exception:
            log.exception('Error processing image')
