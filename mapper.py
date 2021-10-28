# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 17:18:29 2021

@author: Alfred Costello
"""

#!/usr/bin/env python

import sys

# Take each line in stdin and assign it as a key with a value.
# stdin will contain a filename per line
for line in sys.stdin:
    keys = line.strip()
    for key in keys:
        value = 1
        print( "%s\t%d" % (key, value) )