# **Zotero/GoogleDrive PDF-Linker - Cloud** #

This is the *Cloud* version of the [Zotero/GoogleDrive PDF-Linker](https://github.com/mtekman/ZoteroGoogleDrive-PDFLinker).

It does not need an exported CSV file of your library, but syncs articles from your Zotero-Cloud account, with shareable links from a folder in your Google Drive.

If your local PDFs are not yet uploaded/synced to your Google Drive, this tool will do that for you too.

## Usage

 1. Install *pyzotero* and *pydrive* via pip:  
        `sudo pip install pyzotero pydrive`


 2. Run `./src/run.py <config file>`


## Configuration

A template config file can be generated via the `--make-config` parameter, producing the following file:


	[Google Drive]
	#  use pdfs from this folder, or if the folder
	# doesn't exist, create it
	#  as a new directory at top-level root.
	folder name = MyPDFs

	[Zotero Settings]
	#  can be found at https://www.zotero.org/settings/keys, 'create new private key'
	api key = N4vY534Lt0pCl455
	#  library id found at https://www.zotero.org/settings/keys, 'your userid for api calls is <libraryid>'
	user library id = 1234567
	user collection name = mycollection

	[PDF Settings]
	#  what to do with each pdf:
	#  - any conjunction of attaching the pdf as a child item,
	#    and/or overwriting or clearing the url field of the item
	#  - valid modes are: attach_pdf, remove_pdf, url_set, url_clear
	mode = attach_pdf
	#
	# pdfs are either handled internally by zotero and synced to their servers
	# or are accessed from an external path on your local machine.
	#  - if you use zotero storage, provide the cache directory, or the full external path /foo/bar/pdfs/etc/
	#  - zotero storage folder in linux is at '~/.zotero/zotero/<blah>.default/zotero/storage/'
	#                      and in windows is likely under the appdata folder somewhere
	#                      and in macOS is likely under `/Users/<your_user_name>/Zotero/storage/`
	storage = /change/this/path

This file can then be passed in as first parameter to the run script.


### Note / Good Practice Conventions

 Do not nest directories for best results.
 
 As before, this is *not* a one-time only operation. Every time you add to your library, you will need to re-run the script. Thankfully it only edits items that do not already have links.
