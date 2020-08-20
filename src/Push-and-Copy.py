#!/usr/bin/env python3

from tkinter import Tk, Listbox, StringVar
from tkinter import ttk
import tkinter.font as tkFont
import pyperclip
import os
import sys


# returns Tuple of (isValidArgument, errMessage)
def checkArgsValidity(args):
    if len(args) <= 0:
        return (
            False,
            "[Error] Please give command line args one or more.\n"
            + "Usage: Push-and-Copy.py filepath1 [filepath]...",
        )

    for path in args:
        if os.path.isdir(path):
            return (False, "[Error] '" + path + "' : Not a file. It is directory.")

        if not os.path.exists(path):
            return (False, "[Error] '" + path + "' : No such file.")

    return (True, "")


# returns all contents of file as str type.
def readAll(path):
    f = open(path, mode="r")
    contents = f.read()
    f.close()
    return contents


def main(args):
    # コマンドライン引数のファイルパスのバリデーション
    isValidArgument, errMessage = checkArgsValidity(args)

    if not isValidArgument:
        print(errMessage, file=sys.stderr)
        sys.exit(1)

    filepaths = args
    basenames = list(map(os.path.basename, filepaths))
    longestBasename = max(map(len, basenames))

    # Root
    root = Tk()
    root.title("Push and Copy")

    # Frame; styleがよくわかってないけど白くできたのでヨシ！
    style = ttk.Style()
    style.configure("BW.TLabel", background="white")
    frame = ttk.Frame(root, padding=20, style="BW.TLabel")

    # 使い方のラベル
    usageLabel = ttk.Label(
        frame,
        text="Selecting the filename, the file contents will be copied to clipboard.",
        font=tkFont.Font(family="monospace", size=11),
        background="white",
        padding=(0, 20),
    )

    # コピーしたことをフィードバックするためのラベル
    labelText = StringVar()
    label = ttk.Label(
        frame,
        textvariable=labelText,
        font=tkFont.Font(family="monospace", size=14),
        background="white",
        padding=16,
    )

    # コマンドライン引数のファイルパス群をリスト表示する Listbox
    pathListbox = Listbox(
        frame,
        listvariable=StringVar(value=basenames),
        selectmode="single",
        font=tkFont.Font(family="monospace", size=28),
        cursor="hand1",
        selectbackground="#acdcff",
        bg="#fcfcfc",
        fg="#505050",
        activestyle="none",
        height=len(basenames),
        width=max(longestBasename + 2, 16),
    )

    # pathListbox でアイテム選択イベント発火時に実行する処理
    # 選択されたファイルパスのファイル内容をクリップボードにコピーする
    def selectedAction(event):
        idx = pathListbox.curselection()[0]
        path = args[idx]
        pyperclip.copy(readAll(path))
        labelText.set("Copied " + path + " !")
        pass

    # イベント発火時の処理登録
    pathListbox.bind("<<ListboxSelect>>", selectedAction)

    frame.pack()
    usageLabel.pack()
    pathListbox.pack()
    label.pack()

    root.mainloop()
    pass


if __name__ == "__main__":
    args = sys.argv
    main(args[1:])
