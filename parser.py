import pprint


class DataParser:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self.parse_to_string_dict()

    def parse_to_string_dict(self):
        current_epoch = ""
        with open(self.filename, 'r') as f:
            for line in f:
                if not line.startswith('   '):
                    current_epoch = line.strip().split('_')[0]
                    self.data[current_epoch] = []
                else:
                    line = line.strip()
                    sat = {}
                    sat['satid'], sat['ro'], sat['P1'], sat['P2'], sat['L1'], sat['L2'], sat['Mw'], sat['Md'], sat[
                        'Td'], sat['Tw'], sat['Tw_estimate'], sat['dt'], sat['dTrec_estimate'], sat['A'], sat[
                        'windup_metr'], sat['elevation'], sat['x_sat'], sat['y_sat'], sat['z_sat'], sat['P3'], sat[
                        'L3'], sat['R_geom'] = tuple(line.split('\t'))
                    sat_data = {sat['satid']: sat}
                    self.data[current_epoch].append(sat_data)

    def parse_to_sat_dict(self):
        current_epoch = ""
        with open(self.filename, 'r') as f:
            for line in f:
                if not line.startswith('   '):
                    current_epoch = line.strip().split('_')[0]
                    self.data[current_epoch] = {}
                else:
                    line = line.strip()
                    sat = {}
                    sat['satid'], sat['ro'], sat['P1'], sat['P2'], sat['L1'], sat['L2'], sat['Mw'], sat['Md'], sat[
                        'Td'], sat['Tw'], sat['Tw_estimate'], sat['dt'], sat['dTrec_estimate'], sat['A'], sat[
                        'windup_metr'], sat['elevation'], sat['x_sat'], sat['y_sat'], sat['z_sat'], sat['P3'], sat[
                        'L3'], sat['R_geom'] = tuple(line.split('\t'))
                    vision = SatVision(sat, current_epoch)
                    self.data[current_epoch].append(vision)


class SatVision:
    def __init__(self, sat_params, epoch):
        self.epoch = epoch
        self.satid = sat_params['satid']
        self.ro = int(sat_params['ro'])
        self.P1 = int(sat_params['P1'])
        self.P2 = int(sat_params['P2'])
        self.L1 = int(sat_params['L1'])
        self.L2 = int(sat_params['L2'])
        self.Mw = int(sat_params['Mw'])
        self.Md = int(sat_params['Md'])
        self.Td = int(sat_params['Td'])
        self.Tw = int(sat_params['Tw'])
        self.Tw_estimate = int(sat_params['Tw_estimate'])
        self.dt = int(sat_params['dt'])
        self.dTrec_estimate = int(sat_params['dTrec_estimate'])
        self.A = int(sat_params['A'])
        self.windup_metr = int(sat_params['windup_metr'])
        self.elevation = int(sat_params['elevation'])
        self.x_sat = int(sat_params['x_sat'])
        self.y_sat = int(sat_params['y_sat'])
        self.z_sat = int(sat_params['z_sat'])
        self.P3 = int(sat_params['P3'])
        self.L3 = int(sat_params['L3'])
        self.R_geom = int(sat_params['R_geom'])




if __name__ == '__main__':
    parser = DataParser("data/leij_1-10.dat")
    pprint.pprint(parser.data['1:0:0.000000'], indent=2)

