# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 07:42:10 2019

@author: 李鹏飞
"""

Learn something new,：

1. for cycling through a list of contents:

    markers = itertools.cycle(("+","*","o"))
    marker = next(markers)

2. to get ta string for the current time including year, month and weeks：
    FileNameExt = time.strftime("%d%m%Y_%H-%M-%S")
	
3. matplotlib new version >2.0.0 seems gives different behavior, the figure always pops up to front and given focus. solutions: 1. still questionable, downgrade matplotlib to lower version? 2. find solution to not focus. This means I might have to use the older version of all packages for python. Tried: down graded to 2.0.0 but failed, due to png or some other packages not satisfying to the system.
