#!/bin/zsh
if [ $# -eq 0 ]; then
	# set -- bdist_rpm --spec-only
	set -- bdist_rpm
fi
python ./setup.py "${@}"
