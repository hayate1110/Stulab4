import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm

INPUT_PATH = os.path.join("week2","RxData_fix","*","*","192.168.100.9_csv.log")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "1803_RX_LEVEL"]

def unit_conv(x):
    if x < 0:
        x += 256
        x = (x / 2) - 256
    else:
        x = (x / 2) - 256
    return x

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)

    df["time"] = pd.to_datetime(df["time"])
    df["1803_RX_LEVEL"] = pd.to_numeric(df["1803_RX_LEVEL"])

    df["1803_RX_LEVEL"] = df["1803_RX_LEVEL"].apply(unit_conv)

    df = df.set_index("time")
    
    path = path.split("/")
    output_path = os.path.join(path[0], "RxData_unit_conv", path[2], path[3])
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(output_path + f"/{path[4]}", index_label="datetime")