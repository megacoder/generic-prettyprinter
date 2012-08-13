#!/usr/bin/env python

from	distutils.core			import	setup
import	glob
import	os
from	DistUtilsExtra.command	import	*

setup(
	name             ='generic-prettyprinter',
	version          ='0.0.13',
	description      ='Generic Pretty Printer, using plugins',
	author           ='Tommy Reynolds',
	author_email     ='Tommy.Reynolds@MegaCoder.com',
	license          ='GPL',
	url              ='http://www.MegaCoder.com',
	long_description =open('README').read(),
	packages         =['gpp' ],
	package_dir      ={ 'gpp':'src/gpp' },
	package_data     ={ 'gpp': [ 'plugins/*.py' ] },
	entry_points     ={
		'console_scripts': [
			'gpp = gpp:Main'
		]
	},
	scripts			=[
		'scripts/gpp'
	],
)
