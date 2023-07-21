import numpy as np
import numpy.ma as ma

import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

import cmocean
import dask

filein = '/lus/work/NAT/gda2307/aalbert/eORCA05.L121/eORCA05.L121-AGDA004-S/1h/2012/eORCA05.L121-AGDA004_y2012m01d01.1h_gridT.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_4.2.nc'
var = 'votemper'
lev = 0
ttime = 10 
proj = ccrs.Orthographic(central_latitude=30.0, central_longitude=-30.0)
reg = 'global'
cmap = cmap=cmocean.cm.thermal
vmin = -2
vmax = 30
title = 'Surface temperature at lev = '+str(lev)+' and time = '+str(ttime)
plotname ='plots/map_temp_eORCA05.L121-AGDA004_lev'+str(lev)+'_time'+str(ttime)+'.png'

fig = plt.figure(figsize=(15,15))
sub = 111

def one_plot_surf(fig, sub, filein, filemask, var, lev, ttime, proj, reg, cmap, vmin, vmax):

    ds=xr.open_dataset(filein)
    mask=xr.open_dataset(filemask)

    data=ds[var][ttime,lev]
    lon=mask.glamt[0]
    lat=mask.gphit[0]
    if (var == 'votemper'):
        tmask=mask.tmaskutil
        unit = 'deg C'
    if (var == 'vosaline'):
        tmask=mask.tmaskutil
        unit = 'PSU'
    elif (var == 'vozocrtx'):
        tmask=mask.umaskutil
        unit = 'ms-1'


    datam=np.ma.array(data,mask=1-tmask)

    ax = fig.add_subplot(sub,projection=proj)

    if reg == 'global':
        ax.set_global()
    elif reg == 'wed':
        ax.set_extent([-90, 10, -90, -60], crs=ccrs.PlateCarree())
    elif reg == 'natl':
        ax.set_extent([-100, 50, 50, 70])

    pcolor=ax.pcolormesh(lon,lat,datam,transform=ccrs.PlateCarree(),shading='flat',cmap=cmap,vmin=vmin,vmax=vmax)
#    ax.add_feature(cfeature.LAND,facecolor='grey')
#    ax.coastlines()
#    gl=ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                  linewidth=0.5, color='gray', alpha=0.5)
#    gl.top_labels   = False
#    gl.right_labels = False
#    gl.bottom_labels   = False
#    gl.left_labels = False
#    gl.xlocator = plt.FixedLocator(range(-180, 181, 20))
#    gl.ylocator = plt.FixedLocator(range(-90, 91, 30))

    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='vertical',fraction=0.026, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)

one_plot_surf(fig, sub, filein, filemask, var, lev, ttime, proj, reg, cmap, vmin, vmax)
plt.savefig(plotname)
