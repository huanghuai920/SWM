"""
This is a shallow water model that uses centered difference and 
the leap-frog scheme to solve the following equations:

    du/dt - fv = -g*d(eta)/dx - kappa*u
    dv/dt + fu = -g*d(eta)/dy - kappa*v
    deta/dt + d((eta + H)*u)/dx + d((eta + H)*u)/dy = Q

The model is divided into four parts:

params.py - Used to set constants or other model parameters.
advect.py - Contains functions used for solving the equations, 
            including handling boundaries and the tendency term.
util.py -   Contains plotting tools and functions to save variables.
main.py -   The main program, where the initial field setup and 
            the main loop are executed. Running this file will 
            call the variables or functions from the other three files.
"""

import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile
from glob import glob
import warnings 
import os

from params import *
from advect import boundary, initialize_vars,  \
                   tendency_u, tendency_v, tendency_eta
from tools import plot_figure, save_data_nc

warnings.filterwarnings('ignore')

# =============================================================================
# buildup simulation info
# -----------------------------------------------------------------------------
casename = 'test'
output_dir = f'../DATA/{casename}'
try: os.rmdir(f'{output_dir}')
except: pass

# create archive directory
try:    os.makedirs(f'{output_dir}/archive')
except: pass

# copy codes
try: os.makedirs(f'{output_dir}/CODE')
except: pass
for file in glob('./*.py'):
    copyfile(file, f'{output_dir}/CODE/{file}')
# =============================================================================



# =============================================================================
# initial condition
# set initial condition here
# 
# eta_0:    fluid surface perturbation (m)
# u_0:      x-component wind (m/s)
# v_0:      y-component wind (m/s)
# Q_0:      heat source (m/s) (need to set add_heating)
# hb_0:     topography (m/s) (need to set add_topography)
# -----------------------------------------------------------------------------
# fluid surface perturbation (m)
eta_0 = np.zeros((ny, nx))

# x-component wind (m/s)
u_0 = np.zeros((ny, nx))

# y-component wind (m/s)
v_0 = np.zeros((ny, nx))

# heat source (m/s)
Q_0 = np.zeros((ny, nx))

# topography (m)
hb_0 = np.zeros((ny, nx))
# =============================================================================


# =============================================================================
# setup arrays for model calculation
# -----------------------------------------------------------------------------
eta = initialize_vars(eta_0, copy_time=True)    # fluid surface
u   = initialize_vars(u_0, copy_time=True)      # x-direction wind
v   = initialize_vars(v_0, copy_time=True)      # y-direction wind
Q   = initialize_vars(Q_0, copy_time=False)     # heat source
hb  = initialize_vars(hb_0, copy_time=False)    # topography

# setup time indicator
t_ind = [0,1,2]
old, mid, new = t_ind
# =============================================================================



# =============================================================================
# main loop
# -----------------------------------------------------------------------------
for ITT in range(nt):
    # calculate the next step
    eta[new,1:-1,1:-1] = eta[old,1:-1,1:-1] + tendency_eta(eta, u, v, Q, hb, t_ind)
    u[new,1:-1,1:-1]   = u[old,1:-1,1:-1]   + tendency_u(eta, u, v, t_ind, f)
    v[new,1:-1,1:-1]   = v[old,1:-1,1:-1]   + tendency_v(eta, u, v, t_ind, f)
    
    # periodic boundary
    eta[new] = boundary(eta[new])
    u[new]   = boundary(u[new])
    v[new]   = boundary(v[new])
    
    # time filter  for leap frog scheme
    eta[mid] += r*(eta[new]+eta[old]-2*eta[mid])
    u[mid]   += r*(u[new]+u[old]-2*u[mid])
    v[mid]   += r*(v[new]+v[old]-2*v[mid])

    # rotate time indicator
    t_ind = [old, new, mid]
    new, mid, old = t_ind
    
    if ITT%nsave == 0:
        save_data_nc(ITT, eta[mid,1:-1,1:-1], u[mid,1:-1,1:-1], v[mid,1:-1,1:-1], 
                     savepath=f'{output_dir}/archive')
    
    if ITT%nplot == 0:
        plot_figure(ITT, xx, yy, eta[mid,1:-1,1:-1], u[mid,1:-1,1:-1], v[mid,1:-1,1:-1])
# =============================================================================

plt.show()




