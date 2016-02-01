import argparse
import logging
import os

from functions import *
from classes import *

# ARGPARSE
parser = argparse.ArgumentParser(description='Thesis analyzer')
parser.add_argument('-p', metavar='path', nargs='+', default=[False],
                   help='path to a directory containing thesises')
parser.add_argument('-l', metavar='list', nargs='?', default=True,
                   help='returns list of thesises stored under specified directory')
parser.add_argument('-lang', metavar='language', nargs='?',
                   help='optional: possibility to filter on language')
parser.add_argument('-study', metavar='study', nargs='?',
                   help='optional: possibility to filter on study')
parser.add_argument('-s', metavar='stats', nargs='?', default=True,
                   help='generate statistics for specified optional filters -lang and -study')
parser.add_argument('-sid', metavar='stats_id', nargs='?',
                   help='generate statistics for specified thesis id. Use -l to get the thesis id')
parser.add_argument('-kml', metavar='kml', nargs='?', default=True,
                   help='generate kml output for specified study (-study)')

args = parser.parse_args()
path = args.p[0]
to_list = not(args.l)
lang = args.lang
study = args.study
kml = not(args.kml)
stats = not(args.s)
stats_id = args.sid

# if no path has been given, ask for one:
if path == False:
    path = input("Specify path to a folder containing thesises: ")

    print("Possible commands to give ")

# check if the inputted path is really an existing directory
try:
    assert os.path.isdir(path)
except AssertionError:
    print("Input is not a (valid) directory!")
    raise SystemExit

print(path)

rootdir = RootDir(path)

print()

if to_list:
    print("Listing all thesises based on filter lang=%s and study=%s:" % (lang, study))
    rootdir.list(lang, study, True)

if stats:
    print("Parsing files for study %s and language %s. This may take a while!" % (study, lang))
    rootdir.get_stats(lang=lang, study=study)

if stats_id:
    print("Parsing thesis %s:" % stats_id)
    rootdir.get_stats_id(int(stats_id))


if kml and study:
    print("Parsing files for study", study)
    rootdir.get_kml(study=study)
elif kml:
    print("You must specify a study to generate the kml! See -h for help!")
    raise SystemExit

if all((to_list, stats, stats_id, kml)) == False:
    print("See -h help for possible commands!")










