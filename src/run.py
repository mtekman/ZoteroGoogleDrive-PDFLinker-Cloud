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

# Flow:
#   - Sync local storage with GoogleDrive
#         - Check local storage (Zstorage, or elsewhere) and hash out MD5s (this is quick, always make new hashes)
#         - if GDrive folder does not exist:
#                 prompt user for creation and copy/rename all from storage to drive.
#                 generate GoogleDrive hashes and shareable links and store in the server
#                      Hash file contains -> md5, local_title, remote title, link
#         - else perform sync to server:             
#                 - Get list of gdrive files, check against google hash file (remote title)
#                   and generate new hash file if there is a difference.
#                 - Read in local storage hash and check if there anything missing
#                   (ignore new files on cloud, we have no local path to download them to)
#                 - while there are missing files:
#                      - upload any missing files under the rename schema, regenerate gdrive hashes, and attempt resync
#
#   - Google Drive is now up to date. We have a list of Google Hashes (md5, local, remote, link)
#
#   - Access Zotero Personal library on server, and link attachments:
#          - Get list of MD5s for all attachments
#          - Match Md5s with GoogleDrive links, and link shareable URL to the parent item
#
#   - Library now has updated links to Gdrive, it is up to the user to clone and share it.



localstorage_hashmap = HashFiles( setting['pdf','storage'] ).map

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
