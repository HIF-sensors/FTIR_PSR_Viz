import pandas as pd
import os
import numpy as np

class Dataloader:
    def __init__(self, reflectance_paths=None, absorbance_paths=None):
        self.reflectance_paths = reflectance_paths
        self.absorbance_paths = absorbance_paths
        self.reflectance_df = None
        self.absorbance_df = None
        self.rescaled_df = None
        if self.reflectance_paths:
            self.load_reflectance()
            self.rescale_data()
        if self.absorbance_paths:
            self.load_absorbance()
        

    @staticmethod
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def load_reflectance(self):
        all_energy = []
        for file_path in self.reflectance_paths:
            filename = os.path.basename(file_path)
            # TODO
            # Check if it's actually 'Reflectance'
            ##
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
        self.reflectance_df = pd.DataFrame(all_energy, columns=wavelength_list)
        
        # TODO
        # else : Write an error message

    def load_absorbance(self):
        all_energy = []
        # wavelength_list = []
        for file_path in self.absorbance_paths:
            filename = os.path.basename(file_path)
            # TODO
            # Check if it's actually 'Absorbance'
            ##
            # sample_energy = [filename]
            # wavelength_list = ['sample']
            sample_energy = []
            wavelength_list = []
            with open(file_path, 'r') as f:
                lines = f.readlines()
            for line0 in lines:
                line = line0.strip().split(" ")
                if self.is_float(line[0]):
                    energy = float(line[-1])
                    sample_energy = [energy] + sample_energy
                    # TODO
                    # Fill wavelength list only for one sample file to avoid
                    # iterative process
                    ##
                    wavenumber = float(line[0])
                    wavelength = (1/wavenumber)* (10 ** 7)
                    wavelength_list = [wavelength] + wavelength_list
                    # sample_energy.append(energy)
                    # wavelength_list.append(wavelength)
            wavelength_list = ['sample'] + wavelength_list
            sample_energy = [filename] + sample_energy
            all_energy.append(sample_energy)
        self.absorbance_df = pd.DataFrame(all_energy, columns=wavelength_list)


    def rescale_data(self):
        new = []
        for index, row in self.reflectance_df.iterrows():
            text = [row.iloc[0]]
            energy = np.array(row)[1:]
            min_val = energy.min()
            max_val = energy.max()
            rescaled_energy = list((energy - min_val) / (max_val - min_val))
            new.append(text+rescaled_energy)

        self.rescaled_df = pd.DataFrame(new, columns=list(self.reflectance_df.columns))
        pass



    