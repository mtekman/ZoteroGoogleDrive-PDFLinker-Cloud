#!/usr/bin/env python3

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

from sys import stderr as cerr

class GoogleShareable :
  """For an EXISTING gdrive folder, generate shareable links and write to cache"""
  
  def __init__(self, foldername, output_file, start_from=0):

    self.map = {} # filename -> shareable link

    # Do not overwrite previous search
    if GoogleShareable.fileExists(output_file):
      self.__reload(output_file)                      # Load map from file
    else:
      self.__generateLinks(output_file, foldername, start_from)   # Generate new map and file
    print("",file=cerr)


  @staticmethod
  def fileExists(filename):

    try:
      pop = open(filename,'r')
      data = pop.readline()
      pop.close()

      if len(data.strip()) == 0:
        return False  # Blank file
      
      return True   # does exist with data
    except IOError:
      return False    # does not exist


  @staticmethod
  def __getFolderId(drive, foldername):
    file_list = drive.ListFile(
      {'q': "'%s' in parents and trashed=false" % 'root'}).GetList()

    for f in file_list:
      if f['mimeType']=='application/vnd.google-apps.folder': # if folder
        if foldername == f['title']:
          print("%s --> %s" % (foldername, f['id']), file=cerr)
          return f['id']


    print("Cannot find folder %s\nAvailable folders:\n%s\nPlease change your config file to one of these.\n" % (
      foldername,
      '\n'.join(["   "+x['title'] for x in file_list])
    ), file=cerr)
    exit(-1)


  @staticmethod
  def __listFiles(parent, drive):  # depth = 1
    filelist=[]
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
    for f in file_list:
      if f['mimeType']!='application/vnd.google-apps.folder': # if not folder
        filelist.append(f)

    if len(filelist) == 0:
      print(parent, "has no files within", file=cerr)
      exit(-1)

    return filelist



  def __reload(self, inp):
    
    with open(inp,'r') as popped:
      count = 0;
      print("Google : [reading in previously collated data]", file=cerr)

      for line in popped:
        pdfname, newlink = line.splitlines()[0].split('\t')
        count += 1
        #print("%5d -- %s   " % (count, pdfname), file=cerr, end='\r')

        if pdfname in self.map:
          print("         - duplicate pdf ", pdfname, file=cerr)

        self.map[pdfname] = newlink

      popped.close()
      print("         - %d pdfs mapped to links " % count, file=cerr)


      
  def ____writeListToFile(self, outfile, file_list, count = 0):
    # Permissions for anyone to view (not edit)
    perm = { 'type': 'anyone', 'value' : 'anyone', 'role' : 'reader', 'withLink': True}

    with open(outfile,'a') as out: # append

      for f in file_list:
        f.InsertPermission( perm );

        pdfname = f['title'].strip()
        newlink = f['alternateLink'].strip()
        
        count += 1
        print("%4d --  %s   " % (count, pdfname), file=cerr, end='\r')

        if pdfname in self.map:
          print("Duplicate!", pdfname, file=cerr)

        print("%s\t%s" % (pdfname, newlink), file=out)
        self.map[pdfname] = newlink

      out.close()
      print("\n%d links saved to file [%s]" % (count, outfile), file=cerr)

      return count
    
          

  def __generateLinks(self, output, foldername, start_from = 0):
    gauth = GoogleAuth()                # Create local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()          # An appropriate settings.yaml must exist
    #gauth.CommandLineAuth()

    drive = GoogleDrive(gauth)   # Create GoogleDrive instance with authenticated GoogleAuth instance

    folderID  = GoogleShareable.__getFolderId(drive, foldername)
    file_list = GoogleShareable.__listFiles(folderID, drive)

    print("Total PDFs to process: %d" % len(file_list), file=cerr)

    # Long list, process in chunks of 200 items or so
    start_it = start_from
    step = 200
    end_it = start_it + step

    while True:
      if end_it > len(file_list):
          end_it = len(file_list)
          break

      temp_list = file_list[start_it:end_it]

      self.____writeListToFile(output, temp_list, start_it)

      start_it += step
      end_it += step        
        

      
    
    
