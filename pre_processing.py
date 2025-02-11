import numpy as np
import pandas as pd

def rescale_data(df):
    new = []
    for index, row in df.iterrows():
        text = [row.iloc[0]]
        energy = np.array(row)[1:]
        min_val = energy.min()
        max_val = energy.max()
        rescaled_energy = list((energy - min_val) / (max_val - min_val))
        new.append(text+rescaled_energy)

    rescaled_df = pd.DataFrame(new, columns=list(df.columns))
    return rescaled_df