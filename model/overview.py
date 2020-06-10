import pandas as pd


def overview(df):
    
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