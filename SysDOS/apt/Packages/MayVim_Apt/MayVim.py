# -*- coding: utf-8 -*-
"""
Create on Mon Mar 11 19:32:25 2024
@author: fangg
"""
import os
import random

class MayVim:
    def __init__(self):
        self.lines = []
        self.is_saved = True
        self.current_line = 0
        self.insert_mode = False
        self.filename = ""

    def start(self):
        # 帮助文件的读取
        with open(os.path.dirname(__file__) + "\\Welcome.dat", "r") as welcome:
            readlines = welcome.readlines()
            for line in range(6):
                print(readlines[line], end='')
            rand_num = random.randint(1, 3)
            print(readlines[5 + rand_num], end='')
            for i in range(10, len(readlines)):
                print(readlines[i])
        while True:
            self.display()
            command = input(":")
            self.execute_command(command)

    def display(self):
        for i, line in enumerate(self.lines):
            prefix = ": " if i == self.current_line else "   "
            print(f"{prefix}{line}")

    def open_file(self):
        try:
            filename = input("请输入打开的文件名: ")
            self.filename = filename
            with open(self.filename, "r") as file:
                self.lines = file.readlines()
            self.current_line = len(self.lines) - 1
            for i in self.lines:
                print(i, end='')
            while True:
                self.display()
                while True:
                    command = input(":")
                    self.execute_command(command)
        except FileNotFoundError:
            print("没有找到该文件！")

    def execute_command(self, command):
        if command == "i":
            self.insert_mode = True
            self.insert_text()
        elif command == "w":
            self.save_file()
        elif command == "q":
            if self.is_saved:
                quit()
            else:
                print("No saved file!")
        elif command == "q!":
            sure = input("你确定吗？ (y/n): ")
            if sure == "y":
                quit()
        elif command == "j":
            self.move_cursor_down()
        elif command == "k":
            self.move_cursor_up()
        elif command == "x":
            self.save_file()
            quit()
        elif command == "o":
            self.open_file(self.filename)
        elif command == "help iccf":
            self.help_iccf()
        elif command == "help unicef":
            self.help_unicef()

    def insert_text(self):
        self.is_saved = False
        while True:
            line = input()
            if line == ".":
                self.insert_mode = False
                self.current_line -= 1
                break
            self.lines.insert(self.current_line, line)
            self.current_line += 1

    def save_file(self):
        if self.filename == "":
            self.filename = input("输入文件名（带后缀）来保存：")
        if self.lines[0] == "#! ShellFile" and not self.filename.endswith(".sh"):
            self.filename = self.filename + ".sh"
        with open(self.filename, "w") as f:
            for i in self.lines:
                f.write(i + "\n")
        self.is_saved = True

    def move_cursor_down(self):
        if self.current_line < len(self.lines) - 1:
            self.current_line += 1

    def move_cursor_up(self):
        if self.current_line > 0:
            self.current_line -= 1

    def delete(self, length):
        try:
            self.lines[self.current_line] = self.lines[self.current_line][:len(self.lines[self.current_line]) - length]
            self.move_cursor_down()
        except IndexError:
            print("无法删除！d 命令只能删除一行内的数据！")

    def help_iccf(self):
        print("\x1b[1mShe is waiting for your help!\x1b[0m\n\
The south of Uganda has been suffering from the highest HIV infection rate in the world. \n\
Parents die of AIDS, just when their children need them most. An extended family can be their new home. \n\
Fortunately there is enough food in this farming district. \n\
But who will pay their school fees, provide medical aid and help them grow up? \n\
That is where ICCF Holland helps in the hope that they will be able to take care of themselves, \n\
and their children, in the long run.")
        print("https://www.iccf.nl/index.html")

    def help_unicef(self):
        print("每月支持计划\n参加“爱心为儿童”计划，您的每月持续支持，能帮助改变更多孩子的命运！")
        print("https://www.unicef.cn/take-action/donate-monthly")

if __name__ == '__main__':
    may_vim = MayVim()
    may_vim.start()