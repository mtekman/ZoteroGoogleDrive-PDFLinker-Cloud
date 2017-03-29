#!/usr/bin/env python3

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

    concerns = dupes + no_overlap
    if concerns > 0:
        print('''\nGoogle/Zotero: [PDF intersection]
         - %d duplicates
         - %d non-overlapping files\n''' % (dupes, no_overlap), file=cerr)

    perc = concerns * 100 / len(map)
    if perc > 1:
        print("Warning: %d%% ( > 1%% ) of your Google PDF Files are duplicates\n" % perc,
              "        or do not overlap well with their Zotero counterparts.",
              file = cerr)

    ans = input("Proceed? [Y/n] ")
    ans = ans.strip()

    if ans == "" or ans[0].upper() == "Y":
        return map

    print("Aborting.")
    exit(-1)
