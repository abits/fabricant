# -*- coding: utf-8 -*-
#!/bin/env python2

from fabricant import settings
from fabricant.services import Box


def run_init():
    box = Box()
    box.fetch_base_box()

if __name__ == '__main__':
    if settings.action == 'init':
        run_init()
