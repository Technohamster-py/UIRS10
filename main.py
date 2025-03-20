from parser import DataParser
import igs
import heapq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILENAME = "data/leij_1-10.dat"
DELTA_T = 30
SATELLITES = []

if __name__ == '__main__':
    site = igs.IgsSite(FILENAME.split('/')[1][0:4])
    print(site)

    data_parser = DataParser(FILENAME)
    satellites = data_parser.epoch_to_sat_dict()

    lengths = ((key, len(value)) for key, value in satellites.items())
    top_sats = [int(sat[0]) for sat in heapq.nlargest(3, lengths, key=lambda x: x[1])]

    data = pd.read_csv(data_parser.convert_to_csv())
    selected_data = data[data['satid'].isin(top_sats)]

    sat_data = {sat_id: selected_data[selected_data['satid'] == sat_id] for sat_id in top_sats}

    for sat_id, sat in sat_data.items():
        x, y, z = sat['x_sat'].values, sat['y_sat'].values, sat['z_sat'].values
        epoch = sat['epoch'].values

        for i in range(len(x)-1):
            dx = (x[i+1] - x[i]) / DELTA_T
            dy = (y[i+1] - y[i]) / DELTA_T
            dz = (z[i+1] - z[i]) / DELTA_T
            V = np.sqrt(dx**2 + dy**2 + dz**2)
