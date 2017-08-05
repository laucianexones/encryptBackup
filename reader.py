# -*- encoding: utf-8 -*-
import os

s = "ğüıç"
print type(s)
print s

us = s.decode('utf-8')
print type(us)
print us
