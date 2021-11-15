import pandas as pd
import math
# cải thiện data
owid_covid_data = pd.read_csv('owid_covid_data.csv')


# constanst
# based on Global Data on National Paliarments
Australia_and_New_Zealand_list = ['Australia','New Zealand']

Caribbean_list = ['Anguilla','Antigua and Barbuda','Aruba','Bahamas','Barbados','Bermuda','Bonaire Sint Eustatius and Saba',
                 'British Virgin Islands','Cayman Islands','Cuba','Curacao','Dominica','Dominican Republic','Grenada','Haiti',
                 'Jamaica','Montserrat','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines',
                 'Sint Maarten (Dutch part)','Trinidad and Tobago','Turks and Caicos Islands']

Central_Africa_list = ['Burundi','Cameroon','Central African Republic','Chad','Congo','Democratic Republic of Congo',
                      'Equatorial Guinea','Gabon','Rwanda','Sao Tome and Principe']

Central_America_list = ['Belize','Costa Rica','El Salvador','Guatemala','Honduras','Nicaragua','Panama']

Central_and_Eastern_Europe_list = ['Albania','Armenia','Azerbaijan','Belarus','Bosnia and Herzegovina','Bulgaria','Croatia',
                                  'Czechia','Estonia','Georgia','Hungary','Kosovo','Latvia','Lithuania','Moldova','Montenegro',
                                  'North Macedonia','Poland','Romania','Russia','Serbia','Slovakia','Slovenia','Ukraine']

Central_Asia_list = ['Kazakhstan','Kyrgyzstan','Tajikistan','Turkmenistan','Uzbekistan']

East_Africa_list = ['Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Somalia','South Sudan','Sudan','Tanzania','Uganda']

East_Asia_list = ['China','Hong Kong','Japan','Macao','Mongolia','South Korea','Taiwan']

Middle_East_list = ['Bahrain','Egypt','Iraq','Israel','Jordan','Kuwait','Lebanon','Oman','Palestine','Qatar','Saudi Arabia',
                   'Syria','United Arab Emirates','Yemen']

North_Africa_list = ['Algeria','Libya','Mauritania','Morocco','Tunisia']

Nordic_countries_list = ['Denmark','Faeroe Islands','Finland','Greenland','Iceland','Norway','Sweden']

North_America_list = ['Canada','Mexico','United States']

Pacific_Islands_list = ['Cook Islands','Fiji','French Polynesia','Kiribati','Marshall Islands','Micronesia (country)','Nauru',
                       'New Caledonia','Niue','Palau','Papua New Guinea','Pitcairn','Samoa','Solomon Islands','Tokelau',
                       'Tonga','Tuvalu','Vanuatu','Wallis and Futuna']

South_America_list = ['Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Falkland Islands','Guyana','Paraguay','Peru',
                     'Suriname','Uruguay','Venezuela']

South_Asia_list = ['Afghanistan','Bangladesh','Bhutan','India','Iran','Maldives','Nepal','Pakistan','Sri Lanka']

South_East_Asia_list = ['Brunei','Cambodia','Indonesia','Laos','Malaysia','Myanmar','Philippines','Singapore','Thailand',
                       'Timor','Vietnam']

Southern_Africa_list = ['Angola','Botswana','Eswatini','Lesotho','Madagascar','Malawi','Mauritius','Mozambique','Namibia',
                       'Seychelles','South Africa','Zambia','Zimbabwe']

Southern_Europe_list = ['Cyprus','Gibraltar','Greece','Italy','Malta','Northern Cyprus','Portugal','San Marino','Spain',
                       'Turkey','Vatican']

West_Africa_list = ['Benin','Burkina Faso','Cape Verde',"Cote d'Ivoire",'Gambia','Ghana','Guinea','Guinea-Bissau','Liberia',
                   'Mali','Niger','Nigeria','Saint Helena','Senegal','Sierra Leone','Togo']

Western_Europe_list = ['Andorra','Austria','Belgium','France','Germany','Guernsey','Ireland','Isle of Man','Jersey',
                      'Liechtenstein','Luxembourg','Monaco','Netherlands','Switzerland','United Kingdom']

def check_region(x):
    if x in Australia_and_New_Zealand_list:
        return 'Australia and New Zealand'
    elif x in Caribbean_list:
        return 'Caribbean'
    elif x in Central_Africa_list :
        return 'Central Africa'
    elif x in Central_America_list :
        return 'Central America'
    elif x in Central_and_Eastern_Europe_list :
        return 'Central and Eastern Europe'
    elif x in Central_Asia_list :
        return 'Central Asia'
    elif x in East_Africa_list :
        return 'East Africa'
    elif x in East_Asia_list :
        return 'East Asia'
    elif x in Middle_East_list :
        return 'Middle East'
    elif x in North_Africa_list :
        return 'North Africa'
    elif x in Nordic_countries_list :
        return 'Nordic countries'
    elif x in North_America_list :
        return 'North America'
    elif x in Pacific_Islands_list :
        return 'Pacific Islands'
    elif x in South_America_list :
        return 'South America'
    elif x in South_Asia_list :
        return 'South Asia'
    elif x in South_East_Asia_list :
        return 'South East Asia'
    elif x in Southern_Africa_list :
        return 'Southern Africa'
    elif x in Southern_Europe_list :
        return 'Southern Europe'
    elif x in West_Africa_list :
        return 'West Africa'
    else : 
        return 'Western Europe'

def AddRegion(df):
   df['region'] = df['location'].apply(lambda x : check_region(x))
   
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

# add regions for alnylis in region
AddRegion(owid_covid_data)
# expand date  for smoth serice chart
owid_covid_data = AddFullTimeSr(owid_covid_data)
# mở rộng dữ liệu cho nhưng ngày không ghi chép
# owid_covid_data =  AddFullTimeSr(owid_covid_data)
# thêm dữ liệu cho các cột trống theo chieuf tăng dần
FillAccesdingDat(owid_covid_data,['total_vaccinations_per_hundred'])
#lưu lại
owid_covid_data.to_csv(path_or_buf='owid_covid_data_reduce.csv',index=False)


