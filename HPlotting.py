# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:03:07 2022

@author: oerskqpv
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#%%
####################################################################
        
##################----------- Plotting -----------##################   
plt.figure()
plt.plot(np.multiply(TotalHitsInit,Ni), Time_Store[:,0])
plt.title('Computation Time as a Function of Hits')# + ', Nmin = ' + str(Nmin))
plt.ylabel('Computation Time [s]')
plt.xlabel('Amount of Hits [-]')
plt.grid()

plt.figure()
plt.loglog(np.multiply(TotalHitsInit,Ni), Time_Store[:,0])
plt.title('Computation Time as a Function of Hits')# + ', Nmin = ' + str(Nmin))
plt.ylabel('Computation Time [s]')
plt.xlabel('Amount of Hits [-]')
plt.grid()

#%%
fig = plt.figure()
ax = plt.axes(projection='3d')
xdata = []
ydata = []
zdata = []
for i in range(len(Event_Log[0].Hits)):
    xdata.append(Event_Log[0].Hits[i].Hydrophone.X)
    ydata.append(Event_Log[0].Hits[i].Hydrophone.Y)
    zdata.append(Event_Log[0].Hits[i].Hydrophone.Z)
ax.scatter3D(xdata[1:-1], ydata[1:-1], zdata[1:-1], color = 'green', label = 'Hit Locations');       
ax.scatter3D(xdata[0], ydata[0], zdata[0], color = 'red', label = 'Root Hit')   
ax.scatter3D(Sources[0].X, Sources[0].Y, Sources[0].Z, color = 'blue', label = 'Source')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')  
ax.set_title('Hit Locations Plot')
ax.legend(loc = "upper left")
list_center = [(xdata[0],ydata[0],zdata[0])]
list_radius = [500]
ax.plot(xdata, zdata, 'r+', zdir='y', zs=500)
ax.plot(ydata, zdata, 'g+', zdir='x', zs=-500)
ax.plot(xdata, ydata, 'k+', zdir='z', zs=-500)

def plt_sphere(list_center, list_radius):
  for c, r in zip(list_center, list_radius):
    ax = fig.gca(projection='3d')

    # draw sphere
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = r*np.cos(u)*np.sin(v)
    y = r*np.sin(u)*np.sin(v)
    z = r*np.cos(v)
    zdummy = np.multiply(np.ones([50,50]),-500)

    # ax.plot_surface(x-c[0], y-c[1], z-c[2], color=np.random.choice(['g','b']), alpha=0.5*np.random.random()+0.5)
    # ax.plot(x, y, 'k+', zdir='z', zs=-500)
    # ax.plot_wireframe(x, y, z, color="r")
    ax.plot_wireframe(x, y, zdummy, color="r")
plt_sphere(list_center, list_radius) 
plt.show()


plt.figure()
plt.plot(xdata[1:-1], zdata[1:-1], 'g*')
plt.plot(xdata[0], zdata[0], 'r*', label = 'Root Hit')
plt.plot(Sources[0].X, Sources[0].Z, 'b*', label = 'Source')
xdummy = np.linspace(-500,500,1000)
z1 = np.multiply((zdata[0] + 100), np.ones(1000))
z2 = np.multiply((zdata[0] - 100), np.ones(1000))
plt.plot(xdummy, z1, 'r')
plt.plot(xdummy, z2, 'r')
plt.ylabel('Z-Location [m]')
plt.xlabel('X-Location [m]')
plt.title('Pancake Check X vs Z Plot')
plt.legend()

plt.figure()
plt.plot(ydata[1:-1], zdata[1:-1], 'g*')
plt.plot(ydata[0], zdata[0], 'r*', label = 'Root Hit')
plt.plot(Sources[0].Y, Sources[0].Z, 'b*', label = 'Source')
ydummy = np.linspace(-500,500,1000)
z1 = np.multiply((zdata[0] + 100), np.ones(1000))
z2 = np.multiply((zdata[0] - 100), np.ones(1000))
plt.plot(ydummy, z1, 'r')
plt.plot(ydummy, z2, 'r')
plt.ylabel('Z-Location [m]')
plt.xlabel('Y-Location [m]')
plt.title('Pancake Check Y vs Z Plot')
plt.legend()

#%%
plt.figure()
plt.plot(Ni, Average_Events_Detected[:,0])
plt.title('Average Events Detected as a function of N, runs = ' + str(runs) + ' FHits = ' + str(TotalHits) + '\n' + 'VSound = ' + str(Vsound) + ' m/s')
plt.ylabel('Number of Events Detected')
plt.xlabel('Number of Hydrophones (Nz = 5, Nx = Ny)')
#plt.xlabel('Number of Hydrophones (Random Locs)')       

plt.figure()
plt.plot(TotalHitsInit, Average_Events_Detected[0,:])
plt.title('Average Events Detected as a function of False Hits, runs = ' + str(runs) + ', N = ' + str(N) + '\n' + 'VSound = ' + str(Vsound) + ' m/s')
plt.ylabel('Average Number of Events Detected')
plt.xlabel('Number of False Hits per Hydrophone')
#plt.xlabel('Number of Hydrophones (Random Locs)')  

plt.figure()
plt.loglog(TotalHitsInit, Average_Events_Detected[0,:])
plt.title('Average Events Detected as a function of False Hits, runs = ' + str(runs) + ', N = ' + str(N) + '\n' + 'VSound = ' + str(Vsound) + ' m/s')
plt.ylabel('Average Number of Events Detected')
plt.xlabel('Number of False Hits per Hydrophone')   

plt.figure()
plt.plot(TotalHitsInit, Average_Hits_Event[0,:])
plt.title('Average Hits per Event as a function of False Hits, runs = ' + str(runs) + ', N = ' + str(N) + '\n' + 'VSound = ' + str(Vsound) + ' m/s')
plt.ylabel('Average Number of Hits per Event')
plt.xlabel('Number of False Hits per Hydrophone')   

#%%
# Note: Text files has lines with X,Y,Z,Time. Values are separated by a space.
with open('Event.txt', 'w') as f:
    for iwrite in range(len(Event_Log_Buffer[0].Hits)):
        f.write(str(Event_Log_Buffer[0].Hits[iwrite].Hydrophone.X) + ' ')
    f.write('\n')
    for iwrite in range(len(Event_Log_Buffer[0].Hits)):
        f.write(str(Event_Log_Buffer[0].Hits[iwrite].Hydrophone.Y) + ' ')
    f.write('\n')
    for iwrite in range(len(Event_Log_Buffer[0].Hits)):
        f.write(str(Event_Log_Buffer[0].Hits[iwrite].Hydrophone.Z) + ' ')
    f.write('\n')
    for iwrite in range(len(Event_Log_Buffer[0].Hits)):
        f.write(str(Event_Log_Buffer[0].Hits[iwrite].Time) + ' ')
    f.close()

#%%
# Note: Output is X,Y,Z,Time, so B[0] is a list with all X-Locations, B[1] with all Y-Locations etc.
A = []
with open('Event.txt') as f:
    for line in f:
        A.append(line.strip())
        print(line.strip())

    B = [None for x in range(len(A))]
    for i1 in range(len(A)):
        A_Temp = A[i1].split()
        B[i1] = []
        for i2 in range(len(A_Temp)):
            B[i1].append(float(A_Temp[i2]))
#%%
ALocX = []
ALocY = []
ALocZ = []
for i in range(len(Appended_Phones)):
    num = Appended_Phones[i]
    ALocX = np.append(ALocX, Hydrophones[num]['X'])
    ALocY = np.append(ALocY, Hydrophones[num]['Y'])
    ALocZ = np.append(ALocZ, Hydrophones[num]['Z'])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(ALocX, ALocY, ALocZ)

#%% 
# Compute Residuals Here, and see what noise residuals look like, use something like residual from average loc of event
HitLocsX = np.zeros(len(Event_Log[0].Hits))
HitLocsY = np.zeros(len(Event_Log[0].Hits))
HitLocsZ = np.zeros(len(Event_Log[0].Hits))

for i in range(len(Event_Log[0].Hits)):
    HitLocsX[i] = Event_Log[0].Hits[i].Hydrophone.X
    HitLocsY[i] = Event_Log[0].Hits[i].Hydrophone.Y
    HitLocsZ[i] = Event_Log[0].Hits[i].Hydrophone.Z
    
AverageX = np.mean(HitLocsX)
AverageY = np.mean(HitLocsY)
AverageZ = np.mean(HitLocsZ)

MeanLoc = HClasses.Source(AverageX, AverageY, AverageZ)

DistHits = np.zeros([len(Event_Log[0].Hits),len(Event_Log[0].Hits)])
Dt = np.zeros([len(Event_Log[0].Hits),len(Event_Log[0].Hits)])
    
for i1 in range(len(Event_Log[0].Hits)):
    DistHits[i1], Dt[i1] = HNuPulse.HDistSource(Event_Log[0].Hits[i1], MeanLoc, Vsound)

# DistHitsList = []
# DtList = []
# for i1 in range(len(Event_Log[0].Hits)):
#     for i2 in range(i1+1,len(Event_Log[0].Hits)):
#         DistHitsList.append(DistHits[i1,i2])
#         DtList.append(Dt[i1,i2])

plt.figure()
plt.plot(DistHits, Dt, '*')