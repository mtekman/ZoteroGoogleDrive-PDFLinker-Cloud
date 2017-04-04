from sys import stderr as cerr

class GoogleCommonLib:
    """Common methods for handling Google Drive requests"""

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
                    print("%s --> %s" % (foldername, f['id']), file=cerr)
                    return f['id']


        # No matches, offer selection
        valid_f_names = ["   "+x['title'] for x in folder_potentials]
                
        print("Cannot find folder %s\nAvailable folders:\n%s" % (
            foldername, '\n - '.join(valid_f_names)
        ), file=cerr)

        if create:
            ans = input("Would you like to create '%s' regardless, and sync your local files to it? [y/N] " % foldername)
            if ans[0].lower() == 'y':
                print("Creating new remote directory '%s' at root..." % foldername, file=cerr)
                return GoogleCommonLib.createFolder(drive, foldername)


        # Not create, exit on failure
        exit(-1)

