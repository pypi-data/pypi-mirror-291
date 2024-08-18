import os
import msvcrt
from typing import List


class Option:
    def __init__(self, content: str) -> None:
        self.index = None
        self.content = content

    # def __new__(cls) -> Self:
    #     super.__new__()


class Menu:

    def __init__(self) -> None:
        self.options: List[Option] = []
        self.checked: Option = None

    def addOption(self, option: Option):
        option.index = len(self.options)
        self.options.append(option)
        if not self.checked:
            self.checked = self.options[0]

    def activate(self):
        while True:
            self._showMenu()
            key = self._getKey()
            if key == 'enter':  # Enter key to select
                return self.checked.index
            elif key == 'esc':
                break
            elif key in ('up', 'down'):  # Up or Down arrow
                self.checked = (self._nextOption() if key ==
                                'down' else self._lastOption())
            else:
                continue

    def _getKey(self):
        try:
            key = msvcrt.getch()  # get keypress
            if key == b'\x1b':  # Esc key to exit
                return 'esc'
            elif key == b'\r':  # Enter key to select
                return 'enter'
            elif key == b'\x48':  # Up or Down arrow
                return 'up'
            elif key == b'\x50':  # Up or Down arrow
                return 'down'
            else:
                return key.decode('utf-8')
        except Exception as e:
            pass

    def _lastOption(self):
        i = self.checked.index-1
        return self.options[len(self.options)-1 if i < 0 else i]

    def _nextOption(self):

        i = self.checked.index+1
        return self.options[0 if i >= len(self.options) else i]

    def _showMenu(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("当前目标:", self.checked.index)
        for option in self.options:
            if self.checked.index == option.index:
                print(f"[>] {option.index}.{option.content}")
            else:
                print(f"[*] {option.index}.{option.content}")
        print("\n使用方向键移动,Enter键选择,Esc键退出。")


if __name__ == '__main__':

    m = Menu()
    m.addOption(Option('查看配置'))
    m.addOption(Option('添加账户'))
    m.addOption(Option('删除账户'))

    i = m.activate()
    print('+++++++++++++++++')
    print(i)
    print('+++++++++++++++++')
