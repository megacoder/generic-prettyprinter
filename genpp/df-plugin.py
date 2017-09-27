#!/usr/bin/python

import	os
import	sys
import  superclass
import  align

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'df-pp'
    DESCRIPTION = """Display df(1) output in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.pre_open_file()
        return

    def pre_open_file( self ):
        self.items   = align.Align( titles = 1 )
        return

    def next_line( self, line ):
        tokens = map(
            str.strip,
            line.split( '#', 1 )[0].split()
        )
        if len( tokens ) > 0:
            if tokens[0] == 'Filesystem':
                # Coalesce 'Mounted' 'on' into 'Mounted on'
                tokens[-2] = ' '.join( tokens[-2:] )
                # Save all but isolated 'on', which is the final arg
                tokens = tokens[:-1]
            self.items.add( tokens )
        return

    def report( self, final = False ):
        if not final:
            self.items.set_title_alignment( 'aaaaal' )
            self.items.set_alignment( 'laaaal' )
            for _,tokens in self.items.get_items():
                self.println( ' '.join( tokens ) )
        return

if __name__ == '__main__':
    fn = '<selftest>'
    pp = PrettyPrint()
    pp.pre_begin_file()
    pp.begin_file( fn )
    for line in [

'Filesystem     1K-blocks Used Available Use% Mounted on',
'devtmpfs         8074184 0   8074184   0% /dev',
'tmpfs            8087180 77472   8009708   1% /dev/shm',
'tmpfs            8087180 1596   8085584   1% /run',
'tmpfs            8087180 0   8087180   0% /sys/fs/cgroup',
'/dev/sda3      973615104 16010288 955722896   2% /',
'tmpfs            8087180 1464   8085716   1% /tmp',
'/dev/sda1         999320 179612    750896  20% /boot',
'/dev/sdc1      976760000 917364256  53972544  95% /home',
'/dev/sdc1      976760000 917364256  53972544  95% /opt',
'tmpfs            1617440 16   1617424   1% /run/user/42',
'tmpfs            1617440 40   1617400   1% /run/user/1000',
'ACDFuse         10485760 -9444732965739215659520 -64282112 100% /home/reynolds/cloud/acd',


    ]:
        pp.next_line( line )
    pp.end_file( fn )
    pp.post_end_file()
    pp.report( final = True )

