import pandas as pd
import os
import glob
import numpy as np
import dat

def normalize_needed_cols(df: pd.DataFrame):
    ''' This function reads selected columns from dataframes and normalize '''