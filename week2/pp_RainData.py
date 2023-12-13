import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm

INPUT_PATH = os.path.join("week2","RainData","*","*.csv")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "rain"]

def typecheck(x):
    '''
    数値または日付型に変換できるかできないかを判定する関数
    :param x: 
    :return: 変換後のxの型
    '''
    try:
        x = float(x)
    except:
        try:
            x = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
        except:
            x = x
    return type(x)

for path in tqdm.tqdm(data_path_list):
    date = path.split("/")[2]
    date = f"{date[:4]}-{date[4:6]}-{date[6:]} "
    try:
        df = pd.read_csv(path, header=None, skiprows=2, names=col_names)
    except:
        df = pd.read_csv(path, header=None, skiprows=2, names=col_names, encoding="shift-jis")

    df["time"] = df["time"].apply(lambda x: x.replace("/","-"))
    df = df.mask(df.applymap(typecheck)==str, np.nan) # 型チェック後、strになるものはnp.nanで置き換え
    df = df.dropna()

    df["time"] = pd.to_datetime(df["time"])
    df["rain"] = pd.to_numeric(df["rain"])

    df = df.set_index("time")

    date_range = pd.date_range(start=f"{date}00:00:00", end=f"{date}23:59:59", freq="10s")
    df_new = pd.DataFrame(index = date_range, columns=df.columns)
    
    df_new.loc[df.index, :] = df
    df_new = df_new.fillna(method='ffill')
    df_new = df_new.fillna(method='bfill')
    
    path = path.split("/")
    output_path = os.path.join(path[0], "RainData_fix", path[2])
    os.makedirs(output_path, exist_ok=True)
    df_new.to_csv(output_path + f"/{path[3]}", index_label="datetime")