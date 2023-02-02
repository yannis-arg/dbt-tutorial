import pandas as pd


df = pd.read_json('aura_surveys_sample_2023.ndjson', lines=True)


print(df.columns)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df.head(n=5))