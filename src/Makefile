TARGETS=all check clean clobber distclean install uninstall
TARGET=all

PREFIX=${DESTDIR}/opt
BINDIR=${PREFIX}/bin
SUBDIRS=

INSTALL=install

.PHONY: ${TARGETS} ${SUBDIRS}

define	INSTALL_template
.PHONY:	install-${1}
install:: install-${1}
install-${1}:: ${1}
	@cmp -s $${BINDIR}/${1} ${1} || /bin/sh -xc "${INSTALL} -Dc -m ${MODE} ${1} ${PREFIX}/${1}"
endef

FILES	:=$(wildcard *-pp)

all::	${FILES}

${TARGETS}::

clobber distclean:: clean

check::	${FILES}
	./${FILES} ${ARGS}

$(foreach f,${FILES},$(eval $(call INSTALL_template,${f})))

uninstall::
	cd ${BINDIR} && ${RM} ${FILES}

ifneq	(,${SUBDIRS})
${TARGETS}::
	${MAKE} TARGET=$@ ${SUBDIRS}
${SUBDIRS}::
	${MAKE} -C $@ ${TARGET}
endif
