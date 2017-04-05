from sys import stderr as cerr
from os import path

class GoogleCommonLib:
    """Common methods for handling Google Drive requests"""

    @staticmethod
    def getShareableLink(drive, gfile):
        """Pulls existing, or generates a new one"""
        url = GoogleCommonLib.getExistingShareableLink( drive, gfile )
        if url == None:
            print("[GoogleCommonLib] Making shareable url for: %s" % gfile['title'].split('/')[-1], file=cerr)
            url = GoogleCommonLib.generateShareableLink( drive, gfile )

        return url


    @staticmethod
    def getExistingShareableLink(drive, file):
        if file['shared']:
            url = file['alternateLink'].strip()
            if len(url) > 10:
                return url
        return None

    
    @staticmethod    
    def generateShareableLink(drive, file):
        perm = { 'type': 'anyone',
                 'value' : 'anyone',
                 'role' : 'reader',
                 'withLink': True }

        file.InsertPermission( perm );
        return file['alternateLink']


    @staticmethod
    def listFilesInFolder(drive, folderID):
        filelist=[]
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folderID}).GetList()
        for f in file_list:
            if f['mimeType']!='application/vnd.google-apps.folder': # if not folder
                filelist.append(f)

        if len(filelist) == 0:
            print("[Warning] GoogleCommonLib folder[%s] has no files within" % folderID, file=cerr)


        return filelist


    @staticmethod
    def uploadFile(drive, parentID, filename, title = None):
        """UploadsFile, returns ID"""
        if title == None:
            title = path.basename( filename )

        f = drive.CreateFile({"title" : title,
                              "parents": [{"kind": "drive#fileLink", "id": parentID}]})
        f.SetContentFile( filename )
        f.Upload()
        return f
        

    @staticmethod
    def createFolder(drive, foldername):
        """Returns new folder ID on completion"""
        newfold = drive.CreateFile({'title': foldername, 
                                    "mimeType": "application/vnd.google-apps.folder"})
        newfold.Upload()
        return newfold['id']
    

    @staticmethod
    def getFolderId(drive,foldername, create=False):
        folder_potentials = []       
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % 'root'}).GetList()

        for f in file_list:
            if f['mimeType']=='application/vnd.google-apps.folder': # if folder
                folder_potentials.append( f )
                if foldername == f['title']:
                    print("[Info] Folder %s[%s]" % (foldername, f['id']), file=cerr)
                    return f['id']


        # No matches, offer selection
        valid_f_names = ["   "+x['title'] for x in folder_potentials]
                
        print("Cannot find folder %s\nAvailable folders:\n%s" % (
            foldername, ' - ' + ('\n - '.join(valid_f_names) ) + '\n'
        ), file=cerr)

        if create:
            ans = input("Would you like to create '%s' regardless, and sync your local files to it? [y/N] "
                        % foldername)
            
            if ans[0].lower() == 'y':
                print("Creating new remote directory '%s' at root..." % foldername, file=cerr)
                return GoogleCommonLib.createFolder(drive, foldername)

            print("Aborting.", file = cerr)


        # Not create, exit on failure
        exit(-1)

