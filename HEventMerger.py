# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:31:59 2022

@author: oerskqpv
"""
import numpy as np

def HSortEventLog(Event_Log):
    """Sort all the data according to ascending order of the hits"""
    for isort in range(len(Event_Log)):
        Temp_Hits = np.zeros(len(Event_Log[isort].Hits))
        for jsort in range(len(Event_Log[isort].Hits)):
            Temp_Hits[jsort] = Event_Log[isort].Hits[jsort].Time
            
        TempHitsInd = Temp_Hits.argsort()
        Temp_Hits = Temp_Hits[TempHitsInd[::1]]  # you don't return this, so this has no effect
        Event_Log[isort].Hits = [Event_Log[isort].Hits[i] for i in TempHitsInd]
        
    return Event_Log

def HEventMerger(Event_Log_Buffer):
    """Merge events which have overlap (e.g tb1<=tb2<te1)."""
    
    ### Gebruik van enumerate hier is veel eleganter!!!
    
    Event_Merge_Count = np.zeros(len(Event_Log_Buffer))
    if len(Event_Log_Buffer) == 0:
        return Event_Log_Buffer, Event_Merge_Count
            
    for imerg1 in range(len(Event_Log_Buffer)-1):
        if Event_Merge_Count[imerg1] > 0:
            continue
        for imerg2 in range(imerg1+1,len(Event_Log_Buffer)):
            if imerg1 != imerg2:
                t_begin1 = Event_Log_Buffer[imerg1].Hits[0].Time
                t_end1 = Event_Log_Buffer[imerg1].Hits[-1].Time
                t_begin2 = Event_Log_Buffer[imerg2].Hits[0].Time
                t_end2 = Event_Log_Buffer[imerg2].Hits[-1].Time
                if t_begin2 >= t_begin1 and t_begin2 <= t_end1:
                    Event_Log_Buffer[imerg1].Hits = Event_Log_Buffer[imerg1].Hits + Event_Log_Buffer[imerg2].Hits
                    Event_Merge_Count[imerg2] += 1
                    
                    # Insert Sorting Algorithm here!! Done!
                    Temp_Hits = np.zeros(len(Event_Log_Buffer[imerg1].Hits))
                    for jsort in range(len(Event_Log_Buffer[imerg1].Hits)):
                        Temp_Hits[jsort] = Event_Log_Buffer[imerg1].Hits[jsort].Time
                        
                    TempHitsInd = Temp_Hits.argsort()
                    Temp_Hits = Temp_Hits[TempHitsInd[::1]]
                    Event_Log_Buffer[imerg1].Hits = [Event_Log_Buffer[imerg1].Hits[i] for i in TempHitsInd]
                    
    Event_Log_Keep = []
    for ikeep, count in enumerate(Event_Merge_Count):
        if count == 0:
            Event_Log_Keep.append(Event_Log_Buffer[ikeep]) 
    
    return Event_Log_Keep, Event_Merge_Count
