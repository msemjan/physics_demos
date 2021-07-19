#!/usr/bin/env python3

import tkinter
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from matplotlib.figure import Figure  

root = tkinter.Tk()
root.wm_title("Ising model")

fig = Figure(figsize=(4, 2)) #, dpi=100)
subplot = fig.add_subplot(1,1,1)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.



def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

class Lattice:
    def __init__(self, J: float, L: int, h: float):
        self.L = L
        self.h = h
        self.J = J
        self.n_steps = 100
        self.get_random_state()
        self.set_beta(2.0)
        self.energy = self.get_energy()
        self.m = np.sum(self.s)
        self.X, self.Y = np.meshgrid(range(L), range(L))

    def get_energy(self):
        energy = 0.0
        for i in range(self.L):
            for j in range(self.L):
                energy -= 0.5 * self.s[i][j]*(self.J*(self.s[i][(j+1)%self.L] +
                                                      self.s[i][(j-1)%self.L] +
                                                      self.s[(i+1)%self.L][j] +
                                                      self.s[(i-1)%self.L][j])+
                                              self.h)
        return energy

    def get_random_state(self):
        self.s = 2*np.random.randint(2, size=(self.L, self.L)) - 1
        self.energy = self.get_energy()
        self.m = np.sum(self.s)

    def reset_state(self):
        self.get_random_state()
        global fig
        self.draw(fig)

    def update(self):
        for i in range(self.L):
            for j in range(self.L):
                dE = 2*self.s[i][j]*(self.J*(self.s[i][(j+1)%self.L] + 
                                             self.s[i][(j-1)%self.L] +
                                             self.s[(i+1)%self.L][j] + 
                                             self.s[(i-1)%self.L][j])+
                                     self.h)

                if np.random.rand() < np.exp(-dE*self.beta):
                    self.energy += dE
                    self.m -= 2*self.s[i][j]
                    self.s[i][j] *= -1

    def set_beta(self, val):
        self.beta = int(val)/1000

    def set_field(self, val):
        self.h = int(val)/10

    def draw(self, fig):
        global canvas
        plt.pcolormesh(self.s, cmap=plt.cm.RdBu);
        plt.title('Beta = %f, h = %f, E = %f, m = %f'%(
                  self.beta, self.h, self.energy/(self.L**2), 
                  self.m/(self.L**2)))
        plt.pause(0.01)
        canvas.draw()
        
    def set_n_steps(self, val):
        self.n_steps = int(val)

    def simulate(self):
        global fig
        for n in range(self.n_steps):
            self.update()
            self.draw(fig)

model = Lattice(1.0, 30, 0.0)
model.draw(subplot)
canvas.draw()


# Adds a slider and a lable for the number of MC steps (athough, these should 
# be called sweeps, to be honest)
lable1 = tkinter.Label(master=root, text="Steps")
lable1.pack(side=tkinter.LEFT, expand=1, fill='x')
scale1 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.VERTICAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   10,
                       to           =   50, 
                       command      =   model.set_n_steps)
scale1.set(model.n_steps)
scale1.pack(side=tkinter.LEFT)

# Adds a slider and a lable for the number of the inverse temperature beta
lable2 = tkinter.Label(master=root, text="Beta")
lable2.pack(side=tkinter.LEFT, expand=1, fill='x')
scale2 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.VERTICAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   0,
                       to           =   2000, 
                       command      =   model.set_beta)
#scale2.set(model.beta)
scale2.set(0.0)
scale2.pack(side=tkinter.LEFT)

# Adds a slider and a lable for the number of the inverse temperature field
lable3 = tkinter.Label(master=root, text="Field")
lable3.pack(side=tkinter.LEFT, expand=1, fill='x')
scale3 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.VERTICAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   -10,
                       to           =   +10, 
                       command      =   model.set_field)
#scale3.set(model.beta)
scale3.set(0.0)
scale3.pack(side=tkinter.LEFT)

# Adds a button to redraw
button1 = tkinter.Button(master=root, text="Simulate", command=model.simulate)
button1.pack(side=tkinter.BOTTOM, expand=1, fill='x')

# Adds a button to get random state
button2 = tkinter.Button(master=root, text="Random State", command=
        model.reset_state)
button2.pack(side=tkinter.BOTTOM, expand=1, fill='x')

# Adds a button to quit
button3 = tkinter.Button(master=root, text="Quit", command=_quit)
button3.pack(side=tkinter.BOTTOM, expand=1, fill='x')

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
