import numpy as np
import pandas as pd

import seaborn
sns.set_style("darkgrid")

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from fds_profiling.visualisation.image_encoding import hex_to_rgb, plot_360_n0sc0pe

def bar_chart(df):
    """
    df: frequency table
    """
    
    df.plot.barh()
#     plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)


def histogram(series: pd.Series):
    
    x = np.array(series.dropna())
    
    # Cut the window in 2 parts
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, 
                                    gridspec_kw={"height_ratios": (.15, .85)}
                                   )

    sns.boxplot(x, ax=ax_box)
    sns.distplot(x, ax=ax_hist)

    ax_box.set(yticks=[])
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    
    return plot_360_n0sc0pe(plt)
