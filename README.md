# GreenWithEnvy2 (GWE2)

## About

GWE2 is a GTK system utility designed to provide information, control the fans and overclock your NVIDIA video card
and graphics processor.

This is a fork of [gwe](https://gitlab.com/leinardi/gwe) by Roberto Leinardi. It is not affiliated with the original author.

## 💡 Features
<img src="/data/icons/hicolor/48x48@2x/apps/gwe.png" width="96" align="right" hspace="0" />

* Show general GPU stats (model name, driver version, gpu/memory/power usage, clocks, temps, etc)
* GPU and Memory overclock offset profiles
* Custom Fan curve profiles
* Change power limit
* Historical data graphs

<img src="/art/screenshot-1.png" width="800" align="middle"/>

## 📦 How to get GWE
If you don't like to reading manuals and/or you don't know what the Nvidia CoolBits are,
you can watch the following How To made for the original project by [Intelligent Gaming](https://www.youtube.com/channel/UCH4d4o0Otxa7BNYs5Z5UEjg):

[![How To Overclock And Control Fans On An nVidia Graphic Card In Linux - Green With Envy / GWE](https://img.youtube.com/vi/HAKe9ladLvc/0.jpg)](https://www.youtube.com/watch?v=HAKe9ladLvc)

> *Note:* Flathub packages are currently unavailable until this package is submitted to flathub.

### Install from source code

#### Build Time Dependencies

<details>
<summary> (click for details)</summary>

| Distro                | pkg-config         | Python 3.9+   | gobject-introspection       | meson | ninja-build | appstream-util |
| --------------------- | ------------------ | ------------- | --------------------------- | ----- | ----------- | -------------- |
| Arch Linux            | pkg-config         | python        | gobject-introspection       | meson | ninja       | appstream-glib |
| Fedora                | pkgconf-pkg-config | python3-devel | gobject-introspection-devel | meson | ninja-build | appstream-util |
| OpenSUSE              | pkgconf-pkg-config | python3-devel | gobject-introspection-devel | meson | ninja-build | appstream-glib |
| Ubuntu / Debian       | pkg-config         | python3-dev   | libgirepository1.0-dev      | meson | ninja-build | appstream-util |

Arch Linux:
```bash
$ sudo pacman -S pkg-config python gobject-introspection meson ninja appstream-glib
```
Fedora:
```bash
$ sudo dnf install pkgconf-pkg-config python3-devel gobject-introspection-devel meson ninja-build appstream-util
```
OpenSUSE:
```bash
$ sudo zypper install pkgconf-pkg-config python3-devel gobject-introspection-devel meson ninja-build appstream-glib
```
Ubuntu/Debian:
```bash
$ sudo apt install pkg-config python3-dev libgirepository1.0-dev meson ninja-build appstream-util
```
</details>

#### Run Time Dependencies
<details>
<summary> (click for details)</summary>

| Distro        | Python 3.9+ | pip         | gobject-introspection       | libappindicator          | gnome-shell-extension-appindicator |
| ------------- | ----------- | ----------- | --------------------------- | ------------------------ | ---------------------------------- |
| Arch Linux    | python      | python-pip  | gobject-introspection       | libappindicator3         | gnome-shell-extension-appindicator |
| Fedora        | python3     | python3-pip | gobject-introspection-devel | libappindicator-gtk3     | gnome-shell-extension-appindicator |
| OpenSUSE      | python3     | python3-pip | gobject-introspection       | libappindicator3-1       | gnome-shell-extension-appindicator |
| Ubuntu / Debian | python3   | python3-pip | libgirepository1.0-dev      | gir1.2-ayatanaappindicator3-0.1 | gnome-shell-extension-appindicator |
[comment]: <> (TODO: confirm if only debian and only KDE-Plasma. Might affect more systems and Desktop Environments)

Arch Linux:
```bash
$ sudo pacman -S python python-pip gobject-introspection libappindicator3 gnome-shell-extension-appindicator
```
Fedora:
```bash
$ sudo dnf install python3 python3-pip gobject-introspection-devel libappindicator-gtk3 gnome-shell-extension-appindicator
```
OpenSUSE:
```bash
$ sudo zypper install python3 python3-pip gobject-introspection libappindicator3-1 gnome-shell-extension-appindicator
```
Ubuntu / Debian:
```bash
$ sudo apt install python3 python3-pip libgirepository1.0-dev gir1.2-ayatanaappindicator3-0.1 gnome-shell-extension-appindicator
```
</details>

#### Python Dependencies

> **Note:** Some dependencies aren't available in some distributions.  If you have some that are missing,
 it is recommended you install in a virtual environment(like `pipx`) to avoid conflicts with the distribution's packages.

<details>
<summary>(click for details)</summary>

Dependencies from [requirements.txt](requirements.txt):

| Distro          | injector         | packaging         | peewee         | nvidia-ml-py   | PyGObject      | python-xlib  | requests         | reactivex         |
| --------------- | ---------------- | ----------------- | -------------- | -------------- | -------------- | ------------ | ---------------- | ----------------- |
| Arch            | --               | python-packaging  | python-peewee  | --             | python-gobject | python-xlib  | python-requests  | python-reactivex  |
| Fedora          | python3-injector | python3-packaging | python3-peewee | --             | python3-gobject | python3-xlib | python3-requests | python3-reactivex |
| OpenSUSE        | python-injector  | python-packaging  | python-peewee  | python-nvidia-ml-py3 | python-gobject | python-python-xlib | python-requests | python-reactivex |
| Ubuntu / Debian | python3-injector | python3-packaging | python3-peewee | python3-pynvml | python3-gi     | python3-xlib | python3-requests | python3-rx        |

> **Note:**  Some of these haven't been tested. I might have missed packages.  Please open a bug if you
find mistakes.

Arch Linux:

```bash
$ sudo pacman -S python-packaging python-peewee python-gobject python-xlib python-requests python-reactivex
```
Fedora:
```bash
$ sudo dnf install python3-injector python3-packaging python3-peewee python3-gobject python3-xlib python3-requests python3-reactivex
```
OpenSUSE:
```bash
$ sudo zypper install python-injector python-packaging python-peewee python-nvidia-ml-py3 python-gobject python-python-xlib python-requests python-reactivex
```
Ubuntu/Debian:
```bash
$ sudo apt install python3-injector python3-packaging python3-peewee python3-pynvml python3-gi python3-xlib python3-requests python3-rx
```

##### Using pip to install missing dependencies

Some dependencies aren't available in some distributions.  If you have some that are missing,
it is recommended you install in a virtual environment(like `pipx`) to avoid conflicts with
the distribution's packages.

If you still want to install globally and are willing to risk the issues, run the following **after installing all
 the packages available for your distribution**.

```bash
# do a dry run and make sure you are okay with the changes pip will make
$ sudo -H pip3 install --dry-run --break-system-packages -r requirements.txt

# Re-run to make the changes.
# WARNING: this might break your system's python packages
$ sudo -H pip3 install --break-system-packages -r requirements.txt
```
</details>

#### Clone project and install

If you have not installed GWE yet:

```bash
git clone --branch release https://github.com/sir-maniac/GreenWithEnvy2.git
cd GreenWithEnvy2
```
##### Install in an environment (recommended)

After installing pipx, run:

```bash
$ pipx install .
```

##### Alterative: Install system-wide

Install as many python packages as you can for your distribution, and install
 any others using pip, as detailed under Python Dependencies.

```bash
$ meson setup . build --prefix /usr/local
$ meson compile -C build
$ sudo meson install -C build
```

#### Update old installation

If you installed GWE2 from source code previously and you want to update it:

Check python requirements above and ensure they are installed/updated

```bash
$ cd GreenWithEnvy2
$ git fetch
$ git checkout release
$ git reset --hard origin/release

# Reinstall with pipx
$ pipx uninstall gwe2 && pipx install .

# Or for a system-wide install
$ meson setup . build --reconfigure --prefix /usr/local
$ meson compile -C build
$ sudo meson install -C build
```
#### Run

Once installed, to start it you can simply execute on a terminal:
```bash
$ gwe2
```

#### ⚠ Bumblebee and Optimus

If you want to use GWE with Bumblebee you need to start it with `optirun` and set the `--ctrl-display` parameter to `:8`:

```bash
$ optirun gwe2 --ctrl-display ":8"
```

### Packages for the original GWE

The following packages are still available for the original gwe.  They are here informational purposes.
Support for them is limited, as bug fixes and changes won't appear in those packages.

#### Arch Linux

Install the `gwe` package from the AUR using your favourite helper, for example `yay -S gwe`.

#### Fedora

GWE avaliable in official Fedora [repos](https://src.fedoraproject.org/rpms/gwe) for F31+: `sudo dnf install gwe`

For older Fedora releases you can use [COPR package](https://copr.fedorainfracloud.org/coprs/atim/gwe/): `sudo dnf copr enable atim/gwe -y && sudo dnf install gwe`

### Flathub Limitations

#### Beta Drivers

Currently [Flatpak does not support Nvidia Beta drivers](https://github.com/flathub/org.freedesktop.Platform.GL.nvidia/issues/1)
like 396.54.09 or 415.22.05.

#### Bumblebee and Optimus

Currently [Flatpak does not support Bumblebee](https://github.com/flatpak/flatpak/issues/869). If you want to use GWE with Bumblebee
you need to install it from the source code.



<details>
<summary>
ℹ️ TODO (click for details)
</summary>

- [x] Show general GPU info
- [x] Show power info
- [x] Show clocks info
- [x] Show GPU temp in both app and app indicator
- [x] Show fan info
- [x] Allow to hide main app window
- [x] Add command line option to start the app hidden
- [x] Add Refresh timeout to settings
- [x] Add command line option to add desktop entry
- [x] About dialog
- [x] Distributing with PyPI
- [x] Show chart of selected fan profile
- [x] Allow to select and apply a fan profile
- [x] Add/Delete/Edit multi speed fan profiles (fan curve)
- [x] Add option to restore last applied fan profile on app startup
- [x] Find better icons for app indicator
- [x] Try to lower resource consumption (mostly caused by `nvidia-settings` invocations)
- [x] Show historical data of most important values in a separate dialog (requires GTK 3.24/GNOME 3.30)
- [x] Add overclock profiles
- [x] Add option to restore last applied overclock profile on app startup
- [ ] Disable unsupported preferences
- [x] Distributing with Flatpak
- [x] Publishing on Flathub
- [ ] Distributing with Snap
- [x] Check if NV-CONTROL is available and tell the user if is not
- [ ] Add support for multi-GPU
- [ ] Allow to select profiles from app indicator
- [ ] Add support for i18n (internationalization and localization)
</details>

<!--
## Application entry
To add a desktop entry for the application run the following command (not supported by Flatpak):
```bash
gwe --application-entry
```
If you don't want to create this custom rule you can run gwe as root
(using sudo) but we advise against this solution.
-->
## ⌨️ Command line options

  | Parameter                 | Description                               | Source | Flatpak |
  |---------------------------|-------------------------------------------|:------:|:-------:|
  |-v, --version              |Show the app version                       |    x   |    x    |
  |--debug                    |Show debug messages                        |    x   |    x    |
  |--hide-window              |Start with the main window hidden          |    x   |    x    |
  |--ctrl-display DISPLAY     |Specify the NV-CONTROL display             |    x   |    x    |
  |--autostart-on             |Enable automatic start of the app on login |    x   |         |
  |--autostart-off            |Disable automatic start of the app on login|    x   |         |

## 🖥️ Build, install and run with Flatpak
If you don't have Flatpak installed you can find step by step instructions [here](https://flatpak.org/setup/).

Make sure to have the Flathub remote added to the current user:

> *Note:* This fork hasn't been submitted to flathub yet, however you can still
 build and install the flatpak package locally.

### Clone the repo
```bash
git clone --recurse-submodules -j4 https://github.com/sir-maniac/GreenWithEnvy2.git
```
It is possible to build the local source or the remote one (the same that Flathub uses)
### Local repository
```bash
./build.sh --flatpak-local --flatpak-install
```
### Remote repository
```bash
./build.sh --flatpak-remote --flatpak-install
```
### Run
```bash
flatpak run io.github.sir_maniac.gwe2 --debug
```

## ❓ FAQ
### I see some message about CoolBits in the Overclock/Fan profile section, what's that?
Coolbits was a Windows registry hack for Nvidia graphics cards Windows drivers, that allows
tweaking features via the Nvidia driver control panel.
Something similar is available also on Linux and is the only way to enable Overclock and manual Fan control.
To know more about Coolbits and how to enable them click
[here](https://wiki.archlinux.org/index.php/NVIDIA/Tips_and_tricks#Enabling_overclocking)
(to enable both OC and Fan control you need to set it to `12`).

### Can I make the power limit survive a reboot?
GWE cannot set the power limit automatically because, to change this value, root permission is required.
If your distribution is using systemd, you can easily set the power limit on boot creating a custom service.

Simply create a new file `/etc/systemd/system/nvidia-tdp.timer` and paste the following text inside:
```
[Unit]
Description=Set NVIDIA power limit on boot

[Timer]
OnBootSec=5

[Install]
WantedBy=timers.target
```

Then create another file `/etc/systemd/system/nvidia-tdp.service` and paste the following text inside (replace `XXX` with the power limit value you want to set):
```
[Unit]
Description=Set NVIDIA power limit

[Service]
Type=oneshot
ExecStartPre=/usr/bin/nvidia-smi -pm 1
ExecStart=/usr/bin/nvidia-smi -pl XXX
```

Finally, run the following command:
```
sudo systemctl enable nvidia-tdp.timer
```

### The Flatpak version of GWE is not using my theme, how can I fix it?
To fix this issue install a Gtk theme from Flathub. This way, Flatpak applications will automatically pick the
installed Gtk theme and use that instead of Adwaita.

Use this command to get a list of all the available Gtk themes on Flathub:
```bash
flatpak --user remote-ls flathub | grep org.gtk.Gtk3theme
```
And then just install your preferred theme. For example, to install Yaru:
```
flatpak install flathub org.gtk.Gtk3theme.Yaru
```

### I have installed the app using Flatpak, but all the GWE fields are empty
This issue can be usually solved by closing GWE, executing `flatpak update` and starting GWE again.
This is necessary to be sure to have the latest [org.freedesktop.Platform.GL.nvidia](https://github.com/flathub/org.freedesktop.Platform.GL.nvidia).
If, after the update, all the fields are still empty, feel free to open a new issue on the project tracker.

### Why the memory overclock offsets effectively applied does not match the one set in the Nvidia Settings app?
Because Memory Transfer Rate, what Nvidia Settings reports and changes,
is different from the effective Memory Clock, what is actually being
displayed by GWE. It is also what other Windows applications like MSI Afterburner show.
The Memory Transfer Rate is simply double the Memory Clock.

### Where are the settings and profiles stored on the filesystem?
| Installation type |                     Location                     |
|-------------------|:------------------------------------------------:|
| Flatpak           | `$HOME/.var/app/io.github.sir_maniac.gwe2/`      |
| Source code       | `$XDG_CONFIG_HOME` (usually `$HOME/.config/gwe`) |

### GreenWithEnvy, why using such name?
The name comes from the slogan of the GeForce 8 series, that was "Green with envy".
Nvidia is meant to be pronounced "invidia", which means envy in Latin (and Italian). And their logo is green so, GreenWithEnvy

## 💚 How to help the project
### Help is needed for the following topics
 - Support for Wayland (see [#9](https://github.com/sir-maniac/GreenWithEnvy2/issues/9))
 - Snap (see [#10](https://github.com/sir-maniac/GreenWithEnvy2/issues/10))

### Can I support this project some other way?

Something simple that everyone can do is to star it on [GitHub](https://github.com/sir-maniac/GreenWithEnvy2).
Feedback is always welcome: if you found a bug or would like to suggest a feature,
feel free to open an issue on the [issue tracker](https://github.com/sir-maniac/GreenWithEnvy2/issues).

## ℹ️ Acknowledgements
Special thanks to:
 -  **Roberto Leinardi** for authoring GWE and assisting other contributors working to keep it alive.

Thanks (from the original gwe):
 - GabMus and TingPing for the huge help with Flatpak
 - @999eagle for maintaining the [AUR package](https://aur.archlinux.org/packages/gwe/)
 - @tim74 for maintaining the [COPR package](https://copr.fedorainfracloud.org/coprs/atim/gwe/)
 - Lighty for moderating the [Discord](https://discord.gg/YjPdNff) server
 - fbcotter for the [py3nvml](https://github.com/fbcotter/py3nvml/) library
 - all the devs of the [python-xlib](https://github.com/python-xlib/python-xlib/) library
 - tiheum for the [Faenza](https://www.deviantart.com/tiheum/art/Faenza-Icons-173323228) icons set, from which I took the current GWE launcher icon
 - all the people that helped testing and reported bugs

## 📰 Media coverage for the original GWE
 - [OMG! Ubuntu](https://www.omgubuntu.co.uk/2019/02/easily-overclock-nvidia-gpu-on-linux-with-this-new-app) 🇬🇧
 - [GamingOnLinux](https://www.gamingonlinux.com/articles/greenwithenvy-an-impressive-tool-for-overclocking-nvidia-gpus.13521) 🇬🇧
 - [Phoronix](https://www.phoronix.com/scan.php?page=news_item&px=GreenWithEnvy-0.11-Released) 🇬🇧
 - [ComputerBase](https://www.computerbase.de/2019-02/green-envy-uebertakten-nvidia-grafikkarten-linux/) 🇩🇪
 - [lffl](https://www.lffl.org/2019/02/overclock-scheda-nvidia-linux.html) 🇮🇹
 - [osside blog](https://www.osside.net/2019/02/greenwithenvy-gwe-linux-easy-nvidia-status-overclock/) 🇮🇹
 - [Diolinux](https://www.diolinux.com.br/2019/02/greenwithenvy-uma-nova-forma-de-voce-gerenciar-gpu-nvidia.html?m=1) 🇧🇷
 - [Blog do Edivaldo](https://www.edivaldobrito.com.br/overclock-em-gpus-nvidia-no-linux/) 🇧🇷
 - [Linux Adictos](https://www.linuxadictos.com/greenwithenvy-programa-para-overclocking-en-gpus-nvidia.html) 🇪🇸


## 📝 License
```
This file is part of gwe.

Copyright (c) 2025 Ryan Bloomfield
Copyright (c) 2019 Roberto Leinardi

gwe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gwe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gwe.  If not, see <http://www.gnu.org/licenses/>.
```
