# Get the raw data

This is [my raw data source](https://www.cia.gov/the-world-factbook/about/archives/). Here there compressed html files (years 2000 up to 2020). You can find older info in [Project Gutenberg](https://www.gutenberg.org/).

## Steps, Linux Machine

### First step
Go to [source/bash_scripts](./source/bash_scripts) and execute the script start.sh

The script start.sh builds the directory [~/Data/CIA/factbook/factbook_html_zip](~/Data/CIA/factbook/factbook_html_zip).
This script uses wget to download an html page from [my raw data source](https://www.cia.gov/the-world-factbook/about/archives/), and then uses awk to extract some urls to zip files.

You can find the output of start.sh at the directory [~/Data/CIA/factbook/factbook_html_zip](~/Data/CIA/factbook/factbook_html_zip): 
1. index.html
2. download.txt
3. zip_links.txt

### Second step
Go to [source/bash_scripts](./source/bash_scripts) and execute the script download.sh

### Third step
After downloading, go to [source/bash_scripts](./source/bash_scripts) and execute the script unzip_factbook.sh
 
