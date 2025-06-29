﻿import itertools
import os
import sys
from enum import Enum
from pathlib import WindowsPath
from typing import Any, Callable, List, Optional, Tuple


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


keyhac_literal_special_source: List[Tuple[str, str]] = [
    ("[", "OpenBracket"),
    ("]", "CloseBracket"),
    ("\\", "BackSlash"),
    ("`", "BackQuote"),
    ("'", "Quote"),
    (",", "Comma"),
    (".", "Period"),
    ("/", "Slash"),
    ("-", "Minus"),
    ("+", "Plus"),
    (";", "Semicolon"),
]
""""文字のリテラル表現と、Keyhacの特殊なキー表現の対応リスト。"""


def keyhac_literal_special(literal: str) -> Optional[str]:
    """リテラル表現をKeyhacの表現に変換する。"""
    return next((t[1] for t in keyhac_literal_special_source if t[0] == literal), None)


def keyhac_special_literal(special: str) -> Optional[str]:
    """Keyhacの表現をリテラル表現に変換する。"""
    return next((t[0] for t in keyhac_literal_special_source if t[1] == special), None)


dvorak = "[]\\`',.pyfgcrl/+aoeuidhtns-;qjkxbmwvz"
"""
USキーボードでDvorakとQwertyで差分が生じそうなリストのDvorak。
Dvorak的には=と+は=をプレーンとするが、Keyhac的には+がプレーン。
"""

qwerty = "-+\\`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
"""USキーボードでDvorakとQwertyで差分が生じそうなリストのQWERTY。"""


def d2q(key: str) -> str:
    """
    Dvorak to Qwerty.
    """
    literal = keyhac_special_literal(key) or key
    try:
        fi = dvorak.index(literal)
        to = qwerty[fi]
        return keyhac_literal_special(to) or to
    except ValueError:
        return key


def q2d(key: str) -> str:
    """
    Qwerty to Dvorak.
    """
    literal = keyhac_special_literal(key) or key
    try:
        fi = qwerty.index(literal)
        to = dvorak[fi]
        return keyhac_literal_special(to) or to
    except ValueError:
        return key


process_name_of_linux: List[str] = [
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


def check_func_linux(window) -> bool:
    """WSLのプロセスらしいものを検出します。"""
    return window.getProcessName() in process_name_of_linux


def check_func_emacs(window) -> bool:
    """
    check_func of ActivateWindowCommand argument.
    It is based on the Fakeymacs code `https://github.com/smzht/fakeymacs`
    """
    return window.getClassName() == "Emacs" or (
        window.getProcessName() in process_name_of_linux
        and
        # ウィンドウのタイトルを検索する正規表現を指定する
        # Emacs を起動しているウィンドウを検索できるように、
        # Emacs の frame-title-format 変数を設定するなどして、識別できるようにする
        window.getText().startswith("emacs ")
    )


def set_keymap_dvorak_for_linux(_, keymap_window) -> None:
    """WSLg向けに全てDvorakに変換する。"""
    # "C-M-a"みたいなprefixを全て合成する。
    modifiers = ["S", "C", "A"]
    prefixs = [
        "-".join(c)
        for n in range(1, len(modifiers) + 1)
        for c in itertools.combinations(modifiers, n)
    ]
    for key in dvorak:
        f = keyhac_literal_special(key) or key
        t = q2d(key)
        # 単発のキー入力を変換する。
        keymap_window[f] = t
        # prefix付きのキー入力を変換する。
        for p in prefixs:
            keymap_window[p + "-" + f] = p + "-" + t


def set_keymap_weblike(keymap, keymap_window, for_linux=False) -> None:
    # Linux(WSLg)はDvorak設定を内部で行わないためキーを変換する必要がある。
    # 内部Windowsではそうではないため変換関数を分岐する。
    if for_linux:
        t = q2d
    else:
        # Pythonにはビルドインの恒等関数は無いのかな?
        t = lambda x: x

    keymap_window["C-y"] = "C-" + t("v")
    keymap_window["C-g"] = "Esc"
    keymap_window["C-Slash"] = "C-" + t("z")

    keymap_window["C-a"] = "Home"
    keymap_window["C-o"] = "C-" + t("t")
    keymap_window["A-o"] = "C-S-" + t("t")
    keymap_window["C-e"] = "End"
    keymap_window["C-u"] = ["Home", "S-End", "C-" + t("x"), "Delete"]

    keymap_window["C-d"] = "Delete"
    keymap_window["C-h"] = "Left"
    keymap_window["A-h"] = "C-Left"
    keymap_window["C-t"] = "Up"
    keymap_window["C-n"] = "Down"
    keymap_window["C-s"] = "Right"
    keymap_window["A-s"] = "C-Right"
    keymap_window["A-Minus"] = "C-S-" + t("t")

    keymap_window["C-q"] = "C-" + t("w")
    keymap_window["C-k"] = ["S-End", "C-" + t("x")]
    keymap_window["C-x"] = keymap.defineMultiStrokeKeymap("C-" + t("x"))
    keymap_window["C-x"]["C-g"] = "Esc"
    keymap_window["C-x"]["h"] = "C-" + t("a")
    keymap_window["C-b"] = "Back"
    keymap_window["A-b"] = "C-Back"
    keymap_window["C-m"] = "Enter"
    keymap_window["C-w"] = "C-" + t("x")
    keymap_window["A-w"] = "C-" + t("c")


def run_or_raise(
    keymap: Any,
    exe_name: Optional[str] = None,
    class_name: Optional[str] = None,
    window_text: Optional[str] = None,
    check_func: Optional[Callable[[Any], bool]] = None,
    force: bool = False,
    command: Optional[str] = None,
    param: Optional[str] = None,
) -> Callable[[], Any]:
    """
    XMonadの
    [runOrRaise](https://hackage.haskell.org/package/xmonad-contrib-0.17.1/docs/XMonad-Actions-WindowGo.html#v:runOrRaise)
    をKeyhacに移植する。
    既にプロセスやウィンドウが存在すればそれにフォーカスして、
    存在しなければ起動する。
    Keyhacの型情報を適切に参照するのが難しいため型定義に`Any`がしばしば入る。
    """

    def inner() -> Any:
        """機能を提供する関数を返す必要があるので内部で関数を生成する。"""
        isActive = keymap.ActivateWindowCommand(
            exe_name, class_name, window_text, check_func, force
        )()
        if isActive != None:
            # ウィンドウが見つかった場合一応その値を返す。
            return isActive
        else:
            # ウインドウが見つからなかった場合、起動する。
            com = command or exe_name
            if com == None:
                raise ValueError(f"command: {command}, exe_name: {exe_name}")
            keymap.ShellExecuteCommand(None, com, param, "", swmode="maximized")()
            return isActive

    return inner


def program_files(*pathsegments: str) -> WindowsPath:
    """`C:/Program Files/`以下を単純に参照します。"""
    # Keyhacが現状32bitで動いているため、64ビット版のディレクトリを指してくれるように指定します。
    return WindowsPath(os.environ["ProgramW6432"], *pathsegments)


def start_menu_programs(*pathsegments: str) -> WindowsPath:
    """
    典型的には、
    `C:/Users/ユーザ名/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/`
    以下を参照します。
    """
    roaming = os.environ["APPDATA"]
    return WindowsPath(
        roaming, "Microsoft", "Windows", "Start Menu", "Programs", *pathsegments
    )


def configure_windows(keymap) -> None:
    keymap.clipboard_history.enableHook(False)

    keymap_global = keymap.defineWindowKeymap()
    # W-qで大抵のウィンドウを閉じれるようにします。
    keymap_global["W-q"] = "A-F4"
    # ウィンドウ最大化を簡単に行えるようにします。
    keymap_global["W-Semicolon"] = "W-Up"
    # アクションセンターではなく通知を開きます。
    keymap_global["W-a"] = "W-n"

    keymap_global["W-d"] = run_or_raise(
        keymap,
        exe_name="Discord.exe",
        command=str(start_menu_programs("Discord Inc", "Discord.lnk")),
    )
    keymap_global["W-h"] = run_or_raise(
        keymap,
        exe_name="firefox.exe",
        command=str(program_files("Mozilla Firefox", "firefox.exe")),
    )
    keymap_global["W-t"] = run_or_raise(
        keymap, exe_name="WindowsTerminal.exe", command="wt.exe"
    )
    keymap_global["W-n"] = run_or_raise(
        keymap,
        check_func=check_func_emacs,
        command=str(program_files("WSL", "wslg.exe")),
        param="--cd ~ -d NixOS -- emacs",
    )
    keymap_global["W-s"] = run_or_raise(keymap, exe_name="slack.exe")
    keymap_global["W-c"] = run_or_raise(
        keymap,
        exe_name="claude.exe",
        command=str(start_menu_programs("Anthropic", "Claude.lnk")),
    )
    keymap_global["W-b"] = run_or_raise(
        keymap,
        exe_name="KeePassXC.exe",
        command=str(program_files("KeePassXC", "KeePassXC.exe")),
    )
    keymap_global["W-m"] = run_or_raise(
        keymap,
        exe_name="thunderbird.exe",
        command=str(program_files("Mozilla Thunderbird", "thunderbird.exe")),
    )
    keymap_global["W-z"] = run_or_raise(
        keymap,
        exe_name=str(
            WindowsPath(
                os.environ["LOCALAPPDATA"],
                "Programs",
                "youtube-music",
                "YouTube Music.exe",
            )
        ),
    )

    set_keymap_dvorak_for_linux(
        keymap, keymap.defineWindowKeymap(check_func=check_func_linux)
    )

    keymap_discord = keymap.defineWindowKeymap(exe_name="Discord.exe")
    set_keymap_weblike(keymap, keymap_discord)
    keymap_discord["A-j"] = "A-S-Down"
    keymap_discord["A-k"] = "A-S-Up"
    keymap_discord["A-t"] = "A-Up"
    keymap_discord["A-n"] = "A-Down"
    keymap_discord["C-m"] = "S-Enter"
    keymap_discord["C-Comma"] = "29"  # 無変換
    keymap_discord["C-Period"] = "28"  # 変換

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

    # WindowsネイティブのEmacsのみを探索する。
    keymap_emacs = keymap.defineWindowKeymap(exe_name="emacs.exe")
    keymap_emacs["C-m"] = "Enter"

    set_keymap_weblike(keymap, keymap.defineWindowKeymap(exe_name="chrome.exe"))

    keymap_slack = keymap.defineWindowKeymap(exe_name="slack.exe")
    set_keymap_weblike(keymap, keymap_slack)
    keymap_slack["A-j"] = "A-S-Down"
    keymap_slack["A-k"] = "A-S-Up"
    keymap_slack["A-t"] = "A-Up"
    keymap_slack["A-n"] = "A-Down"
    keymap_slack["Enter"] = "C-Enter"
    keymap_slack["C-Comma"] = "29"  # 無変換
    keymap_slack["C-Period"] = "28"  # 変換

    keymap_claude = keymap.defineWindowKeymap(exe_name="claude.exe")
    set_keymap_weblike(keymap, keymap_claude)
    keymap_claude["C-o"] = "C-k"  # 新規チャット
    keymap_claude["C-m"] = "S-Enter"
    keymap_claude["Enter"] = "C-Enter"
    keymap_claude["C-Comma"] = "29"  # 無変換
    keymap_claude["C-Period"] = "28"  # 変換

    set_keymap_weblike(keymap, keymap.defineWindowKeymap(exe_name="YouTube Music.exe"))

    keymap_lm_studio = keymap.defineWindowKeymap(exe_name="LM Studio.exe")
    set_keymap_weblike(keymap, keymap_lm_studio)
    keymap_lm_studio["C-o"] = "C-n"  # 新規チャット
    keymap_lm_studio["C-m"] = "S-Enter"
    keymap_lm_studio["Enter"] = "C-Enter"
    keymap_lm_studio["C-Comma"] = "29"  # 無変換
    keymap_lm_studio["C-Period"] = "28"  # 変換

    set_keymap_weblike(keymap, keymap.defineWindowKeymap(exe_name="Code.exe"))


def configure(keymap) -> None:
    keymap.setTheme("black")
    configure_windows(keymap)
