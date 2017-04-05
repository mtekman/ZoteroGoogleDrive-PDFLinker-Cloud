#!/usr/bin/env python3

from pyzotero   import zotero
from ZoteroLibs import ZoteroLibs
from LogFile    import LogFile


class ZoteroSync:

    def __init__(self, apikey, userlibrary_id, usercollection_name):
        
        self.__log    = LogFile('ZoteroSync').log

        self.__zot    = zotero.Zotero(
            userlibrary_id, "user",
            apikey
        )

        self.__collID = ZoteroLibs.findCollectionID(
            self.__zot,
            usercollection_name
        )

        self.__log(self.__collID)



    def retrieveAttachments(self):

        callback = 
        
        ZoteroLibs.iterateTopLevelItems(
            self.__zot,
            self.__collID,
            callback,
            "%d %d %d"
        )
