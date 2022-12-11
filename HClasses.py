# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:36:34 2022

@author: oerskqpv
"""
from dataclasses import dataclass

##################----------- Classes -----------##################
@dataclass
class Hydrophone:
    ID: int
    IDLoc: int 
    X: float
    Y float 
    Z: float
    #Hits: int

@dataclass
class Hit:
    Hydrophone: float
    Time: float
    Amplitude: float
    Type: int         # 14 = nu, -1 = noise

@dataclass
class Event:
    Hits: int
    
    # by calling Event.Hits it automatically prints this, so not needed

    # def ShowHits(self):   # !! Fix This, Nice Debugging Feature! !!
    #     Times = np.zeros(len(self.Hits))
    #     for i in range(len(self.Hits)):
    #         Times[i] = self.Hits[i].Time
    #     return "{}".format(Times)

@dataclass
class Source:
    X: float
    Y: float
    Z: float
        
def main():
    pass
    
if __name__ == "__main__":
    main()
