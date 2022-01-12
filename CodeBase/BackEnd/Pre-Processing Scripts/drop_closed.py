import pandas as pd
import json

path = "data (1).json"
# data = json.loads(path)
data = pd.read_json(path)
df = pd.DataFrame(data)
print(df.head)
print(set(df['business_status'].values))
df = df[df.business_status != "CLOSED_TEMPORARILY"]
print(df.head)
print(df.columns)
result = df.to_json(orient="records")
parsed = json.loads(result)
with open("places.txt", "w") as of: 
    json.dump(parsed, of)
