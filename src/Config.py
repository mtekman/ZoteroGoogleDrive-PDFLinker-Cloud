#!/usr/bin/env python3

import configparser
from kludge import *
from sys import stderr as cerr

class Config:

    def __init__(self, filename):
        """Reads in the user set config file and sets the target google and zotero folders and libraries"""

        ## Parse
        self.__cp = configparser.ConfigParser()
        self.__cp.read(filename)

        try:
            self.setting = {
                'general'  : {
                    'personal_only'       : self.__cp.getboolean("General", "Personal Only")
                },
                'google'   : {
                    'copy'                : self.__cp.getboolean("Google Drive", "Copy"),
                    'fold'                : self.__get("Google Drive", "Folder Name"),
                    'rename'              : self.__get("Google Drive", "Rename"),
                    'rename_schema'       : self.__get("Google Drive", "Rename Schema")
                },
                'zotero'   : {
                    'api_key'             : self.__get("Zotero Settings", "API Key"),
                    'user' : {
                        'lib_id'          : self.__get("Zotero User + Group", "User Library ID"),
                        'collection_name' : self.__get("Zotero User + Group", "User Collection Name")
                    },
                    'group': {
                        'lib_id'          : self.__get("Zotero User + Group", "Group Library ID"),
                        'collection_name' : self.__get("Zotero User + Group", "Group Collection Name")
                    }
                },
                'debug'                  : self.__cp.getboolean("Other", "Debug"),
                'pdf'      : {
                    'mode'               : self.__parsePDFMode("PDF Settings", "Mode"),
                }
            }
                           
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError) as cne:
            print("[Error] Config: %s" % cne, file=cerr)
            exit(-1)




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
