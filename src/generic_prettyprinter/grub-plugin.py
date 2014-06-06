#!/usr/bin/python

import  re
import  os
import  sys
import  math
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'grub-pp'
    DESCRIPTION="""Output /boot/grub/grub.conf in canonical form."""

    def __init__( self, out = sys.stdout ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self._prepare()
        return

    def _prepare( self ):
        self.default   = 0
        self.in_stanza = False
        self.stanza    = []
        self.widths    = {}
        self.content   = []
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def _end_stanza( self ):
        if self.in_stanza:
            self.stanza.sort()
            self.content.append(
                ( True, self.stanza )
            )
            self.in_stanza = False
            self.stanza = []
        return

    def end_file( self, name ):
        self._end_stanza()
        self._show()
        super( PrettyPrint, self ).end_file( name )
        return

    def next_line( self, line ):
        if len(line) == 0: return
        if line[0] == '#':
            self.content.append(
                ( False, [line] )
            )
        else:
            line = line.split( '#', 1 )[0].rstrip()
            if line[0].isspace():
                tokens = line.split()
                n = len(tokens)
                if n > 0:
                    for i in xrange( 0, n ):
                        try:
                            self.widths[i] = max(
                                self.widths[i],
                                len(tokens[i])
                            )
                        except Exception, e:
                            self.widths[i] = len(tokens[i])
                    self.in_stanza = True
                    self.stanza.append( tokens )
            else:
                self._end_stanza()
                if line.startswith( 'default=' ):
                    self.default = int( line[8:] )
                    self.content.append(
                        ( False, [line] )
                    )
                elif line.startswith( 'title' ):
                    self.content.append(
                        ( False, [line] )
                    )
        return

    def _show( self ):
        title_no = -1
        for (detail,entry) in self.content:
            if detail:
                for tokens in entry:
                    n = len(tokens)
                    sep = '\t'
                    for i in xrange( 0, n ):
                        fmt = '%%s%%-%-ds' % self.widths[i]
                        print fmt % (sep, tokens[i]),
                        sep = ' '
                    print
            else:
                line = entry[0]
                if line.startswith( 'title' ):
                    title_no += 1
                    mo = re.search(  r'^.*\((.*)\).*$', line )
                    if mo is None:
                        extra = ''
                    else:
                        extra = mo.group(1)
                    print '#'
                    if self.default == title_no:
                        print '# Stanza %d: (DEFAULT) %s' % (title_no, extra)
                    else:
                        print '# Stanza %d: %s' % (title_no, extra)
                    print '#'
                print line
