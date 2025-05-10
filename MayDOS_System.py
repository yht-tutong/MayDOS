# 导入系统相关模块
import os
import sys
import random
import time
import getpass
import json
import shutil
import chardet
import psutil

# 导入自定义系统库
import SysDOS.Bin.SysLib as syslib
import SysDOS.apt.apt as apt

# 不生成__pycache__文件夹
sys.dont_write_bytecode = True

# 开始运行
syslib.FixUsersFolder()
# 创建系统访问管理器实例，用于后续设置访问类型和用户管理操作
AccessManager = syslib.SystemAccessManager()
# 设置系统访问类型为"Normal"，以适应不同的访问控制需求
AccessManager.SetAccessType("Normal")

# 登录
# 检测Users文件夹是否存在
# 列出当前系统中的所有用户名
UserNameList = syslib.ListUsers()
# 如果用户列表为空，说明没有用户，因此需要注册一个新用户
if UserNameList == []:
    syslib.UserRegister()
    # 清理屏幕
    os.system("cls")
    # 注册用户后，重新列出系统中的所有用户名
    UserNameList = syslib.ListUsers()
# 提示用户输入要登录的用户名，用于后续的登录验证
tmpUserName = input(f"输入要登陆的用户名:")
# 检查临时用户名是否在用户列表中
if tmpUserName in UserNameList:
    try:
        # 如果用户名存在，尝试打开对应的用户文件以读取密码
        with open(f".\\Users\\{tmpUserName}.txt") as f:
            hashed_user_password = f.read().strip()
        # 验证输入的密码是否与文件中的密码匹配
        if syslib.verify_password(hashed_user_password, input("请输入密码：")):
            # 密码匹配，登录成功
            print(f"{syslib.Font.GREEN}登录成功!{syslib.Style.END}")
            Username = tmpUserName
        else:
            # 密码不匹配，提示错误并退出程序
            print(f"{syslib.Font.RED}密码错误{syslib.Style.END}")
            sys.exit(1)
    except SystemExit:
        # 捕获系统退出异常，确保程序能够正确退出
        exit()
    except:
        # 捕获其他异常，处理损坏的密码情况
        print("损坏的密码")
        quit()
else:
    # 用户名不存在，提示无效用户并退出程序
    print("无效用户")
    quit()

# 进入系统

# 清屏
os.system("cls")

class Main:
    def __init__(self):
        self.commands = {
            "cat": self.cat_command,
            "sudo": self.sudo_command,
            "usebook": self.usebook_command,
            "rm": self.rm_command,
            "apt": self.apt_command,
            "top": self.top_command,
            "uitheme": self.uitheme_command,
            "pwd": self.pwd_command,
            "touch": self.touch_command,
            "mv": self.mv_command,
            "cp": self.cp_command,
            "exit": self.exit_command,
            "reboot": self.reboot_command,
            "cd": self.cd_command,
            "user": self.user_command,
            "cls": self.cls_command,
            "register": self.register_command,
            "su": self.su_command,
            "sysver": self.sysver_command,
            "ls": self.ls_command,
            "md": self.md_command,
            "shut": self.shut_command,
            "fuck": self.fuck_command,
            "sh": self.sh_command,
            "echo": self.echo_command,
            "man": self.man_command,
            "rename": self.rename_command,
            "write": self.write_command,
            "getenv": self.getenv_command
        }
        
        # 初始化shell变量和函数字典
        self.shell_variables = {}
        self.shell_functions = {}
        self.Username = Username
        self.hashed_password = hashed_user_password
        self.shell_variables["CURRENT_PATH"] = os.getcwd()
        self.shell_variables["USER_NAME"] = self.Username
        self.shell_variables["WORKING_PATH"] = os.getcwd()
        self.current_path = self.shell_variables["CURRENT_PATH"]
        self.path = self.current_path
        self.apt_get = apt.Apt()
    
    def getenv_command(self, args, sargs):
        loaded = json.load(open(syslib.current_path + "\\SysDOS\\SystemConfig.json", "r"))
        if args[0] in loaded:
            print(syslib.Color_Replace(f"%RED{args[0]}=%WHITE{loaded[args[0]]}"))
        elif args[0] in self.shell_variables:
            print(syslib.Color_Replace(f"%RED{args[0]}=%WHITE{self.shell_variables[args[0]]}"))
        else:
            print(syslib.Color_Replace("%RED未找到此环境变量，请确定您的输入或它是否已被创建！%WHITE"))

    def cat_command(self, args, sargs):
        try:
            # 获取文件路径
            path_1 = args[0]  
            # 使用chardet检测文件编码
            encoding = chardet.detect(open(os.path.abspath(path_1), "rb").read())["encoding"]
            # 打开文件，准备读取内容
            f = open(os.path.abspath(path_1), "r", encoding=encoding)
            # 读取文件内容并按行分割
            content = f.read().split("\n")
            # 关闭文件
            f.close()
            # 遍历文件内容的每一行
            for i in range(len(content)):
                # 颜色高亮
                keywords = ["elif", "if", "echo", "cat", "man", "sh", "shut", "md", "else", "ls",
                            "sysver", "su", "register", "cls", "user", "cd", "reboot", "exit", "cp",
                            "mv", "touch", "pwd", "uitheme", "top", "apt", "rm", "usebook", "sudo", "fi", "getenv"]
                environment_var = ["$WORKING_PATH", "$USER_NAME", "$CURRENT_PATH"]
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                op = ["==", "<<", ">>", ">=", "<="]
                if content[0] == "#! ShellFile" or path_1.endswith(".sh"):
                    for j in numbers:
                        content[i] = content[i].replace(str(j), "%BLUE" + str(j) + "%END")
                    for j in keywords:
                        content[i] = content[i].replace(j, "%RED" + j + "%END")
                    for j in environment_var:
                        content[i] = content[i].replace(j, "%GREEN" + j + "%END")
                    content[i] = content[i].replace("function", "%REDfunction%BLUE")
                    for j in op:
                        content[i] = content[i].replace(j, "%BEIGE" + j + "%END")
                    content[i] = content[i].replace("(", "%END" + "(")
                    content[i] = content[i].replace("{", "%END" + "{")
                content[i] = syslib.Color_Replace(content[i])
                # 打印行号和内容
                if "n" in sargs:
                    print(syslib.Font.WHITE + str(i + 1) + syslib.Style.END + " " + (i + 1 < 10) * " " + (
                            i + 1 < 100) * " " + content[i])
                else:
                    print((i + 1 < 10) * " " + (i + 1 < 100) * " " + content[i])
        except Exception as e:
            try:
                # 捕获异常并打印错误信息
                print(
                    f"{syslib.Font.RED}尝试访问 {syslib.Style.END}{os.path.abspath(path_1)}{syslib.Font.RED} 时报错：{syslib.Style.END}"
                    f"{os.path.abspath(path_1)} {syslib.Font.YELLOW}不是一个有效的文件。{syslib.Style.END}")
                # 打印具体的异常信息
                print(e)
            except Exception as e:
                print("出现未知错误：" + syslib.Font.RED + str(e) + syslib.Style.END)
                print("请将它报告到我们的 Github Issues 上。我们会很快处理问题。")

    def sudo_command(self, args, sargs):
        try:
            flag = 0
            # 检查访问模式是否为"Normal"，如果是，则尝试提升为"Root"权限
            if AccessManager.GetAccessType() == "Normal":
                # 获取用户密码输入，并与存储的密码进行比较
                if syslib.verify_password(self.hashed_password, getpass.getpass(f"[sudo] {self.Username}的密码：")):
                    # 密码正确，提升权限并设置路径
                    AccessManager.SetAccessType("Root")
                    path = r"home\MayDOS"
                else:
                    # 密码错误，显示错误信息
                    print(f"[{syslib.Font.RED}Error{syslib.Style.END}] 密码不正确!")
            if args[0] == "su":
                flag = 1
            else:
                self.execute_command(args[0], args[1:])
            if not flag:
                AccessManager.SetAccessType("Normal")
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)

    def usebook_command(self, args, sargs):
        # 打开usebook.txt文件，准备读取内容
        with open(syslib.current_path + "\\SysDOS\\Bin\\usebook.txt", "r", encoding="utf-8") as menu:
            # 逐行读取文件内容并打印
            for text in menu.readlines():
                print(syslib.Color_Replace(text), end='')
        print()

    def rm_command(self, args, sargs):
        # 删除文件
        try:
            while True:
                sure = input(syslib.Color_Replace(r"%RED确认删除？%WHITE(y/n)"))
                if sure == "y":
                    if os.path.isfile(args[0]):
                        os.remove(args[0])
                        break
                    elif os.path.isdir(args[0]):
                        os.rmdir(args[0])
                        break
                elif sure == "n":
                    break
                else:
                    print("请输入 y 或 n！")
        except FileNotFoundError:
            print("没有找到该文件/文件夹！")
        except Exception:
            print("无法识别您的输入！")
        else:
            print(syslib.Color_Replace("%GREEN成功执行！%WHITE"))

    def apt_command(self, args, sargs):
        if "h" in sargs:
            self.apt_get.help()
            return
        try:
            if args[0] == "update":
                self.apt_get.update()
            elif args[0] == "list":
                self.apt_get.output_list()
            elif args[0] == "start":
                program_status = self.apt_get.start_program(args[1])
                if not program_status:
                    print(syslib.Font.RED + "没有找到该软件包！" + syslib.Style.END)
            elif args[0] == "add":
                try:
                    self.apt_get.add_file(os.getcwd(), args[1])
                except Exception:
                    print(syslib.Font.RED + "无法识别该文件！" + syslib.Style.END)
            else:
                print(syslib.Font.RED + "没有找到该命令！" + syslib.Style.END)
        except Exception as e:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)

    def top_command(self, args, sargs):
        try:
            processes = list(psutil.process_iter())

            # 打印表头
            header = (
                f'________Name________{syslib.Font.BLUE}|{syslib.Style.END}_PID_{syslib.Font.BLUE}|'
                f'{syslib.Style.END}__RAM__{syslib.Font.BLUE}|{syslib.Style.END}'
                f'________Name________{syslib.Font.BLUE}|{syslib.Style.END}_PID_{syslib.Font.BLUE}|'
                f'{syslib.Style.END}__RAM__{syslib.Font.BLUE}|{syslib.Style.END}'
            )
            print(header)

            for i in range(0, len(processes), 2):
                # 处理当前进程
                if i < len(processes):
                    process = processes[i]
                    try:
                        name = process.name()
                        pid = process.pid
                        mem_usage = round(process.memory_percent(), 2)
                    except psutil.NoSuchProcess:
                        continue  # 如果进程不存在，则跳过

                    name_str = name if len(name) <= 20 else name[:17] + "..."
                    print(f'{name_str:<20}{syslib.Font.BLUE}|{syslib.Style.END}'
                        f'{pid:<5}{syslib.Font.BLUE}|{syslib.Style.END}'
                        f'{mem_usage:<6}%{syslib.Font.BLUE}|{syslib.Style.END}', end='')

                # 处理下一个进程
                if i + 1 < len(processes):
                    process = processes[i + 1]
                    try:
                        name = process.name()
                        pid = process.pid
                        mem_usage = round(process.memory_percent(), 2)
                    except psutil.NoSuchProcess:
                        continue  # 如果进程不存在，则跳过

                    name_str = name if len(name) <= 20 else name[:17] + "..."
                    print(f'{name_str:<20}{syslib.Font.BLUE}|{syslib.Style.END}'
                        f'{pid:<5}{syslib.Font.BLUE}|{syslib.Style.END}'
                        f'{mem_usage:<5} %{syslib.Font.BLUE}|{syslib.Style.END}')
                else:
                    print()
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)

    def write_command(self, args, sargs):
        try:
            file = args[0]
            text = " ".join(args[1:])
            with open(file, "w", encoding="utf-8") as f:
                f.write(text)
            print(syslib.Font.GREEN + "成功写入！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)

    def uitheme_command(self, args, sargs):
        if args[0] == "set":
            with open(fr"{self.current_path}\Developers\{args[1]}", "r") as f:
                a = f.read().split("\n")
                Normal_input_tmp = syslib.Color_Replace(a[0]).format(Username=self.Username, path=syslib.current_path)
                Root_input_tmp = syslib.Color_Replace(a[1]).format(Username=self.Username, path=syslib.current_path)
            with open(f"{syslib.current_path}\\using_theme.txt", "w") as f:
                f.write(syslib.DeColor_Replace(Normal_input_tmp) + "\n" + syslib.DeColor_Replace(Root_input_tmp))
        elif args[0] == "reset":
            Normal_input_tmp = ""
            Root_input_tmp = ""
            with open(f"{syslib.current_path}\\using_theme.txt", "w") as f:
                f.write(syslib.DeColor_Replace('%GREEN(%BEIGE{self.Username}@MayDOS%GREEN)-[%WHITE{path}%GREEN]%BEIGE$%WHITE') + "\n" +
                        syslib.DeColor_Replace("%BEIGE(%REDroot@MayDOS%BEIGE)-[%WHITE%BOLD{path}%END%BEIGE]%RED#%WHITE"))

    def pwd_command(self, args, sargs):
        print(os.getcwd())

    def touch_command(self, args, sargs):
        try:
            with open(args[0], 'x', encoding='utf-8') as filecreate:
                filecreate.write('')
        except FileExistsError:
            print(syslib.Font.RED + "该文件已经存在！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入" + syslib.Style.END)

    def rename_command(self, args, sargs):
        # 重命名文件
        try:
            os.rename(args[0], args[1])
        except FileNotFoundError:
            print(syslib.Font.RED + "没有找到该文件！" + syslib.Style.END)
        except OSError:
            print(syslib.Font.RED + "该文件/文件夹已经存在！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入" + syslib.Style.END)

    def man_command(self, args, sargs):
        if not args:
            print(syslib.Style.END + "Man 手册目录：")
            for i in range(len(os.listdir(syslib.current_path + "\\SysDOS\\Man\\"))):
                print(syslib.Font.BLUE + os.listdir(syslib.current_path + "\\SysDOS\\Man\\")[i][:-4] +
                    syslib.Style.END + " 命令")
            return
        try:
            print(syslib.Style.END, end="")
            with open(syslib.current_path + "\\SysDOS\\Man\\" + args[0] + ".txt", "r", encoding="utf-8") as f:
                man = f.readlines()
            for i in man:
                i = i.replace("RED", syslib.Font.RED)
                i = i.replace("END", syslib.Style.END)
                i = i.replace("GREEN", syslib.Font.GREEN)
                i = i.replace("BEIGE", syslib.Font.BEIGE)
                i = i.replace("BLUE", syslib.Font.BLUE)
                i = i.replace("YELLOW", syslib.Font.YELLOW)
                i = i.replace("WHITE", syslib.Font.WHITE)
                print(i, end="")
        except FileNotFoundError:
            print(syslib.Font.RED + "没有找到该命令的帮助！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)
    def mv_command(self, args, sargs):
        try:
            shutil.move(args[0], args[1])
        except FileNotFoundError:
            print(syslib.Font.RED + "没有找到该文件！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入" + syslib.Style.END)
        else:
            print(syslib.Font.GREEN + syslib.Style.ITALIC + "成功执行！" + syslib.Style.END)

    def cp_command(self, args, sargs):
        try:
            shutil.copy2(args[0], args[1])
        except FileNotFoundError:
            print(syslib.Font.RED + "没有找到该文件/文件夹！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入" + syslib.Style.END)
        else:
            print(syslib.Font.GREEN + syslib.Style.ITALIC + "成功执行！" + syslib.Style.END)

    def exit_command(self, args, sargs):
        # 检查当前的访问类型是否为Root
        if AccessManager.GetAccessType() == "Root":
            # 如果是Root，则降级访问类型为Normal，并重置相关变量
            AccessManager.SetAccessType("Normal")
            path = "~"
        else:
            # 如果不是Root，则直接退出程序
            quit()

    def reboot_command(self, args, sargs):
        # 清屏然后重新运行
        os.system("cls")
        self.main()

    def cd_command(self, args, sargs):
        topath = args[0]
        path = self.path
        try:
            if not ".." in topath.split("/") and not syslib.is_x(topath, "/") and not syslib.is_x(topath, "\\ "[:-1]):
                os.chdir(topath)
                if self.path == "/":
                    self.path = self.path + topath
                else:
                    self.path = self.path + "/" + topath
            elif self.path != "/" and  ".." in topath.split("/"):
                os.chdir(topath)
                self.path = "/" * (os.getcwd() == self.current_path) + "/".join(self.path.split("/")[:0 - topath.count("..")])
            elif self.path == "/":
                pass
        except FileNotFoundError:
            print(syslib.Font.RED + "没有找到该位置！" + syslib.Style.END)
            self.path = path
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)
            self.path = path

    def user_command(self, args, sargs):
        if len(args) < 2:
            print("User命令帮助:\n"
                  "user show all            列出当前所有用户以及当前登录用户\n"
                  "user change password     更换当前账户的密码")
        else:
            # 处理显示所有用户的情况
            if args[0] == "show":
                if args[1] == "all":
                    print('当前系统下可用用户:')
                    for i in syslib.ListUsers():
                        # 根据用户名是否为当前用户，输出不同的提示信息
                        print(i if i != self.Username else i + " <-当前用户")
            # 处理更改用户信息的情况
            elif args[0] == "change":
                # 更改密码的逻辑
                if args[1] == "password":
                    print(f"更改{self.Username}的密码:")
                    if syslib.verify_password(self.hashed_password, getpass.getpass("输入旧密码")):
                        # 输入并确认新密码
                        PasswordToChange = getpass.getpass("输入新密码")
                        UserPassword = PasswordToChange
                        # 将新密码加密并写入文件
                        hashed_user_password = syslib.hash_password(UserPassword)
                        f = open(os.path.abspath(f"Users\\{self.Username}.txt"), "w")
                        f.write(hashed_user_password)
                        f.close()
                        print("更改成功!")
                    else:
                        print("更改失败!")
                # 更改用户名的逻辑
                elif args[1] == "username":
                    print(f"更改{self.Username}的用户名:")
                    self.UsernameNew = input("输入新用户名:")
                    # 确保新用户名非空且不存在于系统用户列表中
                    if (self.UsernameNew != "" or self.UsernameNew.isspace()) and self.UsernameNew not in syslib.ListUsers():
                        # 更新用户名，先复制文件再删除原文件
                        open(f"Users/{self.UsernameNew}.txt", "w").write(open(f"Users/{self.Username}.txt").read())
                        os.remove(os.path.abspath(f"Users/{self.Username}.txt"))
                        print(f"{syslib.Font.GREEN}更改成功!{syslib.Style.END}")
                        self.Username = self.UsernameNew
                    elif self.UsernameNew == "" or self.UsernameNew.isspace():
                        print(f"{syslib.Font.RED}在试图更改用户名时报错:{syslib.Font.YELLOW}用户名为空!{syslib.Style.END}")
                    elif self.UsernameNew in syslib.ListUsers():
                        print(f"{syslib.Font.RED}在试图更改用户名时报错:{syslib.Font.YELLOW}用户名已存在!{syslib.Style.END}")

                # 如果操作命令不是前两者，则显示帮助信息
                else:
                    print("User命令帮助:\n"
                          "user show all            列出当前所有用户以及当前登录用户\n"
                          "user change password     更换当前账户的密码")

    def cls_command(self, args, sargs):
        # 典型的清屏
        os.system('cls')

    def register_command(self, args, sargs):
        # 注册用户
        syslib.UserRegister()

    def su_command(self, args, sargs):
        try:
            # 获取系统中所有的用户名单
            UserNameList = syslib.ListUsers()
            if UserNameList != []:
                # 解析命令行参数，获取目标用户名
                tmpUserName = args[0]
                if tmpUserName in UserNameList:
                    # 读取目标用户的密码文件
                    with open(os.path.abspath(f"{syslib.current_path}/Users/{tmpUserName}.txt")) as f:
                        TmpUserPassword = f.read()
                    # 循环提示用户输入密码，直到正确
                    while True:
                        pwd = getpass.getpass("输入密码:")
                        if syslib.verify_password(TmpUserPassword, pwd):
                            # 密码匹配，更新当前用户名和密码
                            self.Username = tmpUserName
                            UserPassword = TmpUserPassword
                            break
                        else:
                            # 密码错误，提示用户
                            print(f"{syslib.Font.RED}密码错误！{syslib.Style.END}")
                else:
                    # 目标用户不存在，提示用户
                    print(f"{syslib.Font.RED}没有此用户！{syslib.Style.END}")
            else:
                # 系统中只有一个用户，提示用户注册新用户
                print("只有一个用户!\n请使用'register'命令注册用户")
        except IndexError:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)

    def sysver_command(self, args, sargs):
        print(f'系统版本：MayDOS 1.1.5.0 Normal')
        print('开发：MayDOS开发团队 版权所有2023(C)')

    def ls_command(self, args, sargs):
        if not args:
            try:
                print(f"当前下的文件：")
                files = syslib.ls(os.getcwd(), sargs)
                for i in files:
                    print(i)
                print(f"共{len(files)}个文件。")
            except ValueError:
                print(
                    f"{syslib.Font.RED}尝试访问 {syslib.Style.END}当前目录{syslib.Font.RED} 时报错：{syslib.Style.END}"
                    f"当前目录 {syslib.Font.YELLOW}不是一个有效的文件夹。{syslib.Style.END}")
        else:
            # 列出指定目录下的文件
            tmpcmd = args[0]
            # 检查是否尝试访问系统目录且用户权限非Root，若是，则提示权限不足
            if os.path.abspath(tmpcmd).startswith(r"C:\Windows") and AccessManager.GetAccessType() != "Root":
                print(
                    f"{syslib.Font.RED}尝试访问 {syslib.Style.END}{os.path.abspath(tmpcmd)}{syslib.Font.RED} 时报错：{syslib.Font.YELLOW}权限不足。"
                    f"{syslib.Style.END}")
                return
            try:
                print(f"{os.path.abspath(tmpcmd)}下的文件：")
                for i in syslib.ls(tmpcmd, sargs):
                    print(i)
                print(f"共{len(syslib.ls(tmpcmd, sargs))}个文件。")
            except ValueError:
                print(
                    f"{syslib.Font.RED}尝试访问 {syslib.Style.END}{os.path.abspath(tmpcmd)}{syslib.Font.RED} 时报错：{syslib.Style.END}"
                    f"{os.path.abspath(tmpcmd)} {syslib.Font.YELLOW}不是一个有效的文件夹。{syslib.Style.END}")

    def md_command(self, args, sargs):
        try:
            os.mkdir(args[0])
        except FileExistsError:
            print(syslib.Font.RED + "该文件夹已经存在！" + syslib.Style.END)
        except Exception:
            print(syslib.Font.RED + "无法识别您的输入！" + syslib.Style.END)

    def shut_command(self, args, sargs):
        # 真的关机
        if input(f"确认关机（\x1b[31m这可不是闹着玩的\x1b[0m）？[Y/n]") == "Y":
            if sys.platform == 'win32':
                os.system('shutdown -P')

        else:
            return

    def fuck_command(self, args, sargs):
        if not args:
            print("安利一部电影：我是谁：没有绝对安全的密码")
            print("在B站上可以直接看")
            print("           ——Fang-Omega")
        elif args[0] == "you":
            print("Fuck You!!!")
            sys.exit(0)
        else:
            print("FUCK.")

    def sh_command(self, args, sargs):
        if len(args) == 0:
            print("用法: sh <脚本文件名>")
        else:
            try:
                with open(args[0], 'r') as script_file:
                    script_content = script_file.read()
                self.execute_shell_script(script_content)
            except FileNotFoundError:
                print(f"{syslib.Font.RED}脚本文件 {args[0]} 不存在{syslib.Style.END}")
            except Exception as e:
                print(f"{syslib.Font.RED}执行脚本时发生错误: {str(e)}{syslib.Style.END}")

    def echo_command(self, args, sargs):
        print(' '.join(args))

    def execute_command(self, cmd, args, sargs):
        try:
            assert len(cmd) <= 60
        except AssertionError:
            print(syslib.Font.RED + "错误：超过命令长度最大限制" + syslib.Style.END)
            return
        if cmd in self.commands:
            self.commands[cmd](args, sargs)
        elif not cmd:
            return
        elif not self.apt_get.run_command(cmd):
            fuck_list = ["usebook", "md", "shut", "ls", "cls", "sysver", "sudo", "su",
                         "reboot", "cat", "register", "cp", "md", "top", "user", "exit", "uitheme", "cd", "pwd", "mv", "touch",
                         "apt", "sh", "man", "rename", "echo", "write", "getenv", "setenv"]
            for i in range(len(cmd) - 1):
                if cmd[:i] + cmd[i + 1] + cmd[i] + cmd[i + 2:] in fuck_list:
                    did_you_mean = input(
                        "你是说 " + cmd[:i] + cmd[i + 1] + cmd[i] + cmd[i + 2:] + " ".join(
                            [""] + args if args else args) + " 吗？(y/n)")
                    if did_you_mean == "y":
                        cmd = cmd[:i] + cmd[i + 1] + cmd[i] + cmd[i + 2:] + " ".join(
                            [""] + args if args else args)
                        self.execute_command(cmd, args, sargs)
                    break
            else:
                for i in range(len(cmd)):
                    if cmd[:i] + cmd[i + 1:] in fuck_list:
                        did_you_mean = input(
                            "你是说 " + cmd[:i] + cmd[i + 1:] + " ".join([""] + args if args else args) + " 吗？(y/n)")
                        if did_you_mean == "y":
                            cmd = cmd[:i] + cmd[i + 1:] + " ".join([""] + args if args else args)
                            self.execute_command(cmd, args, sargs)
                        break
                else:
                    for i in range(len(cmd)):
                        if cmd[:i] in fuck_list:
                            args.insert(0, cmd[i:])
                            did_you_mean = input("你是说 " + cmd[:i] + " " + " ".join(args) + " 吗？(y/n)")
                            if did_you_mean == "y":
                                cmd = cmd[:i]
                                self.execute_command(cmd, args, sargs)
                            break
                    else:
                        if cmd.startswith("$") and cmd[1:] in self.shell_variables.keys():
                            print(syslib.Color_Replace(f"%RED{cmd[1:]}=%WHITE{self.shell_variables[cmd[1:]]}"))
                        else:
                            List_RAN = ['MayDOS有摸鱼部门和搞事部门！', '0.4.1是0.4.2之前最多BUG的版本',
                                        'MayDOS其实从0.4.0开始就有可安装版本了呢~', 'MayDOS的安装版本自动更新会报错！',
                                        'MayDOS现在已经有很多人参与开发了呢', 'MayDOS的开发人员似乎对MayDOS没有激情',
                                        'MayDOS的软件API是自研的', '你知道MayDOS其实在0.4以后有了阁小小的GUI吗？', '移除了HIM']
                            print(
                                f"{syslib.Font.RED}未定义的指令{syslib.Font.YELLOW} {cmd} {syslib.Font.RED}，请输入'usebook'以查看使用手册和帮助{syslib.Style.END}")
                            print("Tips: ", random.choice(List_RAN))

    def main(self):
        os.system(r'title MayDOS')  # 更改标题
        os.system("cls")

        syslib.current_path = os.getcwd()

        # 打印动画
        with open(syslib.current_path + "\\SysDOS\\Bin\\icon.txt", "r", encoding="utf-8") as icon:
            for text in icon.readlines():
                print(text, end='')
        print()

        time.sleep(0.25)

        # 准备MayDOS命令行环境
        print(f'正在准备你的MayDOS命令行......')

        # 初始化命令行回显状态
        echo_off = False
        # 初始化当前路径
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        alls = ["", ""] if not os.path.exists("SysDOS\\Bin\\using_theme.txt") else open("SysDOS\\Bin\\using_theme.txt").read().split("\n")
        Root_input_tmp = alls[1]
        Normal_input_tmp = alls[0]
        fuck = False

        # 提示用户如何打开使用手册和帮助
        print(f'请输入"usebook"以打开MayDOS的使用手册和帮助')

        while True:  # 进入命令行循环
            # 将 path 中的 current path 替换成根目录（/）
            self.path = self.path.replace(self.current_path, "/")
            self.path = self.path.replace("/Home", "~")
            # 根据当前的访问类型（Root或其他用户）以及是否关闭回显来获取用户输入的命令
            Root_input = (syslib.Color_Replace(r"%BEIGE(%REDroot@MayDOS%BEIGE)-[%END%BOLD{path}%END%BEIGE]%RED#%END").
                          format(path=self.path)) if Root_input_tmp == "" else syslib.Color_Replace(Root_input_tmp).format(path=self.path)
            Normal_input = (syslib.Color_Replace(r'%GREEN(%BEIGE{Username}@MayDOS%GREEN)-[%END{path}%GREEN]%BEIGE$%END').
                            format(Username=self.Username, path=self.path)) if Normal_input_tmp == "" else syslib.Color_Replace(Normal_input_tmp).format(Username=self.Username, path=self.path)

            if AccessManager.GetAccessType() == "Root":
                # 如果echo_off未启用，则显示特定的提示信息，其中包括路径和用户输入的上一个命令
                if not echo_off:
                    user_input = input(Root_input + syslib.Style.END)
                else:
                    # 如果echo_off启用，则不显示任何提示信息，直接获取用户输入
                    user_input = input(syslib.Style.END)
            else:
                # 对于非Root用户，处理方式类似，但提示信息中的用户名和权限级别会有所不同
                if not echo_off:
                    user_input = input(Normal_input + syslib.Style.END)
                else:
                    # 如果echo_off启用，则不显示任何提示信息，直接获取用户输入
                    user_input = input(syslib.Style.END)

            # 定义“被引号包裹的”列表，使后续“特殊参数”判断时跳过这些参数
            hasqm = []
            # 分隔命令与参数
            if "\"" in user_input:
                parts = user_input.split("\"")
                cmd_parts = parts[0].strip().split()
                args = []
                for part in parts[1:]:
                    if part.strip():
                        if part.strip().startswith("-"):
                            hasqm.append(part.strip())
                        args.append(part.strip())
                if cmd_parts:
                    cmd = cmd_parts[0]
                    args = cmd_parts[1:] + args
                else:
                    cmd = ""
                    args = []
            else:
                cmd_parts = user_input.split()
                if cmd_parts:
                    cmd = cmd_parts[0]
                    args = cmd_parts[1:]
                else:
                    cmd = ""
                    args = []


            tmpargs = args
            # 定义“特殊参数”，即为横线开头的参数
            sargs = []

            try:
                for i in range(len(args)):
                    if args[i].startswith("-") and len(args[i]) >= 2 and not args[i] in hasqm:
                        for j in list(args[i][1:]):
                            if not j in sargs:
                                sargs.append(j)
                        del args[i]
                        break
            except IndexError:
                args = tmpargs

            self.shell_variables["WORKING_PATH"] = os.getcwd()
            self.execute_command(cmd, args, sargs)

    def execute_shell_script(self, script_content):
        lines = script_content.split('\n')
        flag = 0
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # 对注释的判断
            if line.startswith('##') and not flag:
                flag = not flag
                i += 1
                continue
            if line.startswith('#') or flag:
                i += 1
                continue


            # 对函数的判断
            if line.startswith('function '):
                func_name = line.split()[1].split('(')[0]
                func_body = []
                i += 1
                if lines[i] == "{":
                    i += 1
                while i < len(lines) and not lines[i].strip() == '}':
                    func_body.append(lines[i])
                    i += 1
                self.shell_functions[func_name] = func_body

            # 对变量的判断
            elif '=' in line and not line.startswith('if '):
                var_name = line.split('=', 1)[0]
                var_value = line.split('=', 1)[1]
                self.shell_variables[var_name.strip()] = var_value.strip()

            # 对条件语句的判断
            elif line.startswith('if '):
                condition = line[3:].strip()
                i += 1
                if_block = []
                elif_blocks = []
                else_block = None
                current_block = if_block
                while i < len(lines) and not lines[i].strip() == 'fi':
                    if lines[i].strip().startswith('elif '):
                        elif_blocks.append((lines[i][5:].strip(), []))
                        current_block = elif_blocks[-1][1]
                    elif lines[i].strip() == 'else':
                        else_block = []
                        current_block = else_block
                    else:
                        current_block.append(lines[i])
                    i += 1
                
                if self.evaluate_condition(condition, self.shell_variables):
                    self.execute_block(if_block)
                else:
                    for elif_condition, elif_block in elif_blocks:
                        if self.evaluate_condition(elif_condition, self.shell_variables):
                            self.execute_block(elif_block)
                            break
                    else:
                        if else_block:
                            self.execute_block(else_block)
            elif line.startswith('for '):
                # 实现for循环
                for_variable_name = line.split()[1]

                self.shell_variables[for_variable_name] = None
                for j in range(int(line.split("{")[1].split(",")[0]), int(line.split("{")[1].split(",")[1][:-1])):
                    self.shell_variables[for_variable_name] = j
                    self.execute_shell_command(line, self.shell_variables, self.shell_functions)
                    if line[i] != "done":
                        i += 1
                    else:
                        break

            elif line.startswith('while '):
                # 实现while循环
                pass
            else:
                self.execute_shell_command(line, self.shell_variables, self.shell_functions)
            i += 1

    def execute_block(self, block):
        for line in block:
            self.execute_shell_command(line.strip(), self.shell_variables, self.shell_functions)

    def evaluate_condition(self, condition, variables):
        # 简单的条件评估,可以根据需要扩展
        parts = condition.split()
        if len(parts) == 3:
            left, op, right = parts
            left = variables.get(left, left)
            right = variables.get(right, right)
            if op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<<':
                return left < right
            elif op == '>>':
                return left > right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right
        return False

    def execute_shell_command(self, command, variables, functions):
        # 替换变量
        for var, value in variables.items():
            enuvar = ["CURRENT_PATH", "WORKING_PATH", "USER_NAME"]
            command = command.replace(f"${str(var)}", str(value))

        # 检查是否是函数调用
        if command in functions:
            for line in functions[command]:
                self.execute_shell_command(line, variables, functions)
        else:
            if len(command) > 2:
                # 执行常规命令
                cmd_parts = command.split()
                cmd = cmd_parts[0]
                args = cmd_parts[1:]
                self.execute_command(cmd, args, [])


Main = Main()
Main.main()
