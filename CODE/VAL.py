import os
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import math
from sklearn.metrics import mean_absolute_error

from netCDF4 import Dataset
import multiprocessing
from multiprocessing import Array
import time


# Load the in-situ data
IS_data = pd.read_csv('DATA_PATH', sep=',', header=0) # You have to load the in-situ dataset.

# Load the SWEML and reference datas (ESAGB, GLDAS, AMSRE)
df_all = pd.read_csv('DATA_PATH', sep=',', header=0) # Preparation of SWEML data and reference data for the grid points where in-situ measurements are assigned

#Data handle for validation with Reference datasets (Please see the Sector 2.1.2 in paper)
esa_el = IS_data[IS_data['Lat.G.N.RC'] < 35]['ID'].values ## ESAGB
df_esa_removed = df_all[~df_all['ID'].isin(esa_el)]
new_id = df_esa_removed['ID'].drop_duplicates() 
new_id.reset_index(drop=True, inplace=True)

df = df_esa_removed[pd.notna(df_esa_removed['AMSRE'])] ## AMSRE
new_id = df['ID'].drop_duplicates()
new_id.reset_index(drop=True, inplace=True)

# Error value Calculation with each site
manager = multiprocessing.Manager()
dt = manager.list()

def process_data(i):    
    global swe, IS_data, dt, new_id
    
    dt.append([new_id[i],IS_data[IS_data['ID'] == new_id[i]]['Cluster'].values[0],
               IS_data[IS_data['ID'] == new_id[i]]['ERA.Lat.G.N.RC'].values[0],
               IS_data[IS_data['ID'] == new_id[i]]['ERA.Lon.G.N.RC'].values[0],
               IS_data[IS_data['ID'] == new_id[i]]['ELV'].values[0],
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['SWEML'])),
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ERARE'])),
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['GLDAS'])),
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ESAGB'])),
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['AMSRE'])),
               mean_absolute_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['SWEML']) / np.mean(swe['STSWE']),
               mean_absolute_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ERARE']) / np.mean(swe['STSWE']),
               mean_absolute_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['GLDAS']) / np.mean(swe['STSWE']),
               mean_absolute_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ESAGB']) / np.mean(swe['STSWE']),
               mean_absolute_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['AMSRE']) / np.mean(swe['STSWE']),
               np.mean(swe[swe['ID'] == new_id[i]]['SWEML'] - swe[swe['ID'] == new_id[i]]['STSWE']),
               np.mean(swe[swe['ID'] == new_id[i]]['ERARE'] - swe[swe['ID'] == new_id[i]]['STSWE']),
               np.mean(swe[swe['ID'] == new_id[i]]['GLDAS'] - swe[swe['ID'] == new_id[i]]['STSWE']),
               np.mean(swe[swe['ID'] == new_id[i]]['ESAGB'] - swe[swe['ID'] == new_id[i]]['STSWE']),
               np.mean(swe[swe['ID'] == new_id[i]]['AMSRE'] - swe[swe['ID'] == new_id[i]]['STSWE']),
               np.corrcoef(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['SWEML'])[0,1], 
               np.corrcoef(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ERARE'])[0,1],
               np.corrcoef(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['GLDAS'])[0,1], 
               np.corrcoef(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ESAGB'])[0,1],
               np.corrcoef(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['AMSRE'])[0,1],
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['SWEML'])) / (np.max(swe['STSWE'])-np.min(swe['STSWE'])) * 100,
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ERARE'])) / (np.max(swe['STSWE'])-np.min(swe['STSWE'])) * 100,
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['GLDAS'])) / (np.max(swe['STSWE'])-np.min(swe['STSWE'])) * 100,
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['ESAGB'])) / (np.max(swe['STSWE'])-np.min(swe['STSWE'])) * 100,
               math.sqrt(mean_squared_error(swe[swe['ID'] == new_id[i]]['STSWE'], swe[swe['ID'] == new_id[i]]['AMSRE'])) / (np.max(swe['STSWE'])-np.min(swe['STSWE'])) * 100
              ])

def main():
    start = int(time.time())
    pool = multiprocessing.Pool(processes=60)
    pool.map(process_data, range(len(new_id)))
    pool.close()
    pool.join()
    
start = int(time.time())
if __name__ == "__main__":
    main()
    dt = list(dt) 
    dt = np.array(dt, dtype=object)
    dt_df = pd.DataFrame(dt, columns=['ID', 'Cluster', 'Lat', 'Lon', 'ELV',
                                      'RMSE_SWEML', 'RMSE_ERARE', 'RMSE_GLDAS', 'RMSE_ESAGB', 'RMSE_AMSRE',
                                      'MAE_SWEML', 'MAE_ERARE', 'MAE_GLDAS', 'MAE_ESAGB', 'MAE_AMSRE',
                                      'BIAS_SWEML', 'BIAS_ERARE', 'BIAS_GLDAS', 'BIAS_ESAGB', 'BIAS_AMSRE',
                                      'R_SWEML','R_ERARE','R_GLDAS','R_ESAGB', 'R_AMSRE',
                                      'NRMSE_SWEML','NRMSE_ERARE','NRMSE_GLDAS','NRMSE_ESAGB','NRMSE_AMSRE'])
print('time: ',(int(time.time()) - start) / 60, '         Completed!!!!!')


#sorted dataframe
val_results_esa = dt_df.sort_values(by='ID', ascending=True)
val_results_esa_bp = val_results_esa.copy() 





