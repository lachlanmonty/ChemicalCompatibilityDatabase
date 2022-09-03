import pandas as pd
import re

df = pd.read_csv("cole_data.csv")

regex = r" \((.+)\)| (\d+%)|(>\d+%)"


chem = df.groupby(by="chemical").sum().reset_index()

df_2 = df["chemical"].str.split(pat=regex, expand=True)
df_3 = df["chemical"].str.extract(regex)
df_3["sub"] = df_3[[0, 1, 2]].bfill(axis=1).iloc[:, 0]

df_2 = df_2.rename(columns={0: "head"})

df["head"] = df_2["head"]
df["sub"] = df_3["sub"]

df.to_excel("coledata.xlsx", index=False)

