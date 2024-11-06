from params import *
import numpy as np
import matplotlib.pyplot as plot
import time

def initialize_vars(var, copy_time=False):
    ''' initialize variables '''
    var_out = np.zeros((ny+2, nx+2))
    var_out[1:-1,1:-1] = var
    var_out = boundary(var_out)
    if (not copy_time): 
        return var_out
    elif copy_time:
        var3_out = np.zeros((3,ny+2, nx+2))
        var3_out[:] = var_out
        return var3_out


def tendency_u(eta, u, v, t_ind, f):
    ''' calculate x-direction wind tendency 
    eta:   fluid height perturbation   (m)
    u:     x-direction wind (m/s)
    v:     y-direction wind (m/s)
    f:     coriolis parameter   (1/s)
    t_ind: time indicator '''  
    
    old, mid, new = t_ind
    
    # x and y-direction momentum advection
    udu_dx = D2x * u[mid,1:-1,1:-1] * (u[mid,1:-1,2:] - u[mid,1:-1,:-2])
    vdu_dy = D2y * v[mid,1:-1,1:-1] * (u[mid,2:,1:-1] - u[mid,:-2,1:-1])  
    
    # pressure gradient force
    gdp_dx = g*D2x * (eta[mid,1:-1,2:] - eta[mid,1:-1,:-2])
        
    # diffusion
    d2u_dx2 = 1/dx**2 * ( u[old,1:-1,:-2] + u[old,1:-1,2:] + 
                          u[old,:-2,1:-1] + u[old,2:,1:-1] - 4*u[old,1:-1,1:-1])
    
    # calculate all tendency
    du_dt = -udu_dx - vdu_dy - gdp_dx  + k*(d2u_dx2)
    
    # add coriolis force if add_coriolis is True
    if add_coriolis:
        du_dt += f * v[mid,1:-1,1:-1]
    
    return 2*dt*du_dt


def tendency_v(eta, u, v, t_ind, f):
    ''' calculate y-direction wind tendency 
    eta:   fluid height perturbation   (m)
    u:     x-direction wind (m/s)
    v:     y-direction wind (m/s)
    f:     coriolis parameter   (1/s)
    t_ind: time indicator '''   
    
    old, mid, new = t_ind
    
    # x and y-direction momentum advection
    udv_dx = D2x * u[mid,1:-1,1:-1] * (v[mid,1:-1,2:] - v[mid,1:-1,:-2])
    vdv_dy = D2y * v[mid,1:-1,1:-1] * (v[mid,2:,1:-1] - v[mid,:-2,1:-1])  
    
    # pressure gradient force
    gdp_dy  = g*D2y * (eta[mid,2:,1:-1] - eta[mid,:-2,1:-1])
    
    # diffusion
    d2v_dx2 = 1/dx**2 * ( v[old,1:-1,:-2] + v[old,1:-1,2:] + 
                          v[old,:-2,1:-1] + v[old,2:,1:-1] - 4*v[old,1:-1,1:-1])

    # calculate all tendency
    dv_dt = -udv_dx - vdv_dy - gdp_dy + k*(d2v_dx2)
    
    # add coriolis force if add_coriolis is True
    if add_coriolis:
        dv_dt += -f * u[mid,1:-1,1:-1]

    
    return 2*dt*dv_dt    # 回傳變數
    
    
def tendency_eta(eta, u, v, Q, hb, t_ind):
    ''' calculate   
    eta:   fluid height perturbation   (m)
    u:     x-direction wind (m/s)
    v:     y-direction wind (m/s)
    Q:     heating rate     (m/s)
    hb:    topography       (m)
    t_ind: time indicator '''
    
    old, mid, new = t_ind
    
    # calculate fluid depth
    if add_topography:
        h = H + eta[mid]-hb
    else: 
        h = H + eta[mid]
    
    hu = h * u[mid]    # x-direction flow
    hv = h * v[mid]    # y-direction flow
    dhu_dx = D2x * (hu[1:-1,2:] - hu[1:-1,:-2])  # divergence in x-direction
    dhv_dy = D2y * (hv[2:,1:-1] - hv[:-2,1:-1])  # divergence in y-direction
    
    # diffusion
    d2p_dx2 = 1/dx**2 * ( eta[old,1:-1,:-2] + eta[old,1:-1,2:] + 
                          eta[old,:-2,1:-1] + eta[old,2:,1:-1] - 4*eta[old,1:-1,1:-1])
    
    # calculate eta tendency
    deta_dt = -dhu_dx -dhv_dy + k*(d2p_dx2)
    
    # add heating if add_heating is True
    if add_heating:
        deta_dt += -Q[1:-1,1:-1]
    
    return 2*dt*deta_dt

def boundary(var):
    ''' set lateral boundary periodic'''
    var[ 0, :] = var[-2, :]     # copy left boundary to right
    var[-1, :] = var[ 1, :]     # copy right boundary to left
    var[ :, 0] = var[ :,-2]     # copy top boundary to bottom
    var[ :,-1] = var[ :, 1]     # copy bottom boundary to top
    return var



    
    
