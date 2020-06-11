import pandas as pd
from fds_profiling.model.summary import describe_numeric_1d, describe_categorical
from fds_profiling.model.summary import get_table_stats

def describe_table(series: pd.Series, column_types):
    
    info = get_table_stats(series)
    
    overview = [
        { "name": "Number of variables", "value": info["n_var"], "alert": False},
        { "name": "Number of observations", "value": info["n"], "alert": False },
        { "name": "Missing cells", "value": str(info["n_cells_missing"]) + ' (' + str(info["p_cells_missing"]) + '%)', "alert": False },
        { "name": "Duplicate rows", "value": str(info["n_duplicated"]) + ' (' + str(info["p_duplicated"]) + '%)', "alert": False },
        { "name": "Key columns", "value": "-", "alert": False }
    ]
    
    
    column_types_lst = [type_ for col_i, type_ in column_types.items()]
    variable_types_dict = dict((i, column_types_lst.count(i)) for i in column_types_lst)
    
    variable_types = []
    for type_, count in sorted(variable_types_dict.items()):
        variable_types.append(
            { "name": type_, "value": count, "alert": False},
        )

    return [overview, variable_types]

def describe_series(series: pd.Series, column_type):
    
    if (column_type == "NUM"):
        
        info = describe_numeric_1d(series)
    
        descriptive = [
            { "name": "Distinct count", "value": info["distinct_count"], "alert": False},
            { "name": "Missing", "value": str(info["n_missing"]) + ' (' + str(info["p_missing"]) + '%)', "alert": False },
            { "name": "Min - Max", "value": str(info["min"]) + ' - ' + str(info["max"]), "alert": False },
            { "name": "Zeros", "value": str(info["n_zeros"]) + ' (' + str(info["p_zeros"]) + '%)', "alert": False }
        ]

        variability = [
            { "name": "Range", "value": info["range"], "alert": False },
            { "name": "Interquartile range (IQR)", "value": info["iqr"], "alert": False },
            { "name": "Variance", "value": info["variance"], "alert": False },
            { "name": "Standard deviation", "value": info["std"], "alert": False },
            { "name": "Median Absolute Deviation (MAD)", "value": info["std"], "alert": False }
        ]

        moments = [
            { "name": "Mean", "value": info["mean"], "alert": False },
            { "name": "Median", "value": info["50%"], "alert": False },
            { "name": "Skewness", "value": info["skewness"], "alert": False },
            { "name": "Kurtosis", "value": info["kurtosis"], "alert": False }
        ]

        outlier = [
            { "name": "Outlier", "value": str(info["n_outlier"]) + ' (' + str(info["p_outlier"]) + '%)', "alert": False },
            { "name": "Outlier above", "value": str(info["n_outlier_above"]) + ' (' + str(info["p_outlier_above"]) + '%)', "alert": False },
            { "name": "Outlier below", "value": str(info["n_outlier_below"]) + ' (' + str(info["p_outlier_below"]) + '%)', "alert": False }
        ]
    
        return [descriptive, variability, moments, outlier]
    
    elif (column_type != "NUM"):
        
        info = describe_categorical(series)
    
        descriptive = [
            { "name": "Distinct count", "value": info["distinct_count"], "alert": False},
            { "name": "Missing", "value": str(info["n_missing"]) + ' (' + str(info["p_missing"]) + '%)', "alert": False },
            { "name": "Mode", "value": info["mode"], "alert": False }
        ]
    
        return [descriptive]
        
    else:
        pass