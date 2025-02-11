import pandas as pd
import os
import numpy as np

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def load_reflectance(reflectance_paths):
    all_energy = []
    for file_path in reflectance_paths:
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
            if is_float(line[0]):
                wavelength = float(line[0])
                energy = float(line[-1])
                sample_energy.append(energy)
                wavelength_list.append(wavelength)
        all_energy.append(sample_energy)
    reflectance_df = pd.DataFrame(all_energy, columns=wavelength_list)
    
    # TODO
    # else : Write an error message
    return reflectance_df

def load_absorbance(absorbance_paths):
    all_energy = []
    # wavelength_list = []
    for file_path in absorbance_paths:
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
            if is_float(line[0]):
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
    absorbance_df = pd.DataFrame(all_energy, columns=wavelength_list)
    return absorbance_df








    