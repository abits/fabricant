# -*- coding: utf-8 -*-
import urllib
import hashlib
import requests
import os
from fabricant import settings

class BoxInitializationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Box(object):

    def __init__(self):
        box_file = settings.options['box']['name'] + '.qbox'
        self.box_stored = os.path.join(settings.base_boxes_dir, box_file)

    def verify_base_box(self):
        with open(self.box_stored, 'rb') as file_to_check:
            data = file_to_check.read()
            md5_returned = hashlib.md5(data).hexdigest()

        if settings.options['box']['md5'] != md5_returned:
            raise BoxInitializationError()

    def fetch_base_box(self):
        """Retrieve and store base box locally for further use."""
        if not os.path.exists(self.box_stored):
            self._download_file(settings.options['box']['base_url'])
            self.verify_base_box()

    def _download_file(self, url):
        r = requests.get(url, stream=True)
        print self.box_stored
        with open(self.box_stored, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()