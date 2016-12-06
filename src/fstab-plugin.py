#!/usr/bin/python
# Print /etc/fstab getting the fields as close to their intended columns as may
# be.  Long fields push the remainder of the line over as little as is possible
# so that the columns come nearer to alignment.

import	os
import	sys
import  superclass
import  align

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'fstab-pp'
    DESCRIPTION = """Display /etc/fstab files in canonical style."""
    GLOB = None

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def pre_begin_file( self, name = None ):
        super( PrettyPrint, self ).pre_begin_file( name )
        self.entries = align.Align( lj = True )
        return

    def next_line( self, line ):
        items = line.split( '#', 1 )[0].split()
        nItems = len( items )
        # Discard all but regular or bind-mount, lines
        try:
            if (nItems == 4) or (nItems == 6):
                # Make sure mount options are in canonical order
                options = items[ 3 ].split( ',' )
                options.sort()
                items[ 3 ] = ','.join(
                    options
                )
                self.entries.add( items )
        except Exception, e:
            print >>sys.stderr, 'Error handling "{0}"'.format( line )
            print >>sys.stderr, e
        return

    def report( self, final = False ):
        if not final:
            # Output each line with columns according to formats
            for _,items in self.entries.get_items():
                footnote = None
                if len(items)>=5 and items[3]=='nfs' and items[4]=='default':
                    footnote = self.footnote(
                        'NFS default options used; probably slow'
                    )
                self.println(
                    ' '.join( items ) +
                    ('\t*** See footnote %s'.format( footnote ) if footnote
                    else '')
                )
        return

if __name__ == '__main__':
    fn = '<selftest>'
    pp = PrettyPrint()
    pp.pre_begin_file()
    pp.begin_file( fn )
    for line in [
        'UUID=77aa3f76-8f52-49eb-a96b-0c9d72524164 / btrfs subvol=root  0 0',
        'UUID=461d0ef4-1fa3-4c82-854e-3967610f30f1 /boot  ext4 defaults 1 2',
        'UUID=9107d4e3-1572-42dd-bae6-2693f2481cc5 swap swap defaults 0 0',
        'UUID="e5cc94fb-a78e-4f35-9b18-f430ce17c4ae" /home btrfs  defaults 0 0',
        'UUID="ccb40cbc-a095-484e-bbd4-9789cbbc7cdf" /archive btrfs noauto,user 0 0',
        '/home/opt	/opt	 none 	bind',
        '/home/docker	/var/lib/docker none bind',
        '/home/go	/go		none bind',
    ]:
            pp.next_line( line )
    pp.end_file( fn )
    pp.post_end_file()
    pp.report( final = True )

