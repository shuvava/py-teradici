# -*- coding: utf-8 -*-
import os
from sys import path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app'))
path.insert(0, BASE_DIR)
