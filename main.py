#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014 - 2019, Philip Müller <philm@manjaro.org>
#   Copyright 2016, Artoo <artoo@manjaro.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import libcalamares
import subprocess
from shutil import copy2, copytree
from os.path import join, exists
from libcalamares.utils import target_env_call, target_env_process_output


class ConfigController:
    def __init__(self):
        self.__root = libcalamares.globalstorage.value("rootMountPoint")
        self.__keyrings = libcalamares.job.configuration.get('keyrings', [])

    @property
    def root(self):
        return self.__root

    @property
    def keyrings(self):
        return self.__keyrings

    def init_keyring(self):
        target_env_call(["pacman-key", "--init"])

    def populate_keyring(self):
        target_env_call(["pacman-key", "--populate"])

    def terminate(self, proc):
        target_env_call(['killall', '-9', proc])

    def copy_file(self, file):
        if exists("/" + file):
            copy2("/" + file, join(self.root, file))

    def copy_folder(self, source, target):
        if exists("/" + source):
            copytree("/" + source, join(self.root, target),
                     symlinks=True, dirs_exist_ok=True)

    def find_xdg_directory(self, user, type):
        output = []
        target_env_process_output(
            ["su", "-lT", user, "xdg-user-dir", type], output
        )
        return output[0].strip()

    def is_btrfs_root(self) -> bool:
        """
        Checks if the root partition (/) is formatted with Btrfs.
        """
        partitions = libcalamares.globalstorage.value("partitions")

        if not partitions:
            return False

        for partition in partitions:
            if partition.get("mountPoint") == "/":
                return partition.get("fs") == "btrfs"

        return False


    def run(self) -> None:

        bootloader = libcalamares.globalstorage.value("packagechooser_bootloader")

        # --- Snapper config ---
        if self.is_btrfs_root():
            libcalamares.utils.debug("Btrfs detected. Configuring Snapper...")
            

            if exists(join(self.root, "usr/bin/snapper")):

                root_created = False
                home_created = False

                if not exists(join(self.root, "etc/snapper/configs/root")):
                    target_env_call([
                        "snapper", "--no-dbus", "-c", "root", "create-config", "/"
                    ])
                    root_created = True

                if exists(join(self.root, "home")) and not exists(join(self.root, "etc/snapper/configs/home")):
                    target_env_call([
                        "snapper", "--no-dbus", "-c", "home", "create-config", "/home"
                    ])
                    home_created = True

                if root_created:
                    target_env_call([
                        "snapper", "--no-dbus", "-c", "root",
                        "create",
                        "--description", "Initial system snapshot",
                        "--cleanup-algorithm", "number"
                    ])


                if home_created:
                    target_env_call([
                        "snapper", "--no-dbus", "-c", "home",
                        "create",
                        "--description", "Initial home snapshot",
                        "--cleanup-algorithm", "number"
                    ])

                if root_created or home_created:
                    target_env_call(["systemctl", "enable", "snapper-timeline.timer"])
                    target_env_call(["systemctl", "enable", "snapper-cleanup.timer"])

                if exists(join(self.root, "usr/bin/grub-btrfsd")):
                    target_env_call(["systemctl", "enable", "grub-btrfsd.service"])

                

                if bootloader == "grub" and exists(join(self.root, "usr/bin/grub-mkconfig")):
                    target_env_call([
                        "grub-mkconfig", "-o", "/boot/grub/grub.cfg"
                    ])
                elif bootloader == "limine":
                    libcalamares.utils.debug("Limine detected, skipping GRUB config")
            else:
                libcalamares.utils.debug("Snapper not installed")
                return None
        else:
            libcalamares.utils.debug(
                "Non-Btrfs filesystem detected. Removing Snapper stack..."
            )
            target_env_call([
                "sh", "-c",
                "pacman -Rns --noconfirm snapper snap-pac grub-btrfs inotify-tools 2>/dev/null || true"
            ])

        return None


def run():
    config = ConfigController()
    return config.run()
