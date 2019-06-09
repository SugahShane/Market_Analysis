from Trading_Functions.SQN import *
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal


def test_sqn():
    input_data = [1,2,3,4,5,6]
    input_df = pd.DataFrame(input_data)
    output = 3
    period = 5
    sqn_df = sqn(input_df, period)
    assert sqn_df.iloc[6] == output

def test_percent_change():
    input_df = pd.DataFrame({0: [1,2,3,4,5,6]})
    output_df = pd.DataFrame({0: [1.0, 0.5, 0.333333, 0.25, 0.2]})
    percent_change_df = percent_change(input_df).dropna()
    percent_change_array = percent_change_df.to_numpy()
    output_array = output_df.to_numpy()
    array_comparison = (percent_change_array == output_array).all()
    array_comparison2 = np.array_equiv(output_array, percent_change_array)
    df_comparison = percent_change_df.equals(output_df)
    assert df_comparison
