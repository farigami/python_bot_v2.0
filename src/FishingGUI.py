import asyncio
import tkinter as tk
from tkinter.constants import END
from PIL import Image, ImageTk
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
            master = tk.Tk(),
            interval=1/120
        ):
        super().__init__()
        self.Base_dir = Base_dir
        try:
            self.images = {
                'icon': self.ready_img(Path(self.Base_dir / 'img\\main.ico')), 
                'banner': self.ready_img(Path(self.Base_dir / 'img\\banner.png')),
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
        self.donateURL = 'www.donationalerts.com/r/squeaknight'
        self.botArray = botArray
        self.botArrayLenght = 0
        self.tasks = []
        self.tasks.append(loop.create_task(self.mainPage(interval)))
        self.tasks.append(loop.create_task(self.updater(interval)))

    async def mainPage(self, interval):
        self.logo() 
        self.control_button()
        self.LogLabel()
  
        while await asyncio.sleep(interval, True):
            pass

    def logo(self):
        logo_frame = tk.Frame(
            self.master,
            bg='white'
        )
        logo1 = tk.Label(
            logo_frame,
            bd=-2,
            bg='white',
            fg='#31343b',
            text='Squeak', 
            font=('Tahoma', 16, 'bold'),
            cursor='hand2'
            )
        logo2 = tk.Label(
            logo_frame,
            bd=-2,
            bg='white',
            fg='Crimson',
            text='Fishing v2.0',
            font=('Tahoma', 16, 'bold'),
            cursor='hand2'
            )

        logo1.bind("<Button-1>", lambda e: self.callback(self.donateURL))
        logo2.bind("<Button-1>", lambda e: self.callback(self.donateURL))
        logo1.pack(side='left', anchor='n')
        logo2.pack(side='left', anchor='n')
        logo_frame.grid(row=0, column=1, sticky='nsew')
        logo_frame.place(x=5, y=5)
    
    def LogLabel(self):
        message_count = 1
        log_frame = tk.Frame(
            self.master,
            height=7
            )
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(
            log_frame,
            yscrollcommand=scrollbar.set,
            height=7
        )
        
        listbox.insert(tk.END, f'#{message_count} Welcome back')
        message_count += 1
        listbox.pack(fill=tk.BOTH)
        scrollbar.config(command=listbox.yview)
        log_frame.pack(side='bottom', fill=tk.X)
        listbox.insert(tk.END, f'#{message_count} Welcome back')
    

    def control_button(self):
        button_frame = tk.Frame(
            self.master,
            bg='white',
        )
        components = [
            {'title': 'Donate', 'command': lambda: self.callback(self.donateURL)},
            {'title': 'Resize windows', 'command': lambda: self.resizeBtn(self.botArray)}, #add func
            {'title': 'Clear Log', 'command': None}, #add func
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
        button_frame.grid(row=0, column=1,  sticky='nsew')
        button_frame.place(x=600, y=157.5)
    
    def resizeBtn(self):
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
        

