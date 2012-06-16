TARGETS=all check clean clobber distclean install uninstall
TARGET=all

PREFIX=${DESTDIR}/opt
BINDIR=${PREFIX}/bin
SUBDIRS=src

INSTALL=install

.PHONY: ${TARGETS} ${SUBDIRS}

all::

${TARGETS}::

clobber distclean:: clean

check::
	./ ${ARGS}

install::

uninstall::
	${RM} ${BINDIR}/

ifneq	(,${SUBDIRS})
${TARGETS}::
	${MAKE} TARGET=$@ ${SUBDIRS}
${SUBDIRS}::
	${MAKE} -C $@ ${TARGET}
endif
