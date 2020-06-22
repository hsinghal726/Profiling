import pandas as pd


def groupby_aggregator(dataframe, categorical_col, metrics):
    
    metrics_df = pd.DataFrame()
    
    for metric_name, metric_func in metrics:
        metric_df = dataframe.groupby(categorical_col).apply(metric_func).reset_index(name=metric_name)
        
        metrics_df = pd.merge(metric_df, metrics_df, how="outer") if metrics_df.shape[0]!=0 else metric_df

    return metrics_df.set_index(categorical_col)


def count_metric(series: pd.Series, categorical_col):

    ## Count
    count_df = series.value_counts().reset_index()
    count_df.columns = [categorical_col, "Count"]

    unique_values = count_df.shape[0]
    if (unique_values > 10):
        count_df.loc[9] = [ "Others (" + str(unique_values - 9) + ")", count_df.loc[9:, "Count"].sum()]
        count_df = count_df.head(10)

    ## Percent, Cummulative count, Cummulative percent
    total_counts = count_df["Count"].sum()
    count_df["Percent(%)"] = count_df["Count"]/total_counts
    count_df["Cummulative Count"] = count_df["Count"].cumsum()
    count_df["Cummulative Percent(%)"] = count_df["Percent(%)"].cumsum()
    count_df[["Percent(%)", "Cummulative Percent(%)"]] = count_df[["Percent(%)", "Cummulative Percent(%)"]].applymap(lambda x: round(100*x, 1))
    
    return count_df.set_index(categorical_col)