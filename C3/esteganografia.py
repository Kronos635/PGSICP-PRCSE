#!/usr/bin/env python3
# coding: utf-8
#
# 20211217 - PGSICP-PRCSE - Grupo2
#
#
# pipx install stegano
#
# stegano-lsb reveal -i PRCSE-C3.png
#
# resultado obtido: pbatenghyngvbafguvfvfcepfruvqqrazrffntr

# ROT-13:

import codecs

stringToDecode = "pbatenghyngvbafguvfvfcepfruvqqrazrffntr"

## Python has a built-in library to implement the ROT-13 algorithm. https://docs.python.org/3/library/codecs.html

print(codecs.encode(stringToDecode, 'rot_13'))