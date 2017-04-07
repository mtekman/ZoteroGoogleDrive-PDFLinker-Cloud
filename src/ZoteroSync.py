#!/usr/bin/env python3

from pyzotero import zotero
from pickle   import load,dump
from os       import path
from appdirs  import user_cache_dir
from sys      import stderr as cerr

from ZoteroLibs      import ZoteroLibs
from ZoteroItemFuncs import ZoteroItemFuncs
from LogFile         import LogFile
from LocalLibs       import LocalLibs


# This should attach URLs for existing attachments
# It will not attempt to match based on title alone --- or could it?


class ZoteroSync:

    
    def __init__(self, apikey, userlibrary_id, usercollection_name):
        
        self.__log    = LogFile('ZoteroSync').log

        self.__zot    = zotero.Zotero( userlibrary_id, "user", apikey )
        self.__collID = ZoteroLibs.findCollectionID( self.__zot, usercollection_name )

        self.collateMaps()



    def __mapAttachInfo(self, item):

        key = item['key']

        if key in self.__attachmentmap:
            self.__log("Duplicate key", key, self.__attachmentmap[key])

        attach_info, gurl_info = ZoteroItemFuncs.getChildAttachmentInfo(self.__zot, item)
        # do nothing with url info for now
                
        if len(attach_info) > 0:
            self.__attachmentmap[key] = attach_info
            return ( len(attach_info), 1 )

        return ( len(attach_info), 0)



    def collateMaps(self):

        self.keyattachments_file = path.join( user_cache_dir('GoogleZoteroPDFLinker'), "keyattachments.map" )

        if path.exists( self.keyattachments_file ) and path.getsize( self.keyattachments_file ) > 5:

            num_items  = -1
            num_attach = -1
            corrupted  = False
            try:
                with open( self.keyattachments_file, 'rb') as inp:
                    tmp_map   = load(inp)
                    num_items = len(tmp_map)
                    num_attach = 0
                    for x in tmp_map:
                        num_attach += len(tmp_map[x])

                    self.__log("A previous run found %d attachments with %d items." % (num_attach, num_items), flush=True)
            except:
                corrupted = True
                self.__log("Attachment cache exists but is unreadable, regenerating...", flush=True)
                pass
                    
            

            while not corrupted:
                ans = input("Use this data, or refresh attachments on server? [U/r] ").lower()[0]

                if ans == 'u':
                    self.loadMapsFromFile()
                    return 0

                if ans == 'r':
                    break

                print("Please type U or r", file=cerr)
                continue

        # Otherwise pull from server and make the maps
        self.createMaps()
        return 0

    

    def loadMapsFromFile(self):

        with open(self.keyattachments_file, 'rb') as inp:
            self.__attachmentmap = load(inp)

        self.__makeMaps()
        


    def createMaps(self):

        self.retrieveAttachments()

        # write to file
        with open(self.keyattachments_file,'wb') as out:
            dump( self.__attachmentmap, out )

        self.__makeMaps()

    
    def retrieveAttachments(self):
        self.__attachmentmap = {}
        self.__existingGURLs = {}
                
        self.__log("[Info] ZoteroSync: Retrieving attachment data")

        callback = self.__mapAttachInfo;
        
        ZoteroLibs.iterateTopLevelItems(
            self.__zot,
            self.__collID,
            callback,
            "[Processed %d items] %d total attachments across %d items" )


        

    def __makeMaps(self):
        
        self.hashMD5s   = {}  # md5    -> key
        self.hashFnames = {}  # title -> key

        #des = self.__attachmentmap
        #import pdb
        #pdb.set_trace()

        for key in self.__attachmentmap:
            item_data_collective = self.__attachmentmap[key]

            for item_data in item_data_collective:

                fname=""
                md5=""
                if 'path' in item_data:
                    fname = path.basename( item_data['path'] ).strip()
                elif 'fname' in item_data:
                    fname = item_data['fname'].strip()
                    md5   = item_data['md5'].strip()
                else:
                    print("UKNOWN", item_data)
                    continue

                if fname != "":
                    if fname in self.hashFnames and key != self.hashFnames[fname]:
                        self.__log("Duplicate filename", fname, key, self.hashFnames[fname])

                    self.hashFnames[fname] = key

                if md5 != "":
                    if md5 in self.hashMD5s and key != self.hashMD5s[md5]:
                        self.__log("Duplicate MD5", md5, key, self.hashMD5s[md5])

                    self.hashMD5s[md5] = key
