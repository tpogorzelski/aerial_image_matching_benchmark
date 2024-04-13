import streamlit as st
import pandas as pd
import os
import json
import altair as alt

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Moja aplikacja", page_icon=":chart_with_upwards_trend:")


def draw_mean_bar_chart(header):
    st.header('mean '+header)
    df = pd.DataFrame(columns=['matcher', header])
    for matcher in matchers_list:
        matcher_data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
        mean = matcher_data['ransac_arcgis'].mean()
        mean_rot = matcher_data['ransac_rot_arcgis'].mean()
        
        df = df.append({'matcher': matcher, 'mean': mean, 'mean_rot': mean_rot}, ignore_index=True)

    df_melt = df.melt('matcher', var_name='a', value_name='b')

    chart = alt.Chart(df_melt).mark_bar().encode(
        x='b:Q',
        y='matcher:N',
        color='a:N',
        tooltip=['a', 'b']
    )
    st.altair_chart(chart, use_container_width=True)
    
dataset_path = "/mnt/d/Pobrane/dataset_lot1/"

filename_list = os.listdir(dataset_path + "arcgis")
for i, name in enumerate(filename_list):
    filename_list[i] = int(name[:-4])
filename_list = sorted(filename_list)

matchers_list=("loftr", "topicfm", "aspanformer", "dedode", "superpoint+superglue", "superpoint+dualsoftmax", "superpoint+lightglue", "superpoint+mnn", "sift+sgmnet", "sosnet", "hardnet",  "alike",  "r2d2", "darkfeat", "sift", "roma",  "sold2")
# "disk", "disk+dualsoftmax", , "disk+lightglue","d2net", "rord","lanet","DKMv3", "gluestick",

json_data = pd.DataFrame()

for filename in filename_list:
    with open(dataset_path + "gopro/" + str(filename) + '.json', 'r') as file:
        data = json.load(file)
        data["file_gopro"] = filename
        json_data = json_data.append(data, ignore_index=True)
    

st.header("yaw angle")
st.line_chart(json_data, x="file_gopro", y="yaw")
  
col1, col2 = st.columns(2)
with col1:
    st.header("resulant_angle angle")
    st.line_chart(json_data, x="file_gopro", y="resulant_angle")
with col2:
    st.header("resulant_angle_dir")
    st.line_chart(json_data, x="file_gopro", y="resulant_angle_dir")

# altitude_agl / zoom
base = alt.Chart(json_data).encode(
    alt.X('file_gopro:Q', scale=alt.Scale(zero=False)))

line1 = base.mark_line(color='lightblue').encode(
    alt.Y('zoom:Q', axis=alt.Axis(title='zoom', titleColor='lightblue')))

line2 = base.mark_line(color='lightblue').encode(
    alt.Y('altitude_agl:Q', axis=alt.Axis(title='altitude_agl', titleColor='lightblue')))

chart = alt.layer(line1, line2).resolve_scale(y='independent')

st.altair_chart(chart, use_container_width=True)



draw_mean_bar_chart('ransac_arcgis')




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
        data[data.columns[0]][i] = int(name[:-4])
      
    col1, col2, col3 = st.columns(3)
    st.header(matcher)
      
    with col1:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_arcgis", "ransac_rot_arcgis"])

    with col2:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_arcgis", "ransac_rot_google"])

    with col3:
        data = data.sort_values(by=[data.columns[0]])
        st.line_chart(data, x="file_gopro", y=["ransac_arcgis", "ransac_rot_geoportal"])


