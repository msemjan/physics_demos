#!/usr/bin/env python3

import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from math import sqrt, floor

import numpy as np


class Walker_data_wrapper:
    def __init__(self):
        self.n_steps = 50
        self.n_walkers = 50
        self.position = np.zeros([1, self.n_walkers], dtype = int)

    # Setters
    def set_number_of_walkers(self, val):
        self.n_walkers = floor(int(val))

    def set_number_of_steps(self, val):
        self.n_steps = floor(int(val))

    def set_step_len(self, val):
        self.step_len = float(val)

    def reset_walker(self):
        self.position = np.zeros([1, self.n_walkers], dtype = int)
    
    def move_randomly(self):
        self.position += 2*(np.random.rand(1,self.n_walkers)<0.5)-1

walkers = Walker_data_wrapper()

root = tkinter.Tk()
root.wm_title("Opitý námorník - Jednorozmerný prípad")

fig = Figure(figsize=(4, 2)) #, dpi=100)
#fig = Figure() #, dpi=100)
t = np.arange(0, 3, .01)

subplot_distri = fig.add_subplot(1,1,1)
#  subplot_distri.hist(np.transpose(walkers.position), bins = 'auto', align='mid')
subplot_distri.hist(np.transpose(walkers.position), bins = floor(walkers.n_steps) + 1, align = 'mid')
#subplot_distri.axis([-walkers.n_steps/2, walkers.n_steps/2, 0, walkers.n_walkers])
subplot_distri.set_xlim(left = -walkers.n_steps/2, right = walkers.n_steps/2)
#subplot_distri.hist(walkers.position, bins = 'auto')

fig2 = Figure(figsize=(4,2))
#fig2 = Figure()
subplot = fig2.add_subplot(1,1,1)
subplot.scatter(np.zeros([1, walkers.n_walkers], dtype = int), np.zeros([1, walkers.n_walkers], dtype = int))



canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas2 = FigureCanvasTkAgg(fig2, master=root)  # A tk.DrawingArea.

#subplot.axis([-10*walkers.step_len, 10*walkers.step_len, -10*walkers.step_len, 10*walkers.step_len])
subplot.axis([-8, 8, -8, 8])
subplot.grid()
canvas.draw()
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

canvas2.draw()
#canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


# Drawing of trajectories
def redraw():
    global walkers, canvas, canvas2, fig, t, subplot, subplot_distri
    walkers.reset_walker()
    
    z = np.zeros([1, walkers.n_walkers], dtype = int)
    
    
    for ii in range(walkers.n_steps):
        walkers.move_randomly()
        subplot.clear()    
        subplot.axis([-walkers.n_steps/2, walkers.n_steps/2, -1, 1])
        subplot.grid()
        
        subplot.scatter(np.transpose(walkers.position) , np.transpose(z), color='blue')
        #  plt.pause(0.05)
        canvas2.draw()

        if ii % 10 == 0:
            subplot_distri.clear()
            #  subplot_distri.hist(np.transpose(walkers.position), bins = 'auto', align = 'mid')
            subplot_distri.hist(np.transpose(walkers.position), bins = floor(walkers.n_steps/10) + 1, align = 'mid')
            #subplot_distri.axis([-walkers.n_steps/2, walkers.n_steps/2, 0, walkers.n_walkers])
            subplot_distri.set_xlim(left = -walkers.n_steps/2, right = walkers.n_steps/2)
            canvas.draw()

    subplot_distri.clear()
    #subplot_distri.hist(np.transpose(walkers.position), bins = 'auto')
    subplot_distri.hist(np.transpose(walkers.position), bins = floor(walkers.n_steps/10) + 1, align = 'mid')
    #subplot_distri.axis([-walkers.n_steps/2, walkers.n_steps/2, 0, walkers.n_walkers])
    subplot_distri.set_xlim(left = -walkers.n_steps/2, right = walkers.n_steps/2)
    canvas.draw()
    
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


# Adds a slider and a lable for the number of random walkers
lable_walkers = tkinter.Label(master=root, text="Počet chodcov")
lable_walkers.pack(side=tkinter.LEFT, expand=1, fill='x')
scale_walkers = tkinter.Scale(master=root,orient=tkinter.HORIZONTAL,length=300,width=20,
                      resolution=1, sliderlength=10,from_=0,to=1000, command=walkers.set_number_of_walkers)
scale_walkers.set(walkers.n_walkers)
scale_walkers.pack(side=tkinter.LEFT)

# Adds a slider and a lable for the number of steps
lable_steps = tkinter.Label(master=root, text="Počet krokov")
lable_steps.pack(side=tkinter.LEFT, expand=1, fill='x')
scale_steps = tkinter.Scale(master=root,orient=tkinter.HORIZONTAL,length=300,width=20,
                      resolution=1, sliderlength=10,from_=1,to=1000, command=walkers.set_number_of_steps)
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

