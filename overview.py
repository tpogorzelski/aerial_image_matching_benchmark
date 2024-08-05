import streamlit as st
import pandas as pd
import os
import json
import altair as alt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Algorithm comparison results", page_icon=":chart_with_upwards_trend:")

altitudes = [150, 500, 1500]
matchers=("LoFTR", "TopicFM", "AspanFormer", "DeDoDe", "SuperPoint+SuperGlue", "SuperPoint+LightGlue", "DISK", "DISK+DualSoftmax", "SuperPoint+DualSoftmax", "DISK+LightGlue", "SuperPoint+MNN", "SIFT+SGMNet", "SOSNet", "HardNet", "D2Net", "RORD", "ALIKE", "LANET", "R2D2", "DARKFeat", "SIFT", "ROMA", "DKMv3", "GlueStick", "SOLD2")

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
for altitude in altitudes:
    dataset_path = "./experiments/alt_" + str(altitude) + "/"
    for matcher in matchers:
        data = pd.read_csv(dataset_path + matcher.lower() + ".csv", sep=";")
        for provider in list_providers:
            for i in range(len(data)):
                with open(dataset_path + "gopro/" + data['file_gopro'][i][:-3] + 'json', 'r') as file:
                    json_data = json.load(file)
            
                results.append(dict(
                                    Matcher=matcher,
                                    provider=provider,
                                    altitude=altitude,
                                    inliers_count=data['ransac_'+provider][i],
                                    inliers_rot_count=data['ransac_rot_'+provider][i],
                                    processing_time=data['time_'+provider][i],
                                    processing_rot_time=data['time_rot_'+provider][i],
                                    file_gopro=data['file_gopro'][i],
                                    
                                    resultant_angle=group_angle(json_data['resultant_angle']) 
                                    ))

df = pd.DataFrame(results)

fig, ax = plt.subplots(figsize=(4, 10))
_df = df.pivot_table(index='Matcher', columns='altitude', values='inliers_count', aggfunc='median')
ax = _df.iloc[::-1].plot.barh(width=0.8) 
ax.set_xlabel("Median number of correct points")    
ax.set_ylabel("")
ax.legend(loc='lower right')
for i, v in enumerate(_df.iloc[::-1].values):
    mean_value = np.mean(v)  # Oblicz średnią
    ax.text(float(mean_value +5), i-0.3, str(round(mean_value)), fontsize=10)
st.pyplot(plt.gcf())

fig, ax = plt.subplots(figsize=(3, 10))
_df = df.pivot_table(index='Matcher', columns='provider', values='inliers_count', aggfunc='median')
ax = _df.iloc[::-1].plot.barh(width=0.8) 
ax.set_xlabel("Median number of correct points")
ax.set_ylabel("")
ax.legend(loc='lower right')
ax.set_yticklabels([])
for i, v in enumerate(_df.iloc[::-1].values):
    mean_value = np.mean(v)  # Oblicz średnią
    ax.text(float(mean_value +5), i-0.3, str(round(mean_value)), fontsize=10)
st.pyplot(plt.gcf())

st.write('x - median number of correct points')

fig, ax = plt.subplots(figsize=(3.9, 5))
column_order = ['0-5', '5-10', '10-15', '15-20', '>20']
_df = df.pivot_table(index='Matcher', columns='resultant_angle', values='inliers_count', aggfunc='median')
_df = _df.reindex(column_order, axis=1)
ax = _df.iloc[::-1].plot.barh(width=0.8) 
ax.set_xlabel("Median number of correct points")
ax.set_ylabel("")
ax.legend(loc='lower right')
for i, v in enumerate(_df.iloc[::-1].values):
    mean_value = np.mean(v)  # Oblicz średnią
    ax.text(float(mean_value +10), i-0.3, str(round(mean_value)), fontsize=8)
st.pyplot(plt.gcf())

fig, ax = plt.subplots(figsize=(3, 5))
_df = df.pivot_table(index='Matcher', values=['inliers_count', 'inliers_rot_count'], aggfunc='median')    
ax = _df.iloc[::-1].plot.barh(width=0.8)  
ax.set_xlabel("Median number of correct points")
ax.set_ylabel("")
ax.legend(loc='lower right')
ax.set_yticklabels([])
for i, row in enumerate(_df.iloc[::-1].values):
    if row[0] != 0: 
        increase = round((row[1]/row[0]-1)*100)
    else: 
        increase = 0
    ax.text(row[1]+3, i, '+'+str(increase)+'%', fontsize=8)
st.pyplot(plt.gcf())
        
st.write('x - median number of correct points')

# plt.subplot(1, 3, 1)
# st.header('The number of correct points for each algorithm grouped by if map rotation')
# _df = pd.DataFrame({'Matcher': matchers, 'inliers_rot_count': df.groupby('Matcher')['inliers_rot_count'].median(), 'inliers_count': df.groupby('Matcher')['inliers_count'].median()})
# ax = _df.iloc[::-1].plot.barh(width=0.8)
# ax.set_xlabel("Median number of correct points")
# st.pyplot(plt.gcf())

st.header('The correct point density distribution for each algorithm')
plt.figure(figsize=(20,36))
sns.violinplot(data=df, x="inliers_count", y="Matcher", cut=0, density_norm="width")
st.pyplot(plt.gcf())

aggregated = []
for (matcher,provider), g in df.groupby(['Matcher','provider']):
    aggregated.append(dict(Matcher=matcher,
                           provider=provider,
                           inliers_count=g.inliers_count.mean(),
                           inliers_rot_count=g.inliers_rot_count.mean(),
                           processing_time=g.processing_time.mean(),
                           processing_rot_time=g.processing_rot_time.mean(),
                           count=len(g)))

df_agg = pd.DataFrame(aggregated)


# df_agg['ratio'] = df_agg['inliers_count'] / df_agg['processing_time']
# _df = df_agg.pivot_table(index='Matcher', values='ratio', aggfunc='median')
# ax = _df.iloc[::-1].plot.barh(width=0.8)  
# # ax.set_xlabel("Median number of correct points")
# ax.set_ylabel("")
# # ax.legend(loc='lower right')
# ax.set_yticklabels([])
# # for i, row in enumerate(_df.iloc[::-1].values):
# #     ax.text(row[0]+3, i, '+'+str(row[0])+'%', fontsize=8)
# st.pyplot(plt.gcf())
    
    
    
df_agg['ratio'] = df_agg['inliers_count'] / df_agg['processing_time'] * 1000
_df = df_agg.pivot_table(index='Matcher', values='ratio', aggfunc='median')
ax = _df.iloc[::-1].plot.barh(width=0.8) 
ax.set_xlabel("Mean matches per second")    
ax.set_ylabel("")
for i, value in enumerate(_df.iloc[::-1].values):
    ax.text(value[0], i-0.3, str(round(value[0])), fontsize=10)

plt.legend().set_visible(False)  
st.pyplot(plt.gcf())

    
    
    
    
plt.figure(figsize=(20,6))
sns.scatterplot(data=df_agg, x='processing_time',y='inliers_count',size='count', hue=df_agg['Matcher'])
legend = plt.legend(ncol=5, loc='upper left')
legend.set_title('')
x = df_agg['processing_time']
y = df_agg['inliers_count']
plt.annotate("Jane", (x[5], y[5]), (2,5), 'data', \
                arrowprops=dict(arrowstyle="-|>", \
                connectionstyle="angle3", lw=1), \
                size=16, ha="center")

st.pyplot(plt.gcf())

st.header('The processing time density distribution for each algorithm grouped by map provider')
df['Matcher'] = df['Matcher'].str.replace('+','+\n')
plt.figure(figsize=(25,6))
sns.violinplot(data=df, x="Matcher", y="processing_time", hue="provider", cut=0, density_norm="width")
plt.yscale('log')
st.pyplot(plt.gcf())

st.header('The processing time density distribution for each algorithm grouped by map provider')
plt.figure(figsize=(25,6))
sns.scatterplot(data=df, x='Matcher',y='inliers_count', hue=df['provider'])
st.pyplot(plt.gcf())



plt.figure(figsize=(25,6))
sns.violinplot(data=df, x="Matcher", y="inliers_count", cut=0, density_norm="width")
st.pyplot(plt.gcf())

plt.figure(figsize=(25,16))
sns.violinplot(data=df_agg, x="Matcher", y="inliers_count", density_norm="width")
st.pyplot(plt.gcf())

st.header('violinplot - inliers_count vs provider') 
plt.figure(figsize=(20,8))
sns.violinplot(data=df, x="provider", y="inliers_count", cut=0, density_norm="width")
st.pyplot(plt.gcf())

st.header('violinplot - inliers_count vs provider with aggregation by provider') 
plt.figure(figsize=(20,10))
sns.violinplot(data=df_agg, x="provider", y="inliers_rot_count", cut=0, inner=None, label='inliers_rot_count')
sns.violinplot(data=df_agg, x="provider", y="inliers_count", cut=0, inner=None, label='inliers_count') # TODO: zmienić na hue
plt.xlabel("provider", fontsize=16)
plt.ylabel("inliers count", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.ylim(0, 780)
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend([handles[0], handles[-1]], [labels[0], labels[-1]], fontsize=16)
st.pyplot(plt.gcf())

plt.figure(figsize=(20,18))
sns.violinplot(data=df_agg, x="inliers_count", y="Matcher", density_norm="width")
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.kdeplot(data=df, x='inliers_count',hue='Matcher')
plt.xlim(0,10)
st.pyplot(plt.gcf())

plt.figure(figsize=(20,8))
sns.kdeplot(data=df, x='processing_time',hue='Matcher')
plt.xlim(0,1500)
st.pyplot(plt.gcf())

plt.figure(figsize=(10,6))
sns.kdeplot(data=df, x='inliers_count',hue='provider')
plt.xlim(0,200)
st.pyplot(plt.gcf())

plt.figure(figsize=(10,6))
sns.kdeplot(data=df, x='processing_time',hue='provider')
plt.xlim(0,1500)
st.pyplot(plt.gcf())

##############

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

