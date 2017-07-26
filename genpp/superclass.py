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
        self.sc_footnotes    = []
        return

    def get_lineno( self ):
        return self.sc_lineno

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

    def own_glob( self ):
        try:
            pattern = self.GLOB
            if pattern == '-':
                retval = '-'
            else:
                retval = glob.glob( pattern )
        except Exception, e:
            retval = [ '-' ]
        return retval

    def advise( self, names = [ '-' ] ):
        self.sc_multi = len( names )
        return

    def allow_continuation( self, value = '\\' ):
        self.sc_do_backslash = value
        return

    def start( self ):
        # Called before first file is processed.
        return

    def process( self, name ):
        if name == '-':
            try:
                self.do_open_file( sys.stdin )
            except Exception, e:
                self.error( 'error handling {stdin}' )
                raise e
        elif os.path.isfile( name ):
            try:
                self._do_file( name )
            except Exception, e:
                self.error( 'processing "{0}"'.format( name ) )
                raise e
        elif os.path.isdir( name ):
            try:
                names = sorted( os.listdir( name ) )
            except Exception, e:
                self.error(
                    'could not read directory "{0}"'.format( name )
                )
                raise e
            self.sc_multi += len( names )
            for entry in names:
                if not self.ignore( entry ):
                    try:
                        self.process(
                            os.path.join(
                                name,
                                entry
                            )
                        )
                    except Exception, e:
                        self.error(
                            'could not process derived file "{0}"'.format(
                                name
                            )
                        )
        elif os.path.islink( name ):
            self.error( 'ignoring symlink "%s".' % name )
        else:
            self.error( 'unknown file type, ignoring "%s".' % name )
            raise ValueError
        return

    def pre_begin_file( self, fn = None ):
        return

    def begin_file( self, fn ):
        if self.sc_multi > 1:
            if self.sc_fileno > 1:
                self.println()
            self.println( 'File %d of %d: %s' % (self.sc_fileno, self.sc_multi, fn) )
            self.println()
        return

    def end_file( self, fn ):
        if self.sc_fileno < self.sc_multi:
            self.println()
        self.sc_filename = None
        self.sc_lineno = 0
        return

    def post_end_file( self, name = None ):
        self.report()
        return

    def next_line( self, s ):
        self.println( s )
        return

    def _do_file( self, fn ):
        self.sc_fileno += 1
        self.sc_filename = fn
        self.sc_lineno = 0
        self.pre_begin_file( fn )
        self.begin_file( fn )
        if fn == '-':
            try:
                self.do_open_file( sys.stdin )
            except Exception, e:
                self.error( 'could not process "{stdin}"' )
                raise e
        else:
            try:
                with open( fn, 'rt' ) as f:
                    try:
                        self.do_open_file( f )
                    except Exception, e:
                        self.error( 'processing "{0}" failed.'.format( fn ) )
                        raise e
            except Exception, e:
                self.error( 'could not open "{0}"'.format( fn ) )
                raise e
        self.end_file( fn )
        self.post_end_file()
        return

    def do_open_file( self, f = sys.stdin, name = '{stdin}' ):
        try:
            line = ''
            for segment in f:
                self.sc_lineno += 1
                line += segment.rstrip()
                if self.sc_do_backslash and line[-1] == self.sc_do_backslash:
                    line[-1] = ' '
                    continue
                self.next_line( line )
                line = ''
        except Exception, e:
            self.error( 'error processing file "{0}"'.format( name ) )
            raise e
        return

    def ignore( self, name ):
        return False

    def do_dir( self, dn ):
        for root,dirs,files in sorted( os.walk( dn ) ):
            self.sc_multi += len( files )
            for entry in files:
                if not self.ignore( entry ):
                    self.do_file(
                        os.path.join(
                            root,
                            entry
                        )
                    )
        for dir in sorted( dirs ):
            self.do_dir(
                os.path.join(
                    root,
                    dir
                )
            )
        return

    def println( self, s = '' ):
        print >>self.sc_out, s
        return

    def report( self, final = False ):
        # Called between file openings and at finish
        return

    def finish( self ):
        self.report( final = True )
        self.show_footnotes()
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

    def next_footnote_pos( self ):
        return len(self.sc_footnotes) + 1

    def footnote( self, s ):
        N = self.next_footnote_pos()
        self.sc_footnotes.append( s )
        return N

    def show_footnotes( self, title = 'Footnotes' ):
        if self.sc_footnotes:
            self.println()
            self.println( title )
            self.println( '-' * len( title ) )
            self.println()
            N = len( self.sc_footnotes )
            fmt = '{{0:{0}d}}. {{1}}'.format(
                len( str(N) )
            )
            for n,s in enumerate( self.sc_footnotes ):
                self.println(
                    fmt.format( n+1, s )
                )
            self.sc_footnotes = None
        return
