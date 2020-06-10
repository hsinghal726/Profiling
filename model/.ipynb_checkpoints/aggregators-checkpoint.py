import pandas as pd


def groupby_aggregator(df, cat_col, metrics):
    
#     return df
    
    metrics_df = pd.DataFrame()
    
    for metric_name, metric_func in metrics.items():
        metric_df = df.groupby(cat_col).apply(metric_func).reset_index(name=metric_name)
        
        metrics_df = pd.merge(metric_df, metrics_df, how="outer") if metrics_df.shape[0]!=0 else metric_df

    return metrics_df.set_index(cat_col)