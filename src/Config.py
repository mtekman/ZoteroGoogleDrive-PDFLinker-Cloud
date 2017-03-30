#!/usr/bin/env python3

import configparser
from kludge import *
from sys import stderr as cerr

class Config:

    def __init__(self, filename):
        """Reads in the user set config file and sets the target google and zotero folders and libraries"""

        self.__cp = configparser.ConfigParser(allow_no_value=True)

        self.map = {
            'general'  : {
                'personal_only'       : (self.__cp.getboolean, "General", "Personal Only",
                                         "False", "#  If set true will only process personal libraries\n#  and not create/process group libraries.")
            },
            'google'   : {
                'fold'                : (self.__get, "Google Drive", "Folder Name",
                                         "MyPDFs", "#  Use PDFs from this folder, or if the folder doesn't exist, create it\n#  as a new directory at top-level root."),
                'copy'                : (self.__cp.getboolean, "Google Drive", "Copy",
                                         "True", "#  If PDFs are already on the drive, don't copy or rename if true"),
                'rename'              : (self.__get, "Google Drive", "Rename",
                                         "False",  "#  otherwise:\n#  Rename PDFs when copying to the Drive by item metadata"),
                'rename_schema'       : (self.__get, "Google Drive", "Rename Schema",
                                         "*Y--*J--*A--*T",
                                         "#  If true, schema uses following placeholders:\n"+
                                         "#      *A - Authors, *F - First Author, *L - Last Author\n"+
                                         "#      *Y - Year,    *J - Journal,      *T - Title\n"+
                                         "#  all whitespace is replaced with and underscore '_'\n"+
                                         "# below produces: 1996--ElectricPepper--Mikey_GW__Sharon_GS--On_The_Topic_Of_Disease.pdf")
            },
            'zotero'   : {
                'api_key'             : (self.__get, "Zotero Settings", "API Key",
                                         "N4vY534Lt0pCl455", "#  Can be found at https://www.zotero.org/settings/keys, 'Create new Private Key'"),
                'storage:'            : (self.__get, "Zotero Settings", "Storage",
                                         "Zotero", "#\n# PDFs are either handled internally by Zotero and synced to their servers\n"+
                                         "# or are accessed from an external path on your local machine.\n"+
                                         "#  - Values are either 'Zotero' or the full external path /foo/bar/PDFs/etc/"),
                'user' : {
                    'lib_id'          : (self.__get, "Zotero User + Group", "User Library ID",
                                         "1234567", "#  Library ID found at https://www.zotero.org/settings/keys, 'Your userID for API calls is <libraryID>'"),
                    'collection_name' : (self.__get, "Zotero User + Group", "User Collection Name",
                                         "testthese", "")
                },
                'group': {
                    'lib_id'          : (self.__get, "Zotero User + Group", "Group Library ID",
                                         "2345678",  "#\n#  Group settings are ignored if General:Personal Only is set true, otherwise:\n"+
                                         "#   - Library ID found at https://www.zotero.org/groups/, clicking on your group, '/groups/<groupID>'\n"+
                                         "#   - If the collection name cannot be found it will be created"),
                    'collection_name' : (self.__get, "Zotero User + Group", "Group Collection Name",
                                         "groupcollname", "")
                }
            },
            'pdf'      : {
                'mode'                : (self.__parsePDFMode,  "PDF Settings", "Mode",
                                         "attach_pdf", "#  What to do with each PDF:\n"+
                                         "#  - any conjunction of attaching the PDF as a child item,\n"+
                                         "#    and/or overwriting or clearing the URL field of the item\n"+
                                         "#  - valid modes are: attach_pdf, url_set, url_clear"),
            },
            'debug'                   : (self.__cp.getboolean, "Other", "Debug",
                                         "False",  "#  Read only mode, processes nothing")
            

        }

        if filename == "--make-config":
            self.createConfig()
            print("Config written, please edit and run again.", file=cerr)
            exit(0)

        ## Parse
        self.readConfig()
        print(self.setting)





    def __processConfig(self, keys, brief):
        """ Used by readConfig per setting option"""
        func, section, option, default, text = brief

        map = self.setting
        for key in keys[:-1]:
            map = map.setdefault(key, {})
        
        try:
            map[keys[-1]] = func(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError) as cne:
            print("[Error] Config: %s" % cne, file=cerr)
            exit(-1)      



    def readConfig(self):
        self.setting = {}
        self.__iterateMap( self.__processConfig )


    def createConfig(self):

        def setConfig(keys, brief):
            try:
                func, section, option, default, text = brief
            except ValueError as e:
                print(brief)
                print(e)
                exit(0)

            if not self.__cp.has_section(section):
                self.__cp.add_section(section)

            # Add comments
            if text != "":
                self.__cp.set(section, text)
                
            self.__cp.set(section,option, default)
            
        self.__iterateMap( setConfig )

        with open('config.txt','w') as out:
            self.__cp.write(out)


    def __iterateMap(self, cb):

        def recur(item, access_key, key_array, cb):

            if type(item) != dict:
                cb(key_array + [access_key], item)
                return 0

            for key in item:
                recur(item[key], key, key_array, cb)

            return 0

        recur(self.map, None, [], cb)
    
    
       




    def __get(self, section, name ):
        """Return value from config file"""
        value = self.__cp.get(section, name)
        if value == -1:
            return None

        return value       
        

    def __parsePDFMode(self, heading, name):

        pdf_workmap = {}
        work_modes = self.__get(heading, name).split(',')

        for mode in work_modes:
            mode = mode.strip()
            pdf_workmap[mode] = True              

        if ( 'url_set' in pdf_workmap ) and ('url_clear' in pdf_workmap):
            print("config: Cannot use 'url_set' and 'url_clear' at the same time", file=cerr)
            exit(-1)
        
        if ("attach_pdf" not in pdf_workmap) and ('url_set' not in pdf_workmap ) and ('url_clear' not in pdf_workmap):
            print("config: No PDF mode specified, quitting.")
            exit(0)
        
        return pdf_workmap

Kludge() # do it here for flow
