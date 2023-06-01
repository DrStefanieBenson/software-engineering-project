!pip install streamlit
!pip install plotly-express

import streamlit as st
import pandas as pd
import plotly_express as px

df_car_ads = pd.read_csv('vehicles_us.csv')

st.header('The Number of Days Ad is Listed Per Price and Vehicle Condition')
fig = px.scatter(df_car_ads, x="days_listed", y="price", color="condition",
                 size='days_listed', hover_data=['make','type'], color_discrete_sequence=px.colors.qualitative.Light24,
                 width = 1000, height = 1000, title='The Number of Days Ad is Listed Per Price and Condition of Vehicle')
fig.show()


st.header('Number of Ads Per Car Manufacturer')
ads_by_make= pd.DataFrame(df_car_ads.groupby('make')['model'].count())
ads_by_make.reset_index(inplace=True)
ads_by_make.columns = ['make', 'number of ads']

st.header('Number of Ads Per Vehicle Type')
fig = px.bar(ads_by_type,
             x = 'type',
             y = 'number_of_ads',
             color='type',
             color_discrete_sequence=px.colors.qualitative.Light24,
            title='Number of Ads Per Vehicle Type')
fig.show()


