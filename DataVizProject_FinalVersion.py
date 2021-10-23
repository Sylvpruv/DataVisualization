##Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import folium
import plotly.express as px

##Nettoyage du dataset mapstr.geojson

df = pd.read_json('mapstr.geojson')
df2 = pd.DataFrame(list(df['features']))
df3 = pd.DataFrame(list(df2['geometry']))
df4 = pd.DataFrame(list(df2['properties']))
df5 = pd.concat([df3,df4], axis = 1)
df6 = df5.drop(columns = ["type", "tags"])
df6 = df6.fillna('Pas de commentaire')


#df6 = mapstr.goejson nettoyé

#Concatenation du dataset mapstr.geojson avec mapstr.csv
df7 = pd.read_csv('mapstr_.csv')
df8 = pd.concat([df6,df7.tags], axis = 1)

#division de la colonne tag en 3 colonnes: tag1, tag2, tag3
df9 = df8['tags'].str.split('#', expand=True)
df8 = df8.drop(columns =['tags'])
df10 = pd.concat([df8,df9], axis = 1)
df10 = df10.rename(columns = {0 :'tag1', 1: 'tag2', 2:'tag3'})
df10 = df10.fillna('-')

#séparation des coordonnées
coord = pd.DataFrame(list(df6['coordinates']))
coord = coord.rename(columns={1: 'latitude', 0: 'longitude'})
coord = coord[['latitude', 'longitude']]
df10 = df10.drop(columns =['coordinates'])

df11 = pd.concat([df10, coord], axis = 1)
df11 = df11.drop(columns=['icon'])

#ajout du nom des villes

villes = ['Paris','Marseille','Amsterdam','Joinville-le-Pont','Calais','Villejuif','Ris-Orangis','Perpignan']
city=[]
a = []

for i in df11['address']:
    for j in villes:
        if j in i:
            city.append(j)

city.append('Paris')
df11 =df11.assign(city=city) #df11 dataset final

##Introduction

st.title('Sylvain Pruvot - Data Visualization')

st.header("What is Mapstr?")
st.write('')

image = Image.open('mapstr.png')

st.image(image)

st.write("Mapstr is an app, a social network and a mapping service that allows you to save your favorite places and share them with your friends ")

st.write('')

st.write("I have been using this application since July 2022 so this data partly tells about my last vacation and the places that marked me the most")

st.write('')

st.subheader('My dataset')
st.write('')
df11
st.write('')

st.subheader('Interactive map')

#select box pour choisir les tags
select_tag1 = st.selectbox('Choose Tag1', sorted(df11.tag1.unique()))
df_temp1= df11[df11['tag1'] == select_tag1]

select_tag2 = st.selectbox('Choose Tag2 (optional)', sorted(df_temp1.tag2.unique()))
df_temp2= df_temp1[df_temp1['tag2'] == select_tag2]

select_tag3 = st.selectbox('Choose Tag3 (optional)', sorted(df_temp2.tag3.unique()))
df_temp3= df_temp2[df_temp2['tag3'] == select_tag3]

if (select_tag2 == '-' ) & (select_tag3 == '-'):
    df_temp_final= df_temp1

if (select_tag3 == '-') & (select_tag2 != '-' ):
    df_temp_final = df_temp2

if (select_tag2 != '-' ) & (select_tag3 == '-'):
    df_temp_final= df_temp2

if (select_tag2 != '-' ) & (select_tag3 != '-'):
    df_temp_final= df_temp3




st.write('Number of résults:') 
a = len(df_temp_final)
a

#Map plot
fig = px.scatter_mapbox(df_temp_final, lat="latitude", lon="longitude", hover_name="name", hover_data=["address", "userComment"],color_discrete_sequence=["red"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig

df_temp_final = df_temp_final.drop(columns=['tag1', 'tag2', 'tag3', 'latitude','longitude'])
df_temp_final

st.write('')

st.write('My addresses are concentrated in only 8 cities')

## Pie Chart Tag1 by Country

st.subheader('City by city statistics')
st.write('')


select_tag5 = st.selectbox('Choose a city', sorted(df11.city.unique()))
st.write('')

temp = df11[df11['city'] == select_tag5]

st.write('number of places in '+ select_tag5 + ' :')
st.write(len(temp))
st.write('')


temp1 = temp['tag1'].value_counts().rename_axis('city').reset_index(name='tag1')
temp2 = temp['tag1'].value_counts()

st.bar_chart(temp2)

fig2 = px.pie(temp1, values='tag1', names='city', color_discrete_sequence=px.colors.sequential.RdBu,title='type of place in ' + select_tag5)
fig2

st.write('')


##Information avancées sur les lieux

st.subheader('Advanced places information')

st.write('')

select_tag4 = st.selectbox('Choose tag', sorted(df11.tag1.unique()))
df_temp4 = df11[df11['tag1'] == select_tag4]
df12 = df_temp4['tag2'].value_counts()
df13 = df_temp4['tag3'].value_counts()
df14 = pd.concat([df12, df13], axis = 0)

if '-' in df14:
     df14 = df14.drop('-')


b = len(df_temp4)
st.write(('Number of ') + select_tag4 + ' :') 
b


st.bar_chart(df14)


#Retaurants insights

st.subheader('My restaurant:')

temp3 = df11[df11['tag1'] == 'Restaurant']
temp4 = temp3['tag2'].value_counts().rename_axis('restaurants').reset_index(name='tag2')
#temp4 = temp4.drop(temp4[(temp4['tag2']=='-')])

fig = px.pie(temp4, values = 'tag2', names='restaurants')
fig