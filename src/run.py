#!/usr/bin/env python3

from sys import argv,stderr

arg_conf="--make-config"

if not(len(argv) == 3 or (len(argv)==2 and argv[1]==arg_conf)):
    name = argv[0].split('/')[-1]
    print('''
    %s <config file> <exported local zotero CSV>

 or %s %s


''' % (name,name, arg_conf), file=stderr)
    exit(-1)


from GoogleShareable import *
from ZotExportReader import *
from ZoteroEdit import *
from Config import *
from helper import *

conf    = Config(argv[1])
csvfile = argv[2]

exit(0)

# Map out google shares and Zotero export
#
goog = GoogleShareable( gfold, gfold+".output.txt" )  # Map: pdf -> sharelink
zoer = ZotExportReader( csvfile )                     # Map: pdf -> [{title, year, author, PDF}]

title_map = intersect_maps( goog.map, zoer.map )

zed = ZoteroEdit( zlibid, api_key, title_map, debug )
col = zed.findCollectionID( zname )

zed.processItems( col, work_mode )
