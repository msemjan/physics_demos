#!/usr/bin/env python3

"""
===========================
The double pendulum problem
===========================

This simple application allows its user to easily demonstrate the double 
pendulum problem and show how this system behaves for different initial 
conditions.

"""

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c


import tkinter 
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation



def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


class Pendulum:
    """
    This class contains data and methods important for the solution of 
    the double pendulum problem. 
    """
    def __init__(self, L1 = 1.0, L2 = 1.0, M1 = 1.0, M2 = 1.0,
                 th1 = 0.0, w1 = 0.0, th2 = 0.0, w2 = 0.0):
        self.G = 9.8  # acceleration due to gravity, in m/s^2
        self.L1 = L1  # length of pendulum 1 in m
        self.L2 = L2  # length of pendulum 2 in m
        self.M1 = M1  # mass of pendulum 1 in kg
        self.M2 = M2  # mass of pendulum 2 in kg

        # th1 and th2 are the initial angles (degrees)
        # w10 and w20 are the initial angular velocities (degrees per second)
        self.th1 = th1
        self.w1 = w1
        self.th2 = th2
        self.w2 = w2

        # create a time array from 0..100 sampled at 0.05 second steps
        self.dt = 0.05
        self.t = np.arange(0.0, 30, self.dt)

        # initial state
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

    def derivs(self, state, t):
        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        del_ = state[2] - state[0]
        den1 = (self.M1 + self.M2)*self.L1 - self.M2*self.L1*cos(del_)**2
        dydx[1] = (self.M2*self.L1*(state[1]**2)*sin(del_)*cos(del_) +
                   self.M2*self.G*sin(state[2])*cos(del_) +
                   self.M2*self.L2*(state[3]**2)*sin(del_) -
                   (self.M1 + self.M2)*self.G*sin(state[0]))/den1

        dydx[2] = state[3]

        den2 = (self.L2/self.L1)*den1
        dydx[3] = (-self.M2*self.L2*(state[3]**2)*sin(del_)*cos(del_) +
                   (self.M1 + self.M2)*self.G*sin(state[0])*cos(del_) -
                   (self.M1 + self.M2)*self.L1*(state[1]**2)*sin(del_) -
                   (self.M1 + self.M2)*self.G*sin(state[2]))/den2

        return dydx

    def set_th1(self, val):
        self.th1 = int(val)
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

    def set_th2(self, val):
        self.th2 = int(val)
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

    def set_w1(self, val):
        self.w1 = int(val)
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

    def set_w2(self, val):
        self.w2 = int(val)
        self.state = np.radians([self.th1, self.w1, self.th2, self.w2])

    def solve(self):
        """
        Solves the double pendulum problem for the currently set up initial 
        conditions and displays a short animation.
        """

        # integrate your ODE using scipy.integrate.
        self.y = integrate.odeint(self.derivs, self.state, self.t)

        self.x1 = self.L1*sin(self.y[:, 0])
        self.y1 = -self.L1*cos(self.y[:, 0])

        self.x2 = self.L2*sin(self.y[:, 2]) + self.x1
        self.y2 = -self.L2*cos(self.y[:, 2]) + self.y1

        fig = plt.figure()
        l = self.L1 + self.L2
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(-l, l), ylim=(-l, l))
        ax.grid()

        self.line, = ax.plot([], [], 'o-', lw=2)
        self.time_template = 'time = %.1fs'
        self.time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        ax.set_title("th1 = %d, th2 = %d, w1 = %d, w2 = %d"%(self.th1, self.th2, self.w1, self.w2))

        ani = animation.FuncAnimation(fig, self.animate, np.arange(1, len(self.y)),
                          interval=25, blit=True, init_func=self.init)

        # ani.save('double_pendulum.mp4', fps=15)
        plt.show()

    def init(self):
        self.line.set_data([], [])
        self.time_text.set_text('')
        return self.line, self.time_text

    def animate(self, i):
        thisx = [0, self.x1[i], self.x2[i]]
        thisy = [0, self.y1[i], self.y2[i]]

        self.line.set_data(thisx, thisy)
        self.time_text.set_text(self.time_template % (i*self.dt))
        return self.line, self.time_text


# Commands below are GUI-related 

root = tkinter.Tk()
root.wm_title("Double pendulum")
pendulum = Pendulum()


# Adds a slider and a lable for the Initial angle 1
lable1 = tkinter.Label(master=root, text="Initial angle 1 [deg]")
lable1.pack(side=tkinter.TOP, expand=1, fill='x')
scale1 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.HORIZONTAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   -360,
                       to           =   +360, 
                       command      =   pendulum.set_th1)
scale1.set(pendulum.th1)
scale1.pack(side=tkinter.TOP)

# Adds a slider and a lable for the initial angle 2
lable2 = tkinter.Label(master=root, text="Initial angle 2 [deg]")
lable2.pack(side=tkinter.TOP, expand=1, fill='x')
scale2 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.HORIZONTAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   -360,
                       to           =   +360, 
                       command      =   pendulum.set_th2)
scale2.set(pendulum.th2)
scale2.pack(side=tkinter.TOP)

# Adds a slider and a lable for the initial angular velocity 1
lable3 = tkinter.Label(master=root, text="Initial angular velocity 1 [deg/s]")
lable3.pack(side=tkinter.TOP, expand=1, fill='x')
scale3 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.HORIZONTAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   -1000,
                       to           =   +1000, 
                       command      =   pendulum.set_w1)
scale3.set(pendulum.w1)
scale3.pack(side=tkinter.TOP)

# Adds a slider and a lable for the initial angular velocity 2
lable4 = tkinter.Label(master=root, text="Initial angular velocity 2 [deg/s]")
lable4.pack(side=tkinter.TOP, expand=1, fill='x')
scale4 = tkinter.Scale(master       =   root,
                       orient       =   tkinter.HORIZONTAL,
                       length       =   300,
                       width        =   20,
                       resolution   =   1, 
                       sliderlength =   10,
                       from_        =   -1000,
                       to           =   +1000, 
                       command      =   pendulum.set_w2)
scale4.set(pendulum.w2)
scale4.pack(side=tkinter.TOP)

# Adds a button to redraw
button1 = tkinter.Button(master=root, text="Solve", command=pendulum.solve)
button1.pack(side=tkinter.RIGHT, expand=1, fill='x')

# Adds a button to quit
button2 = tkinter.Button(master=root, text="Quit", command=_quit)
button2.pack(side=tkinter.RIGHT, expand=1, fill='x')

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
