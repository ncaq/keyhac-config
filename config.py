from typing import List
import sys
from enum import Enum


class Platform(Enum):
    """The platform for support of Keyhac."""

    WINDOWS = "windows"
    MAC = "mac"


def detect_platform_of_keyhac() -> Platform:
    if sys.platform == "win32":
        return Platform.WINDOWS
    elif sys.platform == "darwin":
        return Platform.MAC

    raise ValueError(sys.platform)


current_platform = detect_platform_of_keyhac()


def set_keymap_weblike(keymap, keymap_window) -> None:
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
    keymap_window["A-Minus"] = "C-S-t"

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


process_name_of_x11_server: List[str] = [
    "mstsc.exe",  # WSLg
    "msrdc.exe",  # WSLg
    "XWin.exe",  # Cygwin/X
    "XWin_MobaX.exe",  # MobaXterm/X
    "XWin_MobaX_1.16.3.exe",  # MobaXterm/X
    "XWin_Cygwin_1.14.5.exe",  # MobaXterm/X
    "XWin_Cygwin_1.16.3.exe",  # MobaXterm/X
    "Xming.exe",  # Xming
    "vcxsrv.exe",  # VcXsrv
    "GWSL_vcxsrv.exe",  # GWSL
    "GWSL_vcxsrv_lowdpi.exe",  # GWSL
    "X410.exe",  # X410
    "Xpra-Launcher.exe",  # Xpra
]


def check_func_emacs(window) -> bool:
    """
    check_func of ActivateWindowCommand argument.
    It is based on the Fakeymacs code `https://github.com/smzht/fakeymacs`
    """
    return window.getClassName() == "Emacs" or (
        window.getProcessName() in process_name_of_x11_server
        and
        # ウィンドウのタイトルを検索する正規表現を指定する
        # Emacs を起動しているウィンドウを検索できるように、
        # Emacs の frame-title-format 変数を設定するなどして、識別できるようにする
        window.getText().startswith("emacs ")
    )


def check_func_mikutter(window) -> bool:
    """WSLのmikutterを検出します。Windowsネイティブでmikutterを動かせたことがないのでネイティブには対応していません。"""
    return (
        window.getProcessName() in process_name_of_x11_server
        and window.getText() == "mikutter"
    )


def configure(keymap) -> None:
    keymap.clipboard_history.enableHook(False)

    keymap.editor = "code"

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont("HackGen Console NFJ", 12)

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    keymap_global = keymap.defineWindowKeymap()
    keymap_global["W-Semicolon"] = "W-Up"
    keymap_global["W-q"] = "A-F4"

    keymap_global["W-h"] = keymap.ActivateWindowCommand(exe_name="firefox.exe")
    keymap_global["W-t"] = keymap.ActivateWindowCommand(exe_name="WindowsTerminal.exe")
    keymap_global["W-n"] = keymap.ActivateWindowCommand(check_func=check_func_emacs)
    keymap_global["W-s"] = keymap.ActivateWindowCommand(check_func=check_func_mikutter)
    keymap_global["W-Minus"] = keymap.ActivateWindowCommand(exe_name="slack.exe")
    keymap_global["W-b"] = keymap.ActivateWindowCommand(exe_name="KeePassXC.exe")
    keymap_global["W-m"] = keymap.ActivateWindowCommand(exe_name="thunderbird.exe")
    keymap_global["W-z"] = keymap.ActivateWindowCommand(exe_name="Amazon Music.exe")

    set_keymap_weblike(
        keymap,
        keymap.defineWindowKeymap(
            exe_name="firefox.exe", class_name="MozillaWindowClass"
        ),
    )
    set_keymap_weblike(
        keymap,
        keymap.defineWindowKeymap(
            exe_name="thunderbird.exe", class_name="MozillaWindowClass"
        ),
    )

    keymap_emacs = keymap.defineWindowKeymap(exe_name="emacs.exe")
    keymap_emacs["C-m"] = "Enter"

    set_keymap_weblike(keymap, keymap.defineWindowKeymap(exe_name="chrome.exe"))

    keymap_mikutter = keymap.defineWindowKeymap(check_func=check_func_mikutter)
    set_keymap_weblike(keymap, keymap_mikutter)
    keymap_mikutter["C-m"] = "S-Enter"

    keymap_slack = keymap.defineWindowKeymap(exe_name="slack.exe")
    set_keymap_weblike(keymap, keymap_slack)
    keymap_slack["A-j"] = "A-S-Down"
    keymap_slack["A-k"] = "A-S-Up"
    keymap_slack["A-t"] = "A-Up"
    keymap_slack["A-n"] = "A-Down"
    keymap_slack["Enter"] = "C-Enter"
    keymap_slack["C-Comma"] = "29"  # 無変換
    keymap_slack["C-Period"] = "28"  # 変換

    set_keymap_weblike(keymap, keymap.defineWindowKeymap(exe_name="Amazon Music.exe"))
