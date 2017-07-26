#!/bin/sh
if [ $# -eq 0 ]; then
	set -- bztar gztar rpm
fi
rm -rf build dist
(
	for PKG in "${@}"; do
		python ./setup.py bdist --format="${PKG}"
	done
) 2>&1 | tee build.log
