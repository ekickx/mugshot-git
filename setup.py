#!/usr/bin/python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#   Mugshot - Lightweight user configuration utility
#   Copyright (C) 2013-2018 Sean Davis <smd.seandavis@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranties of
#   MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess

try:
    import DistUtilsExtra.auto
except ImportError:
    sys.stderr.write("To build mugshot you need "
                     "https://launchpad.net/python-distutils-extra\n")
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', \
    'needs DistUtilsExtra.auto >= 2.18'


def update_config(libdir, values={}):
    """Update the configuration file at installation time."""
    filename = os.path.join(libdir, 'mugshot_lib', 'mugshotconfig.py')
    oldvalues = {}
    try:
        fin = open(filename, 'r')
        fout = open(filename + '.new', 'w')

        for line in fin:
            fields = line.split(' = ')  # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print(("ERROR: Can't find %s" % filename))
        sys.exit(1)
    return oldvalues


def move_icon_file(root, target_data):
    """Move the icon files to their installation prefix."""
    old_icon_path = os.path.normpath(os.path.join(root, target_data, 'share',
                                                  'mugshot', 'media'))
    for icon_size in ['16x16', '22x22', '24x24', '48x48', '64x64', 'scalable']:
        if icon_size == 'scalable':
            old_icon_file = os.path.join(old_icon_path, 'mugshot.svg')
        else:
            old_icon_file = os.path.join(old_icon_path,
                                         'mugshot_%s.svg' %
                                         icon_size.split('x')[0])
        icon_path = os.path.normpath(os.path.join(root, target_data, 'share',
                                                  'icons', 'hicolor', icon_size, 'apps'))
        icon_file = os.path.join(icon_path, 'mugshot.svg')
        old_icon_file = os.path.realpath(old_icon_file)
        icon_file = os.path.realpath(icon_file)

        if not os.path.exists(old_icon_file):
            print(("ERROR: Can't find", old_icon_file))
            sys.exit(1)
        if not os.path.exists(icon_path):
            os.makedirs(icon_path)
        if old_icon_file != icon_file:
            print(("Moving icon file: %s -> %s" % (old_icon_file, icon_file)))
            os.rename(old_icon_file, icon_file)

    # Media is now empty
    if len(os.listdir(old_icon_path)) == 0:
        print(("Removing empty directory: %s" % old_icon_path))
        os.rmdir(old_icon_path)

    return icon_file


def get_desktop_file(root, target_data):
    """Move the desktop file to its installation prefix."""
    desktop_path = os.path.realpath(os.path.join(root, target_data, 'share',
                                                 'applications'))
    desktop_file = os.path.join(desktop_path, 'mugshot.desktop')
    return desktop_file


def update_desktop_file(filename, script_path):
    """Update the desktop file with prefixed paths."""
    try:
        fin = open(filename, 'r', -1, 'utf-8')
        fout = open(filename + '.new', 'w', -1, 'utf-8')

        for line in fin:
            if 'Exec=' in line:
                cmd = line.split("=")[1].split(None, 1)
                line = "Exec=%s" % os.path.join(script_path, 'mugshot')
                if len(cmd) > 1:
                    line += " %s" % cmd[1].strip()  # Add script arguments back
                line += "\n"
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print(("ERROR: Can't find %s" % filename))
        sys.exit(1)


def write_appdata_file(filename_in):
    filename_out = filename_in.rstrip('.in')
    cmd = ["intltool-merge", "-x", "-d", "po", filename_in, filename_out]
    print(" ".join(cmd))
    subprocess.call(cmd, shell=False)


# Update AppData with latest translations first.
write_appdata_file("data/metainfo/mugshot.appdata.xml.in")


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):

    """Command Class to install and update the directory."""

    def run(self):
        """Run the setup commands."""
        DistUtilsExtra.auto.install_auto.run(self)

        print(("=== Installing %s, version %s ===" %
               (self.distribution.get_name(), self.distribution.get_version())))

        if not self.prefix:
            self.prefix = ''

        if self.root:
            target_data = os.path.relpath(self.install_data, self.root) + \
                os.sep
            target_pkgdata = os.path.join(target_data, 'share', 'mugshot', '')
            target_scripts = os.path.join(self.install_scripts, '')

            data_dir = os.path.join(self.prefix, 'share', 'mugshot', '')
            script_path = os.path.join(self.prefix, 'bin')
        else:
            # --user install
            self.root = ''
            target_data = os.path.relpath(self.install_data) + os.sep
            target_pkgdata = os.path.join(target_data, 'share', 'mugshot', '')
            target_scripts = os.path.join(self.install_scripts, '')

            # Use absolute paths
            target_data = os.path.realpath(target_data)
            target_pkgdata = os.path.realpath(target_pkgdata)
            target_scripts = os.path.realpath(target_scripts)

            data_dir = target_pkgdata
            script_path = target_scripts

        print(("Root: %s" % self.root))
        print(("Prefix: %s\n" % self.prefix))

        print(("Target Data:    %s" % target_data))
        print(("Target PkgData: %s" % target_pkgdata))
        print(("Target Scripts: %s\n" % target_scripts))
        print(("Mugshot Data Directory: %s" % data_dir))

        values = {'__mugshot_data_directory__': "'%s'" % (data_dir),
                  '__version__': "'%s'" % self.distribution.get_version()}
        update_config(self.install_lib, values)

        desktop_file = get_desktop_file(self.root, target_data)
        print(("Desktop File: %s\n" % desktop_file))
        move_icon_file(self.root, target_data)
        update_desktop_file(desktop_file, script_path)


DistUtilsExtra.auto.setup(
    name='mugshot',
    version='0.4.1',
    license='GPL-3+',
    author='Sean Davis',
    author_email='smd.seandavis@gmail.com',
    description='lightweight user configuration utility',
    long_description='A lightweight user configuration utility. It allows you '
                     'to easily set profile image and user details for your '
                     'user profile and any supported applications.',
    url='https://launchpad.net/mugshot',
    data_files=[('share/man/man1', ['mugshot.1']),
                ('share/metainfo/', ['data/metainfo/mugshot.appdata.xml'])],
    cmdclass={'install': InstallAndUpdateDataDirectory}
)
