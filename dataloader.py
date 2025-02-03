import pandas as pd
import os
import numpy as np

class Dataloader:
    def __init__(self, data_paths):
        self.data_paths = data_paths
        self.raw_df = None
        self.rescaled_df = None
        self.load_data()
        self.rescale_data()

    @staticmethod
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def load_data(self):
        all_energy = []
        for file_path in self.data_paths:
            filename = os.path.basename(file_path)
            sample_energy = [filename]
            wavelength_list = ['sample']
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            for line0 in lines:
                line = line0.strip().split(" ")
                if self.is_float(line[0]):
                    wavelength = float(line[0])
                    energy = float(line[-1])
                    sample_energy.append(energy)
                    wavelength_list.append(wavelength)
            all_energy.append(sample_energy)
        self.raw_df = pd.DataFrame(all_energy, columns=wavelength_list)

    def rescale_data(self):
        new = []
        for index, row in self.raw_df.iterrows():
            text = [row.iloc[0]]
            energy = np.array(row)[1:]
            min_val = energy.min()
            max_val = energy.max()
            rescaled_energy = list((energy - min_val) / (max_val - min_val))
            new.append(text+rescaled_energy)

        self.rescaled_df = pd.DataFrame(new, columns=list(self.raw_df.columns))
        pass



    