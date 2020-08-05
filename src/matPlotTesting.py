import matplotlib.pyplot as plt
import numpy as np
t=np.linspace(0,2*np.pi,100)
r=1
x=r*np.cos(t)
y=r*np.sin(t)
#different names make different plots
fig, beans= plt.subplots()
fig, ax= plt.subplots()

#adding more .plots to a fig adds more graphs, it does not over-ride the others
beans.plot(x,y,label='circle')
beans.plot(x*x,y*y,label='circle')

ax.plot(x**x,y*x)
#settings for the plot
beans.set_xlabel('x-axis')
beans.set_ylabel('y-axis')
beans.set_title('vrooom')
beans.legend() #Adds a legend


plt.show()

