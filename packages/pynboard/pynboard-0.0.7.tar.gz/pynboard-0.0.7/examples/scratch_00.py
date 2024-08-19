# %%
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd

from pprint import pprint

pd.set_option('display.max_columns', 10)

import plotly.io as pio
from plotly import express as px
import plotly.graph_objects as go

pio.templates.default = "seaborn"
pio.templates[pio.templates.default].layout.width = 800
pio.templates[pio.templates.default].layout.height = 400

from importlib import reload

# %%
import pynboard as pbo

# %%
n = 750
dates = pd.bdate_range("2019-1-1", periods=n)
# eps = np.random.standard_cauchy(size=n)
eps = np.random.normal(size=n)
val = np.cumsum(eps) * 1e4
data = pd.DataFrame({"date": dates, "eps": eps, "val": val})

d = [pd.Timedelta(seconds=s) for s in np.random.choice(600, size=len(data))]
data["dt"] = data["date"] + pd.to_timedelta(d)
data["gr"] = np.random.choice(3, size=len(data))

# %%
pbo.init_html_board(r"c:\temp\pbo\first.html", open_file=True)

# %%
pbo.render_obj(data, pbo.dprops_df(title="bah", precision={"eps": 6}))



# %%
pbo.display_properties.DisplayPropertiesDataFrame()


# %%





# %%