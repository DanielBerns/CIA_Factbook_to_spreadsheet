# CIA_Factbook_to_spreadsheet
I want to extract country info from [CIA World Factbook](https://www.cia.gov/the-world-factbook/) (aka the Factbook), just for learning python and data munging. 

Note that [github.com/factbook](https://github.com/factbook) is a complete info source about the Factbook. There you can find the repo [factbook.json](https://github.com/factbook/factbook.json.git) with json formatted info extracted from the Factbook.


## Get the raw data

This is [my raw data source](https://www.cia.gov/the-world-factbook/about/archives/). Here there compressed html files (years 2000 up to 2020). You can find older info in [Project Gutenberg](https://www.gutenberg.org/).

### Steps, Linux Machine

#### First step
Go to [source/bash_scripts](./source/bash_scripts) and execute the script start.sh

The script start.sh builds the directory [~/Data/CIA/factbook/factbook_html_zip](~/Data/CIA/factbook/factbook_html_zip).
This script uses wget to download an html page from [my raw data source](https://www.cia.gov/the-world-factbook/about/archives/), and then uses awk to extract some urls to zip files.

You can find the output of start.sh at the directory [~/Data/CIA/factbook/factbook_html_zip](~/Data/CIA/factbook/factbook_html_zip): 
1. index.html
2. download.txt
3. zip_links.txt

#### Second step
Go to [source/bash_scripts](./source/bash_scripts) and execute the script download.sh




