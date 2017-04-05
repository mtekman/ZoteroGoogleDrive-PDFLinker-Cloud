#!/usr/bin/env python3

from pyzotero import zotero.zotero
from LogFile import LogFile



def zoteroDebug(apikey,libid, collid):
    zot = zotero.Zotero( libid, "user", apikey )
    items = zot.collection_items(collid)
    import pdb
    pdb.set_trace()





class ZoteroEdit:

    def __init__(self, libraryType, zconfig, titlemap, pdf_settings, debug = False):     
        self.retrieveFilesFromServer();

    def logthis(self, *args):
        print(*args,file=cerr)
        print(*args,file=self.__log)

      
        
    def retrieveFilesFromServer(self):
   
        self.__iterateItemsInCollection(
            self.ItemRetrieveChildFiles, "Done: %d"
        )
        exit(0)
            
    
   def processItems(self, collectionID, work_mode ):
        """Attaches or sets URL"""

        format_string = "Processed %d items"

        if work_mode["attach_pdf"]:
            self.attach_pdf = True
            format_string += ", attached %d URL items "

        if work_mode["url_set"]:
            self.url_set = True
            format_string += ", set %d URL fields"

        if work_mode["url_clear"]:
            self.url_clear = True
            format_string += ", cleared %d URL fields"

        format_string += "           "


        if self.url_set and self.url_clear:
            print("Cannot use 'url_set' and 'url_clear' at the same time.",
                  "Please change in your config.", file=cerr)
            exit(-1)

        if self.url_set or self.url_clear:
            self.url_is_used = True

        self.__iterateItemsInCollection(
            self.__dummyProcess if self.__debug else self.__itemProcess,
            format_string
        )
      
  

       
    def __itemProcess(self, item):
        """Performs an action upon an item, one or many of:
              __itemDirectUrlClear
              __itemDirectUrlSet
              __itemAttachUrlChild
        """
        data = item['data']

        url_action = 0
        attached   = 0

        try:
            title   = data['title'].lower()
            #authors = data['creators'].lower()
            
            if title in self.titlemap:
                map_data = self.titlemap[title]

                if self.url_set:
                    url_action += ZoteroItemFunc.directUrlSet(   self.__zot, item, map_data, self.__log)  # These two are
                elif self.url_clear:                                                                      # mutually-
                    url_action += ZoteroItemFunc.directUrlClear( self.__zot, item, map_data, self.__log ) # exclusive

                if self.attach_pdf:
                    attached   += ZoteroItemFunc.attachUrlChild( self.__zot, item, map_data, self.__log )

            else:
                print("Could not map title", title, file=self.__log)

        except KeyError as e:
            print( "No title in ", data, file=self.__log)

        return (url_action, attached)


    




        
### Example of attachment using zotero storage:
# {'key': 'PSZA7XPI', 'version': 14, 'library': {'type': 'user', 'id': 3808237, 'name': 'mtekman', 'links': {'alternate': {'href': 'https://www.zotero.org/mtekman', 'type': 'text/html'}}}, 'links': {'self': {'href': 'https://api.zotero.org/users/3808237/items/PSZA7XPI', 'type': 'application/json'}, 'alternate': {'href': 'https://www.zotero.org/mtekman/items/PSZA7XPI', 'type': 'text/html'}, 'up': {'href': 'https://api.zotero.org/users/3808237/items/JQZPDSGU', 'type': 'application/json'}, 'enclosure': {'type': 'application/pdf', 'href': 'https://api.zotero.org/users/3808237/items/PSZA7XPI/file/view', 'title': 'allegro.pdf', 'length': 90942}}, 'meta': {}, 'data': {'key': 'PSZA7XPI', 'version': 14, 'parentItem': 'JQZPDSGU', 'itemType': 'attachment', 'linkMode': 'imported_file', 'title': 'Gudbjartsson et al_2005_Allegro version 2.pdf', 'accessDate': '', 'url': '', 'note': '', 'contentType': 'application/pdf', 'charset': '', 'filename': 'Gudbjartsson et al_2005_Allegro version 2.pdf', 'md5': '11e622b16099f9a64a562e9e2a3d94af', 'mtime': 1470313393000, 'tags': [], 'relations': {}, 'dateAdded': '2016-08-04T12:23:13Z', 'dateModified': '2017-03-17T13:34:14Z'}}

### Example of same attachment using external storage:
# {'key': 'LARDKYJA', 'version': 2793, 'parentItem': '2FWFTHJN', 'itemType': 'attachment', 'linkMode': 'linked_file', 'title': '2011_Cliodynamics_Baker_demographic-str-theory-Rome.pdf', 'accessDate': '', 'url': '', 'note': '', 'contentType': 'application/pdf', 'charset': '', 'path': 'W:\\hstanesc\\info\\articles\\2011_Cliodynamics_Baker_demographic-str-theory-Rome.pdf', 'tags': [], 'relations': {}, 'dateAdded': '2017-03-03T10:01:13Z', 'dateModified': '2017-03-03T10:01:13Z'}

# Problem is that external storage does NOT have md5s to work with, and must use title
