import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches

## Load the training data
tr = pd.read_csv("DATA_PATH"); #You have to set the DATA_PATH

## Optimization of the number of cluster
# 1. Elbow[SSE]
SSE = []
batch_size = 8192  # Adjust the batch size based on available memory

for i in range(4,51):
    mbkmeans = MiniBatchKMeans(n_clusters= i, init='k-means++', batch_size=batch_size, random_state=77)
    mbkmeans.fit(tr) 
    SSE.append(mbkmeans.inertia_)
    
# 2. Gap statics
# Gap Statistic for K means
def optimalK(data, nrefs=3, maxClusters=15):
    """
    Calculates KMeans optimal K using Gap Statistic 
    Params:
        data: ndarry of shape (n_samples, n_features)
        nrefs: number of sample reference datasets to create
        maxClusters: Maximum number of clusters to test for
    Returns: (gaps, optimalK)
    """
    gaps = np.zeros((len(range(4, maxClusters)),))
    resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
    for gap_index, k in enumerate(range(4, maxClusters)):
# Holder for reference dispersion results
        start = int(time.time())    
        print('Case  ' + str(k) + '  Start!!!')
        refDisps = np.zeros(nrefs)
# For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
        for i in range(nrefs):
            #print('Sample  N_' + str(i) )
            # Create new random reference set
            randomReference = np.random.random_sample(size=data.shape)
            
            # Fit to it
            km = MiniBatchKMeans(k, batch_size = batch_size, random_state=77)
            km.fit(randomReference)
            
            refDisp = km.inertia_
            refDisps[i] = refDisp
# Fit cluster to original data and create dispersion      
        km = MiniBatchKMeans(k, batch_size = batch_size, random_state=77)
        km.fit(data)
        print('Fit  N_' + str(k) + "   Done :)  ***run time(sec) :", int(time.time()) - start)
        
        origDisp = km.inertia_
# Calculate gap statistic
        gap = np.log(np.mean(refDisps)) - np.log(origDisp)
# Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap
        
        resultsdf = resultsdf.append({'clusterCount':k, 'gap':gap}, ignore_index=True)
        gc.collect()
        
    return(gaps.argmax() + 1, resultsdf)

score_g, df = optimalK(dc, nrefs=10, maxClusters=51)
GAP = df['gap']

# 3. Silhouette coefficient
SCE = []

for i in range(4,51):
    mbkmeans = MiniBatchKMeans(n_clusters= i, init='k-means++', batch_size=batch_size, random_state=77)
    mbkmeans.fit(dc) 
    score = silhouette_samples(tr, mbkmeans.labels_, metric='euclidean')
    SCE.append(score.mean())

## MBK K-means 
k=14
batch_size = 8192  # Adjust the batch size based on available memory
mbkmeans = MiniBatchKMeans(n_clusters=k, init='k-means++', batch_size=batch_size, random_state=77)
mbkmeans.fit(tr)

# Add a new column to the original DataFrame with the cluster labels
tr['Cluster'] = mbkmeans.labels_
Cluster_results = tr[['Name','Lat','Lon','Cluster']]
Cluster_results.to_csv('Cl.csv', index=False)


## Load the Cluster results 
Cluster_Fig_data = pd.read_csv('Cl.csv') # Please go to and get the cluster result from the path ('SWEML/DATA')

## rearrange the Cluster number for visualization
figure_mapping = {9:0, 10:1, 11:2, 12:3, 0:4, 1:5,
                  2:6, 3:7, 4:8, 5:9, 6:10, 7:11, 8:12}

Cluster_Fig_data['Cluster'] = Cluster_Fig_data['Cluster'].replace(figure_mapping)

## Assign the color
cluster_colors = {0: 'magenta', 1: 'lime', 2: 'indigo', 3: 'orange', 4: 'red', 
                  5: 'green', 6: 'blue', 7: 'purple', 8: 'yellow', 9: 'deepskyblue', 
                  10: 'gray', 11: 'brown', 12: 'teal'}
colors = [cluster_colors[cluster] for cluster in Cluster_Fig_data['Cluster']]

## Draw the figure
m = Basemap(projection='cyl', resolution='l', #area_thresh=1.0,
            llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)

plt.figure(figsize=(50,18))

m.drawcoastlines()
m.drawcountries()
m.scatter(Cluster_Fig_data['Lon'], Cluster_Fig_data['Lat'], s=20, latlon=True, 
          c=colors, alpha=1)

parallels = np.arange(-90., 91., 30.);  # y축 눈금선 설정
meridians = np.arange(-180., 181., 30.);  # x축 눈금선 설정
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=40, linewidth=0)  # y축 눈금선
m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=40, linewidth=0)  # x축 눈금선

legend_handles = []
for cluster, color in cluster_colors.items():
    lt = len(Cluster_Fig_data[Cluster_Fig_data['Cluster'] == cluster]['Name'])
    legend_handles.append(mpatches.Patch(color=color, label=f'CL{cluster+1}: {lt} sites'))    

plt.legend(handles=legend_handles, fontsize=27, loc='lower left')

plt.show()
