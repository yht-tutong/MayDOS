# -*- coding: utf-8 -*-
""""
Create on Fri Mar 15 17:33:07 2024
@author: fangg
"""
import os
import json
import sys
import shutil

sys.path.append(os.path.split(sys.path[0])[0])
import SysDOS.Bin.SysLib as syslib


class Apt:

    def __init__(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.apt_list = os.listdir(self.current_path + "\\Packages")
        self.info_list = []
        self.commands = {}
        for package in self.apt_list:
            if package.endswith("_Apt"):
                with open(self.current_path + "\\Packages\\" + package + '\\AptInfo.json', 'r',
                      encoding="utf-8") as apt_info:
                    self.info_list.append(json.loads(apt_info.read()))
        self.update_commands()

    def update(self) -> None:
        self.info_list.clear()
        for package in self.apt_list:
            with open(self.current_path + "\\Packages\\" + package + '\\AptInfo.json', 'r',
                      encoding="utf-8") as update_info:
                self.info_list.append(json.loads(update_info.read()))

    def output_list(self) -> None:
        print(f"=======Package Name======={syslib.Font.BLUE}|{syslib.Style.END}"
              f"====Category===={syslib.Font.BLUE}|{syslib.Style.END}"
              f"=====Owner====={syslib.Font.BLUE}|{syslib.Style.END}"
              f"===Version==={syslib.Font.BLUE}|{syslib.Style.END}"
              f"===Edition==={syslib.Font.BLUE}|{syslib.Style.END}")
        for info in range(len(self.info_list)):
            if len(self.info_list[info]['package_name']) > 26:
                print(self.info_list[info]['package_name'][:23] + f"...{syslib.Font.BLUE}|{syslib.Style.END}", end="")
            else:
                print(self.info_list[info]['package_name'] + (" " * (26 - len(self.info_list[info]['package_name']))) +
                      f'{syslib.Font.BLUE}|{syslib.Style.END}', end="")
            # 输出包名，太长省略

            if len(self.info_list[info]['category']) > 16:
                print(self.info_list[info]['category'][:13] + f"...{syslib.Font.BLUE}|{syslib.Style.END}", end="")
            else:
                print(self.info_list[info]['category'] + (" " * (16 - len(self.info_list[info]['category']))) +
                      f'{syslib.Font.BLUE}|{syslib.Style.END}', end="")

            if len(self.info_list[info]['owner']) > 15:
                print(self.info_list[info]['owner'][:12] + f"...{syslib.Font.BLUE}|{syslib.Style.END}", end="")
            else:
                print(self.info_list[info]['owner'] + (" " * (15 - len(self.info_list[info]['owner']))) +
                      f'{syslib.Font.BLUE}|{syslib.Style.END}', end="")

            if len(self.info_list[info]['version']) > 13:
                print(self.info_list[info]['version'][:10] + f"...{syslib.Font.BLUE}|{syslib.Style.END}", end="")
            else:
                print(self.info_list[info]['version'] + (" " * (13 - len(self.info_list[info]['version']))) +
                      f'{syslib.Font.BLUE}|{syslib.Style.END}', end="")

            if len(self.info_list[info]['edition']) > 13:
                print(self.info_list[info]['edition'][:10] + f"...{syslib.Font.BLUE}|{syslib.Style.END}")
            else:
                print(self.info_list[info]['edition'] + (" " * (13 - len(self.info_list[info]['edition']))) +
                      f'{syslib.Font.BLUE}|{syslib.Style.END}')

    def start_program(self, programs_name: str) -> bool:
        if programs_name + "_Apt" in self.apt_list:
            result = os.system("python \"" + os.path.dirname(__file__) + "\\Packages\\" +
                    programs_name + "_Apt\\" + self.info_list[self.apt_list.index(programs_name + "_Apt")]["init_file"])
            if result != 0:
                print("错误：未知错误！错误信息：")
            return True
        else:
            return False

    def add_file(self, wd, path: str) -> None:
        abspath = os.path.abspath(path)
        os.chdir(wd)
        shutil.copy(abspath, self.current_path + os.path.sep + "Packages")

    def help(self) -> None:
        print("\x1b[0m", end="")
        with open(self.current_path + "\\helpinfo.txt", 'r', encoding="utf-8") as help_file:
            help_list = help_file.readlines()
        for i in help_list:
            print(i, end="")
        print("\n\n\x1b[43m\x1b[30m\x1b[1m本 apt 有着超级牛力！\x1b[0m")

    def update_commands(self):
        try:
            for info in range(len(self.info_list)):
                if self.info_list[info]['command'] != "no_command":
                    self.commands[self.apt_list[info]] = self.info_list[info]['command']
                else:
                    # 六十个字符
                    self.commands[self.apt_list[info]] = "1234567980123456789012345678901234567890123456789012345678901"
        except:
            print(syslib.Font.RED + f"错误：发现了不合 MayDOS 软件开发必读手册 的软件:{self.apt_list[info]}。" + syslib.Style.END)

    def run_command(self, command: str) -> bool:
        for i in self.commands.keys():
            if self.commands[i] == command:
                self.start_program(i[:-4])
                return True
        return False



