import numpy as np
import pandas as pd

def get_table_stats(df: pd.DataFrame) -> dict:
    """
    General statistics for the DataFrame.
    """
    n = len(df)

    table_stats = {
        "n": n,
        "n_var": len(df.columns),
        "n_cells_missing": df.isnull().sum().sum(),
        "n_duplicated": sum(df.duplicated())
    }

    table_stats["p_cells_missing"] = table_stats["n_cells_missing"] / (table_stats["n"] * table_stats["n_var"])
    table_stats["p_duplicated"] = table_stats["n_duplicated"] / (table_stats["n"] * table_stats["n_var"])

    for key, value in table_stats.items():
        try:
            table_stats[key] = round(value, 2)
        except:
            pass
        
    return table_stats

def describe_numeric_1d(series: pd.Series) -> dict:
        
    def mad(arr):
        """ Median Absolute Deviation: a "Robust" version of standard deviation.
            Indices variability of the sample.
            https://en.wikipedia.org/wiki/Median_absolute_deviation
        """
        return np.median(np.abs(arr - np.median(arr)))
    
    stats = {}
                
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = series.value_counts(dropna=True)
    stats["distinct_count_with_nan"] = value_counts_with_nan.count()
    stats["distinct_count_without_nan"] = value_counts_without_nan.count()
    
    # number of observations in the Series
    length = len(series)

    # number of non-NaN observations in the Series
    count = series.count()

    distinct_count = stats["distinct_count_without_nan"]
    
    stats["n"] = length
    stats["distinct_count"] = distinct_count
    stats["p_missing"] = 1 - (count / length)
    stats["n_missing"] = length - count
    stats["is_unique"] = distinct_count == count
    stats["mode"] = series.mode().iloc[0] if count > distinct_count > 1 else series[0]

    values = series.values
    present_values = values[~np.isnan(values)]

    stats["mean"] = np.mean(present_values)
    stats["std"] = np.std(present_values, ddof=1)
    stats["variance"] = np.var(present_values, ddof=1)
    stats["min"] = np.min(present_values)
    stats["max"] = np.max(present_values)
    # Unbiased kurtosis obtained using Fisher's definition (kurtosis of normal == 0.0). Normalized by N-1.
    stats["kurtosis"] = series.kurt()
    # Unbiased skew normalized by N-1
    stats["skewness"] = series.skew()
    stats["mad"] = mad(present_values)
    stats["n_zeros"] = (count - np.count_nonzero(present_values))
    stats["p_zeros"] = stats["n_zeros"] / stats["n"]
    
    stats["range"] = stats["max"] - stats["min"]
    
    quantiles = [.25, .5, .75]
    stats.update(
        {
            f"{percentile:.0%}": value
            for percentile, value in series.quantile(quantiles).to_dict().items()
        }
    )

    stats["iqr"] = stats["75%"] - stats["25%"]
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.NaN
    
    stats["n_outlier_above"] = len(series[series > (stats["75%"] + 1.5*stats["iqr"])])
    stats["n_outlier_below"] = len(series[series < (stats["25%"] - 1.5*stats["iqr"])])
    stats["n_outlier"] = stats["n_outlier_above"] + stats["n_outlier_below"]
    
    stats["p_outlier_above"] = stats["n_outlier_above"] / stats["n"]
    stats["p_outlier_below"] = stats["n_outlier_below"] / stats["n"]
    stats["p_outlier"] = stats["n_outlier"] / stats["n"]
    
    
    for key, value in stats.items():
        try:
            stats[key] = round(value, 2)
        except:
            pass
    
    return stats

def describe_categorical(series: pd.Series) -> dict:
    
    stats = {}
                
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = series.value_counts(dropna=True)
    stats["distinct_count_with_nan"] = value_counts_with_nan.count()
    stats["distinct_count_without_nan"] = value_counts_without_nan.count()
    
    # number of observations in the Series
    length = len(series)

    # number of non-NaN observations in the Series
    count = series.count()

    distinct_count = stats["distinct_count_without_nan"]
    
    stats["n"] = length
    stats["distinct_count"] = distinct_count
    stats["p_missing"] = 1 - (count / length)
    stats["n_missing"] = length - count
    stats["is_unique"] = distinct_count == count
    stats["mode"] = series.mode().iloc[0] if count > distinct_count > 1 else series[0]
    
    for key, value in stats.items():
        try:
            stats[key] = round(value, 2)
        except:
            pass
    
    return stats
