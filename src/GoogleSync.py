#!/usr/bin/env python3

from pydrive.drive   import GoogleDrive
from pydrive.auth    import GoogleAuth
from os              import path

from GoogleCommonLib import GoogleCommonLib
from LocalStorage    import LocalStorage


class GoogleSync:
    """Copies files from remote to server if missing"""


    def sync(self):
        self.hashes_local   = LocalStorage( self.__local ).map                # hash -> filename
        self.hashes_remote  = self.__generateHashMap()  # hash -> (fname, newname, url)

        if self.__syncFiles() > 0:
            # Regenerate hashes to generate shareable links on all newly uploaded files
            self.hashes_remote = self.__generateHashMap()
         
    

    def __init__(self, localfolder, remotefolder):
        gauth = GoogleAuth()              # Create local webserver and auto handles authentication.
        gauth.LocalWebserverAuth()        # An appropriate settings.yaml must exist
        #gauth.CommandLineAuth()

        self.__log       = LogFile('GoogleSync').log
        self.__local     = localfolder
        self.__remote    = remotefolder
        
        self.__drive     = GoogleDrive(gauth)
        self.__folderID  = GoogleCommonLib.getFolderId( self.__drive, remotefolder, True )

        self.sync()



    def __generateHashMap(self):
        """Generates hashes (and shareable links if not already present) from the remote folder"""
        
        hashfile = open('hashfile','w') # used for logging only
        filelist = GoogleCommonLib.listFilesInFolder(self.__drive, self.__folderID)

        hashmap = {}

        for fil in filelist:
            # pull or generate
            url = GoogleCommonLib.getShareableLink(self.__drive, fil)
            ori = fil['originalFilename']
            md5 = fil['md5Checksum']
            tit = fil['title']

            if md5 not in hashmap:
                hashmap[md5]  = ( ori, tit, url )
            else:
                self.__log("Duplicate hash", md5, tit, hashmap[md5][1])
           
            print(md5, ori, tit, url, sep='\t', file=hashfile)

        hashfile.close()
        self.__log("[Info] GoogleSync:", len(hashmap), "hashes")
        return hashmap

        

    
    def __syncFiles(self):
        """Compares local and remote hashes, and uploads missing files to remote"""

        local_hashes = self.hashes_local
        remot_hashes = self.hashes_remote

        upload_list = []

        for lhash in local_hashes:
            if lhash not in remot_hashes:
                upload_list.append( local_hashes[lhash] )


        num_uploads = len(upload_list)

        if num_uploads > 0:
            for l in range(len(upload_list)):

                localfile      = upload_list[l]
                base_localfile = path.basename(localfile)

                self.__log("[%d/%d] Uploading %s..." % (l+1, num_uploads, base_localfile), end ='\t', flush=True)
                GoogleCommonLib.uploadFile( self.__drive, self.__folderID, localfile )
                self.__log(" ", flush=True)

                
        self.__log("Synced.")
        return num_uploads
   


