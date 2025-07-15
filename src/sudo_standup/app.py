from math import floor
from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread


class Counter(Thread):
    def __init__(self, duration: int, progress: tk.IntVar):
        super().__init__()
        self.elapsed = 0
        self.duration = duration*60
        self.progress = progress
        self.interrupt = False

    def stop(self):
        self.interrupt = True

    def reset(self):
        self.elapsed = 0
        self.interrupt = False
        self.progress.set(0)

    def run(self):
        while self.elapsed < self.duration and not self.interrupt:
            sleep(1)
            self.elapsed += 1
            self.progress.set(floor(100 * self.elapsed / self.duration))

        if not self.interrupt:
            sleep(1)


def counters(window: tk.Tk, progress: tk.IntVar, work: int, rest: int):
    work_counter = Counter(work, progress)
    rest_counter = Counter(rest, progress)

    def skip_break():
        window.iconify()
        window.attributes("-fullscreen", False) # type: ignore
        window.state('normal')
        window.geometry("640x480")
        button.place_forget()
        rest_counter.stop()

    button = ttk.Button(window, text='Skip break', command=skip_break)

    while True:
        window.iconify()
        window.attributes("-fullscreen", False) # type: ignore
        button.place_forget()
        work_counter.reset()
        work_counter.run()

        window.state('zoomed')
        window.attributes("-fullscreen", True) # type: ignore
        button.place(x=500, y=400)
        rest_counter.reset()
        rest_counter.run()


window = tk.Tk()
window.geometry("640x480")
window.title("sudo standup")

progress = tk.IntVar()
progressbar = ttk.Progressbar(variable=progress)
progressbar.place(x=300, y=300, width=200)

work = 2
rest = 1

Thread(target=counters, args=[window, progress, work, rest]).start()

window.mainloop()
