from threading import Thread
from time import sleep


from win import Win

class Contoller(Thread, Win):
    def __init__(self, botArray):
        Thread.__init__(self)
        self.botArray = botArray
        self.isStop = False
    
    def run(self):
        while not self.isStop:
            for bot in self.botArray:
                if bot.isStop is True:
                    state, fish = bot.pm.read_int(bot.stateAddress), bot.pm.read_int(bot.fishAddress)
                    if state == 2 and fish == 1 or state == 0:
                        super().postMessage(bot.hwnd, 0x13)
                        bot.score += 1
            sleep(0.1)

    def controller_end(self):
        self.isStop = True
        print('stop in controller')