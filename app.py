import streamlit as st
import pandas as pd
import plotly_express as px

df_car_ads = pd.read_csv('vehicles_us.csv')

#removing outliers-vintage, antique, and classic cars
df_car_ads_mod = pd.DataFrame(df_car_ads.loc[df_car_ads["model_year"] > 2000])

#removing outliers-price
df_car_ads_mod= pd.DataFrame(df_car_ads_mod.loc[df_car_ads_mod['price'] < 42498])

#missingness- cylinders
df_car_ads_mod['cylinders'] = df_car_ads_mod.groupby('model')['cylinders'].ffill()

#missingness- odometer
median_odometer= df_car_ads_mod.groupby('model_year')['odometer'].median()
df_car_ads_mod['odometer'] = df_car_ads_mod['odometer'].fillna(0)
df_car_ads_mod['odometer'] = [x[1]['odometer'] if x[1]['odometer']!= 0\
                              else median_odometer[x[1]['model_year']] for x in df_car_ads_mod.iterrows()  ]

#missingness- paint color
df_car_ads_mod['paint_color'] = df_car_ads_mod['paint_color'].fillna('unknown')

#mmissingness- 4wd vs 2wd
df_car_ads_mod['is_4wd'] = df_car_ads_mod['is_4wd'].fillna(0)

#datetime conversion
df_car_ads_mod['date_posted'] = pd.to_datetime(df_car_ads_mod['date_posted'], format ='%Y-%m-%d')

#adding columns for make & model
df_car_ads_mod['make']= df_car_ads_mod.model.str.split().str.get(0)
df_car_ads_mod['model_ind']= df_car_ads_mod.model.str.split().str.get(1)


#Data Visualization

#Average Price Per Number of Days Ad is Listed 
avg_price_per_days_listed= pd.DataFrame(df_car_ads_mod.groupby('days_listed')['price'].mean())                                     
avg_price_per_days_listed.reset_index(inplace=True)
avg_price_per_days_listed.columns = ['days_listed', 'avg_price']

st.header('The Number of Days Ad is Listed Per Average Price of Vehicle')
fig = px.scatter(avg_price_per_days_listed, x="days_listed", y="avg_price", color="days_listed",
                 color_continuous_scale=px.colors.qualitative.Dark2,
                 width = 1000, height = 1000, title='The Number of Days Ad is Listed Per Average Price of Vehicle')
st.write(fig)


#Total Number of Ads Per Days Listed & Per Condition of Vehicle
condition_days_listed= pd.DataFrame(df_car_ads_mod.groupby(['days_listed','condition']).count())
condition_days_listed.reset_index(inplace=True)

st.header('The Number of Ads Per Days Listed & Per Condition')
fig = px.histogram(condition_days_listed, x="days_listed", title='The Number of Ads Per Days Listed & Per Condition',
                  nbins=20, color="condition", color_discrete_sequence=px.colors.qualitative.Prism)
st.write(fig
         
st.header('The Number of Ads Per Days Listed & Per Condition')
fig = px.scatter(condition_days_listed, x="days_listed", y="price", color="condition",
                 size='price', hover_data=['condition','days_listed'],
                color_discrete_sequence=px.colors.qualitative.Light24,
                 width = 1000, height = 1000, title='The Number of Ads Per Days Listed & Per Condition',
                labels={
                     "days_listed": "Number of Days Advertisement was Posted",
                     "price": "Number of Advertisements",
                     "condition": "Condition of the Vehicle"})
st.write(fig)


#Number of Ads Per Car Manufacturer
ads_by_make= pd.DataFrame(df_car_ads_mod.groupby('make')['model'].count())
ads_by_make.reset_index(inplace=True)
ads_by_make.columns = ['make', 'number of ads']

st.header('Number of Ads Per Car Manufacturer')
fig = px.pie(ads_by_make,
             values='number of ads',
             names='make',
             title='Number of Ads Per Car Manufacturer',
             color='make',
             color_discrete_sequence=px.colors.qualitative.Light24)

st.write(fig)


#Number of Ads Per Vehicle Type
ads_by_type= pd.DataFrame(df_car_ads_mod.groupby('type')['make'].count())
ads_by_type.reset_index(inplace=True)
ads_by_type.columns = ['type', 'number_of_ads']

st.header('Number of Ads Per Vehicle Type')
fig = px.bar(ads_by_type,
             x = 'type',
             y = 'number_of_ads',
             color='type',
             color_discrete_sequence=px.colors.qualitative.Light24,
            title='Number of Ads Per Vehicle Type')
st.write(fig)
