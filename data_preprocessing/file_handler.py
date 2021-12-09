__author__ = 'Naveen'

import pandas as pd
import pyproj
import configparser


config = configparser.ConfigParser()
config.read('properties.ini')


# Input data pre-processing
# Function to convert all string columns to lowercase values
def mask_data(dframe, count, parsed_data=pd.DataFrame()):
    mask = dframe.apply(lambda col: col.str.contains(',').any(),
                        axis=0)
    # Select columns which contains a sub-string Comma
    sub_df = dframe.loc[:, mask]
    if not sub_df.empty:
        split_df = pd.DataFrame(
            [x.rsplit(',', 1) for x in sub_df[sub_df.columns.values[0]].tolist()],
            columns=['columns' + str(count + 1), 'columns' + str(count)])
        # Adding the last column of iteration into a new dataframe as this is the necessary data
        parsed_data['columns' + str(count)] = split_df['columns' + str(count)]
        count += 1
        mask_data(split_df, count)
    parsed_data.dropna(how='all', axis=1, inplace=True)
    return parsed_data


# Reference dataset pre-processing
# Function to convert all string columns to lowercase values
def to_lower(dataframe):
    lower_case_df = dataframe.applymap(lambda s: s.lower() if type(s) == str else s)
    return lower_case_df


# Conversion between co-ordinate systems
def co_ord_conv(code):
    co_ordinate_systems = {
        'ITM': 'epsg:2157',
        'WGS84': 'epsg:4326'
    }
    projection = pyproj.Proj(init=co_ordinate_systems[code])
    return projection
