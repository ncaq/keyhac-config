import sys
import os
import datetime

import pyauto
from keyhac import *


def configure(keymap):
    keymap.editor = "emacsclient.exe"

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont("MS Gothic", 12)

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    keymap_global = keymap.defineWindowKeymap()

    # Clipboard history related
    # Open the clipboard history list
    keymap_global["W-z"] = keymap.command_ClipboardList

    activateFirefox = keymap.ActivateWindowCommand(exe_name="firefox.exe")
    keymap_global["W-h"] = activateFirefox
    activateTermnial = keymap.ActivateWindowCommand(exe_name="mintty.exe")
    keymap_global["W-t"] = activateTermnial
    activateEmacs = keymap.ActivateWindowCommand(exe_name="emacs.exe")
    keymap_global["W-n"] = activateEmacs

    keymap_firefox = keymap.defineWindowKeymap(
        exe_name="firefox.exe", class_name="MozillaWindowClass")

    keymap_firefox["C-g"] = "Esc"
    keymap_firefox["C-Slash"] = "C-z"

    keymap_firefox["C-a"] = "Home"
    keymap_firefox["C-o"] = "C-t"
    keymap_firefox["A-o"] = "C-S-t"
    keymap_firefox["C-e"] = "End"
    keymap_firefox["C-u"] = ["Home", "S-End", "C-x"]

    keymap_firefox["C-d"] = "Delete"
    keymap_firefox["C-h"] = "Left"
    keymap_firefox["A-h"] = "C-Left"
    keymap_firefox["C-t"] = "Up"
    keymap_firefox["C-n"] = "Down"
    keymap_firefox["C-s"] = "Right"
    keymap_firefox["A-s"] = "C-Right"

    keymap_firefox["C-q"] = "C-w"
    keymap_firefox["C-k"] = ["S-End", "C-x"]
    keymap_firefox["C-x"] = keymap.defineMultiStrokeKeymap("C-X")
    keymap_firefox["C-x"]["C-g"] = "Esc"
    keymap_firefox["C-x"]["C-h"] = "C-a"
    keymap_firefox["C-b"] = "Back"
    keymap_firefox["A-b"] = "C-Back"
    keymap_firefox["C-m"] = "Enter"
    keymap_firefox["C-w"] = "C-x"
    keymap_firefox["A-w"] = "C-c"
