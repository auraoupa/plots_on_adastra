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

def one_map_noproj(fig, nx, ny, pos, data, unit, mask, cmap, vmin, vmax, title):

    datam=np.ma.array(data,mask=1-mask)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.pcolormesh(datam,cmap=cmap,vmin=vmin,vmax=vmax)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)

def get_data2D(filei,var,ttime,lev):
    ds=xr.open_dataset(filei)
    if (lev == -1):
        data=ds[var][ttime].squeeze()
    else:
        data=ds[var][ttime,lev].squeeze()
    return data

filein = '/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2.1/DCMTOOLS/NEMOREF/NEMO4/cfgs/eORCA36.L121-AAA001/EXP00/output.abort_merg.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4_4.2.nc'

dsmask=xr.open_dataset(filemask)
navlev=dsmask['nav_lev']

fig = plt.figure(figsize=(30,100))
plotname ='plots/all_maps_output_abort_eORCA36.png'

dep=0
lev=np.where(np.abs(navlev-dep)==np.min(np.abs(navlev-dep)))[0]

tmask0=dsmask['tmask'][0,lev]
temp0=get_data2D(filein,'votemper',0,lev)
one_map_noproj(fig, 8,2,1,  temp0,   '°C', tmask0, cmocean.cm.thermal, -5, 30, 'output abort sea surface temperature eORCA36 ');
salt0=get_data2D(filein,'vosaline',0,lev)
one_map_noproj(fig, 8,2,2,  salt0,   'PSI', tmask0, cmocean.cm.haline, 30, 35, 'output abort sea surface salinity eORCA36 ');
ssh=get_data2D(filein,'sossheig',0,-1)
one_map_noproj(fig, 8,2,3,  ssh,   'm', tmask0, 'tab20c', -0.15, -0.1, 'init sea surface height eORCA36 ');
flx1=get_data2D(filein,'sowaflup',0,-1)
one_map_noproj(fig, 8,2,4,  flx1,   'kg/m2/s', tmask0, cmocean.cm.rain, -0.0005, 0.0005, 'init water flux eORCA36 ');
flx2=get_data2D(filein,'sohefldo',0,-1)
one_map_noproj(fig, 8,2,5,  flx2,   'W/m2', tmask0, cmocean.cm.balance, -500, 500, 'init net heat flux eORCA36 ');
flx3=get_data2D(filein,'soshfldo',0,-1)
one_map_noproj(fig, 8,2,6,  flx3,   'W/m2', tmask0, cmocean.cm.solar,0,1000, 'init shortwave radiation eORCA36 ');
flx4=get_data2D(filein,'soicecov',0,-1)
one_map_noproj(fig, 8,2,7,  flx4,   '-', tmask0, cmocean.cm.gray, 0, 1, 'init ice coverage eORCA36 ');
flx5=get_data2D(filein,'sozotaux',0,-1)
one_map_noproj(fig, 8,2,8,  flx5,   'm/s', tmask0, cmocean.cm.amp, 0, 1, 'init x-wind stress eORCA36 ');
flx6=get_data2D(filein,'sometauy',0,-1)
one_map_noproj(fig, 8,2,9,  flx6,   'm/s', tmask0, cmocean.cm.amp, 0, 1, 'init y-wind stress eORCA36 ');

dep=100
lev=np.where(np.abs(navlev-dep)==np.min(np.abs(navlev-dep)))[0]
tmask100=dsmask['tmask'][0,lev]
temp100=get_data2D(filein,'votemper',0,lev)
one_map_noproj(fig, 8,2,11,  temp100,   '°C', tmask100, cmocean.cm.thermal, -5, 30, 'output abort temperature eORCA36 100m');
salt100=get_data2D(filein,'vosaline',0,lev)
one_map_noproj(fig, 8,2,12,  salt100,   'PSI', tmask100, cmocean.cm.haline, 30, 35, 'output abort salinity eORCA36 100m');

dep=500
lev=np.where(np.abs(navlev-dep)==np.min(np.abs(navlev-dep)))[0]
tmask500=dsmask['tmask'][0,lev]
temp500=get_data2D(filein,'votemper',0,lev)
one_map_noproj(fig, 8,2,13,  temp500,   '°C', tmask500, cmocean.cm.thermal, -5, 30, 'output abort temperature eORCA36 500m');
salt500=get_data2D(filein,'vosaline',0,lev)
one_map_noproj(fig, 8,2,14,  salt500,   'PSI', tmask500, cmocean.cm.haline, 30, 35, 'output abort salinity eORCA36 500m');

dep=1000
lev=np.where(np.abs(navlev-dep)==np.min(np.abs(navlev-dep)))[0]
tmask1000=dsmask['tmask'][0,lev]
temp1000=get_data2D(filein,'votemper',0,lev)
one_map_noproj(fig, 8,2,15,  temp1000,   '°C', tmask1000, cmocean.cm.thermal, -5, 30, 'output abort temperature eORCA36 1000m');
salt1000=get_data2D(filein,'vosaline',0,lev)
one_map_noproj(fig, 8,2,16,  salt1000,   'PSI', tmask1000, cmocean.cm.haline, 30, 35, 'output abort salinity eORCA36 1000m');

plt.savefig(plotname)


