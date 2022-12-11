# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:54:46 2022

@author: oerskqpv
"""
import numpy as np
import HClasses

def HLocationAlg(xrange, yrange, zrange, Z_Spacing, Cluster_Size, LocID, Nx, Ny, Nz, N, D):
    """Create the position of the hydrophones."""
    Locs = np.zeros([N,D])
    if LocID == 2:
        Locs[:, 0] = np.linspace(xrange[0], xrange[1], Nx)  # x-axis
        Locs[:, 1] = np.linspace(yrange[0], yrange[1], Ny)  # y-axis
        Locs[:, 2] = np.linspace(zrange[0], zrange[1], Nz) + Z_spacing  # z-axis
        return Locs
            
    if LocID == 0:# and Cluster_Size == 0:   # !! Is the == 0 necessary? !! 
        N = Nx * Ny * Nz
        Locs[:,0] = np.random.randint(xrange[0],xrange[1],N)  # x-axis
        Locs[:,1] = np.random.randint(yrange[0],yrange[1],N)  #np.zeros(N)   # Y Locations
        Locs[:,2] = np.random.randint(zrange[0],zrange[1],N)  # z-axis
        
    if LocID == 1:
        Locs[:, 0] = np.random.randint(xrange[0], xrange[1], Nx*Ny)  # x-axis
        Locs[:, 1] = np.random.randint(yrange[0], yrange[1], Ny*Nx)  # y-axis
        Locs[:, 2] = np.linspace(zrange[0], zrange[1], Nz) + Z_Spacing  # z-axis
        return Locs
    
def HHydrophoneCreator(Locs, N):
    """ Create a dict of hydrophones with name, location, hits, amplitude"""
    Hydrophones = []
    for Hnum in range(N):
        ID = Hnum+1
        Name = f"X {str(Locs[Hnum,0])}; Y {str(Locs[Hnum,1])}; Z {str(Locs[Hnum,2])}"
        Hydrophones.append(HClasses.Hydrophone(ID,Name, Locs[Hnum,0], Locs[Hnum,1], Locs[Hnum,2]))
    
    return Hydrophones
    
def main():
    pass
    
if __name__ == "__main__":
    main()
