# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:55:13 2022

@author: oerskqpv
"""
import numpy as np
import copy

def HHitSorter(Hits):
    Temp_Hits = np.zeros(len(Hits))
    for i in range(len(Hits)):
        Temp_Hits[i] = Hits[i].Time
        
    TempHitsInd = Temp_Hits.argsort()
    Temp_Hits = Temp_Hits[TempHitsInd[::1]]
    Hits = [Hits[i] for i in TempHitsInd]
    
    return Hits, Temp_Hits

def HRotateX(Hydrophones, ThetaX):
    # This function rotates around the x-axis
    for irx in range(len(Hydrophones)):
        Y1 = Hydrophones[irx].Y * np.cos(ThetaX)
        Y2 = -Hydrophones[irx].Z * np.sin(ThetaX)
        LocYY = Y1 + Y2    # Check These Formulas
    
        Z1 = Hydrophones[irx].Y * np.sin(ThetaX)
        Z2 = Hydrophones[irx].Z * np.cos(ThetaX)
        LocZZ = Z1 + Z2
        
        Hydrophones[irx].Y = LocYY
        Hydrophones[irx].Z = LocZZ
    
    return Hydrophones

def HRotateY(Hydrophones, ThetaY):
    # This function rotates around the y-axis
    for iry in range(len(Hydrophones)):
        X1 = Hydrophones[iry].X * np.cos(ThetaY)
        X2 = Hydrophones[iry].Z * np.sin(ThetaY)
        LocXX = X1 + X2
    
        Z1 = -Hydrophones[iry].X * np.sin(ThetaY)
        Z2 = Hydrophones[iry].Z * np.cos(ThetaY)
        LocZZ = Z1 + Z2
        
        Hydrophones[iry].X = LocXX
        Hydrophones[iry].Z = LocZZ
    
    return Hydrophones

def main():
    pass
    
if __name__ == "__main__":
    main()