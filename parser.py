import pprint
from datetime import timedelta


class DataParser:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self.parse_to_sat_dict()

    # def parse_to_string_dict(self):
    #     current_epoch = ""
    #     with open(self.filename, 'r') as f:
    #         for line in f:
    #             if not line.startswith('   '):
    #                 current_epoch = line.strip().split('.')[0]
    #                 self.data[current_epoch] = []
    #             else:
    #                 line = line.strip()
    #                 sat = {}
    #                 sat['satid'], sat['ro'], sat['P1'], sat['P2'], sat['L1'], sat['L2'], sat['Mw'], sat['Md'], sat[
    #                     'Td'], sat['Tw'], sat['Tw_estimate'], sat['dt'], sat['dTrec_estimate'], sat['A'], sat[
    #                     'windup_metr'], sat['elevation'], sat['x_sat'], sat['y_sat'], sat['z_sat'], sat['P3'], sat[
    #                     'L3'], sat['R_geom'] = tuple(line.split('\t'))
    #                 sat_data = {sat['satid']: sat}
    #                 self.data[current_epoch].append(sat_data)

    def parse_to_sat_dict(self):
        current_epoch = ""
        with open(self.filename, 'r') as f:
            for line in f:
                if not line.startswith('   '):
                    current_epoch = self.parse_time(line.strip().split('.')[0])
                    self.data[current_epoch] = []
                else:
                    line = line.strip()
                    sat = {}
                    sat['satid'], sat['ro'], sat['P1'], sat['P2'], sat['L1'], sat['L2'], sat['Mw'], sat['Md'], sat[
                        'Td'], sat['Tw'], sat['Tw_estimate'], sat['dt'], sat['dTrec_estimate'], sat['A'], sat[
                        'windup_metr'], sat['elevation'], sat['x_sat'], sat['y_sat'], sat['z_sat'], sat['P3'], sat[
                        'L3'], sat['R_geom'] = tuple(line.split('\t'))
                    vision = SatVision(sat, current_epoch)
                    self.data[current_epoch].append(vision)

    def epoch_to_sat_dict(self):
        sat_data = {}
        for epoch in self.data.keys():
            for satellite in self.data[epoch]:
                if not satellite.satid in sat_data.keys():
                    sat_data[satellite.satid] = [satellite]
                else:
                    sat_data[satellite.satid].append(satellite)
        return sat_data

    def parse_time(self, time_str):
        h, m, s = tuple(map(int, time_str.split(':')))
        return timedelta(hours=h, minutes=m, seconds=s)


class SatVision:
    def __init__(self, sat_params, epoch):
        self.epoch = epoch
        self.satid = sat_params['satid']
        self.ro = float(sat_params['ro'])
        self.P1 = float(sat_params['P1'])
        self.P2 = float(sat_params['P2'])
        self.L1 = float(sat_params['L1'])
        self.L2 = float(sat_params['L2'])
        self.Mw = float(sat_params['Mw'])
        self.Md = float(sat_params['Md'])
        self.Td = float(sat_params['Td'])
        self.Tw = float(sat_params['Tw'])
        self.Tw_estimate = float(sat_params['Tw_estimate'])
        self.dt = float(sat_params['dt'])
        self.dTrec_estimate = float(sat_params['dTrec_estimate'])
        self.A = float(sat_params['A'])
        self.windup_metr = float(sat_params['windup_metr'])
        self.elevation = float(sat_params['elevation'])
        self.x_sat = float(sat_params['x_sat'])
        self.y_sat = float(sat_params['y_sat'])
        self.z_sat = float(sat_params['z_sat'])
        self.P3 = float(sat_params['P3'])
        self.L3 = float(sat_params['L3'])
        self.R_geom = float(sat_params['R_geom'])

    def __str__(self):
        return f"{self.satid=}\t{self.epoch}"


if __name__ == '__main__':
    parser = DataParser("data/leij_1-10.dat")