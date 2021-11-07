import asyncio
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import webbrowser
from pathlib import Path

from win import Win

class FishingGUI(tk.Frame, Win):
    def __init__(
            self,
            loop,
            main_end,
            controller_end,
            Base_dir,
            botArray,
            lastActivity,
            master = tk.Tk(),
            interval=1/60
        ):
        super().__init__()
        self.Base_dir = Base_dir
        try:
            self.images = {
                'icon': self.ready_img(Path(self.Base_dir / 'main.ico')), 
            }
        except:self.images = False
        self.loop = loop
        self.master = master
        self.master.title('SqueakFishing')
        if self.images:
            self.master.call('wm', 'iconphoto', self.master._w, self.images['icon'])
        self.master.configure(bg='#fff')
        self.master.geometry('735x435')
        self.master.maxsize(735, 435)
        self.master.minsize(735, 435)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.close(main_end, controller_end))

        self.lastActivity = lastActivity
        self.botArray = botArray
        self.botArrayLenght = 0
        self.contorl_state = False
        self.tasks = []
        self.tasks.append(loop.create_task(self.mainPage(interval)))
        self.tasks.append(loop.create_task(self.updater(interval)))
        self.githubURL = r'https://github.com/farigami/python_bot_v2.0'
        self.donateURL = r'www.donationalerts.com/r/squeaknight'

    async def mainPage(self, interval):
        logLenght = 0
        flag = False
        self.logo() 
        self.menuButton()
        self.logLabel()

        
        while await asyncio.sleep(interval, True):
            if len(self.botArray) != self.botArrayLenght:
                flag = True
                if self.contorl_state:
                    self.contol_destroy()

                self.controlFrame()
                self.control_refresh()
                self.botArrayLenght = len(self.botArray)
                
                
            elif len(self.botArray) == 0 and flag:
                self.contol_destroy()
                self.botArrayLenght = len(self.botArray)
                flag = False
                          
            if len(self.lastActivity) != logLenght:
                time = datetime.now().strftime("%H:%M:%S")
                self.log_listbox.insert(tk.END, f' {time} {self.lastActivity[-1]}')
                logLenght = len(self.lastActivity)

    

    def control_refresh(self):
        
        for index, bot in enumerate(self.botArray):
            tmpbot = (
                bot.windowCaption,
                hex(bot.pid), hex(bot.hwnd),
                ''.join(['Enable' if bot.isStop else 'Disable']),
            )
            for column in range(4):
                self.makeEntry(
                    row=index,
                    column=column,
                    text=tmpbot[column]
                )

    def makeEntry(self, row, column, text):
        tmpEntry =  tk.Entry(
                self.control_listbox,
                fg='blue',
                width=23,
            )

        tmpEntry.grid(row=row, column=column)
        tmpEntry.insert(tk.END, text)
        

    def logo(self):
        logo_frame = tk.Frame(
            self.master,
            bg='white'
        )
        logos = [
            {'text': 'Squeak', 'fg': '#31343b'},
            {'text': 'Fishing v2.0', 'fg': 'Crimson'}
        ]
        for logo in logos:
            tmplogo = tk.Label(
                logo_frame,
                bd=-2,
                bg='white',
                fg=logo['fg'],
                text=logo['text'], 
                font=('Tahoma', 16, 'bold'),
                cursor='hand2'
            )
            tmplogo.bind("<Button-1>", lambda e: self.callback(self.githubURL))
            tmplogo.pack(side='left', anchor='n')
        logo_frame.place(x=5, y=5)
    
    def controlFrame(self):
        self.contorl_state = True
        self.control_frame = tk.Frame(
            self.master,
            bd=-2,
            bg='white',
            width=160,
            height=550
        )
    
        scrollbar = tk.Scrollbar(self.control_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.control_listbox = tk.Listbox(
            self.control_frame,
            bd=-2,
            yscrollcommand=scrollbar.set,
            bg='#cccccc',
        )
        self.control_listbox.pack(side='left', fill=tk.BOTH)
        scrollbar.config(command=self.control_listbox.yview)
        self.control_frame.place(y=160)
        

    def logLabel(self):
        log_frame = tk.Frame(
            self.master,
            height=5
            )
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_listbox = tk.Listbox(
            log_frame,
            yscrollcommand=scrollbar.set,
            height=5
        )
        
        self.log_listbox.insert(tk.END, 'Welcome back fishing log')
        self.log_listbox.pack(fill='both')
        scrollbar.config(command=self.log_listbox.yview)
        log_frame.pack(side='bottom', fill='x')


    def menuButton(self):
        button_frame = tk.Frame(
            self.master,
            bg='white',
        )
        components = [
            {'title': 'Start all bots', 'command': lambda: self.bot_start()},
            {'title': 'Stop all bots', 'command': lambda: self.bot_stop()},
            {'title': 'Donate', 'command': lambda: self.callback(self.donateURL)},
            {'title': 'Resize windows', 'command': lambda: self.resize()}, 
            {'title': 'Clear Log', 'command': lambda: self.clearlog()}, 
        ]
        for component in components:
            tk.Button(
                button_frame,
                text=component['title'],
                command=component['command'],
                width=15,
                height=2,
                bd=-1,
                bg='#d9d9d9',
                font=('Tahoma', 10)

            ).pack(side='top', fill='x', pady=5)
        button_frame.grid(row=0, column=1, sticky='nsew')
        button_frame.place(x=600, y=102.5)
    
    def contol_destroy(self):
        self.control_frame.pack_forget()
        self.control_frame.destroy()

    def clearlog(self):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, 'Welcome back fishing log')

    def bot_start(self):
        for bot in self.botArray:
            bot.findGameProcess()
            if bot.findAddress():
                bot.isStop = True
        try:
            self.contol_destroy()
            self.controlFrame()
            self.control_refresh()
        except:pass

    def bot_stop(self):
        for bot in self.botArray:
            bot.isStop = False
        try:
            self.contol_destroy()
            self.controlFrame()
            self.control_refresh()
        except:pass
            
    def resize(self):
        for bot in self.botArray:
            super().resizeWindow(bot.hwnd)

    def callback(self, url):
        webbrowser.open_new(url)

    def ready_img(self, path, size=False):
        if size:
            return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ANTIALIAS))
        return ImageTk.PhotoImage(Image.open(path))


    async def updater(self, interval):
        while await asyncio.sleep(interval, True):
            self.update()


    def close(self, main_end, controller_end):
        main_end()
        controller_end()
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()