# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:46:59 2022

@author: oerskqpv
"""
import numpy as np
import math
import copy
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Import Functions
import HClasses
import HHydrophones
import HNoiseGen
import HNuPulse
import HToolbox
import HEvent
import HEventMerger

# This code is written with the aim to investigate the efficiency and false alarm rates
# of an array of hydrophones. We use both these as input parameters for this simulation.
# This code uses a predetermined arrangement of Hydrophones
#--- HPP 1.1 ---#

# Code Timing #
st = time.time()

##################----------- Input Parameters -----------##################

# Timeslices #    
runs = 1  # Number of Timeslices
Hitsrange = [0,1]       # Size of Timeslice

# Hydrophone Locations #
LocID = 2   # [0 = Random, 1 = Random X,Y, Evenly Spaced in Z, 2 = Evenly Spaced + Clusters]
Nxi = [10]#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]#np.ones(200,dtype=int)#[4]          # Same length as Nyi, Nzi
Nyi = [10]#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]#np.ones(200,dtype=int)#[4]           # Same length as Nxi, Nzi
Nzi = [10]#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]#np.linspace(1,200,200,dtype=int)#[5]#[5,5,5,5,5]#,12,16,18]#,8,10,12,14,16]#,12,14,16]  # Amount of Hydrophones in z-direction, sqrt(N/Nz) needs to be an integer!! (e.g. 100,4) or needs to be 25
Nxyi = np.multiply(Nxi, Nyi)
Cluster_Size = 1  # Amount of Hydrophones at a z-location
Z_Spacing = 1     # Spacing in Cluster in [m], only relevant if Cluster_Size > 1
Ni = np.multiply(Nxyi, Nzi) * Cluster_Size     # Number of Hydrophones
D = 3      # Number of Dimensions, (x,y,z)
xrange = [-500,500]   # XLoc range in meters      
yrange = [-500,500]   # YLoc range in meters
zrange = [-500,500]   # ZLoc range in meters

# False Hits + Amplitudes #
TotalHitsInit = [2]#[1,2,3,4,5,6,7,8,9,10,12,16,20]#11,12,13,14,15,16,17,18,19,20]#[5,10,20,30,40,60,80,100,120,160]   # 5 per 10 seconds
Amprange = [4,10]      # dB range of hits (Check whether assumed values are correct!!)
Source_Amp = 20        # Amplitude of Source

# Source Location #
Source_X = 0
Source_Y = 0
Source_Z = 0
Source_Loc = [Source_X, Source_Y, Source_Z]
ThetaX = (30/180) * np.pi     # Incoming angle neutrino in radians
ThetaY = (30/180) * np.pi     # Incoming angle neutrino in radians

# Pancake Size and Nmin Value for Event + Clique #
PanDepth = 100                # Depth of Pancake in m
TravelDist = 500              # Maximum detectable Distance from Source
Nmin = int(32)                # !!Make some function of Hydrophone density!!
Max_Dist_Match = 420          # Max_Dist_Match/2 is max distance travelled in both directions  [9,9,9] = 608.25 m [10,10,10] = 596.225 m

# Physical Constants & Parameters #
Vsound = 1.5e3  # Sound velocity in water in m/s

###################################################################
       
##################----------- Running -----------##################    
Events_Detected = np.zeros([len(Ni), len(TotalHitsInit), runs])
Average_Events_Detected = np.zeros([len(Ni),len(TotalHitsInit)])
Average_Hits_Per_Run_Event = np.zeros([len(Ni), len(TotalHitsInit), runs])
Average_Hits_Event = np.zeros([len(Ni),len(TotalHitsInit)])
Time_Store = np.zeros([len(Ni), len(TotalHitsInit)]) 

Sources = [HClasses.Source(Source_X, Source_Y, Source_Z)]  # For now only one(1) source loc
for i in range(len(Ni)):     # First Loop over amount of Hydrophones
    N = Ni[i]
    Nx = Nxi[i]
    Ny = Nyi[i]
    Nz = Nzi[i]
    Locs = np.zeros([N,D])
    Locs = HHydrophones.HLocationAlg(xrange, yrange, zrange, Z_Spacing, Cluster_Size, LocID, Nx, Ny, Nz, N, D)
    
    for p in range(len(TotalHitsInit)):    # Loop over amount of False Hits
        TotalHits = TotalHitsInit[p]
        for run in range(runs):            # Loop over amount of timeslices
            # Correct_Pulses = np.zeros(runs)
            # Creating Hydrophone Locations & Dict #
            
            Hydrophones = HHydrophones.HHydrophoneCreator(Locs, N)
            Hits = HNoiseGen.HHitAppender(Hitsrange, TotalHits, Hydrophones, Amprange, N)

            # Rotation Hydrophone Locs #
            HToolbox.HRotateX(Hydrophones, ThetaX)
            HToolbox.HRotateY(Hydrophones, ThetaY)
            
            # Rotation Sources #
            HToolbox.HRotateX(Sources, ThetaX)
            HToolbox.HRotateY(Sources, ThetaY)
            
            # HRotateY(Hydrophones, -ThetaY)  # When rotating back, reverse order!
            # HRotateX(Hydrophones, -ThetaX)
            
            # Adding Noise Hits & Amplitudes #
            Hits = HNoiseGen.HHitAppender(Hitsrange, TotalHits, Hydrophones, Amprange, N)

            # Adding Neutrino Pulses to Hydrophones #
            Hits, Appended_Phones, Appended_Pulses = HNuPulse.HPulseAppender(Hydrophones, Hits, N, Sources, PanDepth, Vsound, TravelDist, 0)
            # Nmin = int(len(Appended_Phones))
            # Can add more neutrino pulses (For now only at same Loc and Angle!
            #Hits, Appended_Phonesx2, Appended_Pulses2 = HPulseAppender(Hydrophones, Hits, Sources, PanDepth, 0.5)
            
            # Sorting of Hits #
            DebugHits = copy.deepcopy(Hits)
            Hits, Temp_Hits = HToolbox.HHitSorter(Hits)
            
            # Pancake + Causality Algorithm #
            Time_Event_S = time.time()
            
            Event_Log, Buff_Check = HEvent.HEvent(Hits, Nmin, PanDepth, Vsound, Max_Dist_Match, TravelDist)
            
            Event_Log = HEventMerger.HSortEventLog(Event_Log)
            
            Time_Event_E = time.time()
            Time_Event_T = Time_Event_E - Time_Event_S
            
            # Merger Algorithm # !! Check whether correctly applied !!
            Time_Merge_S = time.time()
           
            Event_Log_Buffer = copy.deepcopy(Event_Log)
                
            Event_Log_Buffer, Event_Merge_Count = HEventMerger.HEventMerger(Event_Log_Buffer)
           
            Duplicate_Log = np.zeros(len(Event_Log_Buffer[0].Hits))
            for j1 in range(len(Event_Log_Buffer[0].Hits)):
                for j2 in range(j1+1, len(Event_Log_Buffer[0].Hits)):
                    if Event_Log_Buffer[0].Hits[j1].Hydrophone.ID == Event_Log_Buffer[0].Hits[j2].Hydrophone.ID and Event_Log_Buffer[0].Hits[j1].Time == Event_Log_Buffer[0].Hits[j2].Time:
                        Duplicate_Log[j2] +=1
                 
            Event_Log_Buffer_Keep = []
            Hits_Temp = []
            for j3 in range(len(Duplicate_Log)):
                if Duplicate_Log[j3] == 0:
                    Hits_Temp.append(Event_Log_Buffer[0].Hits[j3])
                    
            Event_Log_Buffer_Keep.append(HClasses.Event(Hits_Temp))
            
            NuCount = 0
            for itype in range(len(Event_Log_Buffer_Keep[0].Hits)):
                if Event_Log_Buffer_Keep[0].Hits[itype].Type == 14:
                    NuCount +=1
            print('NuCount Equals ' + str(NuCount))
            print('Event Has ' + str(len(Event_Log_Buffer_Keep[0].Hits)) + ' Hits')
                    # Event_Log_Buffer_Keep.append(HClasses.Event_Log_Buffer[0].Hits[j3])
            # Hits_Twice = Event_Log_Buffer[0].Hits
            # Event_Log_Twice, Buff_Check_Twice = HEvent.HEvent(Hits_Twice, Nmin, PanDepth, Vsound, Max_Dist_Match, TravelDist)
            # Event_Log_Twice = HEventMerger.HSortEventLog(Event_Log_Twice)
            # Event_Log_Buffer_Twice = copy.deepcopy(Event_Log_Twice)
            # Event_Log_Buffer_Twice, Event_Merge_Count_Twice = HEventMerger.HEventMerger(Event_Log_Buffer_Twice)
            
            Time_Merge_E = time.time()
            Time_Merge_T = Time_Merge_E - Time_Merge_S
            
            Events_Detected[i,p,run] = len(Event_Log_Buffer)
            Hits_Per_Event = []
            if len(Event_Log_Buffer) != 0:
                for ilog in range(len(Event_Log_Buffer)):
                    Hits_Per_Event.append(len(Event_Log_Buffer[ilog].Hits))
        
                Average_Hits_Per_Run_Event[i,p,run] = sum(Hits_Per_Event)/len(Event_Log_Buffer)
        
        Average_Hits_Event[i,p] = sum(Average_Hits_Per_Run_Event[i,p])/runs
        Average_Events_Detected[i,p] = sum(Events_Detected[i,p])/runs
        # if Average_Events_Detected[i,p] >= 0.8:
        #     break
        et = time.time()
        time_elapsed = et - st
        Time_Store[i,p] = time_elapsed/runs
        print('Elapsed time ' + str(time_elapsed)) 
        print('Run Number ' + str(run+1) + ' Completed')
        print('Total False Hits of ' + str(TotalHits) + ' Completed')
        print('----------------------------------')
        
    print('Run with ' + str(N) + ' Hydrophones Completed')
    print('Average Events Detected Equals ' + str(Average_Events_Detected[i,p]))
    print('----------------------------------')

    

