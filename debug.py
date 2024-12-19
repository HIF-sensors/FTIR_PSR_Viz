from dataloader import *
from vizualization import *
if __name__ == '__main__':
    file_paths = ["/Users/nova98/Documents/Nova/Spectrolysis/raw_data_FINEST/finest_18Nov/large_white_material/Face_A/sample_00001.sed",
                "/Users/nova98/Documents/Nova/Spectrolysis/raw_data_FINEST/finest_18Nov/large_white_material/Face_A/sample_00002.sed"
                ]
    dataloader = Dataloader(file_paths)
    viz(dataloader.raw_df)

    pass