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
from ZoteroEdit      import *
from HashFiles       import *
from Config          import *
from helper          import *

setting = Config(argv[1]).setting
csvfile = argv[2]

# For non-Zotero storage, hash out files in the external storage
if setting['pdf','storage'] != "":
    HashFiles( setting['pdf','storage'] )
   
exit(0)

# Map out google shares and Zotero export
#
#goog = GoogleShareable( gfold, gfold+".output.txt" )  # Map: pdf -> sharelink
#zoer = ZotExportReader( csvfile )                     # Map: pdf -> [{title, year, author, PDF}]

#title_map = intersect_maps( goog.map, zoer.map )
title_map = {}

# Edit personal library and/or sync or clone to a group one
zed = ZoteroDispatch(
    setting['zotero'],
    title_map,
    setting['pdf'],
    setting['general']['personal_only'],
    setting['debug']
)
