import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm

INPUT_PATH = os.path.join("week2","RxData","*","*","*.log")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "1803_RX_LEVEL"]

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
            x = datetime.datetime.strptime(x, "%H:%M:%S")
        except:
            x = x
    return type(x)

for path in tqdm.tqdm(data_path_list):
    date = path.split("/")[3]
    date = f"{date[:4]}-{date[4:6]}-{date[6:]} "
    try:
        df = pd.read_csv(path, header=None, skiprows=2, usecols=[0, 1], names=col_names)
    except:
        df = pd.read_csv(path, header=None, skiprows=2, usecols=[0, 1], names=col_names, encoding="shift-jis")

    df = df.mask(df.applymap(typecheck)==str, np.nan) # 型チェック後、strになるものはnp.nanで置き換え

    df = df.dropna()

    if df["time"][0] == "00:00:00":
        is_zero_origin = True

    df["time"] = date + df["time"]
    df["time"] = pd.to_datetime(df["time"])
    df["1803_RX_LEVEL"] = pd.to_numeric(df["1803_RX_LEVEL"])
    df = df.set_index("time")

    date_range = pd.date_range(start=f"{date}00:00:00", end=f"{date}23:59:59", freq="s")
    df_new = pd.DataFrame(index = date_range, columns=df.columns)
    
    df_new.loc[df.index, :] = df
    df_new = df_new.fillna(method='ffill')
    df_new = df_new.fillna(method='bfill')

    date_range = pd.date_range(start=f"{date}00:00:00", end=f"{date}23:59:59", freq="10s") # 10秒ごとの時間のリスト
    df_new = df_new.loc[date_range, :]
    
    path = path.split("/")
    output_path = os.path.join(path[0], "RxData_fix", path[2], path[3])
    os.makedirs(output_path, exist_ok=True)
    df_new.to_csv(output_path + f"/{path[4]}", index_label="datetime")