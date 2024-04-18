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
    st.header("Flight 3, altitude: 150m")
    dataset_path = "./experiments/flight_3/"

matchers=("loftr", "topicfm", "aspanformer", "dedode", "disk", "disk+dualsoftmax", "disk+lightglue", "superpoint+superglue", "superpoint+dualsoftmax", "superpoint+lightglue", "superpoint+mnn", "sift+sgmnet", "sosnet", "hardnet",  "alike",  "r2d2", "darkfeat", "sift", "roma",  "sold2")
list_providers = ['arcgis', 'google', 'geoportal']

def group_angle(angle):
    angle = float(angle)
    if angle < 5:
        return '0-5'
    elif angle < 10:
        return '5-10'
    elif angle < 15:
        return '10-15'
    elif angle < 20:
        return '15-20'
    else:
        return '>20'
     
results = []
for matcher in matchers:
    data = pd.read_csv(dataset_path + matcher + ".csv", sep=";")
    for provider in list_providers:
        for i in range(len(data)):
            with open(dataset_path + "gopro/" + data['file_gopro'][i][:-3] + 'json', 'r') as file:
                json_data = json.load(file)
        
            results.append(dict(
                                matcher=matcher,
                                provider=provider,
                                inliers_count=data['ransac_'+provider][i],
                                inliers_rot_count=data['ransac_rot_'+provider][i],
                                processing_time=data['time_'+provider][i],
                                file_gopro=data['file_gopro'][i],
                                resulant_angle=group_angle(json_data['resulant_angle']) 
                                ))

df = pd.DataFrame(results)

st.header('The number of correct points for each algorithm grouped by provider')
_df = df.pivot_table(index='matcher', columns='provider', values='inliers_count', aggfunc='median')
_df.iloc[::-1].plot.barh(width=0.8)
st.pyplot(plt.gcf())

st.header('The number of correct points for each algorithm grouped by angle of rotation (deg)')
column_order = ['0-5', '5-10', '10-15', '15-20', '>20']
_df = df.pivot_table(index='matcher', columns='resulant_angle', values='inliers_count', aggfunc='median')
_df = _df.reindex(column_order, axis=1)
_df.iloc[::-1].plot.barh(width=0.8)
st.pyplot(plt.gcf())

st.header('The number of correct points for each algorithm grouped by if map rotation')
_df = pd.DataFrame({'matcher': matchers, 'inliers_count': df.groupby('matcher')['inliers_count'].mean(), 'inliers_rot_count': df.groupby('matcher')['inliers_rot_count'].mean()})
_df.iloc[::-1].plot.barh(width=0.8)
st.pyplot(plt.gcf())

plt.figure(figsize=(20,6))
sns.violinplot(data=df, x="matcher", y="inliers_count", hue="provider")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,6))
sns.violinplot(data=df, x="matcher", y="processing_time", hue="provider")
st.pyplot(plt.gcf())

plt.figure(figsize=(10,6))
sns.violinplot(data=df, y="inliers_count", x="matcher")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,6))
sns.scatterplot(data=df, x='matcher',y='inliers_count', hue=df['provider'])
st.pyplot(plt.gcf())

aggregated = []
for (matcher,provider), g in df.groupby(['matcher','provider']):
    aggregated.append(dict(matcher=matcher,
                           provider=provider,
                           inliers_count=g.inliers_count.mean(),
                           processing_time=g.processing_time.mean(),
                           count=len(g)))

df_agg = pd.DataFrame(aggregated)

plt.figure(figsize=(20,6))
sns.scatterplot(data=df_agg, x='processing_time',y='inliers_count',size='count', hue=df_agg['matcher'])
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.violinplot(data=df, x="matcher", y="inliers_count")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.violinplot(data=df_agg, x="matcher", y="inliers_count")
st.pyplot(plt.gcf())

st.header('violinplot - inliers_count vs provider') 
plt.figure(figsize=(20,8))
sns.violinplot(data=df, x="provider", y="inliers_count")
st.pyplot(plt.gcf())

st.header('violinplot - inliers_count vs provider with aggregation by provider') 
plt.figure(figsize=(20,8))
sns.violinplot(data=df_agg, x="provider", y="inliers_count")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,18))
sns.violinplot(data=df_agg, x="inliers_count", y="matcher")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.kdeplot(data=df, x='inliers_count',hue='matcher')
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.kdeplot(data=df, x='processing_time',hue='matcher')
st.pyplot(plt.gcf())

plt.figure(figsize=(10,6))
sns.kdeplot(data=df, x='inliers_count',hue='provider')
st.pyplot(plt.gcf())

plt.figure(figsize=(10,6))
sns.kdeplot(data=df, x='processing_time',hue='provider')
st.pyplot(plt.gcf())

# plt.figure(figsize=(10,10))
# plt.subplot(2,2,1)
# plt.title('multiple="layer"')
# sns.histplot(data=df, x='inliers_count',hue='provider', multiple="layer") #default
# st.pyplot(plt.gcf())

# plt.subplot(2,2,2)
# plt.title('multiple="dodge"')
# sns.histplot(data=df, x='inliers_count',hue='provider', multiple="dodge")
# st.pyplot(plt.gcf())

# plt.subplot(2,2,3)
# plt.title('multiple="stack"')
# sns.histplot(data=df, x='inliers_count',hue='provider', multiple="stack")
# st.pyplot(plt.gcf())

# plt.subplot(2,2,4)
# plt.title('multiple="fill"')
# sns.histplot(data=df, x='inliers_count',hue='provider', multiple="fill")
# st.pyplot(plt.gcf())

