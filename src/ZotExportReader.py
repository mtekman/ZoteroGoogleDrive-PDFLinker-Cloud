#!/usr/bin/env python3

import csv, sys


class ZotExportReader:

    def __init__(self, filename):

        self.titlemap = {}  # basename pdf -> [{Paper, Year, Authors, Pdf}]

        with open(filename,'rt', encoding="utf8") as csvfile:
            exportfile = csv.reader(csvfile, delimiter=',', quotechar='"')

            print("Zotero Export: [reading in CSV file]", file=sys.stderr)

            headers = year = title = attach = author = None
            count = 0
    
            for line in exportfile:

                if count == 0:  # loop peeling's a thing, yeah?
                    headers = line

                    year   = headers.index('Publication Year')
                    title  = headers.index('Title')
                    attach = headers.index('File Attachments')
                    author = headers.index('Author')

                    count += 1
                    continue
              
                yy = int(line[year]) if line[year].strip() != "" else "NONE"
                au = line[author]
                ch = line[attach]
                tt = line[title]
                
                # Multiple attachments are possible
                # - map them to the same item
                attachments = ch.split(';')
                for ach in attachments:
                    # basename for lin and win
                    # + strip characters off end
                    key = ach.split('/')[-1].split('\\')[-1].split('.pdf')[0]+'.pdf'

                
                    if key not in self.titlemap:
                        self.titlemap[key] = []

                    self.titlemap[key].append( {'title':tt, 'year':yy, 'authors':au, 'attachment': ach} )

                count +=1 
                print("        - %d" % count, file=sys.stderr, end='\r')
            print("         - %d pdfs mapped to items" % count, file=sys.stderr)
