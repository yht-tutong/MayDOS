import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import base64
import os

current_path = os.path.abspath(os.getcwd())

messagebox.showinfo("使用说明", "Notepad_GUI 0.1\n保存文件时需要手动输入文件扩展名，此漏洞将在下一个版本修复！")

ver = "Notepad_GUI 0.1"
info = "\n当前功能暂未实现。\n但是你可以在Bilibili上关注Minecraft_2v以了解更新进度。\n或添加作者QQ：2306925195以了解更新进度。"

def add_commands(self, commands: dict, separators: list):
    """
    在 Menu 中添加一组的 command。
    参数：
    self: Tk.Menu
    commands: dict
    separators: list
    其中 commands 表示要添加的 command，
    separators 表示要在哪些 command（从 0 开始）后添加 separator。
    """
    k = 0
    for i in commands.keys():
        self.add_command(label=i, command=commands[i])
        if k in separators:
            self.add_separator()
        k += 1

def version():
    messagebox.showinfo("关于", "Notepad_GUI 0.1\n作者：MayDOS Team")


def use_book():
    messagebox.showinfo("使用说明", "Notepad_GUI 0.1\n保存文件时需要手动输入文件扩展名，此漏洞将在下一个版本修复！")


def new_file():
    text.delete("1.0", tk.END)
    root.title("Notepad_GUI")


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("MayDOS专有格式", "*.MayNote"), ("文本文档", "*.txt"), ("全部文件", "*.*")])
    if file_path:
        try:
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    text.delete("1.0", tk.END)
                    text.insert("1.0", file.read())
                    root.title(f"Notepad_GUI - {file_path}")
            elif file_path.endswith(".MayNote"):
                with open(file_path, "r", encoding="utf-8") as file:
                    encoded_content = file.read()
                    decoded_content = base64.b64decode(encoded_content).decode("utf-8")
                    text.delete("1.0", tk.END)
                    text.insert("1.0", decoded_content)
                    root.title(f"Notepad_GUI - {file_path}")
        except Exception as e:
            messagebox.showerror("打开文件错误", f"无法打开文件：{str(e)}")


def save_file():
    file_path = filedialog.asksaveasfilename(
        filetypes=[("MayDOS专有格式", "*.MayNote"), ("文本文档", "*.txt"), ("全部文件", "*.*")])
    if file_path:
        try:
            if file_path.endswith(".txt"):
                if not file_path.endswith(".txt"):
                    file_path += ".txt"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text.get("1.0", tk.END))
                    root.title(f"Notepad_GUI - {file_path}")
            elif file_path.endswith(".MayNote"):
                encoded_content = base64.b64encode(text.get("1.0", tk.END).encode("utf-8")).decode("utf-8")
                if not file_path.endswith(".MayNote"):
                    file_path += ".MayNote"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(encoded_content)
                    root.title(f"Notepad_GUI - {file_path}")
        except Exception as e:
            messagebox.showerror("保存文件错误", f"无法保存文件：{str(e)}")


def cut():
    text.event_generate("<<Cut>>")


def copy():
    text.event_generate("<<Copy>>")


def paste():
    text.event_generate("<<Paste>>")


def undo():
    try:
        text.edit_undo()
    except tk.TclError:
        pass


def redo():
    try:
        text.edit_redo()
    except tk.TclError:
        pass


def check_update():
    messagebox.showinfo("检查更新", "当前版本为：" + ver + info)


def open_url():
    webbrowser.open("https://space.bilibili.com/3493262897711201")
    messagebox.showinfo("关注作者", "已经打开Bilibili并关注该作者")


def team_member_command():
    team_member = ['姗姗来迟的晚霞',
                   '是螺螺呀',
                   '图佟15',
                   '小严awa',
                   '御坂10032号',
                   '账号已封禁',
                   'Fang-Omega',
                   'bil_fis',
                   'Jincheng(BUID:3493124978510331)',
                   'creeper',
                   'HOW ARE YOU',
                   'kddddddde',
                   '苦麒麟kuqilin',
                   '乐乐',
                   'Mr_xiaoliu',
                   'rRichard',
                   '有点坏儿bitbad']

    messagebox.showinfo("Note", "此名字均为QQ昵称。\n此显示顺序没有特殊排序，遵循QQ上显示的顺序")

    for mem in team_member:
        messagebox.showinfo("团队成员", "我们的团队成员有：" + mem)


root = tk.Tk()
root.title("Notepad_GUI")

text = tk.Text(root, wrap="word", font=("Arial", 10, "normal"))
text.pack(expand=True, fill="both")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="文件", menu=file_menu)
file_menu_commands = {"新建": new_file, "打开": open_file, "保存": save_file, "退出": root.quit}
add_commands(file_menu, file_menu_commands, [2])

edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="编辑", menu=edit_menu)
edit_menu_commands = {"剪切": cut, "复制": copy, "粘贴": paste, "撤销": undo, "重做": redo}
add_commands(edit_menu, edit_menu_commands, [2])

program_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="应用程序", menu=program_menu)
program_menu_commands = {"Help/使用提示": use_book, "检查更新": check_update, "在Bilibili上关注作者": open_url, "关于": version}
add_commands(program_menu, program_menu_commands, [0, 1, 2])

team_member_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="开发者", menu=team_member_menu)
team_member_menu_commands = {"关于团队": team_member_command}
add_commands(team_member_menu, team_member_menu_commands, [])

root.mainloop()
