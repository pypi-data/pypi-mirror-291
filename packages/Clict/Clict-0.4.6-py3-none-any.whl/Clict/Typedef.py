#!/usr/bin/env python
from Clict.lib.fnText import CStr
import sys


class Clict(dict):
	__module__ = None
	__qualname__ = "Clict"
	__version__ = 1
	def __new__(__c, *a, **k):
		# print('__new__ called with:' ,f'{k=}{v=}')
		return super().__new__(__c, *a, **k)

	def __init__(__s, *a, **k):
		super().__init__()
		if a:	__s.__args__(*a)
		if k:	__s.__kwargs__(**k)


	def __setattr__(__s, k, v):
		# print('setattr_called with:' ,f'{k=}{v=}')
		k=__s.__expandkey__(k)
		__s[k]=v
		# super().__setitem__(k,v)

	def __getattr__(__s, k):
		# print('getattr_called with:', f'{k=}')
		k = __s.__expandkey__(k)
		return super().__getitem__(k)

	def __setitem__(__s, k, v):
		# print('setitem_called with:' ,f'{k=}{v=}')
		k=__s.__expandkey__(k)
		super().__setitem__(k,v)

	def __getitem__(__s,k,default=None):
		# print('getitem_called with:' ,f'{k=}')
		k=__s.__expandkey__(k)
		return super().__getitem__(k)

	def __get__(__s, k, default=None):
		# print('__get__ called with:' ,f'{k=}{default}')
		k=__s.__expandkey__(k)
		return super().__getitem__(k)

	def __dict__(s):
		sdict=Clict()
		for attr in super().keys():
			sdict[attr]=s[attr]
		return sdict

	def __missing__(__s,k):
		# print('missing called with:' ,f'{k=}')
		missing=Clict()
		missing.__setparent__(__s)
		__s.__setitem__(k,missing)
		return super().__getitem__(k)

	def __contains__(__s, item):

		return (item in __s.__dict__().keys())

	def __iter__(__s):
		return (i for i in __s.__clean__())

	def __args__(__s,*a):
		for arg in a:
			if isinstance(arg, dict):
				__s.__fromdict__(arg)
			elif isinstance(arg,list):
				__s.__fromlist__(arg)

	def __kwargs__(__s,**k):
		for key in k:
			if isinstance(k[key],(dict,list)):
				__s[key]=Clict(k[key])
			else:
				__s[key]=k[key]

	def __hidden__(__s):
		hidden=Clict()
		pfx=__s.__pfx__()
		for key in [*super().__iter__()]:
			if str(key).startswith(pfx):
				nkey=str(key).removeprefix(pfx)
				nkey=str(nkey).removeprefix('_')
				hidden[nkey]=__s.__getitem__(key)
		return hidden

	def __fromdict__(__s, d):
		for key in d:
			if isinstance(d[key],dict):
				__s[key]=Clict(d[key])
			elif isinstance(d[key],list):
				__s[key]=Clict(d[key])
			else:
				__s[key]=d[key]

	def __fromlist__(__s,l):
		for i,item in enumerate(l):
			__s[__s.__expandkey__(i)]=item

	def __setparent__(__s,p):
		__s._parent=lambda : p
		return __s._parent

	def __getparent__(__s):
		k=__s.__expandkey__('_parent')
		return super().get(k)

	def __clean__(__s):
		result=[]
		for key in [*super().__iter__()]:
			if not str(key).startswith(__s.__pfx__()):
				result+=[key]
		return result

	def __pfx__(__s):
		prefix=type(__s).__name__
		pfx = f'_{prefix}_'
		return pfx

	def __expandkey__(__s, k):
		if isinstance(k,(int,float,complex)):
			k=f'_{k}'

		if str(k).startswith('__'):
			pass
		elif str(k).startswith('_'):
			pfx = __s.__pfx__()
			if not str(k).startswith(pfx):
				k=f'{pfx}{k}'
		return k

	def get(__s,k,default=None):
		# print(f'get called with {k}')
		k=__s.__expandkey__(k)
		return super().get(k)

	def keys(__s):
		return __s.__clean__()

	def items(__s):
		Items={}
		keys= __s.__clean__()
		for key in keys:
			Items[key]=super().__getitem__(key)
		return Items

	def values(__s):
		Values=[]
		keys = __s.__clean__()
		for key in keys:
			Values += [super().__getitem__(key)]
		return Values




	def __str__(__s,Color=False):
		if sys.stdout.isatty() or Color:
			pstr=colorstr(__s)
		else:
			pstr='\u007b'+','.join([f"{str(x)}:{str(__s[x])}" for x in __s])+'\u007d'
		return pstr

	def __repr__(__s):
		rstr=treestr(__s)
		return rstr
def colorstr(s):
	ITEMS = []
	cc=CStr()
	for key in s:
		color=CStr()
		KEY = color(key)
		VAL = s[key]
		if isinstance(VAL, str):
			VAL = color(VAL.__repr__())
		elif isinstance(VAL,dict):
			VAL=VAL.__str__()
		ITEMS += [' {KEY} : {VAL} '.format(KEY=KEY, VAL=VAL)]
	ITEMS = ','.join(ITEMS)
	retstr = '{O}{TXT}{C}\x1b[m'.format(TXT=ITEMS, O=cc(O), C=cc(C))
	return retstr
def treestr(s):
	from textwrap import shorten
	def pTree(s, **k):
		d = s
		keys = len(d.keys())
		plines = []
		for key in s:
			if isinstance(d[key],list):
				for item in d[key]:
					if isinstance(item,dict):
						lkey=listtree(d[key])
			dkey = shorten(str(d[key]) if callable(d[key]) else repr(d[key]), 80	)

			keys -= 1
			TREE = "┗━━━┳━╼ " if keys == 0 else "┣━━━┳━╼ "
			plines += [f"{TREE}{str(key)} :"]
			if isinstance(d[key], dict):
				clines = repr(d[key]).split('\n')
				for l, line in enumerate(clines):
					clines[l] = f"┃   {line}" if keys != 0 else f"    {line}"
				plines += clines
			else:
				plines[-1] = plines[-1].replace('┳', '━') + dkey
		return '\n'.join(plines)

	return pTree(s)




def listtree(lst):
	tree=dict()
	for i,item in enumerate(list):
		tree[i]=item
	tstr=treestr(tree)
	print(tstr)
	return tstr
