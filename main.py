__author__ = 'Naveen'

import datetime
import pandas as pd
import pyproj
import os
import requests
import sys
import warnings
from flask import Flask, jsonify, Response, render_template
from data_preprocessing import file_handler, file_generator
import logging

warnings.filterwarnings('ignore')

app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route("/")
def page_main():
    return render_template('index.html')


@app.route('/geocoder', methods=['GET'])
def api_main():

    try:
        reference_counties_data, reference_townlands_data = file_generator.create_csv(reference_counties_path=
                                                                                      file_handler.config['file paths'][
                                                                                          'COUNTY REFERENCE'],
                                                                                      reference_townlands_path=
                                                                                      file_handler.config['file paths'][
                                                                                          'TOWNLAND REFERENCE'],
                                                                                      input_path=
                                                                                      file_handler.config['file paths'][
                                                                                          'input file'])

        data_cleaned = pd.read_csv(str(file_handler.config['file paths']['CLEANED DATA']), skipinitialspace=True)
        # Join logic from reference table
        itm_data = data_cleaned.merge(reference_counties_data,
                                      left_on='columns1', right_on='English_Name', how='left').merge(
            reference_townlands_data, left_on='columns2', right_on='English_Name_t', how='left')
        # Co-ordinate conversion logic
        itm_data['WGS_Coord'] = itm_data.apply(
            lambda row: pyproj.transform(file_handler.co_ord_conv('ITM'), file_handler.co_ord_conv('WGS84'), row['ITM_E'],
                                         row['ITM_N']) if row['columns2'] != row['English_Name_t'] else
            pyproj.transform(file_handler.co_ord_conv('ITM'), file_handler.co_ord_conv('WGS84'), row['ITM_E_t'],
                             row['ITM_N_t']), axis=1)
        # Conversion of default longitude,Latitude by Pyproj to Lats,Long sequence
        itm_data['WGS_Coord'] = itm_data['WGS_Coord'].astype(str).str[1:-1].str.split(",").str[::-1].str.join(",")
        # Setting up the timestamp of execution
        timestamp = str(datetime.datetime.now().strftime("%Y_%m_%d%H%M%S"))
        # Dumping the csv file generated
        itm_data.to_csv('output_data/{}_output.csv'.format(timestamp), index=False)
        return Response(itm_data,
                        mimetype="text/csv",
                        headers={"Content-disposition":
                                 "attachment; filename={}output.csv".format(timestamp)})
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:

        try:
            print("Server stopped\n")
            sys.exit(0)
        except SystemExit:
            os._exit(0)


