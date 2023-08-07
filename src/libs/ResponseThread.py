import requests
import sys
import threading
import os
import hashlib
import tomli
import traceback

'''
Class: ResponseThread
Purpose: Spawn a thread to handle package list requests
Each package list obtained from GitHub will be cached along with the HTTP E-Tag
When making a request, check the E-Tag is up to date first, if it differs from the one on the server.
Make a request to get the actual package list file.
Cached files are stored inside $HOME/.cache/arcolinx-iso
'''

class ResponseThread(threading.Thread):

    def __init__(self,url,content_type,iso_name, cache_path):
        super().__init__()
        self.url = url
        self.content_type = content_type
        self.iso_name = iso_name
        self.cache_path = cache_path

    def run(self):
        try:
            print("[ResponseThread] Get %s thread id = %s" % (self.content_type, threading.get_native_id()))
            self.headers = { "Content-Type" : self.content_type, "charset" : "UTF-8"  }

            if self.iso_name is not None and self.cache_path is not None:


                # request the header only to get the etag

                # generate md5hash of the file
                self.md5_hash = hashlib.md5(self.iso_name.encode('utf-8')).hexdigest()

                self.cache_file = self.cache_path + "/" + self.md5_hash


                if os.path.exists(self.cache_file):
                    with open(self.cache_file, mode="rb") as f:
                        cached_content = tomli.load(f)


                    cached_etag = cached_content['etag']


                    # make request for etag from github

                    etag = requests.head(self.url).headers['ETag'].replace('W/"','').replace('"','')

                    if cached_etag == etag:
                        print("[ResponseThread] packages.x86_64 ETag match, using cache")
                        # no change use cache
                        self.content = cached_content['content'].strip()

                    else:
                        print("[ResponseThread] packages.x86_64 ETag changed, using server content")
                        # changes use server content
                        self.write_to_disk()


                else:
                    print("[ResponseThread] packages.x86_64 Cache doesn't exist, using server content")
                    self.write_to_disk()
            else:
                r = requests.get(self.url,headers=self.headers, allow_redirects=True)
                if r.status_code == 200:
                    if len(r.text) > 0:
                        self.content = r.text
                else:
                    self.content = None
        except requests.exceptions.ConnectionError:
            print("[ResponseThread] Connection error, failed to make request to %s" % self.url)
            self.content = None
        except Exception:
            print("[ResponseThread] %s" % traceback.format_exc())
            self.content = None



    def write_to_disk(self):

        r = requests.get(self.url,headers=self.headers, allow_redirects=True)
        if r.status_code == 200:
            if len(r.text) > 0:
                self.content = r.text
                etag = requests.head(self.url).headers['ETag'].replace('W/"','').replace('"','')

                cache_file = self.cache_path + "/" + self.md5_hash
                with open(cache_file, "w") as f:
                    f.writelines('etag = "%s"' % etag)
                    f.writelines('\r\ncontent = """\\\r\n%s"""' % self.content.strip())
        else:
            self.content = None
