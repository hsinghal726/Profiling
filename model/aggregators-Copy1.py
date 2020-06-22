import pandas as pd


def groupby_aggregator(dataframe, categorical_col, metrics):
    
    metrics_df = pd.DataFrame()
    
    for metric_name, metric_func in metrics:
        metric_df = dataframe.groupby(categorical_col).apply(metric_func).reset_index(name=metric_name)
        
        metrics_df = pd.merge(metric_df, metrics_df, how="outer") if metrics_df.shape[0]!=0 else metric_df

    return metrics_df.set_index(categorical_col)


def count_metric(series: pd.Series, categorical_col):

    ## Count
    metrics_df = series.value_counts().reset_index()
    metrics_df.columns = [categorical_col, "Count"]

    ## Percent
    total_counts = metrics_df["Count"].sum()
    metrics_df["Percent"] = metrics_df["Count"]/total_counts

    ## Cummulative Count
    metrics_df["Cummulative Count"] = metrics_df["Count"].cumsum()

    ## Cummulative Percent
    metrics_df["Cummulative Percent"] = metrics_df["Percent"].cumsum()

    ## Creating "80%" and "100%" row" (Pareto's principal)

    if (metrics_df.shape[0] > 7):
        ## 80%, 100% index
        index_80 = metrics_df[metrics_df["Cummulative Percent"]<.8].shape[0]+1
        index_100 = metrics_df.shape[0] 

        if (index_80 > 6):
            ## Creating  80% mark
            metrics_df.loc[5] = [
                '"80% mark (' + str(index_80 - 5) + ')"',
                metrics_df.loc[6:index_80, "Count"].sum(),
                metrics_df.loc[6:index_80, "Percent"].sum(),
                metrics_df.loc[index_80-1, "Cummulative Count"],
                metrics_df.loc[index_80-1, "Cummulative Percent"]
            ]

        index_80 = max(index_80, 6)
        ## Creating 100% mark
        metrics_df.loc[6] = [
            '"100% mark (' + str(index_100 - index_80) + ')"',
            metrics_df.loc[index_80:index_100, "Count"].sum(),
            metrics_df.loc[index_80:index_100, "Percent"].sum(),
            metrics_df.loc[index_100-1, "Cummulative Count"],
            metrics_df.loc[index_100-1, "Cummulative Percent"]
        ]
    
    metrics_df = metrics_df.head(7)

    ## Preprocessing
    metrics_df[["Percent", "Cummulative Percent"]] = metrics_df[["Percent", "Cummulative Percent"]].applymap(lambda x: str(round(100*x, 1)) + " %")
    
    return metrics_df.set_index(categorical_col)