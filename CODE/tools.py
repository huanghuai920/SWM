import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from params import *

# =============================================================================
# 設定繪圖及函數
# =============================================================================
def get_zeta(xx, yy, u, v):
    dx = xx[1,1] - xx[0,0] 
    dy = yy[1,1] - yy[0,0]
    zeta = ((np.roll(v,-1,1)-np.roll(v,1,1)) / (2*dx)) - \
           ((np.roll(u,-1,0)-np.roll(u,1,0)) / (2*dy))
    return zeta
    
def plot_figure(i, xx, yy, phi, u, v):

    
    zeta = get_zeta(xx, yy, u, v)
    
    
    # 重新設定繪圖框
    plt.clf() 
    
    # 繪製底色
    '''  work 1.
    # 將顏色的量値固定成適合的範圍
    # hint: plt.pcolormesh(xx, yy, 顏色(phi / zeta), vmin=最小値, vmax=最大値)
    # 以 initial1.py 為例， vmin 可以設定為 9990， vmax 設定為10010'''
    
    plt.pcolormesh(xx, yy,zeta, cmap='jet', vmin=None, vmax=None)  
    
    
    # 畫色條
    plt.colorbar()
    
    # 畫箭頭
    '''  work 2.
    # 將箭頭大小固定成適合的長度
    # hint: plt.quiver(xx, yy, u, v, scale=??) scale 數字大則箭頭長度短
    # 以 initial1.py 為例， scale 可以設定為 2'''
    
    plt.quiver(xx[::8,::8], yy[::8,::8], u[::8,::8], v[::8,::8], scale=None)
    
    
    # 畫地形等高線
    #plt.contour(xx, yy, hb[1:-1,1:-1], 5, colors='k', linewidths=0.5)
    
    # 寫出標題
    plt.title('time: ' + str(i*dt//86400) + ' days ' + 
              str(((i*dt%86400)//3600)) + ':' +
              str((i*dt%3600)//60) + ':' + 
              str((i*dt%60)))
    
    # 設定圖片寬高比
    plt.gca().set_aspect(1)
    
    # 顯示圖片，並停頓 0.001 秒
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















