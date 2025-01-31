import pandas as pd
import os
import numpy as np

class Dataloader:
    def __init__(self, data_paths):
        self.data_paths = data_paths
        self.raw_df = None
        self.normalized_df = None
        self.load_data()
        self.normalize_data()

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

    def normalize_data(self):
        # new_columns = {'sample': self.raw_df['sample']}
        # for col in self.raw_df.columns[1:]:
        #     min_val = self.raw_df[col].min()
        #     max_val = self.raw_df[col].max()
        #     new_columns[col] = (self.raw_df[col] - min_val) / (max_val - min_val)

        # self.normalized_df = pd.DataFrame(new_columns)
        # pass

        new = []
        for index, row in self.raw_df.iterrows():
            text = [row.iloc[0]]
            energy = np.array(row)[1:]
            # mean = np.mean(energy)
            # std = np.std(energy)
            # normalized_energy = ((energy - mean) / std).tolist()
            min_val = energy.min()
            max_val = energy.max()
            normalized_energy = list((energy - min_val) / (max_val - min_val))
            new.append(text+normalized_energy)

        self.normalized_df = pd.DataFrame(new, columns=list(self.raw_df.columns))
        pass



    