#!/usr/bin/env sh
set -o pipefail
# wayland issue loading custom application icons, so set qt platform plugin ti xcb
export QT_QPA_PLATFORM="xcb"
conf_dir="$HOME/.config/arcolinux-iso"
conf="$conf_dir/settings.toml"

echo ":: ArcoLinux ISO Downloader"

test -d "$conf_dir" || mkdir -p "$conf_dir"
if [ ! -s "$conf" ]; then
  echo "--> Configuration file $conf is missing, attempting to generate one."
  cat << EOF > $conf
  title = "Settings file for ArcoLinux ISO Downloader"
  [iso]
  # only change this if you know what your are doing
  cache_path = "~/.cache/arcolinux-iso"

  arcolinuxb = [
  "arco-sway",
  "arco-plasma",
  "arco-hyprland",
  "arco-chadwm",
  "arco-dusk",
  "arco-dwm",
  "arco-berry",
  "arco-hypr",
  "arco-enlightenment",
  "arco-xtended",
  "arco-pantheon",
  "arco-awesome",
  "arco-bspwm",
  "arco-cinnamon",
  "arco-budgie",
  "arco-cutefish",
  "arco-cwm",
  "arco-deepin",
  "arco-gnome",
  "arco-fvwm3",
  "arco-herbstluftwm",
  "arco-i3",
  "arco-icewm",
  "arco-jwm",
  "arco-leftwm",
  "arco-lxqt",
  "arco-mate",
  "arco-openbox",
  "arco-qtile",
  "arco-spectrwm",
  "arco-ukui",
  "arco-wmderland",
  "arco-xfce",
  "arco-xmonad",
  ]

  arcolinux = [
  "arcolinuxs-xanmod-iso",
  "arcolinuxs-zen-iso",
  "arcolinuxs-lts-iso",
  "arcolinuxs-iso",
  "arcolinuxl-iso",
  "arcolinuxd-iso"
  ]


  [[providers]]
  name = "SourceForge"
  # To use another mirror use its short-name, for a full list see https://sourceforge.net/p/forge/documentation/Mirrors/
  mirror = "altushost-swe"
  enabled = true
  desktop_project_key = "arcolinux-community-editions"
  iso_project_key = "arcolinux"

EOF
fi

test -s "$conf" || echo "Failed to locate $conf, exiting." || exit 1
python ../src/ArcoLinuxISOApp.py
