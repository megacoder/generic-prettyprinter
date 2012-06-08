TARGETS=all check clean clobber distclean install uninstall
TARGET=all

PREFIX=${DESTDIR}/opt
BINDIR=${PREFIX}/bin
SUBDIRS=

INSTALL=install

.PHONY: ${TARGETS} ${SUBDIRS}

PPFILES	:=$(wildcard *-pp)

all::	${PPFILES}

${TARGETS}::

clobber distclean:: clean

check::	${PPFILES}
	./${PPFILES} ${ARGS}

install:: ${PPFILES}
	for pp in ${PFILES}; do						\
		${INSTALL} -D $${pp} ${BINDIR}/$${pp};			\
	done

uninstall::
	cd ${BINDIR} && ${RM} ${PPFILES}

ifneq	(,${SUBDIRS})
${TARGETS}::
	${MAKE} TARGET=$@ ${SUBDIRS}
${SUBDIRS}::
	${MAKE} -C $@ ${TARGET}
endif
