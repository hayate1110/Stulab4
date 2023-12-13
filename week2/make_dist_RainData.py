import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm
import matplotlib.pyplot as plt
import japanize_matplotlib

INPUT_PATH = os.path.join("week2","RainData_unit_conv","*","*.csv")
data_path_list = glob.glob(INPUT_PATH)
col_names = ["time", "rain"]
freq = 3

df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=col_names)
    df["time"] = pd.to_datetime(df["time"])
    df["rain"] = pd.to_numeric(df["rain"])

    df_list.append(df)

df = pd.concat(df_list)

print(f"最大値{df['rain'].max()}")
print(f"最小値{df['rain'].min()}")

rain = []
count = []
sum_sec = []
max_rain = int(df["rain"].max()) + 1
for i in range(0, max_rain, freq):
    rain.append(i)
    count.append(((df["rain"] >= i) & (df["rain"] < i+freq)).sum())
df = pd.DataFrame({"rain": rain[::-1], "count": count[::-1]})
df["count"] = df["count"].cumsum()

df.at[df.index[-1], "count"] = 1051000
df["ratio"] = df["count"] / 10510

print(df["ratio"].min())

fig, ax = plt.subplots()
ax.plot(df["ratio"], df["rain"], marker='.', label="降雨強度[mm/h]")
ax.set_xscale('log')
ax.set_title("降雨強度累積時間分布(琉大観測: 2009/06, 2009/10 〜 2009/12)")
ax.set_xlabel("累積時間率(%)")
ax.set_ylabel("降雨強度(mm/h)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x))))
plt.legend()
plt.savefig("week2/rain_dist.png")
#plt.show()