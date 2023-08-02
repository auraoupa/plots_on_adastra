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


filetemp = '/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2.1/DCMTOOLS/NEMOREF/NEMO4/cfgs/eORCA36.L121-AAA001/EXP00/votemper_init.nc'
filesal = '/lus/work/NAT/gda2307/aalbert/DEV/DCM_4.2.1/DCMTOOLS/NEMOREF/NEMO4/cfgs/eORCA36.L121-AAA001/EXP00/vosaline_init.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4_4.2.nc'

plotname ='plots/sections_temp-salt_init_abort_eORCA36.png'
dstemp=xr.open_dataset(filetemp)
dssal=xr.open_dataset(filesal)
datat=dstemp['votemper'][0]
datas=dssal['vosaline'][0]
dsmask=xr.open_dataset(filemask)
tmask=dsmask['tmask'][0]
navlev=dsmask['nav_lev']
navlon=dsmask['nav_lon']
navlat=dsmask['nav_lat']
fig = plt.figure(figsize=(30,150))
datatm=np.ma.array(datat,mask=1-tmask)
datasm=np.ma.array(datas,mask=1-tmask)

def sections_latitude(ax,seclat,seclon1,seclon2,datam,cmap,deplim,unit,title):
    lon=navlon[seclat,seclon1:seclon2]
    if (np.mean(np.diff(lon))<0): 
        lon[np.where(lon<0)]=lon[np.where(lon<0)]+360
    pcolor=ax.pcolormesh(lon,navlev,datam[:,seclat,seclon1:seclon2],cmap=cmap, shading='nearest')
    ax.set_ylim([0,deplim])
    ax.invert_yaxis()
    plt.xlabel('longitude °E')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)

def sections_longitude(ax,seclon,seclat1,seclat2,datam,cmap,deplim,unit,title):
    lat=navlat[seclat1:seclat2,seclon]
    pcolor=ax.pcolormesh(lat,navlev,datam[:,seclat1:seclat2,seclon],cmap=cmap, shading='nearest')
    ax.set_ylim([0,deplim])
    ax.invert_yaxis()
    plt.xlabel('latitude °N')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=17,y=1.08)

def all_sections(ncol,datam,cmap,unit,varname):
    odd=ncol%2
    ax = fig.add_subplot(16,2,2-odd)
    sections_latitude(ax,9181,4062,4135,datam,cmap,70,unit,'init '+str(varname)+' eORCA36 init abort Bering section y='+str(navlat[9181,4062].values)+'°N')
    ax = fig.add_subplot(16,2,4-odd)
    sections_latitude(ax,10145,9600,9945,datam,cmap,5000,unit,'init '+str(varname)+' eORCA36 init abort Fram section y='+str(navlat[10145,9600].values)+'°N')
    ax = fig.add_subplot(16,2,6-odd)
    sections_latitude(ax,9955,8331,8812,datam,cmap,2500,unit,'init '+str(varname)+' eORCA36 init abort Baffin section y='+str(navlat[9955,8331].values)+'°N')
    ax = fig.add_subplot(16,2,8-odd)
    sections_latitude(ax,7154,7446,7498,datam,cmap,900,unit,'init '+str(varname)+' eORCA36 init abort Florida-Bahamas section y='+str(navlat[7154,7446].values)+'°N')
    ax = fig.add_subplot(16,2,10-odd)
    sections_latitude(ax,5563,11763,11934,datam,cmap,3500,unit,'init '+str(varname)+' eORCA36 init abort Mozambique section y='+str(navlat[5563,11763].values)+'°N')
    ax = fig.add_subplot(16,2,12-odd)
    sections_latitude(ax,5258,11406,12959,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort Africa-Australia1 section y='+str(navlat[5258,11406].values)+'°N')
    ax = fig.add_subplot(16,2,14-odd)
    sections_latitude(ax,5258,0,1578,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort Africa-Australia2 section y='+str(navlat[5258,0].values)+'°N')
    ax = fig.add_subplot(16,2,16-odd)
    sections_latitude(ax,5258,2835,7797,datam,cmap,5000,unit,'init '+str(varname)+' eORCA36 init abort Australia-America section y='+str(navlat[5258,2835].values)+'°N')
    ax = fig.add_subplot(16,2,18-odd)
    sections_latitude(ax,5258,8634,10861,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort America-Africa section y='+str(navlat[5258,8634].values)+'°N')
    ax = fig.add_subplot(16,2,20-odd)
    sections_longitude(ax,7435,7003,7106,datam,cmap,1200,unit,'init '+str(varname)+' eORCA36 init abort Cuba-Florida section x='+str(navlon[7003,7435].values)+'°E')
    ax = fig.add_subplot(16,2,22-odd)
    sections_longitude(ax,2725,2732,4696,datam,cmap,5000,unit,'init '+str(varname)+' eORCA36 init abort Australia-Antartica section x='+str(navlon[2732,2725].values)+'°E')
    ax = fig.add_subplot(16,2,24-odd)
    sections_longitude(ax,1524,5359,5854,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort Indonesian throughflow section x='+str(navlon[5359,1524].values)+'°E')
    ax = fig.add_subplot(16,2,26-odd)
    sections_longitude(ax,11050,2576,4832,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort South Africa section x='+str(navlon[2576,11050].values)+'°E')
    ax = fig.add_subplot(16,2,28-odd)
    sections_longitude(ax,12823,2794,4108,datam,cmap,5000,unit,'init '+str(varname)+' eORCA36 init abort Kerguelen section x='+str(navlon[2794,12823].values)+'°E')
    ax = fig.add_subplot(16,2,30-odd)
    sections_longitude(ax,3504,2386,4300,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort Campbell section x='+str(navlon[2386,3504].values)+'°E')
    ax = fig.add_subplot(16,2,32-odd)
    sections_longitude(ax,7914,2954,3790,datam,cmap,6000,unit,'init '+str(varname)+' eORCA36 init abort Drake section x='+str(navlon[2954,7914].values)+'°E')

all_sections(1,datatm,cmocean.cm.thermal,'°C','temperature')
all_sections(2,datasm,cmocean.cm.haline,'PSI','salinity')

fig.subplots_adjust(right=0.8)

plt.savefig(plotname)
