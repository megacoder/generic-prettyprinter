#!/bin/zsh
if [ $# -eq 0 ]; then
	# set -- bdist --format=bztar
	# set -- bdist --format=gztar
	set -- bdist --format=rpm
fi
markdown2 README.md | tee src/gpp/README.html | lynx -dump -stdin >src/gpp/README.txt
python ./setup.py "${@}"
