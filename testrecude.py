import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
# cải thiện data
owid_covid_data = pd.read_csv('owid-covid-data.csv')
# becasue data not contimeus so well need to full it

# locations = owid_covid_data['location'].unique()

# colArr = []

# for loc in locations:
#     df_loc = owid_covid_data[owid_covid_data['location'] == loc]
#     deVAL = 0.0
#     for val in df_loc['total_vaccinations_per_hundred'].values:
#         if (math.isnan(val)): val = deVAL
#         else: deVAL = val
#         colArr.append(val)

def FillAccesdingDat(df, cols):
  locations = df['location'].unique()
  for col in cols: 
    colArr = []  
    for loc in locations:
        df_loc = owid_covid_data[owid_covid_data['location'] == loc]
        deVAL = 0.0
        for val in df_loc[col].values:
          if (math.isnan(val)): val = deVAL
          else: deVAL = val
          colArr.append(val)
    df[col] = pd.Series(colArr)  

FillAccesdingDat(owid_covid_data,['total_vaccinations_per_hundred'])

print(owid_covid_data['total_vaccinations_per_hundred'])

owid_covid_data.to_csv(path_or_buf='owid-covid-data-reduce.csv',index=False)
