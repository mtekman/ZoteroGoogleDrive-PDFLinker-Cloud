#!/usr/bin/env python3

from pyzotero import zotero_errors
 
class ZoteroItemFuncs:
    """Functions that run on each item"""


    @staticmethod
    def getChildAttachmentInfo(zot, item):
        """ """
        res = []  # attachments
        rul = []  # google urls

        try:
            for child in zot.children(item['key']):
                if child['data']['title'] == "Google Drive":
                    rul.append( child['data']['url'] )
                
                if child['data']['itemType'] == 'attachment':

                    if child['data']['linkMode'] == "imported_file":
                        res.append({
                            'md5'   : child['data']['md5'],
                            'fname' : child['data']['filename']
                        })

                    elif child['data']['linkMode'] == "linked_file":
                        res.append({
                            'path'  : child['data']['path']
                        })
                        
        except zotero_errors.UnsupportedParams:
            pass

        return (res, rul)
        

    @staticmethod
    def attachUrlChild(zot, item, map_data, log):
        """Attaches an URL as a child item to the current item. Supports multiple attachments"""

        newlink  = map_data['link']
        children = zot.children(item['key'])
        
        for child in children:
            try:
                if child['data']['title'] == "Google Drive":
                    if child['data']['url'] == newlink:
                        log("Link already exists, doing nothing.",
                              child, newlink, item)
                        return 0

                    else:
                        # Google Drive link exists, but the links don't match...
                        # - 1. it's the same file and google has updated the link (unlikely!)
                        # - 2. or it's another PDF linking to the same item (e.g. supplemental data)
                        #if not self.overwrite_all_links:
                        #    # Removes all
                        #    # 
                        #    return 0
                        #else:
                        #    child['data']['url'] = newlink
                        #    self.__zot.update_item( child['data'] )
                        #    return 1

                        # We assume it's a new PDF that needs linking
                        log("GoogleDrive attachment exists, attaching a new one under the assumption of supplemental data.",
                              child, newlink, item)


            except KeyError:
                pass

        # Handled existing links, now the case for new ones
        #
        new_item = {'itemType': 'attachment', 'linkMode': 'linked_url', 'title'    : "Google Drive", 'accessDate' : '',
                    'note'    : ''          , 'tags'    :           [], 'relations': {}            , 'contentType': '',
                    'charset' : ''          , 'url'     : newlink                                                       }

        # Bind attachment to parentID
        res = zot.create_items([new_item], item['key']  )  
           
        if len(res['successful']) > 0:
            log("Successfully attached", item, map_data['link'])
            return 1

        log("Failed to attach", item, map_data['link'])
        return 0



    @staticmethod
    def directUrlSet(zot, item, map_data, log):
        """Sets a Google Drive link in the URL field of an item"""
        
        if len(item['data']['url'].strip()) < 10:
            log("Updating", item, map_data['link'])

            item['data']['url'] = map_data['link']
            zot.update_item(item['data'])
            return 1

        log("Url not changed, one already exists", item['data']['url'])
        return 0


    
    @staticmethod
    def directUrlClear(zot, item, log):
        """Clears a Google Drive link in the URL field of an item"""

        if  item['data']['url'].startswith("https://drive.google"):
            item['data']['url'] = ""

            zot.update_item( item['data'] )

            log("Cleared Google Drive URL in", item['key'], item['data']['title'])
            return 1

        log("Left URL alone", item['key'], item['data']['title'])
        return 0


    ##### end of url funcs ####

    @staticmethod
    def downloadChildFiles(zot, item, log):
        """Downloads child attachments into local directory"""
        children = zot.children(item['key'])

        if len(children) > 0:
            log("Retrieving child for %s:" % item['data']['title'])
        
        for child in children:
            if child['data']['linkMode'] == 'imported_file':
                filename = child['data']['filename']

                log("  - Saving", filename )
                zot.dump(child['key'], filename, './')
                    
        return (1,1)









    ###### Debug #######

    @staticmethod
    def printItem(self,item):
        print(item)
        return 1


    @staticmethod
    def dummyProcess(self, item):
        return (1,1)
    

