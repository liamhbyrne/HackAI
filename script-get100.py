import pandas as pd

df = pd.read_csv("./final_results.csv")

df.hist(df["visitors"])


"""
known_names = []
for index, row in df.iterrows():
    if row['name'] in known_names:
        df.drop(index, inplace=True)
    else:
        known_names.append(row['name'])

df.to_csv('final.csv')

s=""
for i in range(100):
    name = known_names[i]
    s+=name+"___"
print(s)
"""