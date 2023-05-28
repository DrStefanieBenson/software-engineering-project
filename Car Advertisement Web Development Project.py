#!/usr/bin/env python
# coding: utf-8

# # US Car Advertisement Dataset
# # Exploratory Data Analysis
# 
# ## Introduction
# 
# The dataset analyzed in this project involves car sales data related to make, model, and year of a car as well as other defining characteristics typically included in a car sale ad.  This exploratory data analysis will work to determine the features of the data, identify issues and remedy those issues, as well as display various visual representations of the dataset.  Also, initial observations and meaningful takeaways will be provided at the end based on this analysis.

# ## Load the Packages

# In[1]:


get_ipython().system('pip install streamlit')


# In[2]:


get_ipython().system('pip install plotly-express')


# ## Load the Data

# In[3]:


import pandas as pd
import numpy as np 
from math import factorial
import streamlit as st
import plotly_express as px

from matplotlib import pyplot as plt
import seaborn as sns


# ## Initial Data Analysis

# In[4]:


df_car_ads = pd.read_csv('vehicles_us.csv')


# In[5]:


display(df_car_ads)
print()
df_car_ads.info()
print()
df_car_ads.describe()


# #### Summary
# 
# Initial data observations demonstrate that ads typically include make, model, year, condition, number of cylinders in the engine, type of fuel, measure of the odometer, the transmission type, car body type, color, is 2-wheel drive (2WD) or 4-wheel drive (4WD), and the number of the days spent on the market.
# 
# There are several areas that will need to be addressed when the data is fixed, which includes addressing missing values in the odometer column and the is_4wd column, and adjusting the date posted to datetime. 

# ## Fix the Data

# ### Duplicates

# In[6]:


df_car_ads.duplicated().sum()


# ### Missingness

# In[7]:


df_car_ads.isna().sum()


# #### Addressing Missingness in 'Odomenter" column

# In[8]:


avg_odometer= df_car_ads ['odometer'].mean()


# In[9]:


avg_odometer_rounded= round(avg_odometer,2)

display(avg_odometer_rounded)


# In[10]:


df_car_ads['odometer'] = df_car_ads['odometer'].fillna(avg_odometer_rounded)

df_car_ads.sample(10)


# #### Converting the "date_posted" column to datetime format

# In[11]:


df_car_ads['date_posted'] = pd.to_datetime(df_car_ads['date_posted'], format ='%Y-%m-%d')


# #### Separate the make and model into two separate columns

# In[12]:


df_car_ads['make']= df_car_ads.model.str.split().str.get(0)


# In[13]:


df_car_ads['model_ind']= df_car_ads.model.str.split().str.get(1)
#model_ind is a new column name which only identifies the model of the car independent (ind) of the make

display(df_car_ads.head(10))


# #### Address Missingness in "Cylinders" column
# 
# * use ffill() to fill in NaN values for the 'cylinders' column using like information in the 'model' column.  For example, row 9 shown above for the Honda Pilot has NaN for cylinders, but the same model listed in row 7 has cylinders listed as 6.0.  Using ffill() takes the value from row 7 and inputs it in row 9 to replace the missingness.
# <br><br>
# * The new table shown below indicates this change, and rerunning info() shows that there are no more missing values in cylinders.

# In[14]:


df_car_ads['cylinders'] = df_car_ads.groupby('model')['cylinders'].ffill()

display(df_car_ads.head(10))

df_car_ads.info()


# #### Addressing Missingness in "is_4wd" column

# In[15]:


df_car_ads['is_4wd'] = df_car_ads.groupby('model')['is_4wd'].ffill()

display(df_car_ads.head(10))

df_car_ads.info()


# * When trying to apply the same ffill() method to the 'is_4wd' column, values were not input for any of the missing values, which indicates that there are no models with missing 'is_4wd' data which can pull from a fully completed row of the same model car.  For example, as shown below, there are 4,491 cars with NaN values in the 'is_4wd' column.  When looking at a random model, I see when querying for Toyota Prius, there are 482 entries.  When I conduct a mulitple condition query for those cars that are Toyota Prius and do not have a 1 in the 'is_4wd' column, I return all 482 entries.
# <br><br>
# * It would be feasible to assume that all cars with a NaN value in this column would actually be a 0, indicating that they are not 4wd cars.  So I will replace those NaN values with 0's.

# In[16]:


df_car_ads.query("is_4wd != 1")[['model', 'is_4wd']]


# In[17]:


df_car_ads.query("model == 'toyota prius'")[['model','is_4wd']]


# In[18]:


df_car_ads.query("model == 'toyota prius' and is_4wd != 1")[['model','is_4wd']]


# In[19]:


df_car_ads['is_4wd'] = df_car_ads['is_4wd'].fillna(0)

df_car_ads.sample(10)
print()
df_car_ads.info()


# * After replacing NaN with 0 for the cars in the "is_4wd" column, there are now no missing values in that column
# <br><br>
# * There is no reasonable method to fill in missing values for the model_year or the paint_color, so those values will remain missing.

# ## Data Visualization

# ### <i>Let's revisit the dataset</i>

# In[20]:


display(df_car_ads.head(10))
print()
df_car_ads.describe()


# In[66]:


fig = px.scatter(df_car_ads, x="days_listed", y="price", color="condition",
                 size='days_listed', hover_data=['make','type'], color_discrete_sequence=px.colors.qualitative.Light24,
                 width = 1000, height = 1000, title='The Number of Days Ad is Listed Per Price and Condition of Vehicle')

fig.show()


# ### Ads by Manufacturer

# In[22]:


ads_by_make= pd.DataFrame(df_car_ads.groupby('make')['model'].count())

ads_by_make.reset_index(inplace=True)

ads_by_make.columns = ['make', 'number of ads']

print(ads_by_make)


# In[65]:


sns.barplot(x = 'make', y = 'number of ads', data = ads_by_make, palette='pastel')

plt.xticks(rotation=90)
plt.title('Number of Adverstisements Per Car Manufacturer')
 
plt.show()


# In[35]:


fig = px.pie(ads_by_make,
             values='number of ads',
             names='make',
             title='Number of Ads Per Car Manufacturer',
             color='make',
             color_discrete_sequence=px.colors.qualitative.Light24)

fig.show()


# ### Ads by Manufacturer and Model

# In[36]:


ads_by_make_model= pd.DataFrame(df_car_ads.groupby(['make', 'model_ind'])['model'].count())

ads_by_make_model.reset_index(inplace=True)

print(ads_by_make_model)


# In[63]:


fig = px.sunburst(ads_by_make_model,
                  path=['make', 'model_ind'],
                  values='model',
                  color='model',
                  color_continuous_scale=px.colors.sequential.Plasma_r,
                 title='Make and Model of Car Sales')
fig.show()


# ### Ads by Type of Vehicle

# In[38]:


ads_by_type= pd.DataFrame(df_car_ads.groupby('type')['make'].count())

ads_by_type.reset_index(inplace=True)

ads_by_type.columns = ['type', 'number_of_ads']

print(ads_by_type)


# In[62]:


fig = px.bar(ads_by_type,
             x = 'type',
             y = 'number_of_ads',
             color='type',
             color_discrete_sequence=px.colors.qualitative.Light24,
            title='Number of Ads Per Vehicle Type')
fig.show()


# ### Average Price Per Manufacturer

# In[68]:


avg_price_per_make= pd.DataFrame(df_car_ads.groupby('make')['price'].mean())

avg_price_per_make.reset_index(inplace=True)

print(avg_price_per_make)


# In[41]:


num_ads_and_price_per_make= pd.DataFrame(avg_price_per_make.merge(ads_by_make,
                                                    on= 'make',
                                                    how= 'left'))

display(num_ads_and_price_per_make)


# In[61]:


fig = px.scatter(num_ads_and_price_per_make, x="price", y="number of ads",
                 size="number of ads", color="number of ads",
                 hover_name="make", log_x=True, size_max=60,
                 color_continuous_scale=px.colors.sequential.Plasma_r,
                title=' Price and Number of Ads Per Manufacturer')
fig.show()


# ### Averge Price Per Model Year

# In[43]:


avg_price_per_year= pd.DataFrame(df_car_ads.groupby('model_year')['price'].mean())

avg_price_per_year.reset_index(inplace=True)

print(avg_price_per_year)


# In[67]:


fig = px.line(avg_price_per_year, x="model_year", y="price", title='Average Price Per Model Year of Vehicle')

fig.show()


# ### Average Price Per Type of Car

# In[44]:


avg_price_per_type= pd.DataFrame(df_car_ads.groupby('type')['price'].mean())

avg_price_per_type.reset_index(inplace=True)

print(avg_price_per_type)


# In[45]:


num_ads_and_price_per_type= pd.DataFrame(avg_price_per_type.merge(ads_by_type,
                                                    on= 'type',
                                                    how= 'left'))

display(num_ads_and_price_per_type)


# In[60]:


fig = px.scatter(num_ads_and_price_per_type, x="price", y="number_of_ads",
                 size="number_of_ads", color="number_of_ads",
                 hover_name="type", log_x=True, size_max=60,
                 color_continuous_scale=px.colors.sequential.Plasma_r,
                title= 'Number of Ads and Price of Sale Per Vehicle Type')
fig.show()


# ### Price Per Condition of Car

# In[47]:


avg_price_per_condition= pd.DataFrame(df_car_ads.groupby('condition')['price'].mean())

avg_price_per_condition.reset_index(inplace=True)

print(avg_price_per_condition)


# In[48]:


num_ads_per_condition= pd.DataFrame(df_car_ads.groupby('condition')['type'].count())

num_ads_per_condition.reset_index(inplace=True)

num_ads_per_condition.columns = ['condition', 'number_of_ads']

print(num_ads_per_condition)


# In[49]:


num_ads_and_price_per_condition= pd.DataFrame(avg_price_per_condition.merge(num_ads_per_condition,
                                                    on= 'condition',
                                                    how= 'left'))

display(num_ads_and_price_per_condition)


# ### Number of Days Listed Per Manufactuer

# In[50]:


avg_days_per_make= pd.DataFrame(df_car_ads.groupby('make')['days_listed'].mean())

avg_days_per_make.reset_index(inplace=True)

print(avg_days_per_make)


# ### Number of Days Listed Per Year of Car

# In[51]:


avg_days_per_year= pd.DataFrame(df_car_ads.groupby('model_year')['days_listed'].mean())

avg_days_per_year.reset_index(inplace=True)

print(avg_days_per_year)


# ### Number of Days Listed Per Type of Car

# In[52]:


avg_days_per_type= pd.DataFrame(df_car_ads.groupby('type')['days_listed'].mean())

avg_days_per_type.reset_index(inplace=True)

print(avg_days_per_type)


# ### Number of days per Condition of Car

# In[53]:


avg_days_per_condition= pd.DataFrame(df_car_ads.groupby('condition')['days_listed'].mean())

avg_days_per_condition.reset_index(inplace=True)

print(avg_days_per_condition)


# ### Automatic vs Manual & Sale Price

# In[54]:


price_per_transmission= df_car_ads.groupby('transmission')['price'].mean()

print(price_per_transmission)


# ### Automatic vs Manual & Days Listed

# In[55]:


price_per_transmission_duration= df_car_ads.groupby('transmission')['days_listed'].mean()

print(price_per_transmission_duration)


# ### 4wd vs 2wd & sale price

# In[56]:


price_per_drive= df_car_ads.groupby('is_4wd')['price'].mean()

print(price_per_drive)


# ### 4wd vs 2wd & days listed

# In[57]:


price_per_drive_duration= df_car_ads.groupby('is_4wd')['days_listed'].mean()

print(price_per_drive_duration)


# ### Color & Sale Price

# In[58]:


price_per_color= df_car_ads.groupby('paint_color')['price'].mean()

print(price_per_color)


# ### Color & Days Listed

# In[59]:


days_per_color= df_car_ads.groupby('paint_color')['days_listed'].mean()

print(days_per_color)


# ### Price vs Days Listed

# In[70]:


days_per_price= pd.DataFrame(df_car_ads.groupby('price')['days_listed'].mean())

days_per_price.reset_index(inplace=True)

print(days_per_price)


# In[73]:


fig = px.line(days_per_price, x="price", y="days_listed", title='Average Price Per Days Advertisement is Listed')

fig.show()


# # Conclusions
# 
# This exploratory data analysis served to determine various advertisement trends with a car sale dataset.  The analysis looked at various characteristics typical with automotives to determine trends related to length of sale, price of vehicle, condition of vehicle, and buyer preferences with transmission, color, make, and vehicle type.  The following inferences about these patterns include:
# <br><br>
# ### Entire Dataset
# 1. There are several outliers in the price column over 100k which impact the data.  However, the vast majority of vehicle advertisements are under approximately 75k with the average price for all sales being 12k.
# 2. Although the highest number of days an ad was listed for was 271, the average number of days is 39.5
# <br><br>
# ### Manufacturers
# 3. The most frequently advertised manufacterers are Ford and Chevrolet with 12,672 and 10,611 advertisements, respectively.  Furthermore, the F-150 and Silverado, were the two most popular types of vehicles within those brands.
# 4. The least advertised manufacterers are Mercedes-Benz and Acura with 41 and 236 ads, respectively
# 5. Mercedes-Benz had the highest average sale price of 34.9k even though they had the lowest number of advertisements
# 6. Price per vehicle, when outliers like classic cars or cars with significant after-market upgrades, typically increases the younger the model year.
# <br><br>
# ### Customer Preferences
# 7. The average sale price for all the ads was 39.5k.  When looking at characteristics like color, transmission type, condition of vehicle, model year, type, and drive train, there is no significant difference in how long an ad is listed.  This means that customers are not purchasing cars based on these characteristics.
# 8. Price is not necessarily a deterent for purchasers as there does not appear to be a relationship between the number of days the ad is posted and the price of the car.
# <br><br>
# ### Advertisement Trends
# 9. The most common types of ads are for SUV's, Sedans, and Trucks.  Trucks have the highest average price, followed by SUV's and then Sedans.
# 10. Even though SUV's, Sedans, and Trucks make up the bulk of the ads, there is no significant difference in how quickly they sell.  It is only an indicator of the most common types of cars
# 11. Resale price is more aligned with market norms based on the money factor of the manufacturer.
