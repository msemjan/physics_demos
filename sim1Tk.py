#!/usr/bin/env python3

import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from math import sqrt, floor

import numpy as np

class Walker_data_wrapper:
    def __init__(self):
        self.step_len = 1
        self.n_steps = 100000
        self.n_walkers = 1

    # Setters
    def set_number_of_walkers(self, val):
        self.n_walkers = floor(int(val))

    def set_number_of_steps(self, val):
        self.n_steps = floor(int(val))

    def set_step_len(self, val):
        self.step_len = float(val)

walkers = Walker_data_wrapper()

root = tkinter.Tk()
root.wm_title("Opitý námorník - Dvojrozmerný prípad AKA Difúzia")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
subplot = fig.add_subplot(111)
subplot.plot(np.zeros([1, walkers.n_walkers], dtype = int), np.zeros([1, walkers.n_walkers], dtype = int))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

#subplot.axis([-10*walkers.step_len, 10*walkers.step_len, -10*walkers.step_len, 10*walkers.step_len])
subplot.axis([-8, 8, -8, 8])
subplot.grid()
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


# Drawing of trajectories
def redraw():
    global walkers, canvas, fig, t, subplot
    
    #print("n_steps=",walkers.n_steps,"\nn_walkers=",walkers.n_walkers)
    
    subplot.clear()

    for i_walker in range(walkers.n_walkers):
        x = np.cumsum(walkers.step_len*(2*np.random.rand(1, walkers.n_steps)-1)/sqrt(walkers.n_steps))
        y = np.cumsum(walkers.step_len*(2*np.random.rand(1, walkers.n_steps)-1)/sqrt(walkers.n_steps))

        subplot.axis([-8, 8, -8, 8])
        subplot.grid()
        subplot.plot(x, y)
    canvas.draw()
    

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# Adds a slider and a lable for the length of the steps
lable_len = tkinter.Label(master=root, text="Dĺžka kroku")
lable_len.pack(side=tkinter.LEFT, expand=1, fill='x')
scale_len = tkinter.Scale(master=root,orient=tkinter.HORIZONTAL,length=300,width=20,
                      resolution=.1, sliderlength=10,from_=0,to=4, command=walkers.set_step_len)
scale_len.set(walkers.step_len)
scale_len.pack(side=tkinter.LEFT)

# Adds a slider and a lable for the number of random walkers
lable_walkers = tkinter.Label(master=root, text="Počet chodcov")
lable_walkers.pack(side=tkinter.LEFT, expand=1, fill='x')
scale_walkers = tkinter.Scale(master=root,orient=tkinter.HORIZONTAL,length=300,width=20,
                      resolution=1, sliderlength=10,from_=0,to=100, command=walkers.set_number_of_walkers)
scale_walkers.set(walkers.n_walkers)
scale_walkers.pack(side=tkinter.LEFT)

# Adds a slider and a lable for the number of steps
lable_steps = tkinter.Label(master=root, text="Počet krokov")
lable_steps.pack(side=tkinter.LEFT, expand=1, fill='x')
scale_steps = tkinter.Scale(master=root,orient=tkinter.HORIZONTAL,length=300,width=20,
                      resolution=1, sliderlength=10,from_=1,to=10000, command=walkers.set_number_of_steps)
scale_steps.set(walkers.n_steps)
scale_steps.pack(side=tkinter.LEFT)


# Adds a button to redraw
button = tkinter.Button(master=root, text="Redraw", command=redraw)
button.pack(side=tkinter.RIGHT, expand=1, fill='x')

# Adds a button to quit
button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.RIGHT, expand=1, fill='x')

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
