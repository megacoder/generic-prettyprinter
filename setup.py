#!/usr/bin/env python

from distutils.core import setup

setup(
	name         ='gpp',
	version      ='1.0',
	description  ='Generic Pretty Printer, using plugins',
	author       ='Tommy Reynolds',
	author_email ='Tommy.Reynolds@MegaCoder.com',
	url          ='http://www.MegaCoder.com',
	packages     =['src', 'src/plugins'],
	package_dir = { 'gpp' : 'src' },
)
