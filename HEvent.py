# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:59:38 2022

@author: oerskqpv
"""
import numpy as np
import math
import HClasses

def HTimeDiff(Hit1, Hit2, Vsound):
    Dist = np.sqrt(
            (Hit1.Hydrophone.X - Hit2.Hydrophone.X)**2 + \
            (Hit1.Hydrophone.Y - Hit2.Hydrophone.Y)**2 + \
            (Hit1.Hydrophone.Z - Hit2.Hydrophone.Z)**2
            )
    Time_Diff = Dist / Vsound
    
    return Time_Diff, Dist

def HMatch(Hit1, Hit2, Vsound, TravelDist):
    Dt = abs(Hit1.Time - Hit2.Time)
    Time_Diff, Dist = HTimeDiff(Hit1, Hit2, Vsound)
    TMargin = 1e-3      # 10 ns, ! maybe find a better way to implement this & value !
    if Dist > TravelDist:
        Time_DiffMax = (TravelDist-(Dist-TravelDist))/Vsound
    else:
        Time_DiffMax = Time_Diff
    
    return Time_DiffMax + TMargin >= Dt and Dist <= TravelDist*2

def HClique(Hits, Nmin, Vsound, TravelDist):
    Count = np.ones(len(Hits))   # Assume match with self
    # Look for Causal Hits & add to Counter #
    for i in range(len(Hits)-1):
        for j in range(i+1, len(Hits)):
            if HMatch(Hits[i], Hits[j], Vsound, TravelDist):
                Count[i] += 1
                Count[j] += 1
                
    # Now run Clique algorithm to remove hits with least amount of correlated hits
    
    # Structure infinitely running loop, 
    while True:
        j = 0
        M = 0
        n = len(Hits)i

        # if this is trying to find max in Count, use np.max(Count) (which I added in the if)
        #for i in range(n):
        #    if Count[i] < Count[j]:
        #        j = i
        #    # if Count[i] >= Nmin:
        #    #     M += 1
            
        if np.max(Count) == n:     # number of associated hits is equal to the number of (remaining) hits
            return Hits, Count
    
        #if M < Nmin:         # maximal number of associated hits is less than the specified minimum
            #return Hits, Count, LocX, LocY, LocZ, LocH
    
        # Swap selected Hit to end
        Hits[j], Hits[n-1] = Hits[n-1], Hits[j]
        Count[j], Count[n-1] = Count[n-1], Count[j]
  
        # Decrease number of associated hits for each associated hits
        for i in range(n-1):
            if HMatch(Hits[i], Hits[n-1], Vsound, TravelDist):
                Count[i] -=1
                Count[n-1] -=1
                
            if Count[n-1] == 1:
                del Hits[n-1]
                del Count[n-1]    # This is not really needed!
                break

def HEvent(Hits, Nmin, PanDepth, Vsound, Max_Dist_Match, TravelDist):
    """This function checks whether a hit has enough correlated hits within its pancake,
    if this is the case, the Clique algorithm is employed, then if enough correlated
    hits remain an event is created in the Event_Log with these hits. 
    """
    Event_Log = []
    for pan1 in range(len(Hits)-1):
        Buffer = []
        Buffer.append(Hits[pan1])
        for pan2 in range(pan1+1, len(Hits)):
            Time_Diff, Dist = HTimeDiff(Hits[pan1], Hits[pan2], Vsound)
            if Hits[pan2].Hydrophone.Z <= Hits[pan1].Hydrophone.Z + PanDepth and Hits[pan2].Hydrophone.Z >= Hits[pan1].Hydrophone.Z - PanDepth and Dist <= Max_Dist_Match:
                if HMatch(Hits[pan1], Hits[pan2], Vsound, TravelDist):
                    Buffer.append(Hits[pan2])
        if len(Buffer) >= Nmin:
            Buffer, BufferC = HClique(Buffer, Nmin, Vsound, TravelDist)
            if len(Buffer) >= Nmin:
                Event_Log.append(HClasses.Event(Buffer))
                
    return Event_Log, Buffer


def main():
    pass
    
if __name__ == "__main__":
    main()
