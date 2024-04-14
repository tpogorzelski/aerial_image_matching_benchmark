import streamlit as st
import pandas as pd
import os
import json
import altair as alt

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Flight 1 - results", page_icon=":chart_with_upwards_trend:")

def draw_mean_bar_chart(header):
    st.header(header[7:])
    df = pd.DataFrame(columns=['matcher', header])
    for matcher in matchers_list:
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
    
dataset_path = "./experiments/flight_1/"
   
filename_list = os.listdir(dataset_path + "gopro")
for i, name in enumerate(filename_list):
    filename_list[i] = int(name[:-5])
filename_list = sorted(filename_list)

matchers_list=("loftr", "topicfm", "aspanformer", "dedode", "disk", "disk+dualsoftmax", "disk+lightglue", "superpoint+superglue", "superpoint+dualsoftmax", "superpoint+lightglue", "superpoint+mnn", "sift+sgmnet", "sosnet", "hardnet",  "alike",  "r2d2", "darkfeat", "sift", "roma",  "sold2")
# "disk", "disk+dualsoftmax", , "disk+lightglue","d2net", "rord","lanet","DKMv3", "gluestick",

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

st.header('the mean impact of using yaw trading information for 3 providers')
col1, col2, col3 = st.columns(3)
with col1:
    draw_mean_bar_chart('ransac_arcgis')
with col2:
    draw_mean_bar_chart('ransac_google')
with col3:
    draw_mean_bar_chart('ransac_geoportal')

st.header('the detailed impact of using yaw trading information for 3 providers')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("## Arcgis")
with col2:
    st.markdown("## Google")
with col3:
    st.markdown("## Geoportal")        
        
for matcher in matchers_list:
    
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
        st.line_chart(data, x="file_gopro", y=["ransac_arcgis", "ransac_rot_google"])

    with col3:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_arcgis", "ransac_rot_geoportal"])

