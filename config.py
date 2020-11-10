import sys
import os
import datetime

import pyauto
from keyhac import *

def set_keymap_weblike(keymap, keymap_window):
    keymap_window["C-y"] = "C-v"
    keymap_window["C-g"] = "Esc"
    keymap_window["C-Slash"] = "C-z"

    keymap_window["C-a"] = "Home"
    keymap_window["C-o"] = "C-t"
    keymap_window["A-o"] = "C-S-t"
    keymap_window["C-e"] = "End"
    keymap_window["C-u"] = ["Home", "S-End", "C-x"]

    keymap_window["C-d"] = "Delete"
    keymap_window["C-h"] = "Left"
    keymap_window["A-h"] = "C-Left"
    keymap_window["C-t"] = "Up"
    keymap_window["C-n"] = "Down"
    keymap_window["C-s"] = "Right"
    keymap_window["A-s"] = "C-Right"

    keymap_window["C-q"] = "C-w"
    keymap_window["C-k"] = ["S-End", "C-x"]
    keymap_window["C-x"] = keymap.defineMultiStrokeKeymap("C-X")
    keymap_window["C-x"]["C-g"] = "Esc"
    keymap_window["C-x"]["C-h"] = "C-a"
    keymap_window["C-b"] = "Back"
    keymap_window["A-b"] = "C-Back"
    keymap_window["C-m"] = "Enter"
    keymap_window["C-w"] = "C-x"
    keymap_window["A-w"] = "C-c"

def configure(keymap):
    keymap.editor = "emacsclient.exe"

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont("HackGenNerd", 12)

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    keymap_global = keymap.defineWindowKeymap()
    keymap_global["W-q"] = "A-F4"
    keymap_global["W-z"] = keymap.command_ClipboardList

    keymap_global["W-h"] = keymap.ActivateWindowCommand(exe_name="firefox.exe")
    keymap_global["W-t"] = keymap.ActivateWindowCommand(exe_name="WindowsTerminal.exe")
    keymap_global["W-n"] = keymap.ActivateWindowCommand(exe_name="emacs.exe")
    keymap_global["W-Minus"] = keymap.ActivateWindowCommand(exe_name="slack.exe")
    keymap_global["W-b"] = keymap.ActivateWindowCommand(exe_name="KeePassXC.exe")

    set_keymap_weblike(keymap, keymap.defineWindowKeymap(
        exe_name="firefox.exe", class_name="MozillaWindowClass"))
    set_keymap_weblike(keymap, keymap.defineWindowKeymap(
        exe_name="thunderbird.exe", class_name="MozillaWindowClass"))

    keymap_emacs = keymap.defineWindowKeymap(exe_name="emacs.exe")
    keymap_emacs["C-m"] = "Enter"

    keymap_slack = keymap.defineWindowKeymap(exe_name="slack.exe")
    set_keymap_weblike(keymap, keymap_slack)
    keymap_slack["A-n"] = "A-S-Down"
    keymap_slack["A-t"] = "A-S-Up"
    keymap_slack["A-j"] = "A-Down"
    keymap_slack["A-k"] = "A-Up"
    keymap_slack["Enter"] = "C-Enter"
