'''
Class: ArcoMetadata
Purpose: To hold static information about the different ArcoLinux ISOs.
Depending on whether new ISOs are added, the `metadata` dict can be updated to include it
'''
class ArcoMetadata:
    metadata = {
    "arcolinuxs-xanmod-iso":[
            "Core ISO",
            "Installation = Minimal",
            "Default Desktop = xfc4",
            "Kernel = Xanmod",
            "Software = None",
            "GitHub Repository = https://github.com/arcolinux/arcolinuxs-xanmod-iso"
    ],
    "arcolinuxs-zen-iso":[
            "Core ISO",
            "Installation = Minimal",
            "Default Desktop = xfc4",
            "Kernel = Zen",
            "Software = None",
            "GitHub Repository = https://github.com/arcolinux/arcolinuxs-zen-iso"
    ],
    "arcolinuxs-lts-iso":[
            "Core ISO",
            "Installation = Minimal",
            "Default Desktop = xfc4",
            "Kernel = Linux-LTS",
            "Software = None",
            "GitHub Repository = https://github.com/arcolinux/arcolinuxs-lts-iso"
    ],
    "arcolinuxs-iso":[
            "Core ISO",
            "Installation = Minimal",
            "Default Desktop = xfc4",
            "Kernel = Linux",
            "Software = None",
            "GitHub Repository = https://github.com/arcolinux/arcolinuxs-iso"
    ],
    "arcolinuxl-iso":[
            "Core ISO",
            "Installation = Complete",
            "Default Desktop = xfc4",
            "Kernel = Linux",
            "Software = Lots",
            "GitHub Repository = https://github.com/arcolinux/arcolinuxl-iso"
    ],
    "arcolinuxd-iso":[
            "Core ISO",
            "Installation = Minimal",
            "Default Desktop = None",
            "Kernel = Linux",
            "Software = None",
            "GitHub Repository = https://github.com/arcolinux/arcolinuxd-iso"
    ],
    "arcolinuxb-iso":[
            "Installation = Minimal",
            "Default Desktop = Choose",
            "Kernel = Linux",
            "Software = Minimal",
            "Customize = Build Your Own ISO",
            "GitHub Repository = https://github.com/arcolinuxb"
    ]
}
