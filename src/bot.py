import pymem
from win import Win

class Bot(Win):
    def __init__(
            self, 
            botId=None,
            pm=None, 
            pid=None, 
            client=None, 
            hwnd=None,
            windowCaption=None,
            stateAddress=None, 
            fishAddress=None, 
        ):
        self.botId = botId
        self.pm  = pm
        self.pid = pid
        self.client = client
        self.hwnd = hwnd
        self.state = '0x00FEE074'
        self.fish = '0x010D44C8'
        self.state_offsets = [0xC, 0xC, 0xC, 0x50, 0xC4, 0x204, 0x54]
        self.fish_offsets = [0x0, 0x6C, 0x1C, 0x50, 0x0, 0x38, 0x6C8]
        self.score=0,
        self.windowCaption = windowCaption
        self.stateAddress = stateAddress
        self.fishAddress = fishAddress
        self.isStop = False
    
    def getWindowCaption(self):
        return str(super().getWindowCaption(self.hwnd))

    def isWindowActive(self):
        if super().getWindowCaption(self.hwnd) == self.windowCaption:
            return True
        return False

    def findGameProcess(self):
        '''
        Find Game process
        '''
        self.pm = pymem.Pymem()
        self.pm.open_process_from_id(self.pid)
        self.client = pymem.process.module_from_name(self.pm.process_handle, "trove.exe").lpBaseOfDll

    
    def findAddress(self):
        try:
            tempstate = self.pm.read_int(self.client + int(self.state, 16))
            tempfish = self.pm.read_int(self.client + int(self.fish, 16))
            for i in range(len(self.state_offsets)):
                '''
                Find fish and state address
                '''
                fishAddress = tempfish + self.fish_offsets[i]
                stateAddress = tempstate + self.state_offsets[i]

                tempstate = self.pm.read_int(tempstate + self.state_offsets[i])
                tempfish = self.pm.read_int(tempfish + self.fish_offsets[i])

            self.stateAddress = stateAddress
            self.fishAddress = fishAddress
        except:return False
        return True
