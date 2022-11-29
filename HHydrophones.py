# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:54:46 2022

@author: oerskqpv
"""
import numpy as np
import HClasses

def HLocationAlg(xrange, yrange, zrange, Z_Spacing, Cluster_Size, LocID, Nx, Ny, Nz, N, D):
    # This function creates the Hydrophone locations
    Locs = np.zeros([N,D])
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
        
    if LocID == 1:
        Locs_Initx = np.random.randint(xrange[0], xrange[1], Nx*Ny)
        Locs_Inity = np.random.randint(yrange[0], yrange[1], Ny*Nx)
        Locs_Initz = np.linspace(zrange[0], zrange[1], Nz)
        Fill_Count = 0
        for i in range(Nx*Ny):
                
            for k in range(Nz):
                    
                for l in range(Cluster_Size):
                    Locs[Fill_Count ,0] = Locs_Initx[i]
                    Locs[Fill_Count ,1] = Locs_Inity[i]
                    Locs[Fill_Count ,2] = Locs_Initz[k] + l * Z_Spacing
                    Fill_Count += 1
        
        return Locs
    
def HHydrophoneCreator(Locs, N):
    # This function creates a dict entry for each Hydrophone with name, location, hits, amplitude
    Hydrophones = []
    for Hnum in range(N):
        ID = Hnum+1
        Name = "X" + str(Locs[Hnum,0]) + "Y" + str(Locs[Hnum,1]) + "Z" + str(Locs[Hnum,2])
        Hydrophones.append(HClasses.Hydrophone(ID,Name, Locs[Hnum,0], Locs[Hnum,1], Locs[Hnum,2]))
    
    return Hydrophones
    
def main():
    pass
    
if __name__ == "__main__":
    main()
