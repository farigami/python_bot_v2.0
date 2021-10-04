import os

from threading import Thread
from answers import *


class Menu(Thread):
    def __init__(self, botArray, main_end, controller_end, isStop=False):
        Thread.__init__(self)
        self.botArray = botArray
        self.isStop = isStop
        self.main_end = main_end
        self.controller_end = controller_end

    def run(self):
        print(self.commandSheet())

        while not self.isStop:
            value = input()
            if value == '1':
                '''
                Bot list
                '''
                if len(self.botArray) >= 1:
                    self.clearConsole()
                    print(self.commandSheet())
                    print(BOT_SHEET)
                    for bot in self.botArray:
                        print(
                                f'\033[37m ID [{bot.botId}] \033[32m {bot.windowCaption}  | hwnd-{bot.hwnd} | pid-{bot.pid}',
                                ''.join(['Включен' if bot.isStop is True else 'Выключен'])
                                ) 
                else:
                    self.clearConsole()
                    print(self.commandSheet())
                    print(BOT_SHEET)
                    print('Активных ботов нет')

            elif value == '2':
                '''
                Bot enable
                '''
                value = int(input('Введите ID бота: '))
                for bot in self.botArray:
                    self.clearConsole()
                    print(self.commandSheet())
                    if bot.botId == value:
                        bot.findGameProcess()
                        if bot.findAddress():
                            bot.isStop = True
                            print(f'\033[32m {bot.windowCaption} | hwnd-{bot.hwnd} | pid-{bot.pid} был включен | Поймано-{bot.score}')
                        else:print('Error in findAddress, need new offsets and address')
                          
            elif value == '3':
                '''
                Bot disable
                '''
                value = int(input('Введите ID бота: '))
                for bot in self.botArray:
                    if bot.botId == value:
                        bot.isStop = False
                        self.clearConsole()
                        print(self.commandSheet())
                        print(f'\033[32m {bot.windowCaption} | hwnd-{bot.hwnd} | pid-{bot.pid} был выключен \033')

            elif value == '4':
                '''
                Bot close process
                '''
                self.main_end()
                self.controller_end()
                self.end()
            else:
                print('Error')

    def commandSheet(self):
        return f'\033[32m {COMMAND_SHEET}'

    def clearConsole(self):
        os.system('cls')

    def end(self):
        self.isStop = True
