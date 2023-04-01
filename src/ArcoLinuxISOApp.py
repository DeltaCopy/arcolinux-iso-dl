#!/usr/bin/env python
from PyQt5.QtWidgets import *

from libs.GuiApplication import GuiApplication
import tomli
import argparse
import sys
import os
import shutil
import pathlib
from libs.Settings import Settings
from providers import Sourceforge

conf_dir="$HOME/.config/arcolinux-iso"
settings_file="$HOME/.config/arcolinux-iso/settings.toml"

def read_settings(settings):

    config = None

    with open(settings, mode="rb") as fp:
        config = tomli.load(fp)

    fp.close()

    if config['iso']['arcolinuxb'] is None \
        or len(config['iso']['arcolinuxb']) == 0:
        print(Color.RED + "error: Settings file is missing a list of ArcoLinuxB ISO Names." + Color.END)
        sys.exit(1)

    if config['iso'] is None or len(config['iso']) == 0:
        print(Color.RED + "error: Settings file is missing a list of ArcoLinux ISO names." + Color.END)
        sys.exit(1)

    selected_source = get_download_providers(config)
    selected_mirror = get_download_mirror(config)

    cache_path = None

    if "$HOME" or "~" in config['iso']['cache_path']:
        cache_path = config['iso']['cache_path'].replace("$HOME",str(pathlib.Path.home())).replace("~",str(pathlib.Path.home()))
    else:
        cache_path = config['iso']['cache_path']

    settings = Settings(selected_source,config['iso']['arcolinuxb'],config['iso']['arcolinux'],cache_path,selected_mirror)

    return settings

def get_download_mirror(settings):

    selected_mirror = None
    if "mirror" in str(settings['providers']):
        if len(settings['providers']) > 0:
            for provider in settings['providers']:
                if provider['enabled'] == True:
                    selected_mirror = provider['mirror']
                    break
        elif len(settings['providers'] == 0):
            print("error: Invalid settings, download providers are missing.")
            sys.exit(1)
    else:
        print("error: Settings file is missing a list of download providers.")
        sys.exit(1)


    if selected_mirror == None:
        print("error: Failed to find a valid download provider, please verify the settings file.")
        sys.exit(1)

    return selected_mirror

def get_download_providers(settings):

    selected_provider = None
    if "name" in str(settings['providers']):
        if len(settings['providers']) > 0:
            for provider in settings['providers']:
                if provider['enabled'] == True:
                    selected_provider = provider
                    break
        elif len(settings['providers'] == 0):
            print("error: Invalid settings, download providers are missing.")
            sys.exit(1)
    else:
        print("error: Settings file is missing a list of download providers.")
        sys.exit(1)


    if selected_provider == None:
        print("error: Failed to find a valid download provider, please verify the settings file.")
        sys.exit(1)

    return selected_provider

def create_dir(cache_dir):
    try:
        if(not os.path.exists(cache_dir)):
            os.mkdir(cache_dir)

    except Exception as err:
        print("error: %s" % err)
        sys.exit(1)

def main():
    if not os.path.exists(settings_file.replace("$HOME",str(pathlib.Path.home())).replace("~",str(pathlib.Path.home()))):
        print("Error: failed to locate settings file, the default location is = %s" % settings_file)
        

        sys.exit(1)

    else:
        print("Using settings file inside %s" % settings_file)


    if "$HOME" or "~" in settings_file:
        settings = read_settings(settings_file.replace("$HOME",str(pathlib.Path.home())).replace("~",str(pathlib.Path.home())))
    else:
        settings = read_settings(settings_file)

    create_dir(settings.cache_path)

    app = QApplication([])

    window = GuiApplication(settings)
    app.setDesktopFileName("org.kde.arcolinuxisodl")


    app.exec_()

if __name__ == "__main__":
    main()
