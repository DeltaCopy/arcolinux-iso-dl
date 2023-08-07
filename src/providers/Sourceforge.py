import sys
import xml.etree.ElementTree as ET
from libs.ISO import ISO
from libs.ResponseThread import ResponseThread

SOURCEFORGE_ARCO_FEED = "https://sourceforge.net/projects/arcolinux/rss?path=/"
SOURCEFORGE_ARCOB_FEED = "https://sourceforge.net/projects/arcolinux-community-editions/rss?path=/${desktop}"

'''
Class: Sourceforge
Purpose: Used to parse the XML RSS feed containing a list of filenames
'''

class Sourceforge(object):
    def __init__(self, settings):
        self.settings = settings

    def get_ISO(self,iso_type, selected_iso_name):

        metadata_iso = []

        selected_iso_name = selected_iso_name.replace("-iso","").replace("arco-","").strip()

        if iso_type == "arcolinux-iso":

            self.downloader_t = ResponseThread(SOURCEFORGE_ARCO_FEED,"text/xml",None,None)
            self.downloader_t.start()
            self.downloader_t.join()


        elif iso_type == "arcolinuxb-iso":

            self.downloader_t = ResponseThread(SOURCEFORGE_ARCOB_FEED.replace("${desktop}",selected_iso_name),"text/xml",None,None)
            self.downloader_t.start()
            self.downloader_t.join()




        metadata_iso = self.parse_content(selected_iso_name,self.downloader_t.content)


        self.destroy_thread()
        return metadata_iso


    def destroy_thread(self):
        print("[Thread-Downloader] Delete text/xml")
        del self.downloader_t

    def prompt_download(self,filename,iso):

        accept = input(Color.BOLD + ':: Proceed with download [Y/n]: ' + Color.END)


        if accept == 'Y' or accept == 'y':
            #isoFile = filename
            charset="application/x-iso9660-image; charset=binary"

            downloader = download = ThreadDownloader(iso.link,charset,None,None)
            download.start()
            download.join()


        return accept



    def parse_content(self,selected_iso_name,response):
        root = ET.fromstring(response)
        metadata_iso = []
        temp = []

        for child in root.iter('item'):

            if len(child.find('title').text) > 0 \
                and ".md5" not in child.find('title').text \
                and ".pkglist.txt" not in child.find('title').text \
                and ".sha1" not in child.find('title').text \
                and ".sig" not in child.find('title').text \
                and ".torrent" not in child.find('title').text\
                and selected_iso_name in child.find('title').text:

                if len(child.find('title').text) > 0 and ".sha256" not in child.find('title').text:
                    title = child.find('title').text
                    temp.append(title.split('/')[-1])



                    for el in child:
                        if len(el) > 0:
                            filesize = el.attrib['filesize']




                if len(child.find('link').text) > 0 and ".sha256" not in child.find('link').text:
                    link = child.find('link').text
                    link = link+"?use_mirror="+self.settings.provider['mirror']

                if len(child.find('link').text) > 0 and ".sha256" in child.find('link').text:
                    sha256_link = child.find('link').text
                    sha256_link = sha256_link+"?use_mirror="+self.settings.provider['mirror']

                if len(child.find('pubDate').text) > 0 and ".sha256" not in child.find('link').text:
                    pubDate = child.find('pubDate').text

                if len(child.find('title').text) > 0 and "sha256" in child.find('title').text:
                    sha256_title = child.find('title').text

                    for el in child:
                        if len(el) > 0:
                            sha256_filesize = el.attrib['filesize']

                    if len(temp) > 0:
                        for iso_title in temp:

                            if iso_title in sha256_title:




                                iso = ISO(
                                    iso_title,
                                    link,
                                    sha256_title.split('/')[-1],
                                    sha256_link,
                                    pubDate,
                                    ISO.get_readable_file_size(int(filesize)),
                                    ISO.get_readable_file_size(int(sha256_filesize))
                                )
                            #break



                        metadata_iso.append(iso)

        return metadata_iso
