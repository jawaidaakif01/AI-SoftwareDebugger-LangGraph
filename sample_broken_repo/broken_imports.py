import pandas as pd
from nonexistent_utils import helper_function

def process_data():
    df = pd.DataFrame({"a": [1,2,3]})
    return helper_function(df)

if __name__=="__main__":
    process_data()
    