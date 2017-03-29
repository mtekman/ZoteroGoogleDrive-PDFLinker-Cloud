#!/usr/bin/env python3

import configparser
from kludge import *
from sys import stderr as cerr

class Config:

    def __init__(self, filename):
        """Reads in the user set config file and sets the target google and zotero folders and libraries"""

        self.__cp = configparser.ConfigParser()
        self.map = {
            'general'  : {
                'personal_only'       : (self.__cp.getboolean, "General", "Personal Only",
                                         "False", "# Does not update/create Group libraries if set true.")
            },
            'google'   : {
                'fold'                : (self.__get, "Google Drive", "Folder Name",
                                         "MyPDFs", "# PDF folder - must be uniquely named"),
                'rename'              : (self.__get, "Google Drive", "Rename",
                                         "False",  "# Rename PDFs using schema"),
                'rename_schema'       : (self.__get, "Google Drive", "Rename Schema",
                                         "*Y--*J--*A--*T", "# Schema blahblaahblah")
            },
            'zotero'   : {
                'api_key'             : (self.__get, "Zotero Settings", "API Key",
                                         "N4vY534Lt0pCl455", "# You can get this from blahblah"),
                'user' : {
                    'lib_id'          : (self.__get, "Zotero User + Group", "User Library ID",
                                         "12345", "#Yes I guess"),
                    'collection_name' : (self.__get, "Zotero User + Group", "User Collection Name",
                                         "testthese", "")
                },
                'group': {
                    'lib_id'          : (self.__get, "Zotero User + Group", "Group Library ID",
                                         "54321",  ""),
                    'collection_name' : (self.__get, "Zotero User + Group", "Group Collection Name",
                                         "hhssas", "")
                }
            },
            'debug'                   : (self.__cp.getboolean, "Other", "Debug",
                                         "False",  ""),
            'pdf'      : {
                'mode'                : (self.__parsePDFMode,  "PDF Settings", "Mode",
                                         "attach_pdf", "# Valid modes are"),
            }
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
        config = configparser.RawConfigParser()

        def setConfig(keys, brief):
            try:
                func, section, option, default, text = brief
            except ValueError as e:
                print(brief)
                print(e)
                exit(0)

            if not config.has_section(section):
                config.add_section(section)

            config.set(section,option, default)
            
        self.__iterateMap( setConfig )

        with open('config.txt','w') as out:
            config.write(out)


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
