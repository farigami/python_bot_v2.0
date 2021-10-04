import asyncio
import tkinter as tk
from tkinter.constants import END
from PIL import Image, ImageTk
import webbrowser
from pathlib import Path

class FishingGUI(tk.Frame):
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
        self.master.title('Fishing')
        if self.images:
            self.master.call('wm', 'iconphoto', self.master._w, self.images['icon'])
        self.master.configure(bg='#fff')
        self.master.geometry('735x435')
        self.master.maxsize(735, 435)
        self.master.minsize(735, 435)
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.donateURL = 'https://www.google.com/',
        self.botArray = botArray,
        self.main_end = main_end,
        self.controller_end = controller_end,
        self.tasks = []
        self.tasks.append(loop.create_task(self.mainPage(interval)))
        self.tasks.append(loop.create_task(self.updater(interval)))

    async def mainPage(self, interval):
        #self.logo()
        for i in range(5):
            for j in range(4):
                self.test= tk.Entry(
                    self.master,
                    bg='#d9d9d9',
                    # state=tk.DISABLED,
                    width=25,
                )
                self.test.grid(row=i, column=j)
    
                self.test.insert(END, i * j)



        while await asyncio.sleep(interval, True):
                pass


    def test_func(self):
        self.count += 1
        print(self.count)

    def logo(self):
        logo1 = tk.Label(
            self.master,
            bd=-2,
            bg='white',
            fg='#31343b',
            text='Squeak', 
            font=('Tahoma', 16, 'bold'),
            cursor='hand2'
            )
        logo2 = tk.Label(
            self.master,
            bd=-2,
            bg='white',
            fg='Crimson',
            text='Fishing',
            font=('Tahoma', 16, 'bold'),
            cursor='hand2'
            )

        logo1.bind("<Button-1>", lambda e: self.callback(self.donateURL))
        logo2.bind("<Button-1>", lambda e: self.callback(self.donateURL))
        logo1.pack(side='left', anchor='n')
        logo2.pack(side='left', anchor='n')

    def callback(self, url):
        webbrowser.open_new(url)

    def ready_img(self, path, size=False):
        if size:
            return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ANTIALIAS))
        return ImageTk.PhotoImage(Image.open(path))

    async def updater(self, interval):
        while await asyncio.sleep(interval, True):
            self.update()

        
    def close(self):
        self.main_end
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()
        print(self.botArray)

