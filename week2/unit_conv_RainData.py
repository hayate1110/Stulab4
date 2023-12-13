import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm

INPUT_PATH = os.path.join("week2","RainData_fix","*","*.csv")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "rain"]

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)

    df["time"] = pd.to_datetime(df["time"])
    df["rain"] = pd.to_numeric(df["rain"])

    df["rain"] = df["rain"].apply(lambda x: x * 0.0083333 * 60)

    df = df.set_index("time")
    path = path.split("/")
    output_path = os.path.join(path[0], "RainData_unit_conv", path[2])
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(output_path + f"/{path[3]}", index_label="datetime")
