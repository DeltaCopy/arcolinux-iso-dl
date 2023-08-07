'''
Class: Settings
Purpose: To encapsulate configuration settings stored inside ~/.config/arcolinux-iso/settings.toml file
'''
class Settings (object):
    def __init__(self,provider,arcolinuxb,arcolinux,cache_path,mirror):
        self.provider = provider
        self.arcolinuxb = arcolinuxb
        self.arcolinux = arcolinux
        self.cache_path = cache_path
        self.mirror = mirror
