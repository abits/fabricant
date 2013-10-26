# -*- coding: utf-8 -*-
import urllib
import os
from fabricant import settings

class Box(object):
    def fetch_base_box(url):
        """Retrieve and store base box locally for further use."""
        box_file = settings.options['box']['name'] + '.qbox'
        box_stored = os.path.join(settings.base_boxes_dir, box_file)
        if not os.path.exists(box_stored):
            urllib.urlretrieve (settings.options['box']['base_url'], box_stored)
