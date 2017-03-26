#!/usr/bin/env python3

from sys import stderr as cerr

def readInSettings(filename):
    """Reads in the user set config file and sets the target google and zotero folders and libraries"""

    gfold = zlibid = zname = zotkey = debug = modeset = None
    work_mode = {
        'url_set'   : False,
        'url_clear' : False,
        'attach_pdf': False
    }

    with open(filename,'r') as config:

        print("", file=cerr)
                  
        for line in config:
            if line[0] == '#' or len(line)<5:continue

            if line.startswith("Google Drive Folder Name"):
                gfold  = line.split('=')[-1].strip()
            elif line.startswith("Zotero Group Library ID"):
                zlibid = int( line.split('=')[-1].strip() )
            elif line.startswith("Zotero Group Collection Name"):
                zname  = line.split('=')[-1].strip()
            elif line.startswith("Zotero API Key"):
                zotkey = line.split('=')[-1].strip()
            elif line.startswith("Work Mode"):
                tokens = line.split('=')[-1].strip().split(',')

                for tok in tokens:
                    tok = tok.strip()

                    if tok not in work_mode:
                        print("Invalid work mode '%s'" % tok, file=cerr)
                        exit(-1)

                    work_mode[tok] = True
                    modeset = True

            # Optional
            elif line.startswith("Debug"):
                debug = bool(line.split("=")[-1].strip())
                
            else:
                print("Could not parse:", line, file=cerr)
                exit(-1)
        config.close()
   
    errors=""
    if gfold  == None:errors += "Error: Google Drive Folder Name - not specified\n"
    if zname  == None:errors += "Error: Zotero Group Library ID - not specified\n"
    if zlibid == None:errors += "Error: Zotero Group Collection Name - not specified\n"
    if zotkey == None:errors += "Error: Zotero API Key - not specified\n"
    if modeset== None:errors += "Error: No work mode set\n"
    if errors != "":
        print(errors, file=cerr)
        exit(-1)

    return (gfold, zlibid, zname, work_mode, zotkey, debug)



def intersect_maps( gmap, zmap ):
    """Intersects the Google and Zotero map data using their Title values"""

    pdf_errors = open('pdf_errors.txt','w')

    map = {}

    dupes = 0
    no_overlap = 0

    # Intersect maps
    for pdf in gmap:
        if pdf in zmap:

            glink = gmap[pdf]
            items = zmap[pdf]

            # Create a unique entry for each title that shares the same pdf
            for it in items:
                title = it['title'].lower()

                if title in map:
                    dupes += 1
                    if map[title] == glink:
                        print("Duplicate title [same link]",
                              title, glink, map[title], file=pdf_errors)
                    else:
                        print("Duplicate title [differing link]",
                              title, glink, map[title], file=pdf_errors)
            
                map[title] = { 'link':glink,
                               'title':it['title'],
                               'year':it['year']    }
        else:
            print("Exists in Google Drive only: ",
                  pdf, file=pdf_errors)
            no_overlap += 1
            
    pdf_errors.close()

    if (dupes + no_overlap) > 0:
        print('''\nGoogle/Zotero: [PDF intersection]
         - %d duplicates
         - %d non-overlapping files\n''' % (dupes, no_overlap), file=cerr)
    
    return map
