import requests
import sys
import time
import threading
from PyQt5.QtCore import pyqtSignal, QThread
TIME_LIMIT = 9999

'''
Class: DownloadThread
Purpose: To spawn a thread to handle the download of the ISO and associated ISO.md5 files.
The thread also provides pyqtSignals to ensure the progress bar, download status is updated
on the main gui thread.
'''
class DownloadThread(QThread):
    setTotalProgress = pyqtSignal(int)
    setCurrentProgress = pyqtSignal(int)
    succeeded = pyqtSignal()
    inProgress = pyqtSignal(bool)


    def __init__(self, url, filename,content_type):
        super().__init__()
        self.url = url
        self.filename = filename
        self.content_type = content_type

    def run(self):

        print("[DownloadThread] Get %s thread id = %s" % ( self.content_type, threading.get_native_id()))

        headers = { "Content-Type" : self.content_type, "charset" : "UTF-8" }
        bytes_read = 0
        chunk_size = 5120



        with requests.get(self.url, stream=True,headers=headers, allow_redirects=True) as r:

            if r.headers['Content-Type'] == 'application/octet-stream':

                r.raise_for_status()
                content_length = int(r.headers.get('content-length',0))
                self.setTotalProgress.emit(round(content_length/10))
                if content_length > 0:
                    with open(self.filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if QThread.currentThread().isInterruptionRequested():
                                print("[DownloadThread] Interrupt thread")
                                return
                            if chunk is None:
                                continue
                            elif chunk == b"":
                                self.inProgress.emit(False)
                                break

                            f.write(chunk)
                            bytes_read += round(chunk_size/10)


                            self.setCurrentProgress.emit(bytes_read)



                            self.inProgress.emit(True)
            else:
                print("[DownloadThread] Response is not 'application/octet-stream'")
                self.inProgress.emit(False)
        self.succeeded.emit()
