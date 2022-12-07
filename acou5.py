# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:54:07 2022

@author: oerskqpv
"""

import aa, ROOT
from itertools import product
from ROOT import Evt, Vec, Hit, Trk
from copy import copy

vsound = 1500 # m/s

def detector( D = 1000, N = 10 ) :
    
    "return list of x,y,z tuples (of the hydrophones) on a grid"

    u = [ D/N*i-D/2 for i in range(N) ]
    return list ( product( u,u,u ) ) 
        

def simulate ( det, 
               nupos         = (80,90,100), 
               t             =1.234, 
               amplitude     = 1e6,
               time_accuracy = 10e-6, 
               noise_rate    = 5.00,         # per second
               noise_window  = [-2000/vsound,2000/vsound] ) :

    "Do a toy-simulation of an accoustic event. Expanding sphere with vsound"

    # how many noise hits per hydrophone, on average ? 
    mean_noise = ( noise_window[1]-noise_window[0] ) * noise_rate

    r = Evt() #km3net event
    nu = Trk()
    nu.t = t
    nu.pos.set(*nupos)

    r.mc_trks.push_back( nu )

    for xyz in det :
        p = Vec( *xyz )
        distance = ( p - nu.pos ).len()
        if distance == 0 : continue

        a = amplitude / distance**2; # todo: add pancake shape
        Max_Distance = 500

        if a > 1 and p.z >= nupos[2] - 50 and p.z <= nupos[2] + 50 and distance <= Max_Distance: 
            h = Hit()
            h.a    = a
            h.t    = nu.t + distance / vsound + ROOT.gRandom.Gaus(0,time_accuracy)
            h.pos  = p 
            h.type = 14 # some neutrino
            r.hits.push_back( h )

        for i in range( ROOT.gRandom.Poisson( mean_noise )) :
            h = Hit()
            h.a = 1
            h.t = ROOT.gRandom.Uniform( *noise_window ) 
            h.pos = p
            h.type = -1
            r.hits.push_back( h )          

    return r


def inspect( evt, track ) :

    "Print a table of hits and residuals"

    T = ROOT.Table("type","x", "y", "z","distance(m)","time(s)","resi_fit(s)","resi_true(s)")

    nu = evt.mc_trks[0]

    for h in evt.hits :
        d1 = (h.pos - track.pos ).len()
        r1 = h.t - track.t - d1 / vsound

        d2 = (h.pos - nu.pos ).len()
        r2 = h.t - nu.t - d2 / vsound 
        T.add( h.type, h.pos.x, h.pos.y, h.pos.z, d1, h.t, r1, r2  )

    print (T)


def starting_point( hits , N = 5 ) :

    "Generate a very first estimate of the neutrino position, using the amplitudes"

    hits = sorted( hits, key = lambda h: - h.a )[:N]

    start_track = Trk()

    for h in hits :
        start_track.pos += h.pos
    start_track.pos /= N
    start_track.t    = hits[0].t - ( hits[0].pos - start_track.pos).len() / vsound
    return start_track
    

def starting_point_loop( trk ):
    
    "Use first fits to determine a more accurate estimate of the neutrino position"
    
    start_track = Trk()
    start_track.pos = trk.pos
    start_track.t = trk.t
    
    return start_track


# def select_hits( trk, evt , max_residual ):

#     "Return the hits that have a residual smaller than max_residual"
#     temphits = []
#     for h in evt.hits:
#         # d = (h.pos - trk.pos ).len()
#         temphits.append(h)

#     return filter( lambda h : h.t - trk.t - (h.pos - trk.pos ).len() / vsound < max_residual, temphits )


def select_hits( trk, evt, max_residual ):

    "Return the hits that have a residual smaller than max_residual"
    
    sel_evt = copy(evt)
    sel_evt.hits = [ elem for elem in sel_evt.hits if abs(elem.t - trk.t - (elem.pos - trk.pos ).len() / vsound) < max_residual]
    
    return sel_evt


def get_aashower_fit() :

    "Return a function that can fit hits using the machinery in aashowerfit"

    import rec
    from ROOT import MestShowerPdf, ShowerFit

    m_estimator_pdf = MestShowerPdf()
    showerfit = ShowerFit ( "mest", m_estimator_pdf )
    showerfit.fix_vars( 3,4,6 ) # dont fit direction and energy

    # functions to scale the hit-times so that it looks like
    # sound moves at the speed of light.

    def time_warp( obj ) :
        " e.g. 1500m : 1s => 6903 ns "
        obj.t *= vsound / ROOT.v_light

    def time_unwarp( obj ) :
        obj.t *= ROOT.v_light /vsound


    def fit( evt ) :

        hits = [ copy(h) for h in evt.hits ] # copy since we're going to change the hits
        for h in hits : time_warp( h )
        
        start_track = starting_point( hits )
     
        track = showerfit.fit( start_track, ROOT.Det(), aa.make_vector(hits), 1 )
        
        time_unwarp( track )
        time_unwarp( start_track )

        print (start_track)
        print (track)
        return track

    return fit


def get_homebrew_fit() :

    "Return a function that does the fit using scipy.minimizer"

    from scipy.optimize import minimize
    import numpy as np

    def score( hits, trk ) :
  
        '''
        M-estimator score. 
        the constant determines where the quadratic behaviour becomes linear
        '''

        constant = 1e-4 # in seconds.
        power    = 0.5
        score    = 0

        for h in hits :
            d = (h.pos - trk.pos ).len()
            residual = h.t - trk.t - d / vsound
            score += h.a * ( constant**2 + residual**2) ** power 

        return score


    def make_fitfunc( hits ) :

        T = Trk()

        def fitme( pars ) :
            T.pos.set( pars[0],pars[1],pars[2])
            T.t = pars[3]
            return score( hits, T )
        
        return fitme


    def fit( evt ) :
       
        t = starting_point( evt.hits )
        pars =  np.array([ t.pos.x, t.pos.y, t.pos.z, t.t ])

        f = make_fitfunc( evt.hits ) 
        
        opts={'gtol'   : 1e-4 , 
              'eps'    : 1.4901161193847656e-08, 
              'maxiter': None, 
              'disp'   : False,
              'return_all': False}

        res = minimize( f , pars, method= "bfgs", options = opts )

        r = Trk()
        r.pos.set( res.x[0],res.x[1],res.x[2] )
        r.t = res.x[3]
        r.lik = res.fun
        return r

    return fit


def get_homebrew_fit_loop() :

    "Return a function that does the fit using scipy.minimizer"

    from scipy.optimize import minimize
    import numpy as np

    def score( hits, trk ) :
  
        '''
        M-estimator score. 
        the constant determines where the quadratic behaviour becomes linear
        '''

        constant = 1e-4 # in seconds.
        power    = 0.5
        score    = 0

        for h in hits :
            d = (h.pos - trk.pos ).len()
            residual = h.t - trk.t - d / vsound
            score += h.a * ( constant**2 + residual**2) ** power 

        return score


    def make_fitfunc( hits ) :

        T = Trk()

        def fitme( pars ) :
            T.pos.set( pars[0],pars[1],pars[2])
            T.t = pars[3]
            return score( hits, T )
        
        return fitme


    def fit( evt, trk ) :
       
        t = starting_point_loop( trk )
        pars =  np.array([ t.pos.x, t.pos.y, t.pos.z, t.t ])

        f = make_fitfunc( evt.hits ) 
        
        opts={'gtol'   : 1e-4 , 
              'eps'    : 1.4901161193847656e-08, 
              'maxiter': None, 
              'disp'   : False,
              'return_all': False}

        res = minimize( f , pars, method= "bfgs", options = opts )

        r = Trk()
        r.pos.set( res.x[0],res.x[1],res.x[2] )
        r.t = res.x[3]
        r.lik = res.fun
        return r

    return fit

def NuCount( evt ):
    NuCount = 0
    for j in evt.hits:
        if j.type == 14:
            NuCount += 1
            
    return NuCount

fit = get_homebrew_fit()

det = detector()

evt = simulate( det )

NuCounter = NuCount ( evt )


t = fit (evt)
t_loop = copy(t)

evt_loop = copy( evt )
for i in range(1,31):
    evt_sel = select_hits( t_loop, evt_loop, 3/i )
    t_sel = fit (evt_sel)
    t_loop = t_sel
    evt_loop = evt_sel

# fittie = get_homebrew_fit_loop()
# t_sel = fittie (evt, t_loop)
evt_sel = select_hits( t_loop, evt_loop, 0.01 )
t_sel = fit (evt_sel)

NuCounter_sel = NuCount ( evt_sel )

# Printing of Results
print("table before selection")
inspect( evt, t )

print("table after selection")
inspect( evt_sel, t_sel )

print('Check Whether Selection Works!')
print ("event has", len(evt.hits), "hits before selection")
print("event has", len(evt_sel.hits), "hits after selection")
print ("event has", NuCounter, "neutrino hits before selection")
print ("event has", NuCounter_sel, "neutrino hits after selection")
print("track reconstruction before selection")
print(t)
print("track reconstruction after selection")
print(t_sel)




