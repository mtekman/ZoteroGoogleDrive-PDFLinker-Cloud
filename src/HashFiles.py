#!/usr/bin/env python3

from hashlib import md5
from os import path, mkdir
from glob import glob
from sys import stderr as cerr
from string import ascii_letters, digits
from appdirs import user_cache_dir

class HashFiles:
    """Class to be used in conjunction with the MD5 hashes on Server for attachment types"""

    def __init__(self, storage_dir):

        if not path.isdir(storage_dir):
            print("[Error] HashFiles", storage_dir, "is not a valid storage directory", file=cerr)
            exit(-1)
        
        self.storage_path = path.abspath(storage_dir)

        # Setup user cache and hash file storage
        config_dir = user_cache_dir('GoogleZoteroPDFLinker')
        if not path.exists(config_dir):
            mkdir(config_dir)

        self.hash_filename = path.join(config_dir, HashFiles.__cleanstring(self.storage_path)+".hashes")
        self.map = {} # hash -> file, no collision...

        if not path.exists(self.hash_filename):
            self.generateHashesToCache()
        else:
            self.readHashesFromCache()
        

        


    def readHashesFromCache(self):

        with open(self.hash_filename, 'r') as hash_file:
            for line in hash_file:
                hashv, filen = line.splitlines()[0].split('\t')
                self.map[hashv] = filen
            hash_file.close()           

        print("[Info] HashFiles read in", len(self.map), "hashes.", file=cerr)

    
    def generateHashesToCache(self):
        hash_file = open(self.hash_filename, 'w')

        dupes = {}
        dupe_count = 0

        for filen in glob(self.storage_path+"/**/*.pdf", recursive=True):
            hashv = HashFiles.__md5sum(filen)

            if hashv in self.map:
                if hashv not in dupes:
                    dupes[hashv] = [self.map[hashv]]
                dupes[hashv].append(filen)
                dupe_count += 1
                               

            # Populate map and write
            self.map[hashv] = filen
            print(hashv, filen, sep='\t', file=hash_file)

        hash_file.close()

        with open(self.hash_filename+".dupes", 'w') as hash_dupes:
            for hashv in dupes:
                print(hashv, dupes[hashv], file=hash_dupes)
            hash_dupes.close()
            

        print("[Info] HashFiles populated", len(self.map), #"hashes in", self.hash_filename,
              "of which %d are duplicates of which %d are unique duplicates" % (dupe_count, len(dupes)), file=cerr)


    @staticmethod
    def __cleanstring(string):
        """Should produce a reasonably unique string"""
        valid_chars = "-_.() %s%s" % (ascii_letters, digits)
        return ''.join(c if c in  valid_chars else "__" for c in string)


    @staticmethod
    def __md5sum(fname):
        hash_md5 = md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

        


#HashFiles('/home/tetron/.zotero/zotero/911t4bhn.default/zotero/storage/')
#a.generateHashesToCache()
#a.readHashesFromCache()
