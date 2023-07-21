import numpy as np
import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import cmocean
import dask



filein = '/lus/work/NAT/gda2307/aalbert/eORCA05.L121/eORCA05.L121-AGDA004-S/1h/2012/eORCA05.L121-AGDA004_y2012m01d01.1h_gridT.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_4.2.nc'
var = 'votemper'
lev = 0
ttime = 0 
proj = ccrs.Orthographic(central_longitude=-30,central_latitude=35)
reg = 'global'
cmap = cmap=cmocean.cm.thermal
vmin = -2
vmax = 30
title = 'Surface temperature at lev = '+str(lev)+' adn time = '+str(ttime)
plotname ='plots/map_temp_eORCA05.L121-AGDA004_lev'+str(lev)+'_time'+str(ttime)+'.png'

fig = plt.figure(figsize=(15,15))
sub = 111

def one_plot_surf(fig, sub, filein, filemask, var, lev, ttime, proj, reg, cmap, vmin, vmax, title):

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

    ax = fig.add_subplot(sub,projection=ccrs.PlateCarree(central_longitude=-30))

    if reg == 'global':
        ax.set_global()
    elif reg == 'wed':
        ax.set_extent([-90, 10, -90, -60], crs=ccrs.PlateCarree())
    elif reg == 'natl':
        ax.set_extent([-100, 50, 50, 70])

    pcolor=ax.pcolormesh(lon,lat,ma.masked_invalid(datam),transform=ccrs.PlateCarree(),cmap=cmap,vmin=vmin,vmax=vmax)
    ax.add_feature(cfeature.LAND,facecolor='grey')
    ax.coastlines()
    gl=ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')

    fig.subplots_adjust(right=0.8)
    gl.xlocator = mticker.FixedLocator([-110,-90,-70,-50,-30,-10,10,30,50,70,90,110])
    gl.ylocator = mticker.FixedLocator([-10,0,10,20,30,40,50,60,70,80])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 15, 'color': 'gray'}
    gl.ylabel_style = {'size': 15, 'color': 'gray'}
    gl.xlabels_top = False
    gl.ylabels_left = False

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75,label=unit)
    ax.set_title(title,size=17,y=1.08)


plt.savefig('plot_tos_WED025.png')
