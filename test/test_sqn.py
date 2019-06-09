from Trading_Functions.SQN import sqn
import pandas as pd

def test_sqn():
    input_data = [1,2,3,4,5,6]
    input_df = pd.DataFrame(input_data)
    output = 3
    period = 5
    sqn_df = sqn(input_df, period)
    assert sqn_df.iloc[6] == output
