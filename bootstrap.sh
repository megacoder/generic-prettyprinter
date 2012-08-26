#!/bin/zsh
if [ $# -eq 0 ]; then
	# set -- bdist_rpm --spec-only
	set -- bdist_rpm
fi
if [ ! -f README ]; then
	markdown2 README.md | lynx -dump -stdin >README
fi
python ./setup.py "${@}"
