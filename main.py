from parser import DataParser
import igs
import heapq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import logging
FILENAME = "data/leij_1-10.dat"
DELTA_T = 30
SATELLITES = []

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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

    velocities = []
    angular_velocities = []
    sats = []
    epochs = []

    for sat_id, sat in sat_data.items():
        x, y, z = sat['x_sat'].values, sat['y_sat'].values, sat['z_sat'].values
        epoch = sat['epoch'].values[0:-1]
        V, W = [], []

        table = PrettyTable(["Epoch [s]", "Linear velocity [km/s]", "Angular velocity [rad/s]"])
        table.title = f"Satellite {sat_id}"

        for i in range(len(x)-1):
            dx1 = x[i+1] - site.x
            dy1 = y[i+1] - site.y
            dz1 = z[i+1] - site.z
            D1 = np.array([dx1, dy1, dz1])

            dx2 = x[i] - site.x
            dy2 = y[i] - site.y
            dz2 = z[i] - site.z
            D2 = np.array([dx2, dy2, dz2])

            prod = np.dot(D1, D2)
            M1 = np.linalg.norm(D1)
            M2 = np.linalg.norm(D2)

            w = np.acos(prod / (M1 * M2)) / DELTA_T
            W.append(w)

            v = w * M2 / 1000
            V.append(v)

            table.add_row([epoch[i], v, w])

        velocities.append(V)
        angular_velocities.append(W)
        sats.append(sat_id)
        epochs.append(epoch)
        print(table)

    colors = plt.cm.tab10(np.linspace(0, 1, 3))

    plt.figure(figsize=(12, 12))
    for i in range(len(sats)):
        plt.plot(epochs[i], velocities[i], label=sats[i], color=colors[i])
        plt.axhline(sum(velocities[i])/len(velocities[i]), color=colors[i], linestyle='--')
    plt.xlabel("Epoch [s]")
    plt.ylabel("Velocity [km/s]")
    ax = plt.gca()
    plt.legend(loc='best')
    plt.suptitle(f"Velocities of Satellites")
    plt.savefig("figures/velocities.png")

    plt.figure(figsize=(12, 12))
    for i in range(len(sats)):
        plt.plot(epochs[i], angular_velocities[i], label=sats[i], color=colors[i])
        plt.axhline(sum(angular_velocities[i])/len(angular_velocities[i]), color=colors[i], linestyle='--')
    plt.xlabel("Epoch [s]")
    plt.ylabel("Angular Velocity [rad/s]")
    ax = plt.gca()
    plt.legend(loc='best')
    plt.suptitle(f"Angular velocities of Satellites")
    plt.savefig("figures/angular_velocities.png")
