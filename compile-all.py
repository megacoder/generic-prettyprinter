#!/usr/bin/python
# vim: noet sw=4 ts=4

import	compileall
import	sys

sys.stderr = sys.stdout

compileall.compile_dir( 'generic_prettyprinter', force = 1 )
