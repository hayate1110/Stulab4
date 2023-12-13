import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm
import matplotlib.pyplot as plt
import japanize_matplotlib

INPUT_PATH = os.path.join("week2","RxData_fix","*","*","192.168.100.11_csv.log")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "1803_RX_LEVEL"]
freq = -3

df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)
    df["time"] = pd.to_datetime(df["time"])
    df["1803_RX_LEVEL"] = pd.to_numeric(df["1803_RX_LEVEL"])

    df_list.append(df)

df = pd.concat(df_list)
print(f"最大値{df['1803_RX_LEVEL'].max()}")
print(f"最小値{df['1803_RX_LEVEL'].min()}")

level = []
count = []
sum_sec = []
min_level = int(df["1803_RX_LEVEL"].min()) -1
for i in range(0, min_level, freq):
    level.append(i)
    count.append(((df["1803_RX_LEVEL"] <= i) & (df["1803_RX_LEVEL"] > i+freq)).sum())
df = pd.DataFrame({"rx_level": level[::-1], "count": count[::-1]})
df["count"] = df["count"].cumsum()
df.at[df.index[-1], "count"] = 1051000
df["ratio"] = df["count"] / 10510

#df["rx_level"] *= -1

fig, ax = plt.subplots()
ax.plot(df["ratio"], df["rx_level"], marker='.', label="受信強度[dB]")
ax.set_xscale('log')
ax.set_title("受信強度累積時間分布 26GHz(琉大観測: 2009/06, 2009/10 〜 2009/12)")
ax.set_xlabel("累積時間率(%)")
ax.set_ylabel("降雨強度(mm/h)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x))))
plt.legend()
plt.savefig("week2/rx_dist_26.png")
#plt.show()