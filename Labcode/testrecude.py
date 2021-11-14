import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
# cải thiện data
owid_covid_data = pd.read_csv('owid_covid_data .csv')

def AddFullTimeSr(df):
   #drop nan
   df = df[df['continent'].notna()]
   df = df[df['iso_code'].notna()]

   timesr = pd.to_datetime(df['date'].unique()).sort_values()
   df['date'] = pd.to_datetime(df['date'])
   #create new df have same columns with old
   newdf = pd.DataFrame(columns=df.columns)
   newdf.drop(columns=['date'],inplace=True)
   #location 
   locations = df['location'].unique()

   for loc in locations:   
      loc_df = df[df['location'] == loc]

      new_loc_df = pd.DataFrame(columns=loc_df.columns)
      #phải cố data trước
      new_loc_df['date'] = pd.Series(timesr)

      new_loc_df['iso_code'] = str(loc_df['iso_code'].unique()[0])
      new_loc_df['continent'] = str(loc_df['continent'].unique()[0])
      new_loc_df['location'] = loc
      #set date as index
      loc_df.set_index('date',inplace=True)
      new_loc_df.set_index('date',inplace=True)
      for id in new_loc_df.index:    
          try:
             row = loc_df.loc[id]
             new_loc_df.loc[id] = row
          except:
            continue 
      newdf = pd.concat([newdf,new_loc_df],axis=0)    
   newdf = newdf.reset_index().rename(columns={'index': 'date'})
   newdf['date'] = newdf['date'].dt.strftime('%Y-%m-%d')
   return newdf   

def FillAccesdingDat(df, cols):
  locations = df['location'].unique()
  for col in cols: 
    colArr = []  
    for loc in locations:
        df_loc = df[df['location'] == loc]
        deVAL = 0.0
        for index,val in df_loc[col].items():
          if (math.isnan(val)): val = deVAL
          else: deVAL = val
          colArr.append(val)
    df[col] = pd.Series(colArr)  
    
# mở rộng dữ liệu cho nhưng ngày không ghi chép
expandate_dat =  AddFullTimeSr(owid_covid_data)
# thêm dữ liệu cho các cột trống theo chieuf tăng dần
FillAccesdingDat(expandate_dat,['total_vaccinations_per_hundred'])

#lưu lại
expandate_dat.to_csv(path_or_buf='owid_covid_data_reduce_gregion_clone.csv',index=False)


