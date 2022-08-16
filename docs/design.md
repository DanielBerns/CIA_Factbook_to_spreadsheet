# Development

Goal: learn how to develop software doing data scraping from the CIA World Factbook

## sprint #1 20220808

1. Download data from CIA website and decompress them
2. Data files live in ~/Data/CIA/factbook/factbook_html_zip

### Bash scripts
I use bash scripts to download zip files with the data from the CIA website and decompress them. 
However, I want to use python scripts, to configure all the code from one point (a class Config)


## sprint #2 20220810 

1. Define how to test python code
2. Define how to configure apps

### Python imports and tests
I found a way to structure python imports, including those in the tests code. 
I merge:
1. the style from [Microblog](https://github.com/miguelgrinberg/microblog), a flask application by Miguel Grinberg;
2. the style from  [Python structure](https://docs.python-guide.org/writing/structure/).

Problems:

1. The problem with **Microblog** style is all the tests live in a file, in the same directory of datamunging apps.
2. The problem with **Python structure** style is that I like *Microblog* style :-; and I don't know how to use in tests.

### data_munging conventions

#### Reports files
1. Reports files live in "~/Reports/data_munging/CIA_World_Factbook-alpha". This setting can be modified partially in data_munging/config.py, constant APPLICATION

#### Configuration
1. python-dotenv to read dotenv files
2. Config class to get environment variables
3. The datamunging apps have a mandatory cli argument: the path to a dotenv file (fixed filename .env), containing a number of key value pairs. The user can change the path to the dotenv file just to do some experiments with different values for the mandatory keys. Given that ".env" files are hidden, write a readme.md in the same directory
4. Content of dotenv files can evolved with time.

#### Code
 |--> bash_scripts              # to be replaced with python code, just to use config.py
 |      |--> start.sh
 |      |--> download.sh
 |      |--> unzip_factbook.sh
 |--> data_munging
 |      |--> actions/
 |      |--> tests/
 |      |--> config.py
 |      |--> data_munger.py
 |      |--> tests_data_munger.py
 |--> demos                    # practice code here
        |--> configure.py      # python-dotenv


## sprint #3 20220816

Now, I have data from the CIA World Factbook, years 2000 to 2020, downloaded and unzipped in ~/Data/CIA/factbook/factbook_html_zip

1. I need to read all the files, one at the time, scrap the data and write some records for further processing.

2. I have seen the [video](https://www.youtube.com/watch?v=iCE1bDoit9Q). 
