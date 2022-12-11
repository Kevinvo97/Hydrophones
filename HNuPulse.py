# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:43:14 2022

@author: oerskqpv
"""
import numpy as np
import math
import HClasses

# these functions looks very similar to HTimeDiff in HEvent.py. Instead of classes you call, it might be much faster to create 1 nested array that you substract and square, then divide d 
def HDistSource(Hydrophones, Sources, Vsound, N):
    """Calculate the distance and time to the source from a Hydrophone."""
    Dist = np.zeros(N, dtype=float)
    for i in range(N):
        Dist[i] = np.sqrt(
                (Hydrophones[i].X - Sources[0].X)**2 + \
                (Hydrophones[i].Y - Sources[0].Y)**2 + \
                (Hydrophones[i].Z - Sources[0].Z)**2
                )
    Time_Pulse =  Dist / Vsound
        
    return Dist, Time_Pulse

def HPulseAppender(Hydrophones, Hits, N, Sources, PanDepth, Vsound, TravelDist, Offset):
    """Add the time of the pulse to the Hits of the Hydrophone dict."""
    Appended_Phones = []
    Appended_Pulses = []
    Distance = []
    Time = []
    Distance, Time = HDistSource(Hydrophones, Sources, Vsound, N)
    Time = Time + Offset
    for i in range(N):
        if Hydrophones[i].Z <= Sources[0].Z + PanDepth/2 and Hydrophones[i].Z >= Sources[0].Z - PanDepth/2 and Distance[i] <= TravelDist:
            Hits.append(HClasses.Hit(Hydrophones[i], Time[i], 0, 14))
            Appended_Phones = np.append(Appended_Phones,i)
            Appended_Pulses = np.append(Appended_Pulses, Time[i])
    return Hits, Appended_Phones, Appended_Pulses

def main():
    pass
    
if __name__ == "__main__":
    main()
