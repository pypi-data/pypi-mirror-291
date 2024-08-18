#!/usr/bin/env bash
set -e

tmp=$(mktemp -d feathercarver.XXXXX)

if [ -z "${tmp+x}" ] || [ -z "$tmp" ]; then
    echo "error: $tmp is not set or is an empty string."
    exit 1
fi

if ! command -v txtar-c >/dev/null; then
    echo go install github.com/rogpeppe/go-internal/cmd/txtar-c@latest
	exit 1
fi

declare -a files=(
	# Makefile # loc: 3
	# README.md # loc: 5
	# make_txtar.sh # loc: 54
	# pyproject.toml # loc: 36
	# requirements-dev.lock # loc: 39
	# requirements.lock # loc: 15
	src/feathercarver/__init__.py # loc: 20
	src/feathercarver/__main__.py # loc: 6
	src/feathercarver/argument_parser.py # loc: 14
	src/feathercarver/file_processor.py # loc: 19
	src/feathercarver/link_fixer.py # loc: 48
	# test.md # loc: 1
	tests/test_link_fixer.py # loc: 203
	
)
for file in "${files[@]}"; do
    echo "$file"
done | tee $tmp/filelist.txt

tar -cf $tmp/feathercarver.tar -T $tmp/filelist.txt
mkdir -p $tmp/feathercarver
tar xf $tmp/feathercarver.tar -C $tmp/feathercarver
rg --no-ignore --hidden --files $tmp/feathercarver

mkdir -p $tmp/gpt_instructions_XXYYBB

cat >$tmp/gpt_instructions_XXYYBB/1.txt <<EOF

EOF

{
    cat $tmp/gpt_instructions_XXYYBB/1.txt
    echo txtar archive is below
    txtar-c -quote -a $tmp/feathercarver
} | pbcopy

rm -rf $tmp
