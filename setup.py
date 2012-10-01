#!/usr/bin/env python

VERSION	= '0.0.33'

from	distutils.core			import	setup
import	glob
import	os
from	DistUtilsExtra.command	import	*

setup(
	name             ='generic-prettyprinter',
	version          = VERSION,
	description      ='Generic Pretty Printer, using plugins',
	author           ='Tommy Reynolds',
	author_email     ='Tommy.Reynolds@MegaCoder.com',
	license          ='GPL',
	url              ='http://www.MegaCoder.com',
	long_description =open('src/gpp/README.txt').read(),
	packages         =['gpp' ],
	package_dir      ={ 'gpp':'src/gpp' },
	package_data     ={ 'gpp': [ 'plugins/*.py' ] },
	scripts			=[
		'scripts/gpp'
	],
)
