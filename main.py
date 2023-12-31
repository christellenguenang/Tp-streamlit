# importation des librairies nécessaires
from datetime import datetime
import streamlit as st
from fastapi import FastAPI
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from flask import Flask, jsonify
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import requests
import uvicorn
import numpy as np
#app = FastAPI()



st.title("Bienvenue sur mon application!")
st.markdown(" ## I. Les Dashboards")

# Importation des bases achats, clics, et impressions
achats = pd.read_csv("achats.csv")
clics = pd.read_csv("clics.csv")
impressions = pd.read_csv("impressions.csv")

# On fusionne les 3 bases
fusion_1 = pd.merge(clics, impressions, on="cookie_id")
fusion = pd.merge(fusion_1, achats, on="cookie_id")

    
    
# Changement du type des variables de temps

fusion['timestamp_x'] = pd.to_datetime(fusion['timestamp_x'], unit='s')
fusion['date_impressions'] = fusion['timestamp_x'].dt.strftime('01-01-1970 %H:%M:%S')
fusion['timestamp_y'] = pd.to_datetime(fusion['timestamp_y'], unit='s')
fusion['date_clics'] = fusion['timestamp_y'].dt.strftime('01-01-1970 %H:%M:%S')
fusion['timestamp'] = pd.to_datetime(fusion['timestamp'], unit='s')
fusion['date_achats'] = fusion['timestamp'].dt.strftime('01-01-1970 %H:%M:%S')

# Création des filtres

with st.sidebar:
    st.write("Les filtres")
    age = st.slider('Age:', min_value=19.0, max_value=69.0, value=(19.0, 69.0))
    campaign = st.multiselect('campaign_id:', options=np.unique(fusion['campaign_id']))
    
# Liaison des filtres et des tableaux

filtre = fusion[(fusion['campaign_id'].isin(campaign)) | fusion['age'].between(*age)]

col1, col2 = st.columns(2)

# Le chiffre d'affaire
with col1:
    chiffre_d_affaires = filtre["price"].sum()
    st.markdown(" ## Chiffre d'affaires")
    st.write(f"<span style='color:#c290b4; font-size:50px; text-align:center;'>{chiffre_d_affaires} € </span>", unsafe_allow_html=True)




# clics sur les bannières

col2.markdown(" ## clics sur les bannières")
fig, ax = plt.subplots(figsize = (100, 50))

plt.bar(filtre['date_clics'].astype(str), filtre['cookie_id'], color = 'blue')
plt.xlabel('heure de clics')
plt.ylabel('nombre de clics')
plt.title('Clics sur les bannières')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
date_format = mdates.DateFormatter('%d-%m')
ax.xaxis.set_major_formatter(date_format)

col2.pyplot(fig)


fig1, fig2 = st.columns(2)

# Age des clients en fonction des produits
fig1.markdown(" ### Age des clients en fonction des produits")

if not filtre.empty and 'age' in filtre.columns:
    # Create the boxplot
    fig, ax = plt.subplots()
    sns.boxplot(data=filtre, x="product_id", y="age", hue=None, order=None)
    fig1.pyplot(fig)
else:
    fig1.write("No data available for the selected filters.")

# Conversions
fig2.markdown(" ## Conversions")
fig = go.Figure(go.Funnel(
    y=['Affichages bannières', 'Clics', 'Souscriptions'],
    x=[filtre['timestamp_x'].count(), filtre['timestamp_y'].count() ,filtre['timestamp'].count()],
    textinfo="value",
     textfont_size=20,
     marker={'color' : "#c290b4"}))


fig.update_layout(
                  funnelmode="stack",
                  showlegend=False)

fig2.plotly_chart(fig)




