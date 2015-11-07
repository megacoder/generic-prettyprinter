#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  glob

class   MetaPrettyPrinter( object ):

    """
        Populate this!
    """

    NAME        = 'superclass'
    DESCRIPTION = 'Man behind the curtain.'
    USAGE       = None
    GLOB        = '*'
    HELPFMT     = '%23s | %s'

    def __init__( self ):
        self.reset()
        return

    def reset( self ):
        self.sc_out          = sys.stdout
        self.sc_fileno       = 0
        self.sc_lineno       = 0
        self.sc_filename     = '{stdin}'
        self.sc_multi        = 0
        self.sc_do_backslash = None
        self.sc_footnotes    = None
        return

    def get_out( self ):
        return self.sc_out

    def get_fileno( self ):
        return self.fc_fileno

    def get_filename( self ):
        return self.filename

    def get_multi( self ):
        return self.multi

    def get_backslash( self ):
        return self.sc_do_backlash

    def own_glob( self, pattern = None ):
        if not pattern:
            pattern = self.GLOB
        if pattern:
            retval = glob.glob( pattern )
        else:
            retval = []
        return retval

    def advise( self, **kwargs ):
        for key in kwargs:
            if key == 'argc':
                self.sc_multi = kwargs[key]
        return

    def allow_continuation( self, value = '\\' ):
        self.sc_do_backslash = value
        return

    def start( self ):
        return

    def do_name( self, name ):
        if os.path.isfile( name ):
            self.do_file( name )
        elif os.path.isdir( name ):
            self.sc_multi = 2
            self.do_dir( name )
        elif os.path.islink( name ):
            self.error( 'ignoring symlink "%s".' % name )
        else:
            self.error( 'unknown file type, ignoring "%s".' % name )
            raise ValueError
        return

    def pre_begin_file( self ):
        return

    def begin_file( self, fn ):
        if self.sc_multi > 1:
            self.println( 'File %d of %d: %s' % (self.sc_fileno, self.sc_multi, fn) )
            self.println()
        return

    def end_file( self, fn ):
        if self.sc_fileno < self.sc_multi:
            self.println()
        self.sc_filename = None
        self.sc_lineno = 0
        return

    def post_end_file( self ):
        self.report()
        return

    def next_line( self, s ):
        self.println( s )
        return

    def do_file( self, fn ):
        self.sc_fileno += 1
        self.sc_filename = fn
        self.sc_lineno = 0
        self.pre_begin_file()
        self.begin_file( fn )
        try:
            with open( fn, 'rt' ) as f:
                self.do_open_file( f )
        except Exception, e:
            raise e
        self.end_file( fn )
        self.post_end_file()
        self.show_footnotes()
        return

    def do_open_file( self, f = sys.stdin ):
        line = ''
        for segment in f:
            self.sc_lineno += 1
            line += segment.rstrip()
            if self.sc_do_backslash and line[-1] == self.sc_do_backslash:
                line[-1] = ' '
                continue
            self.next_line( line )
            line = ''
        return

    def ignore( self, name ):
        return False

    def do_dir( self, dn ):
        try:
            files = os.listdir( dn )
        except Exception, e:
            self.error( 'cannot list directory "%s".' % dn, e )
            raise e
        files.sort()
        for fn in files:
            if not self.ignore( fn ):
                self.do_name( os.path.join( dn, fn ) )
        return

    def println( self, s = '' ):
        print >>self.sc_out, s
        return

    def report( self, final = False ):
        return

    def finish( self ):
        self.report( final = True )
        return

    def error( self, msg, e = None ):
        self.sc_out.flush()
        if self.sc_filename is not None:
            print >>sys.stderr, 'File %s: ' % self.sc_filename,
        if self.sc_lineno > 0:
            print >>sys.stderr, 'Line %d: ' % self.sc_lineno,
        print >>sys.stderr, msg
        if e is not None:
            print >>sys.stderr, e
            raise e
        return

    def help( self, details = False ):
        self.println(
            self.HELPFMT % (
                self.NAME,
                self.DESCRIPTION
            )
        )
        if self.USAGE:
            self.println(
                self.HELPFMT % (
                    '',
                    self.USAGE
                )
            )
        if details:
            self.println(
                '',
                self.__doc__
            )
        return

    def footnote( self, s ):
        if not self.sc_footnotes:
            self.sc_footnotes = []
        self.sc_footnotes.append( s )
        return

    def show_footnotes( self ):
        if self.sc_footnotes:
            self.println()
            title = 'Footnotes'
            self.println( title )
            self.println( '-' * len( title ) )
            self.println()
            for n,s in enumerate( self.sc_footnotes ):
                self.println(
                    '{0:2d}: {1}'.format(
                        n+1,
                        s
                    )
                )
