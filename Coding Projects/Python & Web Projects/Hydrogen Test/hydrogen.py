#%%
import matplotlib
matplotlib.use('Qt5Agg')
# This should be done before `import matplotlib.pyplot`
# 'Qt4Agg' for PyQt4 or PySide, 'Qt5Agg' for PyQt5
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 20, 500)
plt.plot(t, np.sin(t))
plt.show()


from IPython.display import JSON

data = {"foo": {"bar": "baz"}, "a": 1}
JSON(data)



import numpy as np
import pandas as pd

df = pd.DataFrame({'A': 1.,
                   'B': pd.Timestamp('20130102'),
                   'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                   'D': np.array([3] * 4, dtype='int32'),
                   'E': pd.Categorical(["test", "train", "test", "train"]),
                   'F': 'foo'})

df



from IPython.display import HTML
HTML("<iframe src='https://nteract.io/' width='900' height='490'></iframe>")



[{
  "name": "Jupyter server",
  "options": {
    "baseUrl": "localhost",
    "token": "7a200554db748c6f5c3cb4ecfc9097585b867f16e9a6cc5c"
  }
}]
