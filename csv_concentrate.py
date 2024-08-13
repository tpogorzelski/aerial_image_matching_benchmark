import pandas as pd
import os

#stwórz listę wszystkich nazw plików csv w podanym katalogu
files = os.listdir('experiments/new/gopro_H/20230927_1')

for name in files:
    name = name.split('.')[0]


    data = '20230927_1'
    
    df_gopro = pd.read_csv(f'experiments/new/gopro/{data}/{name.lower()}.csv', sep=';')
    
    
    df_gopro_H = pd.read_csv(f'experiments/new/gopro_H/{data}/{name}.csv', sep=';')
    print('input: ', df_gopro.shape, df_gopro_H.shape)
    
    

    #łączenie csv z gopro i gopro_H
    df_combined = df_gopro
    df_combined['ransac_rot_arcgis'] = df_gopro_H['ransac_rot_arcgis']
    df_combined['H_rot_arcgis'] = df_gopro_H['H_rot_arcgis']
    df_combined['F_rot_arcgis'] = df_gopro_H['F_rot_arcgis']
    df_combined['time_rot_arcgis'] = df_gopro_H['time_rot_arcgis']
    df_combined['ransac_rot_google'] = df_gopro_H['ransac_rot_google']
    df_combined['H_rot_google'] = df_gopro_H['H_rot_google']
    df_combined['F_rot_google'] = df_gopro_H['F_rot_google']
    df_combined['time_rot_google'] = df_gopro_H['time_rot_google']
    df_combined['ransac_rot_geoportal'] = df_gopro_H['ransac_rot_geoportal']
    df_combined['H_rot_geoportal'] = df_gopro_H['H_rot_geoportal']
    df_combined['F_rot_geoportal'] = df_gopro_H['F_rot_geoportal']
    df_combined['time_rot_geoportal'] = df_gopro_H['time_rot_geoportal']
    print('output:', df_combined.shape)
    exit()
    
    # Zapisz połączony DataFrame do nowego pliku CSV
    plik_wyjsciowy = f'experiments/new/{name}.csv'
    df_combined.to_csv(plik_wyjsciowy, index=False, sep=';')

    print(f'Połączony plik CSV został zapisany jako {plik_wyjsciowy}')

 