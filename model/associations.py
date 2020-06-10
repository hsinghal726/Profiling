import pandas as pd


def associations(df, column_name, column_type):
    
    descriptive = [
        {
            "name": "Column 1",
            "value": 200,
            "alert": False
        },
        {
            "name": "Column 2",
            "value": 10,
            "alert": True
        }
    ]
    
    return descriptive