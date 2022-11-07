# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:42:02 2022

@author: oerskqpv
"""

import numpy as np
import math
import copy
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# This code is written with the aim to investigate the efficiency and false alarm rates
# of an array of hydrophones. We use both these as input parameters for this simulation.
# This code uses a predetermined arrangement of Hydrophones
#--- Version 4 ---#
# In this version we will improve the algorithm. We will implement functions,
# and a new Clique algorithm involving rotations and root hits.

# Code Timing #
st = time.time()

##################----------- Input Parameters -----------##################

# Timeslices #ub    
runs = 10  # Number of Timeslices
Hitsrange = [0,1]       # Size of Timeslice

# Hydrophone Locations #
LocID = 2   # [0 = Random, 2 = Evenly Spaced + Clusters]
Nxi = [5]#[1,2,3,4,5,6,7,8,9,10]#np.ones(200,dtype=int)#[4]          # Same length as Nyi, Nzi
Nyi = [5]#[1,2,3,4,5,6,7,8,9,10]#np.ones(200,dtype=int)#[4]           # Same length as Nxi, Nzi
Nzi = [5]#[5,5,5,5,5,5,5,5,5,5]#np.linspace(1,200,200,dtype=int)#[5]#[5,5,5,5,5]#,12,16,18]#,8,10,12,14,16]#,12,14,16]  # Amount of Hydrophones in z-direction, sqrt(N/Nz) needs to be an integer!! (e.g. 100,4) or needs to be 25
Nxyi = np.multiply(Nxi, Nyi)
Cluster_Size = 1  # Amount of Hydrophones at a z-location
Z_Spacing = 1     # Spacing in Cluster in [m], only relevant if Cluster_Size > 1
Ni = np.multiply(Nxyi, Nzi) * Cluster_Size     # Number of Hydrophones
D = 3      # Number of Dimensions, (x,y,z)
xrange = [-500,500]   # XLoc range in meters      
yrange = [-500,500]   # YLoc range in meters
zrange = [-500,500]   # ZLoc range in meters

# False Hits + Amplitudes #
TotalHitsInit = [1,2,3,4,5,6,7,8,9,10,12,16,20]#11,12,13,14,15,16,17,18,19,20]#[5,10,20,30,40,60,80,100,120,160]   # 5 per 10 seconds
Amprange = [4,10]      # dB range of hits (Check whether assumed values are correct!!)
Source_Amp = 20        # Amplitude of Source

# Source Location #
Source_X = 0
Source_Y = 0
Source_Z = 0
Source_Loc = [Source_X, Source_Y, Source_Z]
ThetaX = (30/180) * np.pi     # Incoming angle neutrino in radians
ThetaY = (30/180) * np.pi     # Incoming angle neutrino in radians
PanDepth = 100                # Depth of Pancake in m

# Physical Constants & Parameters #
Vsound = 1.5e3  # Sound velocity in water in m/s

# Initializing #


#####################################################################

##################----------- Functions -----------##################

def HLocationAlg(xrange, yrange, zrange, Z_Spacing, Cluster_Size, LocID, Nx, Ny, Nz):
    # This function creates the Hydrophone locations
    if LocID == 2:
        Locs_Initx = np.linspace(xrange[0], xrange[1], Nx)
        Locs_Inity = np.linspace(yrange[0], yrange[1], Ny)
        Locs_Initz = np.linspace(zrange[0], zrange[1], Nz)
        Fill_Count = 0
        for i in range(Nx):
            
            for j in range(Ny):
                
                for k in range(Nz):
                    
                    for l in range(Cluster_Size):
                        Locs[Fill_Count ,0] = Locs_Initx[i]
                        Locs[Fill_Count ,1] = Locs_Inity[j]
                        Locs[Fill_Count ,2] = Locs_Initz[k] + l * Z_Spacing
                        Fill_Count += 1
                        
        return Locs
            
    if LocID == 0:# and Cluster_Size == 0:   # !! Is the == 0 necessary? !! 
        N = Nx * Ny * Nz
        Locs[:,0] = np.random.randint(xrange[0],xrange[1],N)   # x Locations
        Locs[:,1] = np.random.randint(yrange[0],yrange[1],N)#np.zeros(N)   # Y Locations
        Locs[:,2] = np.random.randint(zrange[0],zrange[1],N)  # Z Locations
        
        return Locs

def HDictCreator(Locs, N):
    # This function creates a dict entry for each Hydrophone with name, location, hits, amplitude
    for Hnum in range(N):
        Hydrophones[Hnum] = None
        Name = "X" + str(Locs[Hnum,0]) + "Y" + str(Locs[Hnum,1]) + "Z" + str(Locs[Hnum,2])
        Hydrophones[Hnum] = {'ID':Name, 'X': Locs[Hnum,0], 'Y': Locs[Hnum,1], 'Z': Locs[Hnum,2], 'H': [], 'A': []}
        
    return Hydrophones

def HDictAppender(Hitsrange, TotalHits, Hydrophones, Amprange, N):
    # This function adds random False Hits + Amplitudes to the Hydrophones dict
    for Hnum in range(N):
        Hydrophones[Hnum]['H'] = []
        Hits = np.sort(np.random.uniform(Hitsrange[0], Hitsrange[1],TotalHits))
        Amplitudes = np.random.uniform(Amprange[0], Amprange[1],TotalHits)
        Hydrophones[Hnum]['H'] = np.append(Hydrophones[Hnum]['H'],Hits)
        
    return Hydrophones

def HDistSource(Hydrophones, Source_Loc, Vsound):
    # This function calculates the distance and time to the source from a Hydrophone
    for i in range(N):
        Dist[i] = math.sqrt((Hydrophones[i]['X'] - Source_Loc[0])**2 + \
                            (Hydrophones[i]['Y'] - Source_Loc[1])**2 + \
                                (Hydrophones[i]['Z'] - Source_Loc[2])**2)
        Time_Pulse[i] =  Dist[i] / Vsound
        
    return Dist, Time_Pulse

def HPulseAppender(Hydrophones, Time_Pulse, LocZH, Source_Z, PanDepth):
    # This function adds the time of the pulse to the Hits of the Hydrophone dict
    Appended_Phones = []
    Appended_Pulses = []
    for i in range(N):
        if LocZH[i] <= Source_Z + PanDepth/2 and LocZH[i] >= Source_Z - PanDepth/2:
            Hydrophones[i]['H'] = np.append(Hydrophones[i]['H'],Time_Pulse[i])
            Hydrophones[i]['H'] = np.sort(Hydrophones[i]['H'])
            Appended_Phones = np.append(Appended_Phones,i)
            Appended_Pulses = np.append(Appended_Pulses, Time_Pulse[i])
    return Hydrophones, Appended_Phones, Appended_Pulses

def HTimeDiff(LocX1, LocX2, LocY1, LocY2, LocZ1, LocZ2):
    Dist = math.sqrt((LocX1 - LocX2)**2 + \
                        (LocY1 - LocY2)**2 + \
                            (LocZ1 - LocZ2)**2)
    DT = Dist / Vsound
    
    return DT

def HMatch(Hit1, Hit2, LocX1, LocX2, LocY1, LocY2, LocZ1, LocZ2):
    Dt = abs(Hit1 - Hit2)
    Time_Diff = HTimeDiff(LocX1, LocX2, LocY1, LocY2, LocZ1, LocZ2)
    TMargin = 1e-8      # 10 ns, ! maybe find a better way to implement this & value !
    
    return Time_Diff + TMargin >= Dt

def HHitSorter(Hydrophones, N):
    LocX = []
    LocY = []
    LocZ = []
    LocH = []
    Hits = []
    for i in range(N):
        for j in range(len(Hydrophones[i]['H'])):
            Hits = np.append(Hits,Hydrophones[i]['H'][j])
            LocX = np.append(LocX,Hydrophones[i]['X'])
            LocY = np.append(LocY,Hydrophones[i]['Y'])
            LocZ = np.append(LocZ,Hydrophones[i]['Z'])
            LocH = np.append(LocH,i)
    
    HitsInd = Hits.argsort()
    LocX = LocX[HitsInd[::1]]
    LocY = LocY[HitsInd[::1]]
    LocZ = LocZ[HitsInd[::1]]
    LocH = LocH[HitsInd[::1]]
    Hits = Hits[HitsInd[::1]]
    
    #Loc[0,:] = LocX
    #Loc[1,:] = LocY
    #Loc[2,:] = LocZ
    #Loc[3,:] = LocH
    
    return Hits, LocX, LocY, LocZ, LocH

def HRotateX(LocX, LocY, LocZ, ThetaX):
    # This function rotates around the x-axis
    Y1 = np.multiply(LocY, np.cos(ThetaX))
    Y2 = -np.multiply(LocZ, np.sin(ThetaX))
    LocYY = np.add(Y1, Y2)    # Check These Formulas
    
    Z1 = np.multiply(LocY, np.sin(ThetaX))
    Z2 = np.multiply(LocZ, np.cos(ThetaX))
    LocZZ = np.add(Z1, Z2)
    
    return LocYY, LocZZ

def HRotateY(LocX, LocY, LocZ, ThetaY):
    # This function rotates around the y-axis
    X1 = np.multiply(LocX, np.cos(ThetaY))
    X2 = np.multiply(LocZ, np.sin(ThetaY))
    LocXX = np.add(X1, X2)
    
    Z1 = -np.multiply(LocX, np.sin(ThetaY))
    Z2 = np.multiply(LocZ, np.cos(ThetaY))
    LocZZ = np.add(Z1, Z2)
    
    return LocXX, LocZZ

def HClique(Hits, LocX, LocY, LocZ, LocH, Nmin):
    Count = np.ones(len(Hits))   # Assume match with self
    # Look for Causal Hits & add to Counter #
    for i in range(len(Hits)-1):
        for j in range(i+1, len(Hits)):
            if HMatch(Hits[i], Hits[j], LocX[i], LocX[j], LocY[i], LocY[j], LocZ[i], LocZ[j]):
                Count[i] += 1
                Count[j] += 1
                
    # Now run Clique algorithm to remove hits with least amount of correlated hits
    
    # Structure infinitely running loop, 
    p = 1
    while p>0:
        j = 0
        M = 0
        n = len(Hits)
        for i in range(n):
            if Count[i] < Count[j]:
                j = i
            if Count[i] >= Nmin:
                M += 1
            
        if Count[j] == n:     # number of associated hits is equal to the number of (remaining) hits
            return Hits, Count, LocX, LocY, LocZ, LocH
    
       # if M < Nmin:         # maximal number of associated hits is less than the specified minimum
        #    return Hits, Count, LocX, LocY, LocZ, LocH
    
    # Swap selected Hit to end
        Hits[j], Hits[n-1] = Hits[n-1], Hits[j]
        Count[j], Count[n-1] = Count[n-1], Count[j]
        LocX[j], LocX[n-1] = LocX[n-1], LocX[j]
        LocY[j], LocY[n-1] = LocY[n-1], LocY[j]
        LocZ[j], LocZ[n-1] = LocZ[n-1], LocZ[j]
        LocH[j], LocH[n-1] = LocH[n-1], LocH[j]
  
    # Decrease number of associated hits for each associated hits
        for i in range(n-1):
            if HMatch(Hits[i], Hits[n-1], LocX[i], LocX[n-1], LocY[i], LocY[n-1], LocZ[i], LocZ[n-1]):
                Count[i] -=1
                Count[n-1] -=1
                
            if Count[n-1] == 1:
                Hits = np.delete(Hits, n-1)
                Count = np.delete(Count, n-1)    # This is not really needed!
                break
            
def HLocationGet(Hydrophones, N):
    # This function retrieves the Hydrophone locations and stores them in an array
    LocXH = []
    LocYH = []
    LocZH = []
    for i in range(N):
        LocXH = np.append(LocXH,Hydrophones[i]['X'])
        LocYH = np.append(LocYH,Hydrophones[i]['Y'])
        LocZH = np.append(LocZH,Hydrophones[i]['Z'])

    return LocXH, LocYH, LocZH

def HEvent(Hits, LocX, LocY, LocZ, LocH, Nmin, PanDepth):
    # This function checks whether a hit has enough correlated hits within its pancake,
    # if this is the case, the Clique algorithm is employed, then if enough correlated
    # hits remain an event is created in the Event_Log with these hits.
    Event_Log = {}
    Event_Count = -1
    for pan1 in range(len((Hits)-1)):
        Buffer = []
        BufferX = []
        BufferY = []
        BufferZ = []
        BufferH = []
        BufferC = []
        Buffer = np.append(Buffer, Hits[pan1])
        BufferX = np.append(BufferX, LocX[pan1])
        BufferY = np.append(BufferY, LocY[pan1])
        BufferZ = np.append(BufferZ, LocZ[pan1])
        BufferH = np.append(BufferH, LocH[pan1])
        for pan2 in range(pan1+1, len(Hits)):
            if LocZ[pan2] <= LocZ[pan1] + PanDepth and LocZ[pan2] >= LocZ[pan1] - PanDepth and HMatch(Hits[pan1], Hits[pan2], LocX[pan1], LocX[pan2], LocY[pan1], LocY[pan2], LocZ[pan1], LocZ[pan2]):
                Buffer = np.append(Buffer, Hits[pan2])
                BufferX = np.append(BufferX, LocX[pan2])
                BufferY = np.append(BufferY, LocY[pan2])
                BufferZ = np.append(BufferZ, LocZ[pan2])
                BufferH = np.append(BufferH, LocH[pan2])
        if len(Buffer) >= Nmin:
            Buffer, BufferC, BufferX, BufferY, BufferZ, BufferH = HClique(Buffer, BufferX, BufferY, BufferZ, BufferH, Nmin)
            if len(Buffer) >= Nmin:
                Event_Count +=1
                Event_Log[Event_Count] = {'H':Buffer, 'X':BufferX, 'Y':BufferY, 'Z':BufferZ, 'HP':BufferH, 'C':BufferC}
                
    return Event_Log

def HSortEventLog(Event_Log):
    # This function sorts all the data according to ascending order of the hits
    for isort in range(len(Event_Log)):
        SortIndex = Event_Log[isort]['H'].argsort()
        Event_Log[isort]['C'] = Event_Log[isort]['C'][SortIndex[::1]]
        Event_Log[isort]['HP'] = Event_Log[isort]['HP'][SortIndex[::1]]
        Event_Log[isort]['X'] = Event_Log[isort]['X'][SortIndex[::1]]
        Event_Log[isort]['Y'] = Event_Log[isort]['Y'][SortIndex[::1]]
        Event_Log[isort]['Z'] = Event_Log[isort]['Z'][SortIndex[::1]]
        Event_Log[isort]['H'] = Event_Log[isort]['H'][SortIndex[::1]]
        
    return Event_Log

# def HEventMerger(Event_Log_Buffer):
#     # This function merges events which have overlap (e.g tb1<=tb2 and te1>=te2)
#     Event_Merge_Count = np.zeros(len(Event_Log_Buffer))
#     for imerg1 in Event_Log_Buffer:
#         t_begin1 = Event_Log_Buffer[imerg1]['H'][0]
#         t_end1 = Event_Log_Buffer[imerg1]['H'][-1]
#         for imerg2 in Event_Log_Buffer:
#             if imerg1 != imerg2:
#                 t_begin2 = Event_Log_Buffer[imerg2]['H'][0]
#                 t_end2 = Event_Log_Buffer[imerg2]['H'][-1]
#                 if t_begin1 >= t_begin2 and t_end1 <= t_end2:
#                     Event_Log_Buffer[imerg2]['H'] = np.append(Event_Log_Buffer[imerg2]['H'], Event_Log_Buffer[imerg1]['H'])
#                     Event_Log_Buffer[imerg2]['C'] = np.append(Event_Log_Buffer[imerg2]['C'], Event_Log_Buffer[imerg1]['C'])                                                          
#                     Event_Log_Buffer[imerg2]['HP'] = np.append(Event_Log_Buffer[imerg2]['HP'], Event_Log_Buffer[imerg1]['HP'])
#                     Event_Log_Buffer[imerg2]['X'] = np.append(Event_Log_Buffer[imerg2]['X'], Event_Log_Buffer[imerg1]['X'])
#                     Event_Log_Buffer[imerg2]['Y'] = np.append(Event_Log_Buffer[imerg2]['Y'], Event_Log_Buffer[imerg1]['Y'])
#                     Event_Log_Buffer[imerg2]['Z'] = np.append(Event_Log_Buffer[imerg2]['Z'], Event_Log_Buffer[imerg1]['Z'])
#                 # Insert Sorting Algorithm here!! Done!
#                     SortInd = Event_Log_Buffer[imerg2]['H'].argsort()
#                     Event_Log_Buffer[imerg2]['C'] = Event_Log_Buffer[imerg2]['C'][SortInd[::1]]
#                     Event_Log_Buffer[imerg2]['HP'] = Event_Log_Buffer[imerg2]['HP'][SortInd[::1]]
#                     Event_Log_Buffer[imerg2]['X'] = Event_Log_Buffer[imerg2]['X'][SortInd[::1]]
#                     Event_Log_Buffer[imerg2]['Y'] = Event_Log_Buffer[imerg2]['Y'][SortInd[::1]]
#                     Event_Log_Buffer[imerg2]['Z'] = Event_Log_Buffer[imerg2]['Z'][SortInd[::1]]
#                     Event_Log_Buffer[imerg2]['H'] = Event_Log_Buffer[imerg2]['H'][SortInd[::1]]
                    
#                     Event_Merge_Count[imerg1] += 1
    
#     for idel in range(len(Event_Merge_Count)):
#         if Event_Merge_Count[idel] >= 1:
#             del Event_Log_Buffer[idel]
            
#     return Event_Log_Buffer, Event_Merge_Count

# Here write a new HEventMerger function which merges the data according to the feedback from Maarten,
# also keep the previous function for now, in case shit hits the fan and stuff breaks.
# Furthermore, fix the delete issue, revolving around symmetric pulses causing every event to have at least one merge.
# Code will probably require a while loop, as I will be deleting events which are merged into another event.
def HEventMerger(Event_Log_Buffer):
    # This function merges events which have overlap (e.g tb1<=tb2<te1)
    Dummy = 1
    Last_Entry = 0
    for ilastget in Event_Log_Buffer:
        Last_Entry = ilastget
    Event_Merge_Count = np.zeros(Last_Entry+1)
    
    while Dummy>0:
        if len(Event_Log_Buffer) == 0:
            break
        
        for ilastget in Event_Log_Buffer:
            Last_Entry = ilastget
            
        for imerg1 in Event_Log_Buffer:
            Del_Holder = 0
            t_begin1 = Event_Log_Buffer[imerg1]['H'][0]
            t_end1 = Event_Log_Buffer[imerg1]['H'][-1]
            for imerg2 in Event_Log_Buffer:
                if imerg1 != imerg2:
                    t_begin2 = Event_Log_Buffer[imerg2]['H'][0]
                    t_end2 = Event_Log_Buffer[imerg2]['H'][-1]
                    if t_begin2 >= t_begin1 and t_begin2 <= t_end1:
                        Event_Log_Buffer[imerg1]['H'] = np.append(Event_Log_Buffer[imerg1]['H'], Event_Log_Buffer[imerg2]['H'])
                        Event_Log_Buffer[imerg1]['C'] = np.append(Event_Log_Buffer[imerg1]['C'], Event_Log_Buffer[imerg2]['C'])                                                          
                        Event_Log_Buffer[imerg1]['HP'] = np.append(Event_Log_Buffer[imerg1]['HP'], Event_Log_Buffer[imerg2]['HP'])
                        Event_Log_Buffer[imerg1]['X'] = np.append(Event_Log_Buffer[imerg1]['X'], Event_Log_Buffer[imerg2]['X'])
                        Event_Log_Buffer[imerg1]['Y'] = np.append(Event_Log_Buffer[imerg1]['Y'], Event_Log_Buffer[imerg2]['Y'])
                        Event_Log_Buffer[imerg1]['Z'] = np.append(Event_Log_Buffer[imerg1]['Z'], Event_Log_Buffer[imerg2]['Z'])
                        # Insert Sorting Algorithm here!! Done!
                        SortInd = Event_Log_Buffer[imerg1]['H'].argsort()
                        Event_Log_Buffer[imerg1]['C'] = Event_Log_Buffer[imerg1]['C'][SortInd[::1]]
                        Event_Log_Buffer[imerg1]['HP'] = Event_Log_Buffer[imerg1]['HP'][SortInd[::1]]
                        Event_Log_Buffer[imerg1]['X'] = Event_Log_Buffer[imerg1]['X'][SortInd[::1]]
                        Event_Log_Buffer[imerg1]['Y'] = Event_Log_Buffer[imerg1]['Y'][SortInd[::1]]
                        Event_Log_Buffer[imerg1]['Z'] = Event_Log_Buffer[imerg1]['Z'][SortInd[::1]]
                        Event_Log_Buffer[imerg1]['H'] = Event_Log_Buffer[imerg1]['H'][SortInd[::1]]
                    
                        Event_Merge_Count[imerg2] += 1
            
            for idel in range(len(Event_Merge_Count)):
                if Event_Merge_Count[idel] >= 1 and idel in Event_Log_Buffer:
                    del Event_Log_Buffer[idel]
                    Del_Holder = 1
           
            if Del_Holder == 1:    # If an event was deleted, restart for loop
                break
            
            if imerg1 == imerg2 and imerg1 == Last_Entry:  # All events are checked
                Dummy = -1
            
    return Event_Log_Buffer, Event_Merge_Count

###################################################################
        
##################----------- Running -----------##################    

# Running #
Correct_Found = np.zeros([len(Ni), len(TotalHitsInit), runs])
Total_Events = np.zeros([len(Ni), len(TotalHitsInit), runs])
False_Events = np.zeros([len(Ni), len(TotalHitsInit), runs])
Correct_Percentage = np.zeros([len(Ni),len(TotalHitsInit)])
Events_Detected = np.zeros([len(Ni), len(TotalHitsInit), runs])
Average_Events_Detected = np.zeros([len(Ni),len(TotalHitsInit)])
Average_Hits_Per_Run_Event = np.zeros([len(Ni), len(TotalHitsInit), runs])
Average_Hits_Event = np.zeros([len(Ni),len(TotalHitsInit)])
for i in range(len(Ni)):     # First Loop over amount of Hydrophones
    N = Ni[i]
    Nx = Nxi[i]
    Ny = Nyi[i]
    Nz = Nzi[i]
    Locs = np.zeros([N,D])
    
    for p in range(len(TotalHitsInit)):    # Loop over amount of False Hits
        TotalHits = TotalHitsInit[p]
        for run in range(runs):            # Loop over amount of timeslices
            # Correct_Pulses = np.zeros(runs)
            # Creating Hydrophone Locations & Dict #
            HLocationAlg(xrange, yrange, zrange, Z_Spacing, Cluster_Size, LocID, Nx, Ny, Nz)
            Hydrophones = {}
            HDictCreator(Locs, N)
            
            # Creating Distances to Source & Pulse Time #
            Dist = np.zeros(N)
            Time_Pulse = np.zeros(N)
            HDistSource(Hydrophones, Source_Loc, Vsound)
            
            # Rotation Hydrophone Locs #
            LocXH, LocYH, LocZH = HLocationGet(Hydrophones, N)
            LocYH, LocZH = HRotateX(LocXH, LocYH, LocZH, ThetaX)
            LocXH, LocZH = HRotateY(LocXH, LocYH, LocZH, ThetaY)
            
            # Adding Hits & Amplitudes & Neutrino Pulses to Hydrophones #
            HDictAppender(Hitsrange, TotalHits, Hydrophones, Amprange, N)
            #Hydrophones, Appended_Phones, Appended_Pulses = HPulseAppender(Hydrophones, Time_Pulse, LocZH, Source_Z, PanDepth)
            # Can add more neutrino pulses!
            #Hydrophones, Appended_Phonesx2, Appended_Pulses2 = HPulseAppender(Hydrophones, Time_Pulse+0.5, LocZH, Source_Z, PanDepth)
            
            # Sorting + Rotation of Hit Locs #
            Hits, LocX, LocY, LocZ, LocH = HHitSorter(Hydrophones, N)
            LocY, LocZ = HRotateX(LocX, LocY, LocZ, ThetaX)
            LocX, LocZ = HRotateY(LocX, LocY, LocZ, ThetaY)
            
            # Pancake + Causality Algorithm #
            Nmin = int(29)  # !!Make some function of Hydrophone density!!
            Event_Log = HEvent(Hits, LocX, LocY, LocZ, LocH, Nmin, PanDepth)
            Event_Log = HSortEventLog(Event_Log)
            
            # Merger Algorithm # !! Check whether correctly applied !!
            Event_Log_Buffer = copy.deepcopy(Event_Log)
            
            # Events_Detected[i,p,run] = len(Event_Log_Buffer)
            # Hits_Per_Event = []
            # for ilog in Event_Log_Buffer:
            #     Hits_Per_Event = np.append(Hits_Per_Event,len(Event_Log_Buffer[ilog]['H']))
                
            # if len(Event_Log_Buffer) != 0:
            #     Average_Hits_Per_Run_Event[i,p,run] = sum(Hits_Per_Event)/len(Event_Log_Buffer)
                
            Event_Log_Buffer, Event_Merge_Count = HEventMerger(Event_Log_Buffer)
            
            Events_Detected[i,p,run] = len(Event_Log_Buffer)
            Hits_Per_Event = []
            for ilog in Event_Log_Buffer:
                Hits_Per_Event = np.append(Hits_Per_Event,len(Event_Log_Buffer[ilog]['H']))
                
            if len(Event_Log_Buffer) != 0:
                Average_Hits_Per_Run_Event[i,p,run] = sum(Hits_Per_Event)/len(Event_Log_Buffer)
        
        Average_Hits_Event[i,p] = sum(Average_Hits_Per_Run_Event[i,p])/runs
        Average_Events_Detected[i,p] = sum(Events_Detected[i,p])/runs
        et = time.time()
        time_elapsed = et - st
        print('Elapsed time ' + str(time_elapsed)) 
        print('Run Number ' + str(run+1) + ' Completed')
        print('Total False Hits of ' + str(TotalHits) + ' Completed')
        print('----------------------------------')
        
    print('Run with ' + str(N) + ' Hydrophones Completed')
    print('----------------------------------')
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

