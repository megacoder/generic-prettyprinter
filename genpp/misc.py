#!/usr/bin/python
# vim: noet sw=4 ts=4

def	peel( iterable, qty ):
	iterator = iter( iterable )
	for num in xrange( qty ):
		yield iterator.next()
	yield iterator
	return

if __name__ == '__main__':
	t5 = range( 1, 6 )
	print 't5={0}'.format( t5 )
	a, b, c = peel( t5, 2 )
	print 'a={0}, b={1}, c={2}'.format(
		a,
		b,
		list(c)
	)
