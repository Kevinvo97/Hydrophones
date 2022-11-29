# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:36:34 2022

@author: oerskqpv
"""

##################----------- Classes -----------##################
class Hydrophone:
    def __init__(self, ID, IDLoc, X, Y, Z):#, Hits):
        self.ID = ID
        self.IDLoc = IDLoc
        self.X = X
        self.Y = Y
        self.Z = Z
        #self.Hits = Hits

class Hit:
    def __init__(self, Hydrophone, Time, Amplitude, Type):
        self.Hydrophone = Hydrophone
        self.Time = Time
        self.Amplitude = Amplitude
        self.Type = Type         # 14 = nu, -1 = noise
        
class Event:
    def __init__(self, Hits):
        self.Hits = Hits
        
    # def ShowHits(self):   # !! Fix This, Nice Debugging Feature! !!
    #     Times = np.zeros(len(self.Hits))
    #     for i in range(len(self.Hits)):
    #         Times[i] = self.Hits[i].Time
    #     return "{}".format(Times)

class Source:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z
        
def main():
    pass
    
if __name__ == "__main__":
    main()