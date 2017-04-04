#!/usr/bin/env python3


class LocalLibs:

    @staticmethod
    def localFileExists(filename):

        try:
            pop = open(filename,'r')
            data = pop.readline()
            pop.close()

            if len(data.strip()) == 0:
                return False  # Blank file
      
            return True   # does exist with data
        except IOError:
            return False    # does not exist
