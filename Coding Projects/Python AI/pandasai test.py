import os
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI


openai_api_key = os.environ["OPENAI_API_KEY"]

llm = OpenAI(api_token=openai_api_key)

pandas_ai = PandasAI(llm)


from pandasai.llm.starcoder import Starcoder
from pandasai.llm.falcon import Falcon
from pandasai.llm.google_palm import GooglePalm

# GooglePalm
#llm = GooglePalm(api_token="YOUR_Google_API_KEY")

# Starcoder
#llm = Starcoder(api_token="YOUR_HF_API_KEY")

# Falcon
#llm = Falcon(api_token="YOUR_HF_API_KEY")

#%%

import pandas as pd

df = pd.read_csv("netflix_dataset.csv", index_col=0)
df.head(3)