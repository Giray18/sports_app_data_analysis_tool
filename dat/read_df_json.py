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
        game_ids = df.index.to_list()
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    df[col] = [i.lower() for i in df[col]]
                except AttributeError:
                    for c in game_ids:
                        df[col][c] =  [v.lower() for v in df[col][c]]
    return df

if __name__ == '__main__':
    read_df_json()