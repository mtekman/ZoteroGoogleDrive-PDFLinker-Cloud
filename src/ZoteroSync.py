#!/usr/bin/env python3

from pyzotero   import zotero

from ZoteroLibs      import ZoteroLibs
from ZoteroItemFuncs import ZoteroItemFuncs
from LogFile         import LogFile


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

        self.__attachmentmap = {}

        self.__log(self.__collID)
        self.retrieveAttachments()
        demap = self.__attachmentmap
        import pdb
        pdb.set_trace()



    def __mapAttachInfo(self, item):

        key = item['key']

        if key in self.__attachmentmap:
            self.__log("Duplicate key", key, self.__attachmentmap[key])

        attach_info = ZoteroItemFuncs.getChildAttachmentInfo(self.__zot, item)
        if len(attach_info) > 0:
            self.__attachmentmap[key] = attach_info
            return ( len(attach_info), 1 )

        return ( len(attach_info), 0)



    def retrieveAttachments(self):

        callback = self.__mapAttachInfo;
        
        ZoteroLibs.iterateTopLevelItems(
            self.__zot,
            self.__collID,
            callback,
            "[%d] %d total attachments across %d files" )
