import streamlit as st
import pandas as pd
import numpy as np
import time
#import matplotlib.pyplot as plt
import plotly.express as px
from plotly.offline import iplot
import plotly.graph_objs as go
import requests
from pandas.io.json import json_normalize
#from streamlit.script_runner import StopException, RerunException

st.image('amb.jpeg')
fig = go.Figure()
st.write("""
# COVID19 FOLLOWING APP 
[Coronavirus COVID19 API](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest#81447902-b68a-4e79-9df9-1b371905e9fa) here you will find the data for this app.
""")

st.write('COVID-19 is an infectious disease caused by a virus named SARS-CoV-2 and was discovered in December 2019 in Wuhan, China. It is very contagious and has quickly spread around the world.'+
         'COVID-19 most often causes respiratory symptoms that can feel much like a cold, a flu, or pneumonia. COVID-19 may attack more than your lungs and respiratory system. Other parts of your body may also be affected by the disease.Some people including those with minor or no symptoms may suffer from post-COVID conditions — or “long COVID.Older adults and people who have certain underlying medical conditions are at increased risk of severe illness from COVID-19.'+
         'There are some governments that are taking measures to prevent a sanitary collapse to be able to take care of all these people.'+
         'I\'m solving this issue here. Here you can notice how some countries/regions are working!')
st.write('When choosing some countries like Martinique,New Calidonia,Nuie,Heard and McDonalds Islands...you will notice that the app will display an error ,don\'t be surprise that is due to the fact that those countries don\'t have their informations in the dataset because we are using an online one')

url = 'https://api.covid19api.com/countries'
r = requests.get(url)
df0 = json_normalize(r.json())

top_row = pd.DataFrame({'Country':['Select a Country'],'Slug':['Empty'],'ISO2':['E']})
# Concat with old DataFrame and reset the Index.
df0 = pd.concat([top_row, df0]).reset_index(drop = True)
st.sidebar.image('cov19.jpg')
st.sidebar.header('Choose by type')
graph_type = st.sidebar.radio('Cases type',('confirmed','deaths','recovered'))
st.sidebar.subheader('Search by country ')
country = st.sidebar.selectbox('Country',df0.Country)
country1 = st.sidebar.selectbox('Compare with another Country',df0.Country)
if st.sidebar.button('Refresh Data'):
    #st.legacy_caching.clear_cache()
    st.experimental_rerun()
    raise RerunException(st.ScriptRequestQueue.RerunData(None))
  
if country != 'Select a Country':
    slug = df0.Slug[df0['Country']==country].to_string(index=False)[1:]
    url = 'https://api.covid19api.com/total/dayone/country/'+slug+'/status/'+graph_type
    r = requests.get(url)
    st.write("""# Total """+graph_type+""" cases in """+country+""" are:"""+str(r.json()[-1].get("Cases")))
    df = json_normalize(r.json())
    layout = go.Layout(
        title = country+'\'s '+graph_type+' cases Data',
        xaxis = dict(title = 'Date'),
        yaxis = dict(title = 'Number of cases'),)
    fig.update_layout(dict1 = layout, overwrite = True)
    fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country))

    
    if country1 != 'Select a Country':
        slug1 = df0.Slug[df0['Country']==country1].to_string(index=False)[1:]
        url = 'https://api.covid19api.com/total/dayone/country/'+slug1+'/status/'+graph_type
        r = requests.get(url)
        st.write("""# Total """+graph_type+""" cases in """+country1+""" are: """+str(r.json()[-1].get("Cases")))
        df = json_normalize(r.json())
        layout = go.Layout(
            title = country+' vs '+country1+' '+graph_type+' cases Data',
            xaxis = dict(title = 'Date'),
            yaxis = dict(title = 'Number of cases'),)
        fig.update_layout(dict1 = layout, overwrite = True)
        fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country1))
        
    st.plotly_chart(fig, use_container_width=True)
    
    
    
else:
    url = 'https://api.covid19api.com/world/total'
    r = requests.get(url)
    total = r.json()["TotalConfirmed"]
    deaths = r.json()["TotalDeaths"]
    recovered = r.json()["TotalRecovered"]
    st.write("""# Worldwide Data:""")
    st.write("Total cases: "+str(total)+", Total deaths: "+str(deaths)+", Total recovered: "+str(recovered))
    x = ["TotalCases", "TotalDeaths", "TotalRecovered"]
    y = [total, deaths, recovered]

    layout = go.Layout(
        title = 'World Data',
        xaxis = dict(title = 'Category'),
        yaxis = dict(title = 'Number of cases'),)
    
    fig.update_layout(dict1 = layout, overwrite = True)
    fig.add_trace(go.Bar(name = 'World Data', x = x, y = y))
    st.plotly_chart(fig, use_container_width=True)
    
st.sidebar.subheader("""Created by [Amadou Kindy Barry] (barrykind86@gmail.com) """)
#st.sidebar.image('logo.jpg', width = 300)


#from streamlit.script_runner import StopException, RerunException

#data1 = pd.read_csv("worldometer_coronavirus_daily_data.csv")
    
