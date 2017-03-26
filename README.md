# **Zotero/GoogleDrive PDF-Linker** #

Zotero has limited cloud storage for PDFs (300MB) which may leave some paper-hoarders keen on sharing their  collection with others, left with few options.

However, GoogleDrive offers (15GB+) which is more than ample for storing PDFs.

So how do you link one with the other?

#### ***"The Simple Way"***
For each PDF in your GoogleDrive, obtain a shareable link and then manually set it to the correct item in your Zotero database. 

***That sounds tedious. Surely there's an easier way?***

Lucky for us, we have this nifty little utility to automate the whole linking process (via "The Simple Way")

## Pre-Requisites 

 1. **Structure your data**
 Your stored PDFs must exist in a single directory without subdirectories, and the items that you wish to share must exist within a single collection. 

 2. **Export your collection as a CSV file**
 Right-click on the local collection you wish to share (under "My Library"), and click 'Export Collection...' selecting CSV (notes are not required). 
This will produce a file that should  contain the filenames of your original attachments as they exist on your system.

 3. **Create a Group library**  
 You will need a Zotero account and it will need to be linked to your Zotero standalone. Within your Zotero standalone application, *copy the contents of a local collection into the group library* by dragging and dropping. It is advisable to test a few items first to see if the attachments are carried over. If they are, delete the entries in the Group library and repeat the drag'n'drop process but holding `SHIFT` at the same time.

 3. **Obtain your Group Library ID and your API key**  

      1. Your Group Library ID can be found by opening the group’s page: https://www.zotero.org/groups/groupname, and hovering over the group settings link. The ID is the integer after /groups/.

      2. Your API key can generated from here: https://www.zotero.org/settings/keys/new
	     Allow library and write access for personal, and Read/Write access for group.
 
 
 4. **Copy (or Move) your PDFs from your current storage location to a folder in your Google Drive** if you have not done so already. Ensure that the folder meets the following requirements:

       1. Unique folder name. If your folder is called "PDFs", ensure that there is no other folder called "PDFs" in your entire Google Drive.

       2. The folder contains your PDFs *only*. Nothing else. No subfolders, or this gets tricky.

 5. ***Record the `GoogleDrive Folder Name`, the `Zotero Group Library ID`, and the `Zotero Group Collection Name` into a config file*** as shown below (supplanting the example data with your own). Do not specify your google account name, this is prompted later.

        # Google Drive Settings
        Google Drive Folder Name = MyPDFs
        
        # Zotero Group Library Settings
        Zotero Group Library ID = 1234567
        Zotero Group Collection Name = sharetheseones
        Zotero API Key = aBcDEFgHIjkLMNoPQrStuvwX

        # What to do with each item
        #  - valid modes are: attach_pdf, url_set, url_clear
        Work Mode = attach_pdf
        Debug = False

The modes can be using in conjunction with each other, where `attach_pdf` appends Google links as seperate child items, and `url_set` directly assigns the Google links to the URL field of an item if that field is empty (`url_clear` resets this process).
 

# Usage #

 1. Install *pyzotero* and *pydrive* via pip:  
        `sudo pip install pyzotero pydrive`

 2. Clone or extract the scripts, and navigate to the directory.  Place your CSV file and your config file into it.
 
 3. Run `src/run.py <config> <CSV>`

A browser should open, and you should be prompted for permission to access your current Google Drive. Allow, and then close the window.

After completion a new linked entry should appear for each of your items under the title "Google Drive" which when clicked upon will open up the PDF from your Google Drive in your browser. All users sharing this library will have access to these links.


# Troubleshooting #

If your library is very large, you may encounter the error `OSError: [Errno 24] Too many open files`. This just means you need to increase the number of open files limit. On Linux this is:

     su root
     ulimit -n 5000

  and then reboot. Windows user may have to adjust an equivalent setting.


# Note #

This is *not* a one-time only operation. Every time you add to your library, you will need to re-run the script. Thankfully it only edits items that do not already have links.