#!/usr/bin/env python
from random import randint
import os

def rgbl2str(rgbl):
	return ';'.join([str(c) for c in rgbl])


def CStr(**k):
	front = k.get('front', k.get('f', color()))
	back = k.get('back', k.get('b', None))
	def cstr(txt):
		if isinstance(front,list):
			CC=front
			ANSI = '\x1b[0;38;2;{COLOR}m{TXT}\x1b[m'.format(COLOR=rgbl2str(CC),TXT='{TXT}')
		if isinstance(back,list):
			CC=back
			ANSI = '\x1b[0;48;2;{COLOR}m{TXT}\x1b[m'.format(COLOR=rgbl2str(CC),TXT=ANSI)
		return ANSI.format(TXT=txt)
	return cstr


def color():
	import sys
	from Clict.lib import fnterm
	if sys.stdout.isatty():
		term=fnterm.info()
		bgval=term['color']['bg']['sum']
	else:
		bgval=0
	cs={}
	rnd = lambda i,j: randint(i, j)
	rgb = lambda: randint(0, 2)
	cs  = [rnd(0,255), rnd(0,255), rnd(0,255)]

	a=lambda : sum(cs) > 512
	b=lambda : sum(cs) < 255
	cond=a if (bgval < 0.5) else b
	while not cond():
		change = rgb()
		rng=(cs[change],255) if (bgval < 0.5) else (0,cs[change])
		newval = rnd(*rng)
		cs[change] = newval

	return cs



def tree_str(s):
	import sys
	from textwrap import shorten
	# from src.isPyPackage.ansi_colors import reset,rgb,yellow,red
	def hasDict(s):
		return any([True for key in s if isinstance(s[key], dict)])

	def overview(s):
		dicts = [item for item in s if isinstance(s[item], dict)]
		sd = len(dicts)
		ld = len(s) - sd
		sd = rgb('yellow', sd)
		ld = rgb('red', ld)
		reset=rgb('reset')
		print(f'({sd}Groups+{ld}items){reset}', end='')

	def pTree(s, **k):
		fancystr = ''
		depth = k.get('depth', 0)
		maxd = 100
		limi = 100
		d = s
		keys = len(d.keys())
		plines = []
		for key in s:
			dkey = shorten(
				f"\x1b[32m{d[key]}\x1b[0m" if callable(d[key]) else str(d[key]), 80
			)
			keys -= 1
			TREE = "┗━┳╼' " if keys == 0 else "┣━━┳╼' "
			plines += [f"{TREE}{str(key)} :"]
			if isinstance(d[key], Clict):
				# plines[-1]=plines[-1].replace('━','┳',2,1)
				clines = repr(d[key]).split('\n')
				for l, line in enumerate(clines):
					clines[l] = f"┃ {line}" if keys != 0 else f"  {line}"
				# fancystr+="  ┗━━ " if keys == 0 else "  ┣━━ "
				# fancystr+=f"\x1b[1;34m{str(key)}\t:\x1b[0m\t"
				# fancystr+='\n'.join(["  ┃  " * (depth)+line for  line in repr(s[key])])
				plines += clines
			else:
				plines[-1] = plines[-1].replace('┳', '━') + dkey
		return '\n'.join(plines)

	return pTree(s)

