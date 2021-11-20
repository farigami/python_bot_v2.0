from threading import Thread
from time import sleep


from win import Win
from shards import Coords

class Contoller(Thread, Win):
    def __init__(self, botArray):
        Thread.__init__(self)
        self.botArray = botArray
        self.isStop = False
    
    def run(self):
        while not self.isStop:
            for bot in self.botArray:
                if bot.isStop:
                    state, fish = bot.pm.read_int(bot.stateAddress), bot.pm.read_int(bot.fishAddress)
                    if state == 2 and fish == 1:
                        super().postMessage(hwnd=bot.hwnd, key=0x13)
                        bot.score += 1
                    elif state == 0:
                        super().postMessage(hwnd=bot.hwnd, key=0x13)

                # if bot.isClear:
                #     for coords in Coords().coords:
                #         super().postWindowDeleteClick(hwnd=bot.hwnd, coords=coords)
                #     bot.isClear = False
            sleep(0.05)
        

    def controller_end(self):
        self.isStop = True

