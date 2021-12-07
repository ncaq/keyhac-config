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


def check_func_emacs(window) -> bool:
    """
    check_func of ActivateWindowCommand argument.
    It is based on the Fakeymacs code `https://github.com/smzht/fakeymacs`
    """
    return window.getClassName() == "Emacs" or (
        window.getProcessName()
        in [
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
        and
        # ウィンドウのタイトルを検索する正規表現を指定する
        # Emacs を起動しているウィンドウを検索できるように、
        # Emacs の frame-title-format 変数を設定するなどして、識別できるようにする
        window.getText().startswith("Emacs ")
    )


def configure(keymap):
    keymap.clipboard_history.enableHook(False)

    keymap.editor = "code"

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont("HackGenNerd Console", 12)

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    keymap_global = keymap.defineWindowKeymap()
    keymap_global["W-Semicolon"] = "W-Up"
    keymap_global["W-q"] = "A-F4"

    keymap_global["W-h"] = keymap.ActivateWindowCommand(exe_name="firefox.exe")
    keymap_global["W-t"] = keymap.ActivateWindowCommand(exe_name="WindowsTerminal.exe")
    keymap_global["W-n"] = keymap.ActivateWindowCommand(check_func=check_func_emacs)
    keymap_global["W-Minus"] = keymap.ActivateWindowCommand(exe_name="slack.exe")
    keymap_global["W-b"] = keymap.ActivateWindowCommand(exe_name="KeePassXC.exe")
    keymap_global["W-m"] = keymap.ActivateWindowCommand(exe_name="thunderbird.exe")

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

    keymap_slack = keymap.defineWindowKeymap(exe_name="slack.exe")
    set_keymap_weblike(keymap, keymap_slack)
    keymap_slack["A-j"] = "A-S-Down"
    keymap_slack["A-k"] = "A-S-Up"
    keymap_slack["A-t"] = "A-Up"
    keymap_slack["A-n"] = "A-Down"
    keymap_slack["Enter"] = "C-Enter"
    keymap_slack["C-Comma"] = "29"  # 無変換
    keymap_slack["C-Period"] = "28"  # 変換
