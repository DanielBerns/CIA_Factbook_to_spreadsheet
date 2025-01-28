#!/usr/bin/env bash

mkdir -p ~/Data/CIA/factbook/factbook_html_zip && cd $_
wget https://www.cia.gov/the-world-factbook/about/archives/

# see https://www.cyberciti.biz/faq/unix-linux-appleosx-bsd-shell-appending-date-to-filename/
now=$(date +"%Y-%m-%d-%H-%M-%S")
echo $now > "download.txt" 

# see https://www.unix.com/shell-programming-and-scripting/146238-extract-urls-index-html-downloaded-using-wget.html
awk 'BEGIN{ RS="<a *href *= *\""} NR>2 {sub(/".*/,"");print; }' index.html | grep -o ".*zip$" > zip_links.txt
