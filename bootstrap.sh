#!/bin/zsh
if [ $# -eq 0 ]; then
	# set -- bdist_rpm --spec-only
	set -- bdist_rpm
fi
if [ ! -f src/gpp/README.txt ]; then
	markdown2 README.md | tee src/gpp/README.html | lynx -dump -stdin >src/gpp/README.txt
fi
python ./setup.py "${@}"
