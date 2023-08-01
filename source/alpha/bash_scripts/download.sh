#!/usr/bin/env bash

cd ~/Data/CIA/factbook/factbook_html_zip

# see https://stackoverflow.com/questions/40986340/how-to-wget-a-list-of-urls-in-a-text-file
wget -i zip_links.txt
