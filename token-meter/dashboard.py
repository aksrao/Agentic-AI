import json
import pandas as pd
import plotly.express as px

with open("token_usage.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

fig = px.bar(df, x="model", y="Total Tokens Used", color="sbu")

fig.show()