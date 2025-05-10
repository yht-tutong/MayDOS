import time, os
import SysDOS.Bin.SysLib as syslib

# 询问用户选择命令行还是图形界面来显示记事本
dis = input("1.命令行[DOS]\n2.图形界面[GUI]\n请选择显示方式：>>")

if dis == '2':
    # 打开并以二进制模式读取 Python 文件的内容
    with open(syslib.current_path + "\\SysDOS\\apt\\Packages\\Notepad_Apt\\Notepad_GUI.py", "rb") as file:
        # 以UTF-8编码方式解码文件内容
        notepad_gui = file.read().decode('utf-8')

    # 执行 Python 代码
    exec(notepad_gui)
    exit()
elif dis != '1':
    print("输入错误，请重新输入")

# 先清屏
os.system('cls')

print("Notepad")


# 获取时间戳，以便进行命名文件
# def get_timestamp():
#     # 获取当前时间的 Unix 时间戳（以秒为单位）
#     timestamp = int(time.time())
#
#     # 将时间戳转换为字符串
#     filename = f"data_{timestamp}.txt"  # 例如：data_1627558217.txt
#
#     return filename


re_filename = ''

# 获取程序当前位置
current_path = os.getcwd()


# 列出一个文件夹下的所有文件，但是只列出以.txt结尾且文件名含有data的文件
def list_files():
    files = os.listdir(current_path + "\\..\\Bin")
    for file in files:
        if file.endswith(".MayNote"): # and "data" in file:
            print(file)


# 根据时间戳保存文件内容
def save_note():
    global re_filename
    note = input("请输入你要保存的内容：")
    re_filename = input("请输入你要保存的文件名（不含后缀）：") + ".MayNote"
    with open(current_path + "\\..\\Bin\\" + re_filename, "w", encoding="utf-8") as file:
        file.write(note)
    print("‘ " + re_filename + " ’文件已保存。")


def list_and_read_note():
    # global list_files(),
    choose = input("请选择直接输入文件路径进行查看【仅支持“UTF-8”编码的文件】（1）\n列出文件进行查看【该选项仅支持打开本编辑器保存的文件】（2）：")

    if choose == "1":
        file_path = input("请输入文件路径：")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                note = file.read()
                print(note)
        except FileNotFoundError:
            print("未找到保存的内容。")


    elif choose == "2":
        list_files()
        # 接收用户输入并判断是否在文件列表中，如果在则读取文件内容，如果不在则提示用户重新输入
        file_name = input("请输入文件名：")
        try:
            with open(current_path + "\\..\\Bin\\" + file_name, "r", encoding="utf-8") as file:
                note = file.read()
                print(note)


        except FileNotFoundError:
            print("未找到保存的内容。")
    else:
        print("无效的选项，请重新输入。")


# 主程序部分
def main():
    while True:
        print("\n菜单：")
        print("1. 保存内容")
        print("2. 查看上次保存的内容")
        print("3. 退出")

        choice = input("请输入选项数字（1\\2\\3）：")

        if choice == "1":
            save_note()
        elif choice == "2":
            list_and_read_note()
        elif choice == "3":
            print("退出记事本。")
            break
        else:
            print("无效的选项，请重新输入。")


# 启动
if __name__ == "__main__":
    main()
