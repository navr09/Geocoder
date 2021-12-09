__author__ = 'Naveen'

import pandas as pd
from data_preprocessing import file_handler


def create_csv(reference_counties_path,reference_townlands_path,input_path):
    reference_counties_data = pd.DataFrame(pd.read_csv(reference_counties_path,
                                                       usecols=['County', 'ITM_E', 'ITM_N', 'English_Name']))
    reference_counties_data = file_handler.to_lower(reference_counties_data)
    reference_townlands_data = pd.DataFrame(pd.read_csv(reference_townlands_path,
                                                        usecols=['County', 'ITM_E', 'ITM_N', 'English_Name']))
    reference_townlands_data.rename(columns={'County': 'County_t', 'ITM_E': 'ITM_E_t', 'ITM_N': 'ITM_N_t'
                                    , 'English_Name': 'English_Name_t'}, inplace=True)
    reference_townlands_data = file_handler.to_lower(reference_townlands_data)

    # Read the input file
    addresses_data = pd.DataFrame(pd.read_csv(input_path))
    # Call the function to parse the input dataset and create a dataframe of inputs.
    data_cleaned = file_handler.mask_data(addresses_data, count=len(addresses_data.columns))
    # Function to convert all string columns to lowercase values
    data_cleaned = file_handler.to_lower(data_cleaned)
    # remove "co. " in county name if present in the county name
    data_cleaned['columns1'] = data_cleaned['columns1'].str.replace("co. ", "")
    data_cleaned.to_csv(str(file_handler.config['file paths']['CLEANED DATA']), index=False)
    return reference_counties_data, reference_townlands_data


