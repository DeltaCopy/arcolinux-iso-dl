import sys
import os

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

'''
Class: ISO
Purpose: Encapsulates an ISO image.
Provides a method to calculate a readable filesize of the ISO
'''
class ISO(object):
    def __init__(self,name,link,sha256_name,sha256_link,pub_date,filesize,sha256_filesize):
        self.name = name
        self.link = link
        self.sha256_name = sha256_name
        self.sha256_link = sha256_link
        self.pub_date = pub_date
        self.filesize = filesize
        self.sha256_filesize = sha256_filesize

    def get_readable_file_size(size_in_bytes):
        index = 0
        while size_in_bytes >= 1024:
            size_in_bytes /= 1024
            index += 1
        try:
            return f'{round(size_in_bytes,1)} {SIZE_UNITS[index]}'
        except IndexError:
            return 'File too large'
