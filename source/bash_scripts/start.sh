#!/usr/bin/env bash

mkdir -p ~/Data/CIA/factbook/factbook_html_zip && cd $_
wget https://www.cia.gov/the-world-factbook/about/archives/
now=$(date +"%Y-%m-%d-%H-%M-%S")
echo $now > "download.txt" 
awk 'BEGIN{ RS="<a *href *= *\""} NR>2 {sub(/".*/,"");print; }' index.html | grep -o ".*zip$" > zip_links.txt
