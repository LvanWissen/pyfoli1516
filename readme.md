# Thesis Analyzer

Commandlinetool to generate statistics for *.NAF.nohyphen files. 

### How to use
    usage: 
        main.py [-h] [-p path [path ...]] [-l [list]] [-lang [language]]
       [-study [study]] [-s [stats]] [-sid [stats_id]] [-kml [kml]]

    optional arguments:
      -h, --help          show this help message and exit
      -p path [path ...]  path to a directory containing thesises
      -l [list]           returns list of thesises stored under specified
                          directory
      -lang [language]    optional: possibility to filter on language
      -study [study]      optional: possibility to filter on study
      -s [stats]          generate statistics for specified optional filters -lang
                          and -study
      -sid [stats_id]     generate statistics for specified thesis id. Use -l to
                          get the thesis id
      -kml [kml]          generate kml output for specified study (-study)
      
#### Example usage
```sh
$ python.py -p \home\user\thesis_vu_2015 -l 
```
```sh
$ python.py -p \home\user\thesis_vu_2015 -s -lang nl -study ltk
```
```sh
$ python.py -p \home\user\thesis_vu_2015 -kml -study fil
```


### Requirements

* Anaconda Python installation and packages
* simplekml (http://simplekml.readthedocs.org/en/latest/)



