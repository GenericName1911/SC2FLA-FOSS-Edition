import sys

import colorama

import platform

from shutil import get_terminal_size

if platform.system() == "Windows":
    colorama.init()

def Time(seconds):
    des = ('msec', 'sec', 'min', 'hours')
    temp = []
    temp.append('%s %s'%(str(float(seconds)).split('.')[1][:3], des[0]))
    seconds = int(seconds)
    temp.append(f'{seconds % 60} {des[1]}')

    seconds //= 60
    while seconds:
        if len(temp) == 3:
            temp.append(f'{seconds % 60} {des[3]}')
            break

        temp.append(f'{seconds % 60} {des[len(temp)]}')
        seconds //= 60

    return ' '.join(temp[::-1])

class Console:
    @staticmethod
    def title(message):
        print(colorama.Fore.GREEN + message.center(get_terminal_size().columns) + colorama.Style.RESET_ALL)
    @staticmethod
    def info(message: str):
        print(colorama.Fore.GREEN + f"[INFO] {message}" + colorama.Style.RESET_ALL)

    @staticmethod
    def warning(message: str):
        print(colorama.Fore.MAGENTA + f"[WARNING] {message}" + colorama.Style.RESET_ALL)

    @staticmethod
    def error(message: str):
        print(colorama.Fore.RED + f"[ERROR] {message}" + colorama.Style.RESET_ALL)

    @staticmethod
    def progress_bar(info, current, total, start=0, end=100, totalCount = -1, currentCount = -1):
        message = colorama.Fore.GREEN
        message += f"\r[{((current + 1) * end + start) // total + start}%] "

        if (totalCount > 0 and currentCount > 0):
            message += f"[{currentCount}/{totalCount} "

        message += info
        message += colorama.Style.RESET_ALL

        sys.stdout.write(message)
