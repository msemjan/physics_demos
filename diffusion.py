import numpy as np
import matplotlib.pyplot as plt

class Experiment:
    def __init__(self, x_max = 2.0, y_max = 2.0, n = 50,
            dx_max = 0.1, dy_max = 0.1, barrier = False):
        self.x_max = x_max
        self.y_max = y_max
        
        self.dx_max = dx_max
        self.dy_max = dy_max

        self.n = n
        self.barrier = barrier

        if not self.barrier:
            self.x = 2*x_max*np.random.rand(self.n,1)-x_max
        else:
            self.x = -x_max*np.random.rand(self.n,1)

        self.y = 2*y_max*np.random.rand(self.n,1)-y_max

    def move(self):
        dx = 2*self.dx_max*np.random.rand(self.n,1)-self.dx_max
        dy = 2*self.dy_max*np.random.rand(self.n,1)-self.dy_max

        if not self.barrier:
            self.x[abs(self.x+dx)<self.x_max] += dx[abs(self.x+dx)<self.x_max]
        else:
            self.x[np.logical_and(0<=-(self.x+dx),-(self.x+dx)<self.x_max)] += dx[np.logical_and(0<=-(self.x+dx),-(self.x+dx)<self.x_max)]


        self.y[abs(self.y+dy)<self.y_max] += dy[abs(self.y+dy)<self.y_max]

    def draw(self, fig):
        fig.clear()
        fig.scatter(self.x, self.y)
        fig.set_xlim(right=self.x_max, left=-self.x_max)
        fig.set_ylim(top=self.y_max, bottom=-self.y_max)
        plt.pause(0.05)
        #plt.show()

dif = Experiment(barrier=True)

fig = plt.figure()
sub = plt.subplot(111)
dif.draw(sub)
#plt.show()

for ii in range(1000):
    dif.move()
    dif.draw(sub)
    if ii == 500:
        dif.barrier = False




