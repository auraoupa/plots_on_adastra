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


filein = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/votemper_MP026-eORCA36_MP026.nc'
filemask = '/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4.nc'

plotname ='plots/sections_temp_init_eORCA36.png'
ds=xr.open_dataset(filein)
data=ds['votemper'][0]
dsmask=xr.open_dataset(filemask)
tmask=dsmask['tmask'][0]
navlev=dsmask['nav_lev']
navlon=dsmask['nav_lon']
navlat=dsmask['nav_lat']
fig = plt.figure(figsize=(15,150))
datam=np.ma.array(data,mask=1-tmask)

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

ax = fig.add_subplot(15,1,1)
sections_latitude(ax,9181,4062,4135,datam,cmocean.cm.thermal,80,'°C','init temperature eORCA36 Bering section y='+str(navlat[9181,4062].values)+'°N')
ax = fig.add_subplot(15,1,2)
sections_latitude(ax,10145,9600,9945,datam,cmocean.cm.thermal,5000,'°C','init temperature eORCA36 Fram section y='+str(navlat[10145,9600].values)+'°N')
ax = fig.add_subplot(15,1,3)
sections_latitude(ax,9955,8331,8812,datam,cmocean.cm.thermal,2500,'°C','init temperature eORCA36 Baffin section y='+str(navlat[9955,8331].values)+'°N')
ax = fig.add_subplot(15,1,4)
sections_latitude(ax,7154,7446,7498,datam,cmocean.cm.thermal,1500,'°C','init temperature eORCA36 Florida-Bahamas section y='+str(navlat[7154,7446].values)+'°N')
ax = fig.add_subplot(15,1,5)
sections_latitude(ax,5563,11763,11934,datam,cmocean.cm.thermal,3500,'°C','init temperature eORCA36 Mozambique section y='+str(navlat[5563,11763].values)+'°N')
ax = fig.add_subplot(15,1,6)
sections_latitude(ax,5258,11406,12959,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Africa-Australia1 section y='+str(navlat[5258,11406].values)+'°N')
ax = fig.add_subplot(15,1,7)
sections_latitude(ax,5258,0,1578,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Africa-Australia2 section y='+str(navlat[5258,0].values)+'°N')
ax = fig.add_subplot(15,1,8)
sections_latitude(ax,5258,2835,7797,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Australia-America section y='+str(navlat[5258,2835].values)+'°N')
ax = fig.add_subplot(15,1,9)
sections_latitude(ax,5258,8634,10861,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 America-Africa section y='+str(navlat[5258,8634].values)+'°N')
ax = fig.add_subplot(15,1,10)
sections_longitude(ax,7435,7003,7106,datam,cmocean.cm.thermal,1500,'°C','init temperature eORCA36 Cuba-Florida section x='+str(navlon[7003,7435].values)+'°E')
ax = fig.add_subplot(15,1,11)
sections_longitude(ax,2725,2732,4696,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Australia-Antartica section x='+str(navlon[2732,2725].values)+'°E')
ax = fig.add_subplot(15,1,12)
sections_longitude(ax,1524,5359,5854,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Indonesian throughflow section x='+str(navlon[5359,1524].values)+'°E')
ax = fig.add_subplot(15,1,13)
sections_longitude(ax,11050,2576,4832,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 South Africa section x='+str(navlon[2576,11050].values)+'°E')
ax = fig.add_subplot(15,1,14)
sections_longitude(ax,12823,2794,4108,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Kerguelen section x='+str(navlon[2794,12823].values)+'°E')
ax = fig.add_subplot(15,1,15)
sections_longitude(ax,3504,2386,4300,datam,cmocean.cm.thermal,6000,'°C','init temperature eORCA36 Campbell section x='+str(navlon[2386,3504].values)+'°E')

#ax.plot([9232,9466], [9272,9146],color='teal',linewidth=3, label='Denmark')
#ax.plot([9741,10077], [9091,8737],color='yellow',linewidth=3, label='Iceland-Scotland')
#ax.plot([7435,7434], [7003,7106],color='blue',linewidth=3, label='Cuba-Florida')
#ax.plot([7914,8004], [3790,2954],color='orange',linewidth=3, label='Drake')
#ax.plot([2725,2724], [4696,2732],color='gold',linewidth=3, label='Australia-Antartica')
#ax.plot([1524,1524], [5854,5359],color='magenta',linewidth=3, label='Indonesian throughflow')
#ax.plot([11050,11050], [2576,4832],color='goldenrod',linewidth=3, label='South Africa')
#ax.plot([12823,12823], [2794,4108],color='whitesmoke',linewidth=3, label='Kerguelen')
#ax.plot([3504,3504], [2386,4300],color='lightgrey',linewidth=3, label='Campbell')


fig.subplots_adjust(right=0.8)
plt.savefig(plotname)
