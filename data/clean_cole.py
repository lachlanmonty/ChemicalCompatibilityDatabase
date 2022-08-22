import pandas as pd

df = pd.read_csv("cole_data.csv")

regex = r"\((.+)\)| (\d+%)|(>\d+%)"


df_2 = df["chemical"].str.extract(regex)

