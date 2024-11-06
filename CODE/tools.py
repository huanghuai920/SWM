import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from params import *
    
def plot_figure(i, xx, yy, phi, u, v):    
    
    plt.clf() 
    
    plt.pcolormesh(xx, yy,phi, cmap='jet', vmin=None, vmax=None)  

    plt.colorbar()
    
    plt.quiver(xx[::8,::8], yy[::8,::8], u[::8,::8], v[::8,::8], scale=None)
    
    plt.title('time: ' + str(i*dt//86400) + ' days ' + 
              str(((i*dt%86400)//3600)) + ':' +
              str((i*dt%3600)//60) + ':' + 
              str((i*dt%60)))
    
    plt.gca().set_aspect(1)
    
    plt.draw()
    plt.pause(0.001)



def save_data_nc(ITT, eta, u, v, savepath='.'):
    fname = 'SWM_%06d.nc'%(ITT/nsave)
    dat = nc.Dataset(f'{savepath}/{fname}', 'w')
    
    dat.createDimension('x', len(x))
    dat.createDimension('y', len(y))
    dat.createDimension('time', 1)
    
    dat.createVariable('x', np.float32, ('x',))
    dat['x'].long_name = 'x-coordinate of grid cell centers in Cartesian system'
    dat['x'].units = 'm'
    dat['x'][:] = x
    
    dat.createVariable('y', np.float32, ('y',))
    dat['y'].long_name = 'y-coordinate of grid cell centers in Cartesian system'
    dat['y'].units = 'm'
    dat['y'][:] = y
    
    dat.createVariable('time', np.float32, ('time',))
    dat['time'].long_name = 'time'
    dat['time'].units = 'minutes since 1900-01-01'
    dat['time'][:] = (ITT * dt) / 60
      
    dat.createVariable('eta', np.float32, ('time','y','x'))
    dat['eta'].long_name = 'fluid surface height perturbation'
    dat['eta'].reference_height = float(H)
    dat['eta'].units = 'm'
    dat['eta'][0] = eta
        
    dat.createVariable('u', np.float32, ('time','y','x'))
    dat['u'].long_name = 'x-component wind'
    dat['u'].units = 'm/s'
    dat['u'][0] = u
    
    dat.createVariable('v', np.float32, ('time','y','x'))
    dat['v'].long_name = 'y-component wind'
    dat['v'].units = 'm/s'
    dat['v'][0] = v
    
    dat.close()















