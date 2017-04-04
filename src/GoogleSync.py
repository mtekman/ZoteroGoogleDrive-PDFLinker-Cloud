#!/usr/bin/env python3

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

from GoogleCommonLib import GoogleCommonLib

from sys import stderr as cerr

class GoogleRemote:
    """Copies files from remote to server if missing"""

    def initAuth(self):
        gauth = GoogleAuth()              # Create local webserver and auto handles authentication.
        gauth.LocalWebserverAuth()        # An appropriate settings.yaml must exist
        #gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)   # Create GoogleDrive instance with authenticated GoogleAuth instance
        self.hashmap = {}
        self.titlemap = {}

    def generateHashMap(self, folderID, withShareable=True):
        hashfile = open('hashfile','w') # used for logging only
        filelist = GoogleCommonLib.listFilesInFolder(self.drive, folderID)

        for fil in filelist:

            url = GoogleCommonLib.getShareableLink(self.drive, fil)  # pull or generate
            ori = fil['originalFilename']
            md5 = fil['md5Checksum']
            tit = fil['title']

            if md5 not in self.hashmap:
                self.hashmap[md5]  = ( ori, tit, url )
                self.titlemap[tit] = md5
            
            print(md5, ori, tit, url, sep='\t', fil=hashfile)
        hashfile.close()
    
  
    def __init__(self, localfolder, remotefolder):
        self.local  = localfolder
        self.remote = remotefolder

        self.initAuth()

        folderID  = GoogleCommonLib.getFolderId(self.drive, remotefolder, True)
        #file = GoogleCommonLib.uploadFile(self.drive, folderID, '/nomansland/MAIN_REPOS/zoterogoogledrive_pdflinker/README.md', "README.md")
        #files = GoogleCommonLib.listFilesInFolder(self.drive, folderID)
        self.generateHashFile( folderID )
        exit(-1)
    

    @staticmethod
    def fileExists(filename):

        try:
            pop = open(filename,'r')
            data = pop.readline()
            pop.close()

            if len(data.strip()) == 0:
                return False  # Blank file
      
            return True   # does exist with data
        except IOError:
            return False    # does not exist



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


GoogleRemote("blah","test")
    
