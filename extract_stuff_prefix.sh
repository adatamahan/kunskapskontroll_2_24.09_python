#!/bin/bash

prefix=${1:-hcaeventyr0}

tei_files=(texts/${prefix}*)

for file in ${tei_files[@]}; do

    echo $file
    data_file_base=`basename "$file" .xml`

    xsltproc  get_titles.xsl $file > "$data_file_base"_titles.text
    xsltproc --stringparam source "$data_file_base"  get_the_text.xsl  $file

done    
