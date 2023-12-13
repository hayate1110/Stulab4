import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm
import matplotlib.pyplot as plt
import japanize_matplotlib

INPUT_PATH = os.path.join("week2","RxData_unit_conv","*","*","*.log")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "RX_LEVEL_18"]
df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)
    df[col_names[0]] = pd.to_datetime(df[col_names[0]])
    df[col_names[1]] = pd.to_numeric(df[col_names[1]])
    df_list.append(df)

df1 = pd.concat(df_list)
df1 = df1.set_index("time")

INPUT_PATH = os.path.join("week2","RxData_fix","*","*","192.168.100.11_csv.log")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "RX_LEVEL_26"]
df_list = []
for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)
    df[col_names[0]] = pd.to_datetime(df[col_names[0]])
    df[col_names[1]] = pd.to_numeric(df[col_names[1]])
    df_list.append(df)

df2 = pd.concat(df_list)
df2 = df2.set_index("time")

INPUT_PATH = os.path.join("week2","RainData_fix","*","*.csv")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "rain"]
df_list = []
for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)
    df[col_names[0]] = pd.to_datetime(df[col_names[0]])
    df[col_names[1]] = pd.to_numeric(df[col_names[1]])
    df_list.append(df)

df3 = pd.concat(df_list)
df3 = df3.set_index("time")
df = df1.join(df2)
df = df.join(df3)
df = df.sort_index()
print(df)

fig = plt.figure()
plt.plot(df.index, df["RX_LEVEL_18"])
plt.plot(df.index, df["RX_LEVEL_26"])
plt.plot(df.index, df["rain"])
plt.show()