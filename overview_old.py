import streamlit as st
import pandas as pd
import os
import json
import altair as alt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Flight 1 - results", page_icon=":chart_with_upwards_trend:")

pages = ["Flight 1", "Flight 2", "Flight 3"]
page = st.sidebar.selectbox("Wybierz stronę", pages)

if page == "Flight 1":
    st.header("Flight 1, altitude: 500m")
    dataset_path = "./experiments/flight_1/"
elif page == "Flight 2":
    st.header("Flight 2, altitude: 1500m")
    dataset_path = "./experiments/flight_2/"
elif page == "Flight 3":
    st.header("Flight 3, altitude: 1500m")
    dataset_path = "./experiments/flight_3/"

matchers=("loftr", "topicfm", "aspanformer", "dedode", "disk", "disk+dualsoftmax", "disk+lightglue", "superpoint+superglue", "superpoint+dualsoftmax", "superpoint+lightglue", "superpoint+mnn", "sift+sgmnet", "sosnet", "hardnet",  "alike",  "r2d2", "darkfeat", "sift", "roma",  "sold2")
list_providers = ['arcgis', 'google', 'geoportal']

results = []
for matcher in matchers:
    data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
    for provider in list_providers:
        for i in range(len(data)):
            results.append(dict(matcher=matcher.replace('+', '+\n'),
                                provider=provider,
                                inliers_count=data['ransac_'+provider][i],
                                processing_time=data['time_'+provider][i]))
            
df = pd.DataFrame(results)



aggregated = []
for (matcher,provider), g in df.groupby(['matcher','provider']):
    aggregated.append(dict(matcher=matcher,
                           provider=provider,
                           inliers_count=g.inliers_count.mean(),
                           processing_time=g.processing_time.mean(),
                           count=len(g)))

df_agg = pd.DataFrame(aggregated)




filename_list = os.listdir(dataset_path + "gopro")
for i, name in enumerate(filename_list):
    filename_list[i] = int(name[:-5])
filename_list = sorted(filename_list)

def draw_mean_bar_chart(header):
    st.header(header[7:])
    df = pd.DataFrame(columns=['matcher', header])
    for matcher in matchers:
        matcher_data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
        mean = matcher_data['ransac_arcgis'].mean()
        mean_rot = matcher_data['ransac_rot_arcgis'].mean()
        
        new_row = pd.DataFrame({'matcher': [matcher], 'mean': [mean], 'mean_rot': [mean_rot]})
        df = pd.concat([df, new_row], ignore_index=True)

    df_melt = df.melt('matcher', var_name='a', value_name='b')

    chart = alt.Chart(df_melt).mark_bar().encode(
        x='b:Q',
        y='matcher:N',
        color='a:N',
        tooltip=['a', 'b']
    )
    st.altair_chart(chart, use_container_width=True)
    

st.header('the mean impact of using yaw trading information for 3 providers')
col1, col2, col3 = st.columns(3)
with col1:
    draw_mean_bar_chart('ransac_arcgis')
with col2:
    draw_mean_bar_chart('ransac_google')
with col3:
    draw_mean_bar_chart('ransac_geoportal')
   



json_data = pd.DataFrame()

for filename in filename_list:
    with open(dataset_path + "gopro/" + str(filename) + '.json', 'r') as file:
        data = json.load(file)
        data["file_gopro"] = filename
        data_df = pd.DataFrame([data]) 
        json_data = pd.concat([json_data, data_df], ignore_index=True)
    
st.header('Angles during flight')
col1, col2, col3 = st.columns(3)
with col1:
    st.header("resulant_angle angle")
    st.line_chart(json_data, x="file_gopro", y="resulant_angle")
with col2:
    st.header("resulant_angle_dir")
    st.line_chart(json_data, x="file_gopro", y="resulant_angle_dir")
with col3:
    st.header("yaw angle")
    st.line_chart(json_data, x="file_gopro", y="yaw")
    
st.header('altitude_agl / zoom')
base = alt.Chart(json_data).encode(
    alt.X('file_gopro:Q', scale=alt.Scale(zero=False)))

line1 = base.mark_line(color='lightblue').encode(
    alt.Y('zoom:Q', axis=alt.Axis(title='zoom', titleColor='lightblue')))

line2 = base.mark_line(color='lightblue').encode(
    alt.Y('altitude_agl:Q', axis=alt.Axis(title='altitude_agl', titleColor='lightblue')))

chart = alt.layer(line1, line2).resolve_scale(y='independent')

st.altair_chart(chart, use_container_width=True)













st.header('Mean number of points vs mean execution time for each matcher') 
points = []
number = 0

for matcher in matchers:
    
    number += 1
    
    matcher_data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
    time_mean = pd.concat([matcher_data['time_arcgis'], matcher_data['time_google'], matcher_data['time_geoportal']]).mean()
    ransac_mean = pd.concat([matcher_data['ransac_arcgis'], matcher_data['ransac_google'], matcher_data['ransac_geoportal']]).mean()

    if "+" in matcher:
        matcher = matcher.replace("+", "+\n")
        
    points.append({"number": number, "matcher": matcher, "X": time_mean, "Y": ransac_mean})
    
data = pd.DataFrame(points, columns=['number', 'matcher', 'X', 'Y'])
    
    
    
    
    
    
st.header('matplotlib - Mean number of points vs mean execution time for each matcher')     
import matplotlib.pyplot as plt
from adjustText import adjust_text

fig, ax = plt.subplots()

ax.scatter(data['X'], data['Y'], s=3)
ax.grid(True, which='both')
ax.set_xlabel('Execution time [ms]')
ax.set_ylabel('Number of points (RANSAC)')
ax.minorticks_on()

texts = []
for i, txt in enumerate(data['number']):
    texts.append(ax.text(data['X'].iloc[i], data['Y'].iloc[i], txt, fontsize=5, ha='center', va='bottom'))

adjust_text(texts)
st.pyplot(fig)

output_text = ', '.join([f"{point['number']}-{point['matcher']}" for point in points])

st.write(output_text)






st.header('Violin plots') 

json_data = pd.DataFrame()

for filename in filename_list:
    with open(dataset_path + "gopro/" + str(filename) + '.json', 'r') as file:
        data = json.load(file)
        data["file_gopro"] = filename
        data_df = pd.DataFrame([data]) 
        json_data = pd.concat([json_data, data_df], ignore_index=True)

matchers = matchers[:10]
points = []
for matcher in matchers:
    
    matcher_data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
    
    for x, y in zip(matcher_data['ransac_arcgis'], json_data['resulant_angle']): #ile punktów było dla kątów (-5, 5), (5-10) itd...
        points.append({"matcher": matcher, "X": x, "Y": y})
    
data = pd.DataFrame(points, columns=['matcher', 'X', 'Y'])
    
# Generowanie wykresu wiolinowego
plt.figure(figsize=(10,6))
sns.violinplot(x='matcher', y='Y', data=data)

# Wyświetlenie wykresu w Streamlit
st.pyplot(plt.gcf())








st.header('the detailed impact of using yaw trading information for 3 providers')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("## Arcgis")
with col2:
    st.markdown("## Google")
with col3:
    st.markdown("## Geoportal")        
        
for matcher in matchers:
    
    data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
    for i, name in enumerate(data[data.columns[0]]):
        data.loc[i, data.columns[0]] = int(name[:-4])  
      
    st.header(matcher)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_arcgis", "ransac_rot_arcgis"])

    with col2:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_google", "ransac_rot_google"])

    with col3:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_geoportal", "ransac_rot_geoportal"])



