import pandas as pd
import matplotlib.pyplot as plt
from fds_profiling.visualisation.image_encoding import hex_to_rgb, plot_360_n0sc0pe

def bar_chart(df):
    """
    df: frequency table
    """
    
    df.plot.barh()
#     plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.2)
    return plot_360_n0sc0pe(plt)