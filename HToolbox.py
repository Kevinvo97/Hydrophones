# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:55:13 2022

@author: oerskqpv
"""
import numpy as np
import copy

def HHitSorter(Hits):
    Temp_Hits = np.array([hit.Time for hit in Hits))
    TempHitsInd = Temp_Hits.argsort()
    Temp_Hits = Temp_Hits[TempHitsInd[::1]]
    Hits = [Hits[i] for i in TempHitsInd]
    
    return Hits, Temp_Hits

def HRotateX(Hydrophones, ThetaX):
    """Rotate around the x-axis."""
    for phone in Hydrophones:
        Y1 = phone.Y * np.cos(ThetaX)
        Y2 = -phone.Z * np.sin(ThetaX)
    
        Z1 = phone.Y * np.sin(ThetaX)
        Z2 = phone.Z * np.cos(ThetaX)
        
        phone.Y = Y1+Y2  # check this formula
        phone.Z = Z1+Z2
    
    return Hydrophones

def HRotateY(Hydrophones, ThetaY):
    """Rotate around the y-axis."""
    for phone in Hydrophones:
        X1 = phone.X * np.cos(ThetaY)
        X2 = phone.Z * np.sin(ThetaY)
    
        Z1 = -phone.X * np.sin(ThetaY)
        Z2 = phone.Z * np.cos(ThetaY)
        
        phone.X = X1+X2
        phone.Z = Z1+Z2
    
    return Hydrophones

def main():
    pass
    
if __name__ == "__main__":
    main()
