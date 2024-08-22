#!/usr/bin/env python
from subprocess import getoutput
from pathlib import Path as P
p=P(P(P(P(P(__file__).parent).parent).parent),'pyproject.toml')
print(p)
VERSION=getoutput(f'cat {p}|head -n 3 |tail -n 1').split('=')[1]
print(VERSION)
