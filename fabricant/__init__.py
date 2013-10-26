# -*- coding: utf-8 -*-
from fabricant.settings import Settings
import os

settings = Settings()
if not os.path.exists(settings.base_boxes_dir):
    os.makedirs(settings.base_boxes_dir)
