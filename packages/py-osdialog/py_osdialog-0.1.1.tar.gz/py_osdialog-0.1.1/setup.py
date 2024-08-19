#!/usr/bin/env python3
# The MIT License (MIT)
#
# Copyright (c) 2024 George Watson
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from setuptools import setup, Extension
import platform
import subprocess

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def pydialog_extension():
    p = platform.system()
    if p == "Darwin":
        return Extension("pydialog",
                         sources=["pydialog.c", "osdialog.c", "osdialog_mac.m"],
                         extra_link_args=["-framework", "Cocoa"])
    elif p == "Windows":
        return Extension("pydialog",
                         sources=["pydialog.c", "osdialog.c", "osdialog_win.c"],
                         libraries=["comdlg32", "user32", "shell32", "advapi32", "shlwapi", "ucrt"])
    else:
        # Assume Linux and check for GTK version
        try:
            gtk_version = subprocess.check_output(["pkg-config", "--modversion", "gtk+-2.0"]).decode('utf-8').strip()
            return Extension("pydialog",
                             sources=["pydialog.c", "osdialog.c", "osdialog_gtk2.c"],
                             libraries=["gtk-2.0"])
        except subprocess.CalledProcessError:
            try:
                gtk_version = subprocess.check_output(["pkg-config", "--modversion", "gtk+-3.0"]).decode('utf-8').strip()
                return Extension("pydialog",
                                 sources=["pydialog.c", "osdialog.c", "osdialog_gtk3.c"],
                                 libraries=["gtk-3.0"])
            except subprocess.CalledProcessError:
                return Extension("pydialog",
                                 sources=["pydialog.c", "osdialog.c", "osdialog_zenity.c"])

setup(
    name="pydialog",
    version="0.1.1",
    author="George Watson",
    author_email="gigolo@hotmail.co.uk",
    description="Python bindings for osdialog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takeiteasy/pydialog",
    include_dirs="/Users/george/git/pydialog",
    ext_modules=[pydialog_extension()],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)