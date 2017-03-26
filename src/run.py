#!/usr/bin/env python3

from sys import argv

if len(argv) != 3:
    print('''
    %s <config file> <exported local zotero CSV>

See README.md for config examples
''' % argv[0].split('/')[-1], file=sys.stderr)
    exit(-1)


from GoogleShareable import *
from ZotExportReader import *
from ZoteroEdit import *
from helper import *
from kludge import *

Kludge()

gfold, zlibid, zname, work_mode, api_key, debug = readInSettings(argv[1])
csvfile = argv[2]

# Map out google shares and Zotero export
#
goog = GoogleShareable( gfold, gfold+".output.txt" )  # Map: pdf -> sharelink
zoer = ZotExportReader( csvfile )                     # Map: pdf -> [{title, year, author, PDF}]

title_map = intersect_maps( goog.map, zoer.map )

zed = ZoteroEdit( zlibid, api_key, title_map, debug )
col = zed.findCollectionID( zname )

zed.processItems( col, work_mode )
