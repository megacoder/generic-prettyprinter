#!/usr/bin/python

import	os
import	sys
import  superclass
import  align

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'nsswitch-pp'
    DESCRIPTION = """Display nsswitch.conf in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.pre_open_file()
        return

    def pre_open_file( self ):
        self.lines   = []
        return

    def next_line( self, line ):
        # Drop comments
        parts = line.split( '#', 1 )[0].strip().split()
        if len( parts ) > 0:
            # Save non-blank lines
            self.lines.append( parts )
        return

    def report( self, final = False ):
        if not final:
            self.lines.sort()
            a = align.Align()
            for parts in self.lines:
                a.add( parts )
            for _,parts in a.get_items():
                self.println( ' '.join( parts ) )
        return

if __name__ == '__main__':
	fn = '<selftest>'
	pp = PrettyPrint()
	pp.pre_begin_file()
	pp.begin_file( fn )
	for line in [
            'bootparams: nisplus [NOTFOUND=return] files',
            'ethers:     files',
            'netmasks:   files',
            'networks:   files',
            'protocols:  files',
            'rpc:        files',
            'services:   files sss',
            'netgroup:   files sss',
            'publickey:  nisplus',
            'automount:  files sss',
            'aliases:    files nisplus',
	]:
		pp.next_line( line )
	pp.end_file( fn )
	pp.post_end_file()
	pp.report( final = True )

