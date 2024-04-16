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

# pages = ["Flight 1", "Flight 2", "Flight 3"]
pages = ["Flight 1"]
page = st.sidebar.selectbox("Wybierz stronę", pages)

if page == "Flight 1":
    st.header("Flight 1, altitude: 500m")
    dataset_path = "./experiments/flight_1/"
# elif page == "Flight 2":
#     st.header("Flight 2, altitude: 1500m")
#     dataset_path = "./experiments/flight_2/"
# elif page == "Flight 3":
#     st.header("Flight 3, altitude: 1500m")
#     dataset_path = "./experiments/flight_3/"

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

plt.figure(figsize=(20,6))
sns.violinplot(data=df, x="matcher", y="inliers_count", hue="provider")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,6))
sns.violinplot(data=df, x="matcher", y="processing_time", hue="provider")
st.pyplot(plt.gcf())

plt.figure(figsize=(10,30))
sns.violinplot(data=df, y="matcher", x="inliers_count", hue="provider")
st.pyplot(plt.gcf())


aggregated = []
for (matcher,provider), g in df.groupby(['matcher','provider']):
    aggregated.append(dict(matcher=matcher,
                           provider=provider,
                           inliers_count=g.inliers_count.mean(),
                           processing_time=g.processing_time.mean(),
                           count=len(g)))

df_agg = pd.DataFrame(aggregated)

plt.figure(figsize=(30,30))
sns.scatterplot(data=df_agg, x='processing_time',y='inliers_count',size='count', hue=df_agg[['matcher','provider']].apply(tuple, axis=1))
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.violinplot(data=df, x="matcher", y="inliers_count")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.violinplot(data=df_agg, x="matcher", y="inliers_count")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.violinplot(data=df, x="provider", y="inliers_count")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.violinplot(data=df_agg, x="provider", y="inliers_count")
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

plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
plt.title('multiple="layer"')
sns.histplot(data=df, x='inliers_count',hue='provider', multiple="layer") #default
st.pyplot(plt.gcf())

plt.subplot(2,2,2)
plt.title('multiple="dodge"')
sns.histplot(data=df, x='inliers_count',hue='provider', multiple="dodge")
st.pyplot(plt.gcf())

plt.subplot(2,2,3)
plt.title('multiple="stack"')
sns.histplot(data=df, x='inliers_count',hue='provider', multiple="stack")
st.pyplot(plt.gcf())

plt.subplot(2,2,4)
plt.title('multiple="fill"')
sns.histplot(data=df, x='inliers_count',hue='provider', multiple="fill")
st.pyplot(plt.gcf())

