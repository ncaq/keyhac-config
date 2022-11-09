import sys
import itertools
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

# 文字のリテラル表現と、Keyhacの特殊なキー表現の対応リスト。
keyhac_literal_special_source = [
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


def keyhac_literal_special(literal: str):
    """リテラル表現をKeyhacの表現に変換する。"""
    return next((t[1] for t in keyhac_literal_special_source if t[0] == literal), None)


def keyhac_special_literal(special: str):
    """Keyhacの表現をリテラル表現に変換する。"""
    return next((t[0] for t in keyhac_literal_special_source if t[1] == special), None)


# USキーボードでDvorakとQwertyで差分が生じそうなリスト。
# リテラル表現。
# Dvorak的には=と+は=をプレーンとするが、Keyhac的には+がプレーン。
dvorak = "[]\\`',.pyfgcrl/+aoeuidhtns-;qjkxbmwvz"
qwerty = "-+\\`qwertyuiop[]asdfghjkl;'zxcvbnm,./"


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


process_name_of_linux = [
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


def check_func_mikutter(window) -> bool:
    """WSLのmikutterを検出します。Windowsネイティブでmikutterを動かせたことがないのでネイティブには対応していません。"""
    return (
        window.getProcessName() in process_name_of_linux
        # `mikutter`や`mikutter (Ubuntu)`が存在する。
        and window.getText().startswith("mikutter")
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
    keymap_window["C-x"]["C-h"] = "C-" + t("a")
    keymap_window["C-b"] = "Back"
    keymap_window["A-b"] = "C-Back"
    keymap_window["C-m"] = "Enter"
    keymap_window["C-w"] = "C-" + t("x")
    keymap_window["A-w"] = "C-" + t("c")


def configure_windows(keymap) -> None:
    keymap.clipboard_history.enableHook(False)

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

    keymap_linux = keymap.defineWindowKeymap(check_func=check_func_linux)
    set_keymap_dvorak_for_linux(keymap, keymap_linux)

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

    keymap_mikutter = keymap.defineWindowKeymap(check_func=check_func_mikutter)
    set_keymap_weblike(keymap, keymap_mikutter, True)
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


def configure_mac(keymap) -> None:
    keymap_global = keymap.defineWindowKeymap()

    # グローバルな範囲でかな漢字変換のキーバインドを設定してしまう。
    # MacではゲームしないのでSlackだけでなくグローバルでやっても気にならない。
    # またEmacsなどでキャプチャ出来ないのでグローバルで行う必要がある。
    keymap_global["Ctrl-" + d2q("Comma")] = "102"  # 英数
    keymap_global["Ctrl-" + d2q("Period")] = "104"  # かな


def configure(keymap) -> None:
    keymap.setTheme("black")

    if current_platform == Platform.WINDOWS:
        configure_windows(keymap)
    elif current_platform == Platform.MAC:
        configure_mac(keymap)
