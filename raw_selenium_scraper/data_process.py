import pandas as pd
import numpy as np
import re

df_main = pd.read_csv("vw_golf_01_07_main_page.csv")
df_single = pd.read_csv("vw_golf_01_07_seperate_page.csv")

raw_df = pd.merge(df_main, df_single, left_on="Dotted link_link", right_on="url")


sub_df = raw_df[['Dotted link', 
                 'Rightarrows descriptions',
                 'Buynowtext link',
                 'Flagrightcol image_alt',
                 'Listingprice link',
                 'description',
                 'page views_alt',
                 'listed time',
                 'Priceandbidcount link']]
sub_df

temp = sub_df.loc[:, 'Rightarrows descriptions'].apply(lambda x: x.split(','))
kms = []
car_types = []
engines = []
drive_types = []
locations = []
for d_list in temp:
    mile = d_list[0]+d_list[1]
    car_type = d_list[2]
    engine = re.sub(r'\D', "", d_list[3])
    if len(d_list) < 5:
        drive_type = ''
        location = ''
    else:
        drive_type = d_list[4].split(';')[0]
        location = d_list[4].split(';')[1]
    
    kms.append(re.sub(r'\D', "",mile))
    car_types.append(car_type)
    engines.append(engine)
    drive_types.append(drive_type)
    locations.append(location)

    
sub_df.loc[:,'kms'] = kms
sub_df.loc[:,'car_types'] = car_types
sub_df.loc[:,'engines'] = engines
sub_df.loc[:,'drive_types'] = drive_types
sub_df.loc[:,'locations'] = locations
sub_df.head()


sub_df.loc[:,'price'] = sub_df.loc[:,'Listingprice link'].apply(lambda x: re.sub(r'\D', "", x) if type(x)==type('str') else x)
sub_df.loc[:,'year'] = sub_df.loc[:,'Dotted link'].apply(lambda x: re.search(r'\d{4}$', x).group())
sub_df.loc[:,'model'] = sub_df.loc[:,'Dotted link'].apply(lambda x: re.search(r'gl|gli|frm|tsi|fsi|gti|tdi|gt|r', x, re.I).group().lower() if re.search(r'gl|gli|frm|tsi|fsi|gti|tdi|gt|r', x, re.I) else 'golf')
sub_df.loc[:, 'price_buynow'] = sub_df.loc[:, 'Buynowtext link'].apply(lambda x: re.sub(r'\D', "", x) if type(x)==type('str') else x)
sub_df.loc[:, 'price_bid'] = sub_df.loc[:, 'Priceandbidcount link'].apply(lambda x: re.sub(r'\D', "", x) if type(x)==type('str') else x)
sub_df.loc[:,'view_count'] = sub_df['page views_alt'].apply(lambda x: int(re.sub(r'\D', "",x)) if type(x)==type('str') else x)
sub_df.price = sub_df.price.astype(float).fillna(0.0)
sub_df.price_buynow = sub_df.price_buynow.astype(float).fillna(0.0)
sub_df.loc[sub_df.price == 0, "price"] = sub_df.price_buynow
sub_df = sub_df.loc[sub_df.price != 0, :]

sub_df.head()


sub_df.model.unique()


cleaned_data = sub_df[['kms',
                 'engines',
                 'drive_types',
                 'price',
                 'year',
                 'model',
                 'description',
                 'view_count',
                 'listed time']]
cleaned_data.head()

cleaned_data.loc[cleaned_data.model == 'golf', :].sort_values(['year', 'kms'], ascending=[0, 1])