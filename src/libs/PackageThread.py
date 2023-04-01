import os
import threading
import subprocess
import datetime
from libs.ISO import ISO
class Package(object):
    def __init__(self, name, install_date, size, version):
        self.name = name
        self.install_date = install_date
        self.size = size
        self.version = version

class PackageThread(threading.Thread):
    def __init__(self):
        super().__init__()

    # https://wiki.archlinux.org/title/Pacman/Tips_and_tricks#List_of_installed_packages
    # # Arch Linux only method, run pacman -Qi and get install date and size
    def run(self):

        pacman_cmd = "/usr/bin/pacman"

        print("[PackageThread] thread id = %s" % threading.get_native_id())
        if os.path.exists(pacman_cmd):
            self.local_pkg_list = []

            print("[PackageThread] Running `pacman -Qiqe`")
            local_pkg_info = subprocess.run([pacman_cmd, "-Qiqe"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding="UTF-8")

            if len(local_pkg_info.stdout.splitlines()) > 0 and local_pkg_info.returncode == 0:

                for pkg in local_pkg_info.stdout.splitlines():

                    if "Name            :" in pkg.strip():
                        pkg_name = pkg.replace("Name","").replace(" ","").replace(":","").strip()


                    if "Version         :" in pkg.strip():
                        pkg_version = pkg.replace("Version","").replace(" ","").replace(":","").strip()

                    if "Installed Size  :" in pkg.strip():
                        pkg_size = pkg.replace("Installed Size","").replace(" ","").replace(":","").strip()

                    if "Install Date    :" in pkg.strip():
                        pkg_install_date = pkg.replace("Install Date","").replace(": ","").strip()
                        if len(pkg_install_date) > 0:
                            pkg_install_date = str(datetime.datetime.strptime(pkg_install_date,"%a %d %b %Y %H:%M:%S %Z"))




                        pkg = Package(pkg_name,pkg_install_date,pkg_size,pkg_version)


                        self.local_pkg_list.append(pkg)
