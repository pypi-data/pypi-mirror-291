
#!/usr/bin/env python
import os
import termios
from pathlib import Path
from configparser import ConfigParser,ExtendedInterpolation
from Clict.Typedef import Clict
from Clict.VERSION import VERSION
def getFileType(c):
	p=c._self.get('path')
	isconfig= lambda t: t.casefold() in ['.ini','.conf','.cfg']
	isexclude= lambda t: t.casefold() in  ['.bak','.old','.disabled','.toml']
	isdisabled= lambda p: p.startswith('_')
	r=Clict()
	r.file=p.is_file()
	r.folder=p.is_dir()
	r.config=isconfig(t=p.suffix)
	r.ignore=isexclude(t=p.suffix)
	r.disable=isdisabled(p.name)
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
	return cfg

class from_Config(Clict):
	__module__ = None
	__qualname__ = "Clict"
	__version__ =VERSION
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
			__s.__type__()

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
		__s.__type__()

	def __type__(__s):
		t=getFileType(__s)
		__s._self.type.file=t.file
		__s._self.type.folder=t.folder
		__s._self.type.config=t.config
		__s._self.type.ignore=t.ignore
		__s._self.type.disable=t.disable

	def __opts__(__s,**opts):
		__s._opts.strip_fileSuffix = True
		__s._opts.strip_filePrefix = True
		__s._opts.strip_folderPrefix = True
		__s._opts.strip_folderSuffix = True
		__s._opts.split_onUnderscore = True
		__s._opts.include_dotFiles = False
		__s._opts.include_dotFolders = False
		__s._opts.suffix_include= ['.conf','.config','.init', '.ini', '.cfg','.toml','.unit','.service','.profile']
		__s._opts.suffix_exclude= ['bak','old']

	def __read__(__s):
		if __s._self.type.get('ignore'):
			__s.CONFIG = 'IGNORED'
			__s._self.name=f'_{__s._self.name}'
		elif __s._self.type.get('disabled'):
			__s.CONFIG = 'DISABLED'
			__s._self.name=f'_{__s._self.name}'
		else:
			if __s._self.type.get('folder'):
				for item in [*__s._self.path.glob('*')]:
					cat=[*__s._self.cat,__s._self.name]
					s=Clict()
					s.p=item
					s.P=__s
					s.name=item.name
					s.cat=cat
					cfg=from_Config(self=s)
					__s[cfg._self.name]=cfg


			elif __s._self.type.get('file'):
				cfg=readConfig(__s._self.path)
				if isinstance(cfg,ConfigParser):
					for section in cfg:
						if section == 'DEFAULT':
							continue
						for key in cfg[section]:
							if key in cfg['DEFAULT']:
								if cfg['DEFAULT'][key] == cfg[section][key]:
									continue
							__s[section][key] = cfg[section][key]

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
