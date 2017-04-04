#!/usr/bin/env python3

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

from GoogleCommonLib import GoogleCommonLib
from LocalStorage    import LocalStorage
from os              import path

from sys import stderr as cerr

class GoogleRemote:
    """Copies files from remote to server if missing"""

    @staticmethod
    def initAuth():
        gauth = GoogleAuth()              # Create local webserver and auto handles authentication.
        gauth.LocalWebserverAuth()        # An appropriate settings.yaml must exist
        #gauth.CommandLineAuth()
        return GoogleDrive(gauth)   # Create GoogleDrive instance with authenticated GoogleAuth instance


    @staticmethod
    def generateHashMap(drive, folderID, withShareable=True):
        
        hashfile = open('hashfile','w') # used for logging only
        filelist = GoogleCommonLib.listFilesInFolder(drive, folderID)

        hashmap = {}

        for fil in filelist:
            # pull or generate
            url = GoogleCommonLib.getShareableLink(drive, fil)
            ori = fil['originalFilename']
            md5 = fil['md5Checksum']
            tit = fil['title']

            if md5 not in hashmap:
                hashmap[md5]  = ( ori, tit, url )
            else:
                print("Duplicate hash", md5, tit, hashmap[md5][1], file=cerr)
           
            print(md5, ori, tit, url, sep='\t', file=hashfile)

        hashfile.close()
        print("[Info] GoogleRemote:", len(hashmap), "hashes.", file=cerr)
        return hashmap
  
  

    def __init__(self, localfolder, remotefolder):
    
        drive     = GoogleRemote.initAuth()
        folderID  = GoogleCommonLib.getFolderId( drive, remotefolder, True )

        local_hashes  = LocalStorage( localfolder ).map                     # hash -> filename
        remot_hashes  = GoogleRemote.generateHashMap( drive, folderID )  # hash -> (fname, newname, url)

        num_uploaded = GoogleRemote.syncFiles( drive, folderID, local_hashes, remot_hashes )

        if num_uploaded > 0:
            # Regenerate hashes to generate shareable links on all newly uploaded files
            remot_hashes = GoogleRemote.generateHashMap( drive, folderID )
            



    @staticmethod
    def syncFiles( drive, folderID, local_hashes, remot_hashes):

        num_uploaded = 0

        for lhash in local_hashes:
            if lhash not in remot_hashes:

                localfile      = local_hashes[lhash]
                base_localfile = path.basename(localfile)

                print("Uploading %s..." % base_localfile, end ='\t', file=cerr)
                GoogleCommonLib.uploadFile( drive, folderID, localfile )
                num_uploaded += 1
                print(" ", file=cerr)

        print("Synced.", file=cerr)
        return num_uploaded
   




    def __reload(self, inp):
    
        with open(inp,'r') as popped:
            count = 0;
            print("Google : [reading in previously collated data]", file=cerr)

            for line in popped:
                pdfname, newlink = line.splitlines()[0].split('\t')
                count += 1
                #print("%5d -- %s   " % (count, pdfname), file=cerr, end='\r')

                if pdfname in self.map:
                    print("         - duplicate pdf ", pdfname, file=cerr)

                self.map[pdfname] = newlink

                popped.close()
                print("         - %d pdfs mapped to links " % count, file=cerr)


      
    def ____writeListToFile(self, outfile, file_list, count = 0):
        # Permissions for anyone to view (not edit)
        perm = { 'type': 'anyone', 'value' : 'anyone', 'role' : 'reader', 'withLink': True}

        with open(outfile,'a') as out: # append

            for f in file_list:
                f.InsertPermission( perm );

                pdfname = f['title'].strip()
                newlink = f['alternateLink'].strip()
        
                count += 1
                print("%4d --  %s   " % (count, pdfname), file=cerr, end='\r')

                if pdfname in self.map:
                    print("Duplicate!", pdfname, file=cerr)

                print("%s\t%s" % (pdfname, newlink), file=out)
                self.map[pdfname] = newlink

            out.close()
            print("\n%d links saved to file [%s]" % (count, outfile), file=cerr)

        return count
    
          

    def __generateLinks(self, output, foldername, start_from = 0):
        gauth = GoogleAuth()                # Create local webserver and auto handles authentication.
        gauth.LocalWebserverAuth()          # An appropriate settings.yaml must exist
        #gauth.CommandLineAuth()

        drive = GoogleDrive(gauth)   # Create GoogleDrive instance with authenticated GoogleAuth instance

        folderID  = GoogleShareable.__getFolderId(drive, foldername)
        file_list = GoogleShareable.__listFiles(folderID, drive)

        print("Total PDFs to process: %d" % len(file_list), file=cerr)

        # Long list, process in chunks of 200 items or so
        start_it = start_from
        step = 200
        end_it = start_it + step

        while True:
            if end_it > len(file_list):
                end_it = len(file_list)
                break

            temp_list = file_list[start_it:end_it]
            
            self.____writeListToFile(output, temp_list, start_it)
            
            start_it += step
            end_it += step        



#GoogleRemote( '/home/tetris/Documents/', "lastTest" )
    
