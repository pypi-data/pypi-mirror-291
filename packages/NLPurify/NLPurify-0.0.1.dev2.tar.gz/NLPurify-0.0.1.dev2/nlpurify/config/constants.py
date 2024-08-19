# -*- encoding: utf-8 -*-

"""
Defination of Constants Values

The module uses traditional approach like regular expressions,
Unicode transalations to extract features or text cleaning. The
constants values are configured here.
"""

import re

MOBILE_NUMBER_PATTERN = re.compile(r"\W\+?[0-9]{1,3}\s?[0-9\s]{1,14}\W")
