#!/usr/bin/env python3

from sys import argv,stderr

arg_conf="--make-config"

if len(argv)!=2 or (len(argv)==2 and argv[1][0]=='-' and argv[1] != arg_conf):
    name = argv[0].split('/')[-1]
    print('''
    %s <config file>

 or %s %s


''' % (name,name, arg_conf), file=stderr)
    exit(-1)


from Config     import *
from GoogleSync import GoogleSync
from ZoteroSync import ZoteroSync
from helper     import *

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
#                    - upload any missing files under the rename schema, regenerate gdrive hashes, and attempt resync
#
#   - Google Drive is now up to date. We have a list of Google Hashes (md5, local, remote, link)
#   - Up to here

#   - Access Zotero Personal library on server, and link attachments:
#          - Get list of MD5s and titles (if md5s not available) for all attachments
#          - Match md5s+titles with GoogleDrive links, and link shareable URL to the parent item
#
#   - Library now has updated links to Gdrive, it is up to the user to clone and share it.

setting = Config(argv[1]).setting

gsyncer = GoogleSync(
    setting['pdf', 'storage'],
    setting['google', 'fold']
)

zsyncer = ZoteroSync(
    setting['zotero', 'api_key'],
    setting['zotero', 'user', 'lib_id' ],
    setting['zotero', 'user', 'collection_name' ],
    setting['pdf', 'mode' ]
)

#glocal = gsyncer.hashes_local
gremot = gsyncer.hashes_remote # md5 -> (original_filename, new_filename, google url)

zremot_md = zsyncer.hashMD5s   # md5 -> key
zremot_fn = zsyncer.hashFnames # title -> key


intersect_maps( gremot, zremot_md, zremot_fn,
                zsyncer.linkByMD5, zsyncer.linkByTitle
)
