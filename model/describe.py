import pandas as pd


def describe(df, column_name, column_type):
    
    descriptive = [
        {
            "name": "Distinct values",
            "value": 200,
            "alert": False
        },
        {
            "name": "Missing values",
            "value": 10,
            "alert": True
        }
    ]
    
    return descriptive