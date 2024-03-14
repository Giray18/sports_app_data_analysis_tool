import pandas as pd
import os
import glob
import numpy as np
import dat
from datetime import datetime, timedelta, date

def read_df_json(path = []):
    ''' This function reads multiple json files from location passed as parameter 
    and transposes them by a condition '''
    # use glob to get all the json files 
    # in the folder
    json_files = glob.glob(os.path.join(path, "*.json"))
    # loop over the list of csv files
    for f in json_files:
        print(f)
        # global df
        # read the json files
        df = pd.read_json(f)
        if len(df.columns) > len(df.index):
            df = df.transpose()
        else:
            df
    return df

if __name__ == '__main__':
    read_df_json()