from parser import DataParser
import igs
import heapq
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
FILENAME = "data/leij_1-10.dat"
DELTA_T = 30
SATELLITES = []


def calculate_azimuth(site_cords: tuple, sat_cords: tuple):
    x_site, y_site, z_site = site_cords
    x_sat, y_sat, z_sat = sat_cords

    delta_x = x_sat - x_site
    delta_y = y_sat - y_site
    delta_z = z_sat - z_site

    azimuth = math.atan(delta_y/delta_x)
    return azimuth


if __name__ == '__main__':
    site = igs.IgsSite(FILENAME.split('/')[1][0:4])
    print(site)

    site_cords = (site.x, site.y, site.z)

    data_parser = DataParser(FILENAME)
    satellites = data_parser.epoch_to_sat_dict()

    lengths = ((key, len(value)) for key, value in satellites.items())
    top_sats = [int(sat[0]) for sat in heapq.nlargest(3, lengths, key=lambda x: x[1])]

    data = pd.read_csv(data_parser.convert_to_csv())
    selected_data = data[data['satid'].isin(top_sats)]

    sat_data = {sat_id: selected_data[selected_data['satid'] == sat_id] for sat_id in top_sats}

    velocities = []
    angular_velocities = []
    sats = []
    epochs = []

    for sat_id, sat in sat_data.items():
        x, y, z, elev = sat['x_sat'].values, sat['y_sat'].values, sat['z_sat'].values, sat['elevation'].values
        epoch = sat['epoch'].values[0:-1]
        V, W = [], []

        table = PrettyTable(["Epoch", "Linear velocity", "Angular velocity"])
        table.title = f"Satellite {sat_id}"

        for i in range(len(x)-1):
            dx = (x[i+1] - x[i]) / DELTA_T
            dy = (y[i+1] - y[i]) / DELTA_T
            dz = (z[i+1] - z[i]) / DELTA_T
            v = np.sqrt(dx**2 + dy**2 + dz**2)
            V.append(v)

            d_theta = (elev[i+1] - elev[i]) / DELTA_T
            d_azim = (calculate_azimuth(site_cords, (x[i+1], y[i+1], z[i+1])) - calculate_azimuth(site_cords, (x[i], y[i], z[i]))) / DELTA_T
            w = d_azim / DELTA_T
            W.append(w)

            table.add_row([epoch[i], v, w])

        velocities.append(V)
        angular_velocities.append(W)
        sats.append(sat_id)
        epochs.append(epoch)
        print(table)

    plt.figure(figsize=(12, 12))
    for i in range(len(sats)):
        plt.plot(epochs[i], velocities[i], label=sats[i])
    plt.xlabel("Epoch")
    plt.ylabel("Velocity [m/s]")
    ax = plt.gca()
    plt.legend(loc='best')
    plt.suptitle(f"Velocities of Satellites")
    plt.savefig("figures/velocities.png")
    # plt.show()

    plt.figure(figsize=(12, 12))
    for i in range(len(sats)):
        plt.plot(epochs[i], angular_velocities[i], label=sats[i])
    plt.xlabel("Epoch")
    plt.ylabel("Angular Velocity [rad/s]")
    ax = plt.gca()
    plt.legend(loc='best')
    plt.suptitle(f"Angular velocities of Satellites")
    plt.savefig("figures/angular_velocities.png")
    # plt.show()