import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches

## Load the Cluster results 
Fig_data = read.table("SWE_Insitu_data_info.txt", sep=";", header=T) # Please go to and get the cluster result from the path ('SWEML/DATA')

## Assign the color
cluster_colors = {'SNOTEL': 'gray', 'CSS': 'purple', 'SCAN': 'deepskyblue', 'RSSD': 'blue', 'CHCN': 'red', 
                  'NVE': 'darkgreen', 'EnviDat': 'darkorange', 'GHCN': 'yellow', 'HSSC':'deeppink'}
colors = [cluster_colors[cluster] for cluster in Fig_data['Network']]

## Draw the figure
m = Basemap(projection='cyl', resolution='l', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)

plt.figure(figsize=(50,40))

m.scatter(Fig_data['ERA.Lon.G.N.RC'], Fig_data['ERA.Lat.G.N.RC'], s=25, latlon=True, 
          c=colors, alpha=1)

m.drawcoastlines()
m.drawcountries()
parallels = np.arange(-90., 91., 30.);  
meridians = np.arange(-180., 181., 30.);  
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=50, linewidth=0)
m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=50, linewidth=0) 

legend_handles = []
for cluster, color in cluster_colors.items():
    lt = len(Fig_data[Fig_data['Network'] == cluster]['ID'])
    legend_handles.append(mpatches.Patch(color=color, label=f'{cluster}: {lt} points'))    

plt.legend(handles=legend_handles, fontsize=40, loc='lower left')

plt.show()
