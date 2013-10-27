# -*- coding: utf-8 -*-
import urllib
import hashlib
import requests
import os
import sys
import math
from fabric.utils import puts
from fabric.colors import *
from fabricant import settings


class Box(object):

    def __init__(self):
        box_file = settings.options['box']['name'] + '.qbox'
        self.box_stored = os.path.join(settings.base_boxes_dir, box_file)

    def verify_base_box(self):
        """Verify base box image."""
        with open(self.box_stored, 'rb') as file_to_check:
            puts('{:<30}'.format('Verifying base box:'), end='')
            data = file_to_check.read()
            sha1_returned = hashlib.sha1(data).hexdigest()
            if settings.options['box']['sha1'] == sha1_returned:
                puts(green('Ok'))
                status = True
            else:
                puts(red('Fail'))
                status = False
            return status

    def fetch_base_box(self):
        """Retrieve and store base box locally for further use."""
        if not os.path.exists(self.box_stored):
            self._download_file(settings.options['box']['base_url'])
        if not self.verify_base_box():
            sys.exit(1)

    def _download_file(self, url):
        """Download base box image."""
        urllib.urlretrieve(url, self.box_stored, self.show_progress)

    def show_progress(self, count, block_size, total):
        """Display progress in percent of download size in curses window.

        :param count: block count
        :param block_size: block size in byte
        :param total: total size of chunk in byte
        """
        total_blocks = math.ceil(total / block_size)
        percent_progress = (count / total_blocks) * 100
        msg = '{:<30}[ {:>.1f}% ]'.format('Downloading base box:', percent_progress)
        puts(msg, end='\r')
