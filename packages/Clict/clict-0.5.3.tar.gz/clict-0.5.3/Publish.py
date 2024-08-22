#!/usr/bin/env python
KEY='\x1b[1;38;2;255;255;255m{K}\x1b[m'

keys=['Project', 'Version','Tests','Result','Upgrading''Building' ]
X=[1,40,1,40,1]
for K in enumerate(keys):
	KEY.format(X=1,Y=i+1,K=K)


L4'|         '
L5'| GIT:              '
L6'| Stage:            '
L7'| Commit:           '
L8'| Push:             '
