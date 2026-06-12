#!/bin/bash
dir=`dirname $(readlink -f $0)`
dir=`readlink -f $dir/../`
echo $dir
python3 -m venv venv
source $dir/venv/bin/activate
pip install -r $dir/scripts/requirement.txt
mkdir output
ln -s ../lib output/lib
