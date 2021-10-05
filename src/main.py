from threading import Thread
from pathlib import Path

import asyncio
from time import sleep


# from menu import Menu
from FishingGUI import FishingGUI
from bot import Bot
from win import Win
from controller import Contoller

class Main(Thread, Win):
    def __init__(self, isStop=False):
        Thread.__init__(self)
        self.Base_dir = Path(__file__).resolve().parent
        self.botArray = []
        self.windowClass = "SDL_app"
        self.windowCaption = "Trove"
        self.isStop = isStop

    def run(self):
        while not self.isStop:
            for index, bot in enumerate(self.botArray):
                if bot.botId != index:
                    bot.botId = index
                    bot.windowCaption = f'Trove Fishbot - {bot.botId + 1}'
                    super().setWindowText(bot.hwnd, bot.windowCaption)
                    
                if not bot.isWindowActive():
                    del self.botArray[index]

            HWND = super().findWindow(self.windowClass, self.windowCaption)
            if HWND:
                PID = super().getWindowThreadProcessId(HWND)
                tempWindowCaption = f'Trove Fishbot - {len(self.botArray) + 1}'
                super().setWindowText(HWND, tempWindowCaption)
                self.botArray.append(Bot(botId=len(self.botArray) + 1, hwnd=HWND, pid=PID, windowCaption=tempWindowCaption))
            sleep(0.1)

    def main_end(self):
        self.isStop = True
        for bot in self.botArray:
            super().setWindowText(bot.hwnd, self.windowCaption)
      
mainObject = Main()
mainObject.start()

controllerObject = Contoller(mainObject.botArray)
controllerObject.start()

loop = asyncio.get_event_loop()
menuobject = FishingGUI( 
    loop=loop,
    main_end=mainObject.main_end,
    controller_end=controllerObject.controller_end,
    Base_dir=mainObject.Base_dir,
    botArray=mainObject.botArray,
)
loop.run_forever()
