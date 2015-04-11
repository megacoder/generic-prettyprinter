#!/bin/zsh
if [ $# -eq 0 ]; then
	# set -- bdist --format=bztar
	# set -- bdist --format=gztar
	set -- bdist --format=rpm
fi
(
	set +x
	python ./setup.py "${@}"
) 2>&1 | tee bootstrap.log
