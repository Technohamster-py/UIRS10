from parser import SatVision, DataParser
import igs
import heapq

FILENAME = "data/leij_1-10.dat"
SATELLITES = []

if __name__ == '__main__':
    site = igs.IgsSite(FILENAME.split('/')[1][0:4])
    satellites = DataParser(FILENAME).epoch_to_sat_dict()

    lengths = ((key, len(value)) for key, value in satellites.items())
    top_sats = heapq.nlargest(3, lengths, key=lambda x: x[1])
