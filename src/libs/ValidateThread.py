import requests
import sys
import threading
import hashlib

'''
Class: ValidateThread
Purpose: Spawns a thread to handle sha256 validation of the downloaded ISO.
If the sha256 from the downloaded .iso.sha256 file and the .iso file match, then the ISO download is ok else it failed.
'''
class ValidateThread(threading.Thread):

    def __init__(self,iso_filename,iso_sha256_filename):
        super().__init__()
        self.iso_filename = iso_filename
        self.iso_sha256_filename = iso_sha256_filename

    def run(self):
        try:
            print("[ValidateThread] ISO filename =  %s, ISO sha256 filename = %s thread id = %s" % (self.iso_filename, self.iso_sha256_filename, threading.get_native_id()))


            sha256_hash = None
            sha256_hashf = None
            sha256_hash = hashlib.sha256()
            self.is_download_ok = False
            with open(self.iso_filename,"rb") as f:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: f.read(4096),b""):
                    sha256_hash.update(byte_block)

                sha256_hash = sha256_hash.hexdigest()

            with open(self.iso_sha256_filename,'r') as f:
                sha256hashf = f.readlines()

            if sha256hashf[0].split(' ')[0] == sha256_hash:
                print("[ValidateThread] sha256 = match, download = ok")
                self.is_download_ok = True
            else:
                print("[ValidateThread] sha256 match = failed, download = failed")
                self.is_download_ok = False

        except Exception as err:
            print(err)
            sys.exit(1)
