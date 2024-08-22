
#!/usr/bin/env python
import os
from pathlib import Path
from configparser import ConfigParser,ExtendedInterpolation
from Clict.Typedef import Clict

def getFileType(c,o):
	select=o.suffix_include
	ignore=o.suffix_exclude
	isconfig= lambda t: any([(t == s)  for s in select])
	isexclude= lambda t: any([(t == s)  for s in ignore])
	isdisabled= lambda p: bool(p.startswith('_'))
	r=Clict()
	r.file=bool(c.path.is_file())
	r.folder=bool(c.path.is_dir())
	r.config=isconfig(c.path.suffix)
	r.ignore=isexclude(c.path.suffix)
	r.disabled=isdisabled(c.path.stem)
	return r


def newConfig():
	cfg = ConfigParser(interpolation=ExtendedInterpolation(),
										 delimiters=':',
										 allow_no_value=True)  # create empty config
	cfg.optionxform = lambda option: option
	return cfg


def readConfig(file):
	try:
		cfg = newConfig()
		cfg.read(file)
	except Exception as E:
		cfg = Clict()
		cfg.file=file
		cfg.error=E

class from_Config(Clict):
	__module__ = None
	__qualname__ = "Clict"
	__version__ = 1
	def __init__(__s,*a,**k):
		__s.__args__(*a)
		__s.__kwargs__(**k)
		__s.__read__()
	def __kwargs__(__s,**k):
		self=k.pop('self',{})
		opts=k.pop('opts',{})
		__s.__self__(**self)
		__s.__opts__(**opts)
	def __args__(__s,*a):
		for path in a[::-1]:
			__s._self.path=path

	def __self__(__s,**self):
		path=self.pop('p',self.pop('path',__s._self.path))
		cat=self.pop('c',self.pop('cat',[]))
		parent=self.pop('P',self.pop('parent',None))
		name=self.pop('n',self.pop('name','root'))
		path=Path(path).expanduser().resolve().absolute()
		__s._self.path=path
		__s._self.parent= lambda : parent
		__s._self.name=path.name
		__s._self.cat=cat
	def __type__(__s):
		t=getFileType(__s._self,__s._self.opts)
		__s._self.type.file=t.file
		__s._self.type.folder=t.folder
		__s._self.type.config=t.config
		__s._self.type.ignore=t.config
		__s._self.type.disabled=t.disabled

	def __opts__(__s,**opts):
		__s._opts.strip_fileSuffix = True
		__s._opts.strip_filePrefix = True
		__s._opts.strip_folderPrefix = True
		__s._opts.strip_folderSuffix = True
		__s._opts.split_onUnderscore = True
		__s._opts.include_dotFiles = False
		__s._opts.include_dotFolders = False
		__s._opts.suffix_include= ['.conf','.config','.init', '.ini', '.cfg','.toml','.unit','.service','.profile']
		__s._opts.suffix_exclude= ['.bak','.old']

	def __read__(__s):
		if __s._self.type.disabled or __s._self.type.ignore:
			__s=None
			return __s
		else:
			if __s._self.type.folder:
				for item in [*__s._self.path.glob('*')]:
					cat=[*__s._self.cat,__s._self.name]
					s=Clict()
					s.p=item
					s.P=__s
					s.name=item.name
					s.cat=cat
					cfg=from_Config(self=s)
					if cfg is not None:
						if __s.__getopt__('strip_folderPrefix'):
							for ss in [*'-_# @']:
								new = ss.join(cfg._self.name.split(ss)[1:])
								cfg._self.name = new or cfg._self.name
						__s[cfg._self.name]=cfg

			elif __s._self.type.file:
				if __s._self.type.config:
					cfg=readConfig(__s._self.path)
				else:
					cfg=None
			if cfg is not None:
				for section in cfg:
					if section == 'DEFAULT':
						continue
					for key in cfg[section]:
						if key in cfg['DEFAULT']:
							if cfg['DEFAULT'][key] == cfg[section][key]:
								continue
						__s[section][key] = cfg[section][key]
			else:
				__s=None


# if '-' in section:
# 	for key in cfg[section]:
# 		if key in cfg['DEFAULT']:
# 			if cfg['DEFAULT'][key] == cfg[section][key]:
# 				continue
#							__s[section.split('-')[0]]['-'.join(section.split('-')[1:]).replace('-', '.')][key]= cfg[section][key]

# 		O=lambda x :__s._optb.get(x)
#
#
# if item.stem.startswith('.'):
# 	if O('ignore_dotfiles'):
# 		continue
# if O('strip_folderext') else str(item)
# and O('strip_folderprefix'):
#
# and O('strip_folderprefix'):
#
