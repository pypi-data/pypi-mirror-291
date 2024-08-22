#!/usr/bin/env python
from pathlib import Path
from configparser import ConfigParser,ExtendedInterpolation
def newConfig():
	cfg = ConfigParser(interpolation=ExtendedInterpolation(),
										 delimiters=':',
										 allow_no_value=True)  # create empty config
	cfg.optionxform = lambda option: option
	return cfg

def to_config(c,p):
	p=Path(p).expanduser().resolve().absolute()
	for item in c:
		if isinstance(c[item],dict):
			if all([isinstance(c[item][subitem], dict) for subitem in c[item]]):
				# folder=Path(p,item)
				# folder.mkdir(0o777,parents=True,exist_ok=True)
			else: # is section
				file=Path(p,item)
				cfg=newConfig()






