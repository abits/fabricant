# -*- coding: utf-8 -*-
#!/bin/env python2

from fabricant.settings import Settings

def run_init():


if __name__ == '__main__':
    settings = Settings()
    if settings.action == 'init':
        run_init()
    print settings.action
    print settings.options
