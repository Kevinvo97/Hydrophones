# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:34:36 2022

@author: oerskqpv
"""
import numpy as np
import HClasses

def HHitAppender(Hitsrange, TotalHits, Hydrophones, Amprange, N):
    """Add random False Hits + Amplitudes to the Hydrophones dict."""
    Hits = []
    for Hnum in range(N):
        Hits_Temp = np.sort(np.random.uniform(Hitsrange[0], Hitsrange[1],TotalHits))
        Amplitudes = np.random.uniform(Amprange[0], Amprange[1],TotalHits)
        for iHits in range(len(Hits_Temp)):
            Hits.append(HClasses.Hit(Hydrophones[Hnum], Hits_Temp[iHits], Amplitudes[iHits], -1))
        
    return Hits

def main():
    pass
    
if __name__ == "__main__":
    main()
