import numpy as np
from pypower.idx_brch import RATE_A
import pandas as pd
from openpyxl import load_workbook
from sys import stdout, stderr

from os.path import dirname, join

from time import time

from numpy import r_, c_, ix_, zeros, pi, ones, exp, argmax, logical_or
from numpy import flatnonzero as find

from pypower.bustypes import bustypes
from pypower.ext2int import ext2int
from pypower.loadcase import loadcase
from pypower.ppoption import ppoption
from pypower.ppver import ppver
from pypower.makeBdc import makeBdc
from pypower.makeSbus import makeSbus
from pypower.dcpf import dcpf
from pypower.makeYbus import makeYbus
from pypower.newtonpf import newtonpf
from pypower.fdpf import fdpf
from pypower.gausspf import gausspf
from pypower.makeB import makeB
from pypower.pfsoln import pfsoln
from pypower.printpf import printpf
from pypower.savecase import savecase
from pypower.int2ext import int2ext

from pypower.idx_bus import PD, QD, VM, VA, GS, BUS_TYPE, PQ, REF, BUS_I, PV, VMIN, VMAX, BASE_KV, ZONE
from pypower.idx_brch import PF, PT, QF, QT, TAP, F_BUS, T_BUS
from pypower.idx_gen import PG, QG, VG, QMAX, QMIN, GEN_BUS, GEN_STATUS
from numpy import zeros, arange, where, ones, exp, pi, linspace, repeat, expand_dims, array, genfromtxt, concatenate, \
    sum, vstack, sqrt, round, hstack, logical_and
from numpy import flatnonzero as find

from scipy.optimize import minimize

import os

class DTU_ADN:
    '''Class Attributes'''
    # Dataset Location
    data_path = os.path.dirname(__file__).replace("\\", "/") + '/data/'
    loc_net_60kV = data_path + 'network_60kV\\',  # Location of the dataset
    loc_timeseries_60kV = data_path + 'timeseries_aggregated_10kV\\',  # Location of the dataset
    loc_net_10kV400V = data_path + 'network_10kV_400V\\',  # Location of the dataset
    loc_timeseries_400V = data_path + 'timeseries_400V\\',  # Location of the dataset
    loc_load_gen_type = data_path + 'network_10kV_400V\\load_and_gen_type\\'
    # System parameters
    sys_freq_HZ = 50
    s_base_mva = 100
    v_baseLV_kv = 10
    v_baseMV_kv = 60
    v_baseHV_kv = 150,
    vm_pu_max = 1.1
    vm_pu_min = 0.9
    slack_max_mw, slack_min_mw = 200, -200
    slack_vm_pu = 1

    # For the 60kV network
    load_bus_names = linspace(26, 47, num=(48 - 26), endpoint=True, dtype=int)
    gen_bus = [19, 20, 21]
    wpp1_base_mw, wpp1_max_mw = 12, 12
    wpp2_base_mw, wpp2_max_mw = 15, 15,

    # Tap changers
    trafo_loc_L1 = array([0, 3, 5, 8, 11, 14,
                          15, 16, 18, 20, 22,
                          25, 27, 29, 31, 34,
                          36, 38, 39, 43, 47,
                          48, 50])  # locations of tap changer in 60kV network
    tap_min_67kv, tap_median_67kv, tap_max_67kv, tap_percent_67kv = 1, 8, 17, 2.006 # this was 2.006 earlier
    tap_min_11kv, tap_median_11kv, tap_max_11kv, tap_percent_11kv = 1, 10, 17, 2.1 # this was 2.1 earlier
    tolerance_for_tap_changers = 1e-5
    max_iter_for_tap_changer = 30

    # class attributes for demand and generation time-series
    # The following variables will be changed to either numpy arrays or dataframes when particular methods are called.
    p_dem_60kV = 0
    q_dem_60kV = 0
    p_gen_60kV = 0

    p_dem_10kV = dict()
    q_dem_10kV = dict()
    p_gen_10kV = dict()

    # Time indices
    start_idx = 0
    end_idx = 0

    def __init__(self):
        # initializing variables
        self.net = dict()
        self.bus = None
        self.gen = None
        self.branch = None
        self.connected_LV_nets = []
        self.gen_10 = dict()
        self.bus_10 = dict()
        self.branch_10 = dict()
        self.net_10 = dict()
        self.net_400 = dict()
        self.net_60_10 = dict()
        self.net_400_timeseries = dict()
        self.net_400_orig_idx = dict()
        self.Ybus_10 = dict()

        # Loading 60kV network dataset.
        self.bus_60 = genfromtxt(DTU_ADN.loc_net_60kV[0] + 'bus_60kV.csv', delimiter=',')
        self.gen_60 = genfromtxt(DTU_ADN.loc_net_60kV[0] + 'gen_60kV.csv', delimiter=',')
        self.branch_60 = genfromtxt(DTU_ADN.loc_net_60kV[0] + 'line_60kV.csv', delimiter=',')

        # '''Preprocessing'''
        # The following step is important because, in pypower or python, numbering starts from 0. 0th bus is the reference bus.
        self.bus_60[:, BUS_I] -= 1
        self.gen_60[:, GEN_BUS] -= 1
        self.branch_60[:, T_BUS] -= 1
        self.branch_60[:, F_BUS] -= 1

        # self.gen_60[1:, QMAX] = 0.33*self.gen_60[1:, PMAX]
        # self.gen_60[1:, QMIN] = -0.33*self.gen_60[1:, PMAX]

        self.branch_60[:, RATE_A] = 100  # P flow limit
        self.branch_60[0, RATE_A] = 250  #

        # Storing shape of the 60kV network
        self.n_bus_60 = self.bus_60.shape[0]
        self.n_gen_60 = self.gen_60.shape[0]
        self.n_branch_60 = self.branch_60.shape[0]

        # Transformer locations
        self.branch_60[DTU_ADN.trafo_loc_L1, TAP] = 1
        # The 60kV network
        self.net_60 = dict(bus=self.bus_60, branch=self.branch_60, gen=self.gen_60,
                           version=2, baseMVA=DTU_ADN.s_base_mva)
        # Define the main network
        self.net = self.net_60.copy()
        self.branch = self.branch_60
        self.bus = self.bus_60
        self.gen = self.gen_60

        # Load the time-series:
        DTU_ADN.p_dem_60kV = pd.read_csv(DTU_ADN.loc_timeseries_60kV[0] + 'bus_P.csv',
                                         index_col=0)  # Active power demand
        DTU_ADN.q_dem_60kV = pd.read_csv(DTU_ADN.loc_timeseries_60kV[0] + 'bus_Q.csv',
                                         index_col=0)  # Reactive power demand
        DTU_ADN.p_gen_60kV = pd.read_csv(DTU_ADN.loc_timeseries_60kV[0] + 'gen_P.csv', index_col=0)  # Generation
        self.out = 0

    def connect_10kV400V_network(self, network_number):
        self.connected_LV_nets = self.connected_LV_nets + [network_number]
        _net_num_str = str(network_number)
        _bus_10 = genfromtxt(DTU_ADN.loc_net_10kV400V[0] + 'bus_' + _net_num_str + '.csv',
                                 delimiter=',', skip_header=1)
        _gen_10 = genfromtxt(DTU_ADN.loc_net_10kV400V[0] + 'gen_' + _net_num_str + '.csv',
                                 delimiter=',', skip_header=1)
        _branch_10 = genfromtxt(DTU_ADN.loc_net_10kV400V[0] + 'line_' + _net_num_str + '.csv',
                                    delimiter=',', skip_header=1)
        # Limit on the load flow in the line
        _branch_10[:, RATE_A] = 100

        'change indices of the 10 kV network'
        new_indices = zeros([_bus_10.shape[0] + 1, 2])  # np.zeros([_bus.shape[0]+1,2])
        new_indices[0, 0], new_indices[0, 1] = network_number, 0
        new_indices[1:, 0] = _bus_10[:, BUS_I] # original
        new_indices[1:, 1] = arange(1, _bus_10.shape[0] + 1) # in the order 0-1

        _gen_idx = array([new_indices[new_indices[:, 0] == kk, 1] for i, kk in enumerate(_gen_10[:, GEN_BUS])])
        _lineF_idx = array([new_indices[new_indices[:, 0] == kk, 1] for i, kk in enumerate(_branch_10[:, T_BUS])])
        _lineT_idx = array(
            [new_indices[new_indices[:, 0] == kk, 1].astype(float) for i, kk in enumerate(_branch_10[:, F_BUS])])

        _bus_10[:, 0] = new_indices[1:, 1] # new indices 0- n
        _gen_10[:, 0] = _gen_idx[:, GEN_BUS] # new indices from 0 - n
        _branch_10[:, T_BUS] = _lineT_idx[:, 0].copy()
        _branch_10[:, F_BUS] = _lineF_idx[:, 0].copy()
        _branch_10 = _branch_10[_branch_10[:, 0].argsort(), :]
        #
        _lineF_idx[:, 0] = _branch_10[:, F_BUS].copy()
        _lineT_idx[:, 0] = _branch_10[:, T_BUS].copy()
        # line indices for the main network:
        _lineF_idx[:, 0] = _lineF_idx[:, 0].copy() + self.bus.shape[0] - 1   # new line indices in the main net
        _lineT_idx[:, 0] = _lineT_idx[:, 0].copy() + self.bus.shape[0] - 1   # new line indices in the main net
        # change 47th to network_number
        '#todo: change this 47 to a variable obtained from the network model'
        _last_bus_node = max(self.net['bus'][:, BUS_I]).astype(int)
        _lineF_idx[_lineF_idx[:, 0] == _last_bus_node, 0] = network_number   # this is the last node
        _lineT_idx[_lineT_idx[:, 0] == _last_bus_node, 0] = network_number   # this is the last node in the main network

        # This will be used later.. only making a copy here
        _to_attach_bus = _bus_10.copy()
        _to_attach_gen = _gen_10.copy()
        _to_attach_branch = _branch_10.copy()

        # add bus of the network to attach to the 10kV network
        _bus_10 = vstack([self.bus_60[network_number, :], _bus_10])
        # changing bus 0 to reference bus
        _bus_10[0, BUS_I], _bus_10[0, BUS_TYPE], _bus_10[0, PD], _bus_10[0, QD] = 0, 3, 0, 0

        # add bus the 60-10kV transformer bus as generator bus
        _gen_10 = vstack([self.gen_60[0, :], _gen_10])
        # The independent 10kV-400V network:
        self.bus_10[_net_num_str] = _bus_10.copy()
        self.gen_10[_net_num_str] = _gen_10.copy()
        self.branch_10[_net_num_str] = _branch_10.copy()
        self.net_10[_net_num_str] = dict(bus=_bus_10.copy(), branch=_branch_10.copy(),
                           gen=_gen_10.copy(),
                           version=2, baseMVA=DTU_ADN.s_base_mva)

        # Careful not to repeat the 60-10kV network bus in the multi-v network.
        # change the bus numbers
        _to_attach_bus[:, 0] = _bus_10[1:, BUS_I] + self.bus.shape[0] - 1
        _to_attach_gen[:, 0] = _gen_10[1:, GEN_BUS] + self.bus.shape[0] - 1

        _to_attach_branch[:, T_BUS] = _lineT_idx[:, 0].copy()
        _to_attach_branch[:, F_BUS] = _lineF_idx[:, 0].copy()

        '#todo : Check why is this here'
        _to_attach_bus[:, VMAX] = 1.5
        _to_attach_bus[:, VMIN] = 0.7

        # _to_attach_gen[:, QMAX] = 0.33*_to_attach_gen[:, PMAX]
        # _to_attach_gen[:, QMIN] = -0.33 * _to_attach_gen[:, PMAX]
        # Concatenating 60kV network with 10-0.4kV network
        self.branch = concatenate((self.branch, _to_attach_branch), axis=0)
        self.bus = concatenate((self.bus, _to_attach_bus), axis=0)
        self.gen = concatenate((self.gen, _to_attach_gen), axis=0)

        self.net = dict(bus=self.bus, branch=self.branch,
                        gen=self.gen,
                        version=2, baseMVA=DTU_ADN.s_base_mva)

        '''Loading demand and generation time series for the 10-0.4kV network'''
        DTU_ADN.demand_timeseries_10_400(network_number)
        DTU_ADN.generation_timeseries_10_400(network_number)
        if sum(new_indices[where(new_indices[:, 0] == DTU_ADN.p_dem_10kV[_net_num_str].columns.values[0])[0][0]:, 0] - DTU_ADN.p_dem_10kV[_net_num_str].columns.values) == 0:
            DTU_ADN.p_dem_10kV[_net_num_str].columns = new_indices[where(new_indices[:, 0] == DTU_ADN.p_dem_10kV[_net_num_str].columns.values[0])[0][0]:, 1]
            DTU_ADN.q_dem_10kV[_net_num_str].columns = DTU_ADN.p_dem_10kV[_net_num_str].columns
        else:
            print('! index realignment not working')
        try:
            DTU_ADN.p_gen_10kV[_net_num_str].columns = self.gen_10[_net_num_str][1:, GEN_BUS]
        except:
            print('! Generation timeseries not complete for 10-0.4kV network')



    def connect_10kV_net_to_60kV(self):
        self.net_60_10 = self.net_60.copy()
        end_node = self.net_60_10['bus'][-1, 0]    # The last node in the network
        for isubnet in self.net_400.keys():
            bus_10 = self.net_400[str(isubnet)]['0']['bus'][1:, :].copy()
            gen_10 = self.net_400[str(isubnet)]['0']['gen'][1:, :].copy()
            branch_10 = self.net_400[str(isubnet)]['0']['branch'].copy()
            # BUS
            bus_10[:, 0] = bus_10[:, 0] + end_node
            # GENs
            gen_10[:, 0] = gen_10[:, 0] + end_node
            # BRANCH
            branch_10[:, 0] = branch_10[:, 0].copy() + end_node
            branch_10[:, 1] = branch_10[:, 1].copy() + end_node
            # Replace branch index which is end node to isubnet
            _loc_brch_end_node = branch_10[:, 0] == end_node
            branch_10[_loc_brch_end_node, 0] = float(isubnet)
            del _loc_brch_end_node
            _loc_brch_end_node = branch_10[:, 1] == end_node
            branch_10[_loc_brch_end_node, 1] = float(isubnet)

            self.net_60_10['bus'] = np.vstack([self.net_60_10['bus'], bus_10])
            self.net_60_10['gen'] = np.vstack([self.net_60_10['gen'], gen_10])
            self.net_60_10['branch'] = np.vstack([self.net_60_10['branch'], branch_10])

            del bus_10, gen_10, branch_10
            end_node = self.net_60_10['bus'][-1, 0]

    def update_60_10_kV_network(self):
        for isubnet in self.net_400.keys():
            _temp_loc = self.net_60_10['bus'][:, ZONE] == int(isubnet)
            self.net_60_10['bus'][_temp_loc, PD] = self.net_400[isubnet]['0']['bus'][1:, PD]
            self.net_60_10['bus'][_temp_loc, QD] = self.net_400[isubnet]['0']['bus'][1:, QD]




    def separate_400V_networks(self):
        for _node in self.connected_LV_nets:
            _str_net_num = str(_node)

            self.Ybus_10[_str_net_num], Yf, Yt = makeYbus(DTU_ADN.s_base_mva, self.bus_10[_str_net_num], self.branch_10[_str_net_num])
            del Yf, Yt

            # find the 10kV_400V transformer nodes
            _temp_idx = self.branch_10[_str_net_num][:, TAP] != 0
            _temp_bus = self.branch_10[_str_net_num][_temp_idx, T_BUS]
            _10_400_transformer_line = vstack([_temp_bus, self.branch_10[_str_net_num][_temp_idx, F_BUS]]).transpose().copy()

            del _temp_bus

            # find the 400 V nodes from the list.
            _bus_400 = self.bus_10[_str_net_num][self.bus_10[_str_net_num][:, BASE_KV] == 0.4, :]

            for aa in range(len(_10_400_transformer_line)):
                if _10_400_transformer_line[aa, 0] in _bus_400[:, BUS_I]:
                    _tempX = _10_400_transformer_line[aa, 1]
                    _10_400_transformer_line[aa, 1] = _10_400_transformer_line[aa, 0].copy()
                    _10_400_transformer_line[aa, 0] = _tempX
                else:
                    pass

            # for the 10kV network
            _bus_bool_10kV = zeros(self.bus_10[_str_net_num].shape[0], dtype=bool)
            _gen_bool_10kV = zeros(self.gen_10[_str_net_num].shape[0], dtype=bool)
            _branch_bool_10kV = zeros(self.branch_10[_str_net_num].shape[0], dtype=bool)

            self.net_400[_str_net_num] = dict()
            self.net_400_timeseries[_str_net_num] = dict()
            self.net_400_orig_idx[_str_net_num] = dict()
            for aa in range(len(_10_400_transformer_line)):

                self.net_400[_str_net_num][str(aa+1)] = dict()
                self.net_400_timeseries[_str_net_num][str(aa+1)] = dict()
                self.net_400_orig_idx[_str_net_num][str(aa+1)] = dict()

                _temp_bus = _10_400_transformer_line[aa, :]
                bus_indices, branch = self.find_connecting_nodes_helper(_temp_bus, _10_400_transformer_line[aa, :], 1,
                                                                        _str_net_num)

                'Bus'
                bus_temp = self.bus_10[_str_net_num][bus_indices.astype(int), :].copy()  # to slice the bus matrix
                _bus_bool = zeros(self.bus_10[_str_net_num].shape[0], dtype=bool)
                _bus_bool[bus_indices.astype(int)] = True
                bus_temp[bus_temp[:, BASE_KV] == 10.0, BUS_TYPE] = 3

                bus_new_idx = arange(0, bus_temp.shape[0])
                '10kV bus'
                _bus_bool_10kV = logical_or(_bus_bool, _bus_bool_10kV)

                'Generator'
                gen_indices = bus_temp[bus_temp[:, 1] == 2, 0]  # to get generator indices
                _gen_bool = zeros(self.gen_10[_str_net_num].shape[0], dtype=bool)
                gen_temp = zeros([len(gen_indices), self.gen_10[_str_net_num].shape[1]])
                for kk in range(len(gen_indices)):
                    _idx = where(self.gen_10[_str_net_num][:, GEN_BUS] == gen_indices[kk])[0]
                    _gen_bool[_idx] = True
                    gen_temp[kk] = self.gen_10[_str_net_num][_idx, :].copy()
                'Why gen_60 , change it to something else?'
                gen_temp = vstack([self.gen_60[0, :], gen_temp]) # adding generator bus
                gen_new_idx = bus_new_idx[bus_temp[:, 1]==2]

                '10kV Generator'
                _gen_bool_10kV = logical_or(_gen_bool_10kV, _gen_bool)

                'Branch'
                branch_temp = zeros([len(branch), self.branch_10[_str_net_num].shape[1]])
                branch_0_new_idx = zeros(len(branch))
                branch_1_new_idx = zeros(len(branch))
                for kk in range(len(branch)):
                    _idx = logical_and(self.branch_10[_str_net_num][:, F_BUS] == branch[kk, 0],
                                       self.branch_10[_str_net_num][:, T_BUS] == branch[kk, 1])
                    if sum(_idx) == 0:
                        _idx = logical_and(self.branch_10[_str_net_num][:, T_BUS] == branch[kk, 0],
                                           self.branch_10[_str_net_num][:, F_BUS] == branch[kk, 1])

                    branch_temp[kk, :] = self.branch_10[_str_net_num][_idx, :].copy()
                    _branch_bool_10kV[_idx] = True
                    # indices
                    branch_0_new_idx[kk] = bus_new_idx[bus_temp[:, BUS_I] == branch_temp[kk, 0]]
                    branch_1_new_idx[kk] = bus_new_idx[bus_temp[:, BUS_I] == branch_temp[kk, 1]]

                del _idx, kk

                'Original Vs new indices arrays'
                _bus_idx_to_save = array([bus_temp[:, BUS_I], bus_new_idx])
                _gen_idx_to_save = array([gen_temp[1:, GEN_BUS], gen_new_idx])
                _branch_idx_to_save = array([branch_temp[:, F_BUS], branch_0_new_idx,
                                             branch_temp[:, T_BUS], branch_1_new_idx])
                _connecting_idx = bus_temp[bus_temp[:, BASE_KV] == 10.0, BUS_I]

                'Changing to new indices'
                bus_temp[:, BUS_I] = bus_new_idx
                gen_temp[1:, GEN_BUS] = gen_new_idx
                branch_temp[:, F_BUS] = branch_0_new_idx
                branch_temp[:, T_BUS] = branch_1_new_idx

                del bus_new_idx, gen_new_idx, branch_0_new_idx, branch_1_new_idx

                'Saving networks'
                self.net_400[_str_net_num][str(aa+1)] = dict(bus=bus_temp, gen=gen_temp, branch=branch_temp,
                                                             version=2, baseMVA=DTU_ADN.s_base_mva)
                del bus_temp, gen_temp, branch_temp

                self.net_400_timeseries[_str_net_num][str(aa+1)] = dict(bus=_bus_bool, gen=_gen_bool[1:])
                del _bus_bool, _gen_bool

                self.net_400_orig_idx[_str_net_num][str(aa+1)] = dict(bus=_bus_idx_to_save, gen =_gen_idx_to_save,
                                                   branch= _branch_idx_to_save, connect_hv = _connecting_idx)
                del _bus_idx_to_save, _branch_idx_to_save, _gen_idx_to_save, _connecting_idx

            _bus_bool_10kV[_10_400_transformer_line[:, 0].astype(int)] = False
            bus_temp = self.bus_10[_str_net_num][~_bus_bool_10kV, :].copy()
            gen_temp = self.gen_10[_str_net_num][~_gen_bool_10kV, :].copy()
            branch_temp = self.branch_10[_str_net_num][~_branch_bool_10kV, :].copy()

            'New indices'
            bus_new_idx = arange(0, bus_temp.shape[0])
            gen_new_idx = bus_new_idx[bus_temp[:, 1] == 2]
            branch_0_new_idx = zeros(len(branch_temp))
            branch_1_new_idx = zeros(len(branch_temp))
            for kk in range(len(branch_temp)):
                branch_0_new_idx[kk] = bus_new_idx[bus_temp[:, BUS_I] == branch_temp[kk, 0]]
                branch_1_new_idx[kk] = bus_new_idx[bus_temp[:, BUS_I] == branch_temp[kk, 1]]

            _bus_idx_to_save = array([bus_temp[:, BUS_I], bus_new_idx])
            _gen_idx_to_save = array([gen_temp[1:, GEN_BUS], gen_new_idx])
            _branch_idx_to_save = array([branch_temp[:, F_BUS], branch_0_new_idx,
                                         branch_temp[:, T_BUS], branch_1_new_idx])
            'Changing to new indices'
            bus_temp[:, BUS_I] = bus_new_idx
            gen_temp[1:, GEN_BUS] = gen_new_idx
            branch_temp[:, F_BUS] = branch_0_new_idx
            branch_temp[:, T_BUS] = branch_1_new_idx

            self.net_400[_str_net_num]['0'] = dict()
            self.net_400[_str_net_num]['0'] = dict(bus=bus_temp, gen=gen_temp, branch=branch_temp,
                                        version=2, baseMVA=DTU_ADN.s_base_mva)
            del bus_temp, gen_temp, branch_temp

            self.net_400_timeseries[_str_net_num]['0'] = dict()
            self.net_400_timeseries[_str_net_num]['0'] = dict(bus=~_bus_bool_10kV, gen=~_gen_bool_10kV[1:])
            del _bus_bool_10kV, _gen_bool_10kV, _branch_bool_10kV

            self.net_400_orig_idx[_str_net_num]['0'] = dict()
            self.net_400_orig_idx[_str_net_num]['0'] = dict(bus=_bus_idx_to_save, gen=_gen_idx_to_save,
                                                 branch=_branch_idx_to_save, connect_hv=0)
            del _bus_idx_to_save, _branch_idx_to_save, _gen_idx_to_save

    def find_connecting_nodes_helper(self, bus_indices, branch, n0, net_num):
        xx = where(self.Ybus_10[net_num][:, bus_indices[n0].astype(int)].toarray() != 0)[0].tolist()
        xx.remove(bus_indices[n0].astype(int))  # remove self
        if n0 == 1:
            xx.remove(bus_indices[0].astype(int))  # 10kV node
        else:
            yy = xx.copy()
            for i in range(len(xx)):
                if xx[i] in bus_indices:
                    yy.remove(xx[i])
            xx = yy.copy()
            del yy
        bus_indices = hstack([bus_indices, array(xx)])
        if len(xx) == 0:
            pass
        else:
            _tempbranch = zeros([len(xx), 2])
            _tempbranch[:, 0] = bus_indices[n0]
            _tempbranch[:, 1] = array(xx)
            branch = vstack([branch, _tempbranch])
        n0 += 1
        if n0 < len(bus_indices):
            bus_indices, branch = self.find_connecting_nodes_helper(bus_indices, branch, n0, net_num)
        return bus_indices, branch

    ''' From here start the time-series related functions'''

    def gen_and_demand_net_60(self, t0):
        '''
        This method updates the 60kV network only with the demand and generation values for time t0
        :param t0: time-stamp index
        :return: updated 60kV network
        '''
        # for the independent 60kV network:
        self.net_60['bus'][26:, PD] = DTU_ADN.p_dem_60kV.iloc[t0, 1:].values.copy()
        self.net_60['bus'][26:, QD] = DTU_ADN.q_dem_60kV.iloc[t0, 1:].values.copy()
        self.net_60['gen'][1:, PG] = DTU_ADN.p_gen_60kV.iloc[t0, :].values.copy()

    def gen_and_demand_net_10(self, t0):
        '''
        THis method updates the 10kV network only with the demand and generation values for time t0
        :param t0: time-stamp index (not a datetime value)
        :return: updated 10kV network only.
        '''
        for _node in self.connected_LV_nets:
            _str_net_num = str(_node)
            self.net_10[_str_net_num]['bus'][DTU_ADN.p_dem_10kV[_str_net_num].columns.values.astype(int), PD] = DTU_ADN.p_dem_10kV[_str_net_num].iloc[t0, :]
            self.net_10[_str_net_num]['bus'][DTU_ADN.q_dem_10kV[_str_net_num].columns.values.astype(int), QD] = DTU_ADN.q_dem_10kV[_str_net_num].iloc[t0, :]
            self.net_10[_str_net_num]['gen'][1:, PG] = DTU_ADN.p_gen_10kV[_str_net_num].iloc[t0, :]

    def gen_and_demand_net_400(self, t0):
        '''
        THis method updates the 0.4kV networks only with the demand and generation values for time t0
        :param t0: time-stamp index (not a datetime value)
        :return: updated 10kV network only.
        '''
        for _node in self.connected_LV_nets:
            _str_net_num = str(_node)

            number_of_400V_nets = len(self.net_400[_str_net_num].keys())

            _dem_idx = zeros(self.bus_10[_str_net_num].shape[0], dtype=bool)
            _dem_idx[DTU_ADN.p_dem_10kV[_str_net_num].columns.values.astype(int)] = True

            for i in range(number_of_400V_nets):
                _temp_dem_idx = logical_and(_dem_idx, self.net_400_timeseries[_str_net_num][str(i)]['bus'])

                _temp_pdem_idx = _temp_dem_idx[DTU_ADN.p_dem_10kV[_str_net_num].columns.values.astype(int)].copy()
                _temp_qdem_idx = _temp_dem_idx[DTU_ADN.q_dem_10kV[_str_net_num].columns.values.astype(int)].copy()

                self.net_400[_str_net_num][str(i)]['bus'][_temp_dem_idx[self.net_400_orig_idx[_str_net_num][str(i)]['bus'][0, :].astype(int)], PD] \
                    = DTU_ADN.p_dem_10kV[_str_net_num].iloc[t0, _temp_pdem_idx].values.copy()

                self.net_400[_str_net_num][str(i)]['bus'][_temp_dem_idx[self.net_400_orig_idx[_str_net_num][str(i)]['bus'][0, :].astype(int)], QD] \
                    = DTU_ADN.q_dem_10kV[_str_net_num].iloc[t0, _temp_qdem_idx].values.copy()

                self.net_400[_str_net_num][str(i)]['gen'][1:, PG] \
                    = DTU_ADN.p_gen_10kV[_str_net_num].iloc[t0, self.net_400_timeseries[_str_net_num][str(i)]['gen']].values.copy()


    def gen_and_demand_net(self, t0):
        '''
        This method updates the 60-10-0.4 kV network with demand and generation values for time t0
        :param t0: time-stamp index
        :param network_number: This is the bus number at which the 10-0.4kV network is attached to the 60kV network
        :return: updated 60-10-0.4kV network
        '''
        # for the connected network
        self.net['bus'][26:self.n_bus_60, PD] = DTU_ADN.p_dem_60kV.iloc[t0, 1:].values.copy()
        self.net['bus'][26:self.n_bus_60, QD] = DTU_ADN.q_dem_60kV.iloc[t0, 1:].values.copy()
        self.net['gen'][1:self.n_gen_60, PG] = DTU_ADN.p_gen_60kV.iloc[t0, :].values.copy()
        # because the 10kV-0.4kV network is connected.
        # turn 10kV nodes of the connected network to 0
        # 10kV-400V network
        _forwarding_bus_idx = self.bus_60.shape[0]
        _forwarding_gen_idx = self.n_gen_60
        for _netnum in self.connected_LV_nets:
            self.net['bus'][_netnum, PD], self.net['bus'][_netnum, QD] = 0.0, 0.0
            _str_netnum = str(_netnum)
            self.net['bus'][DTU_ADN.p_dem_10kV[_str_netnum].columns.values.astype(int) + _forwarding_bus_idx - 1, PD] = DTU_ADN.p_dem_10kV[_str_netnum].iloc[t0, :]
            self.net['bus'][DTU_ADN.q_dem_10kV[_str_netnum].columns.values.astype(int) + _forwarding_bus_idx - 1, QD] = DTU_ADN.q_dem_10kV[_str_netnum].iloc[t0, :]
            _num_gens = len(DTU_ADN.p_gen_10kV[_str_netnum].columns)
            self.net['gen'][_forwarding_gen_idx:_forwarding_gen_idx + _num_gens, PG] = DTU_ADN.p_gen_10kV[_str_netnum].iloc[t0, :].values.copy()
            _forwarding_bus_idx = _forwarding_bus_idx + self.bus_10[_str_netnum].shape[0] - 1
            _forwarding_gen_idx = _forwarding_gen_idx + _num_gens
    def wpps_params_in_60kV(self):
        BUS_C = 0
        S_BASE_C = 1
        VC_MAX = 2
        VC_MIN = 3
        IC_MAX = 4
        RC = 5
        XC = 6
        ZC = 7
        BC = 8
        C1 = 9
        C2 = 10
        C3 = 11
        # Lower limit for grid side converter linierization constants
        # linearization : 
        # Q_lower >= C_1 * v_gen**2+ C_2 * p_gen +  + C_3  
        # Grid side converter parameters for the three WPPs in the 60kV network. 
        self.gsc_60 = array([[19, 12, 1.1, 0.8, 1.25, 0.0114, 0.0096, 0.0, 0.0196, 4.17, -0.0934, 2.7737],
                             [20, 15, 1.1, 0.8, 1.25, 0.0114, 0.0096, 0.0, 0.0220, 4.17, -0.0934, 2.7737],
                             [21, 15, 1.1, 0.8, 1.25, 0.0114, 0.0096, 0.0, 0.0220, 4.17, -0.0934, 2.7737]])

        self.gsc_60[:, ZC] = sqrt(self.gsc_60[:, RC] ** 2 + self.gsc_60[:, XC] ** 2)

    def optimize_tap_position_for_10kv_vref(self, transformer_secondary, transformer_branch, voltage_ref):

        objective_function = lambda tap_position: self.voltage_difference_at_10kV_node(tap_position,
                                                                                       transformer_secondary,
                                                                                       transformer_branch, voltage_ref)
        tap_position_0 = 1

        result = minimize(objective_function, tap_position_0, bounds=[
            [DTU_ADN.tap_min_11kv / DTU_ADN.tap_median_11kv, DTU_ADN.tap_max_11kv / DTU_ADN.tap_median_11kv]],
                          method='L-BFGS-B')
        return result.x

    def voltage_difference_at_10kV_node(self, tap_position, transformer_secondary, transformer_branch, voltage_ref):
        tap_old = self.net['branch'][transformer_branch, TAP]
        self.net['branch'][transformer_branch, TAP] = tap_position
        opt = ppoption(ENFORCE_Q_LIMS=1, VERBOSE=0, OUT_ALL=0)
        try:
            out_net, success = DTU_ADN.runpf(self.net, opt)
            if success == 1:
                v_difference_sq = (voltage_ref - out_net['bus'][transformer_secondary, VM]) ** 2
            else:
                v_difference_sq = 10000
        except:
            v_difference_sq = 10000
        return v_difference_sq

    def save_data_in_array(self, n):
        self.bus_data[2 * n, :] = self.out['bus'][:, PD]
        self.bus_data[2 * n + 1, :] = self.out['bus'][:, QD]

        self.voltage_data[2 * n, :] = self.out['bus'][:, VM]
        self.voltage_data[2 * n + 1, :] = self.out['bus'][:, VA]

        self.line_data[4 * n, :] = self.out['branch'][:, PF]
        self.line_data[4 * n + 1, :] = self.out['branch'][:, QF]
        self.line_data[4 * n + 2, :] = self.out['branch'][:, PT]
        self.line_data[4 * n + 3, :] = self.out['branch'][:, QT]

        loss_all = round(sum(abs(self.out['branch'][:, PF] + self.out['branch'][:, PT])), 3)
        loss_60 = round(sum(abs(self.out['branch'][:52, PF] + self.out['branch'][:52, PT])), 3)
        loss_10 = round(sum(abs(self.out['branch'][52:, PF] + self.out['branch'][52:, PT])), 3)

        self.summary[n, 0] = self.out['gen'][0, PG]
        self.summary[n, 1] = self.out['gen'][0, QG]
        self.summary[n, 2] = self.out['gen'][1, PG]
        self.summary[n, 3] = self.out['gen'][1, QG]
        self.summary[n, 4] = self.out['gen'][2, PG]
        self.summary[n, 5] = self.out['gen'][2, QG]
        self.summary[n, 6] = self.out['gen'][3, PG]
        self.summary[n, 7] = self.out['gen'][3, QG]
        self.summary[n, 8] = loss_all
        self.summary[n, 9] = loss_60
        self.summary[n, 10] = loss_10

        bus_gen = zeros([1, self.out['bus'].shape[0]])
        bus_gen[0, self.net['gen'][:, GEN_BUS].astype(int)] = self.out['gen'][:, PG]
        self.LV_network[3 * n, :] = bus_gen

    def init_array_to_savedata(self):
        end_index = DTU_ADN.end_idx
        start_index = DTU_ADN.start_idx
        n_bus = self.net['bus'].shape[0]
        n_brch = self.net['branch'].shape[0]

        self.bus_data = zeros([2 * (end_index[0] - start_index[0] + 1), n_bus])
        self.line_data = zeros([4 * (end_index[0] - start_index[0] + 1), n_brch])
        self.voltage_data = zeros([2 * (end_index[0] - start_index[0] + 1), n_bus])
        self.LV_network = zeros([3 * (end_index[0] - start_index[0] + 1), n_bus])
        self.summary = zeros([end_index[0] - start_index[0] + 1, 17])
        self.summary_n_bus = zeros([end_index[0]-start_index[0]+1, 5])

    def save_array_to_excel(self, name):
        end_index = DTU_ADN.end_idx
        start_index = DTU_ADN.start_idx

        bus_data = self.bus_data
        voltage_data = self.voltage_data
        summary = self.summary
        LV_network = self.LV_network
        line_data = self.line_data

        time_stamps = DTU_ADN.p_dem_60kV.index.values.copy()

        del_me1 = array(range(start_index[0], end_index[0] + 1))
        del_me = repeat(array(range(start_index[0], end_index[0] + 1)), 2)
        del_me3 = repeat(array(range(start_index[0], end_index[0] + 1)), 3)
        del_me2 = repeat(array(range(start_index[0], end_index[0] + 1)), 4)

        dfbus = pd.DataFrame(data=hstack([expand_dims(del_me, 1), bus_data]), index=time_stamps[del_me])
        dfline = pd.DataFrame(data=hstack([expand_dims(del_me2, 1), line_data]), index=time_stamps[del_me2])
        dfvoltage = pd.DataFrame(data=hstack([expand_dims(del_me, 1), voltage_data]), index=time_stamps[del_me])
        dfsum = pd.DataFrame(data=hstack([expand_dims(del_me1, 1), summary]), index=time_stamps[del_me1])
        dfLVnet = pd.DataFrame(data=hstack([expand_dims(del_me3, 1), LV_network]), index=time_stamps[del_me3])

        writer = pd.ExcelWriter(name, engine='openpyxl', mode="a")
        writer.book = load_workbook(name)
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

        reader0 = pd.read_excel(name, sheet_name='summary')
        reader1 = pd.read_excel(name, sheet_name='bus')
        reader2 = pd.read_excel(name, sheet_name='voltage')
        reader3 = pd.read_excel(name, sheet_name='line')
        reader4 = pd.read_excel(name, sheet_name='pg_pd_qd')

        dfbus.to_excel(writer, sheet_name='bus', header=False, startrow=len(reader1) + 1)
        dfvoltage.to_excel(writer, sheet_name='voltage', header=False, startrow=len(reader2) + 1)
        dfline.to_excel(writer, sheet_name='line', header=False, startrow=len(reader3) + 1)
        dfsum.to_excel(writer, sheet_name='summary', header=False, startrow=len(reader0) + 1)
        dfLVnet.to_excel(writer, sheet_name='pg_pd_qd', header=False, startrow=len(reader4) + 1)
        writer.close()

    @classmethod
    def init_timeseries_index(cls, start_time, end_time):
        '''
        This method provides the index for the start and the end time stamps
        :param start_time: datetime variable
        :param end_time:  datetime variable
        :return:
        '''
        cls.start_idx = where(cls.p_dem_60kV.index.values.copy() == str(start_time))[0]
        cls.end_idx = where(cls.p_dem_60kV.index.values.copy() == str(end_time))[0]

    @classmethod
    def demand_timeseries_10_400(cls, network_number):
        _str_net_num = str(network_number)
        _type_file_lv = pd.read_csv(DTU_ADN.loc_load_gen_type + 'load_' + str(network_number) + '.csv')
        _type_file_lv.sort_values('Node', inplace=True, ignore_index=True)

        _slp = pd.read_csv(DTU_ADN.loc_timeseries_400V[0] + 'load_profile_' + str(network_number) + '.csv')
        even = arange(1, _slp.shape[1], 2)
        _slp_P = _slp.iloc[:, even]
        _slp_Q = _slp.iloc[:, even + 1]
        # changing column names from XX_Y_pu_MW to XX_Y to match slp column in _type_file_lv
        _slp_P.columns = array([xx[:4] for xx in _slp_P.columns.values])
        _slp_Q.columns = array([xx[:4] for xx in _slp_Q.columns.values])

        _df_filler = zeros([_slp.shape[0], _type_file_lv.shape[0]])

        cls.p_dem_10kV[_str_net_num] = pd.DataFrame(_df_filler.copy(), columns=_type_file_lv.Node.values, index=_slp.iloc[:, 0])
        cls.q_dem_10kV[_str_net_num] = pd.DataFrame(_df_filler.copy(), columns=_type_file_lv.Node.values, index=_slp.iloc[:, 0])
        for i in range(_type_file_lv.shape[0]):
            try:
                if _type_file_lv.slp[i] == 'residual':
                    _p = _slp_P.iloc[:, _slp_P.columns.values == 'resi'].values
                    _q = _slp_Q.iloc[:, _slp_Q.columns.values == 'resi'].values
                else:
                    _p = _slp_P.iloc[:, _slp_P.columns.values == _type_file_lv.slp[i]].values * _type_file_lv.mw[i]
                    _q = _slp_Q.iloc[:, _slp_Q.columns.values == _type_file_lv.slp[i]].values * _type_file_lv.mvar[i]
                cls.p_dem_10kV[_str_net_num].iloc[:, i] = _p
                cls.q_dem_10kV[_str_net_num].iloc[:, i] = _q
            except:
                pass
                # Todo: print warning
                #print(f"!! Warning: SLP not defined at a node: {i}")

    @classmethod
    def generation_timeseries_10_400(cls, network_number):
        _str_net_num = str(network_number)
        _gen_type = pd.read_csv(DTU_ADN.loc_load_gen_type + 'gen_type_' + str(network_number) + '.csv')
        _gen_type.sort_values('Node', inplace=True, ignore_index=True)

        _gen_profile = pd.read_csv(
            DTU_ADN.loc_timeseries_400V[0] + 'gen_profile_' + str(network_number) + '.csv')  # Per unit time series
        _gen_profile.columns = array([xx[:-3] for xx in _gen_profile.columns.values])
        _df_filler = zeros([_gen_profile.shape[0], _gen_type.shape[0]])  # just a filler with zero values
        cls.p_gen_10kV[_str_net_num] = pd.DataFrame(_df_filler, columns=_gen_type.Node.values, index=_gen_profile.iloc[:, 0])
        for i in range(_gen_type.shape[0]):
            try:
                _p = _gen_profile.iloc[:, _gen_profile.columns.values == _gen_type.gen_type[i]].values * _gen_type.mw[i]
                cls.p_gen_10kV[_str_net_num].iloc[:, i] = _p
            except:
                print('!! Warning generation profile not found.')

    # This is the power flow from pypower but a few errors are corrected.
    @classmethod
    def runpf(cls, casedata=None, ppopt=None, fname='', solvedcase=''):
        """Runs a power flow.

        Runs a power flow [full AC Newton's method by default] and optionally
        returns the solved values in the data matrices, a flag which is C{True} if
        the algorithm was successful in finding a solution, and the elapsed
        time in seconds. All input arguments are optional. If C{casename} is
        provided it specifies the name of the input data file or dict
        containing the power flow data. The default value is 'case9'.

        If the ppopt is provided it overrides the default PYPOWER options
        vector and can be used to specify the solution algorithm and output
        options among other things. If the 3rd argument is given the pretty
        printed output will be appended to the file whose name is given in
        C{fname}. If C{solvedcase} is specified the solved case will be written
        to a case file in PYPOWER format with the specified name. If C{solvedcase}
        ends with '.mat' it saves the case as a MAT-file otherwise it saves it
        as a Python-file.

        If the C{ENFORCE_Q_LIMS} options is set to C{True} [default is false] then
        if any generator reactive power limit is violated after running the AC
        power flow, the corresponding bus is converted to a PQ bus, with Qg at
        the limit, and the case is re-run. The voltage magnitude at the bus
        will deviate from the specified value in order to satisfy the reactive
        power limit. If the reference bus is converted to PQ, the first
        remaining PV bus will be used as the slack bus for the next iteration.
        This may result in the real power output at this generator being
        slightly off from the specified values.

        Enforcing of generator Q limits inspired by contributions from Mu Lin,
        Lincoln University, New Zealand (1/14/05).

        @author: Ray Zimmerman (PSERC Cornell)
        """
        ## default arguments
        if casedata is None:
            casedata = join(dirname(__file__), 'case9')
        ppopt = ppoption(ppopt)

        ## options
        verbose = ppopt["VERBOSE"]
        qlim = ppopt["ENFORCE_Q_LIMS"]  ## enforce Q limits on gens?
        dc = ppopt["PF_DC"]  ## use DC formulation?

        ## read data
        ppc = loadcase(casedata)

        ## add zero columns to branch for flows if needed
        if ppc["branch"].shape[1] < QT:
            ppc["branch"] = c_[ppc["branch"],
                               zeros((ppc["branch"].shape[0],
                                      QT - ppc["branch"].shape[1] + 1))]

        ## convert to internal indexing
        ppc = ext2int(ppc)
        baseMVA, bus, gen, branch = \
            ppc["baseMVA"], ppc["bus"], ppc["gen"], ppc["branch"]

        ## get bus index lists of each type of bus
        ref, pv, pq = bustypes(bus, gen)

        ## generator info
        on = find(gen[:, GEN_STATUS] > 0)  ## which generators are on?
        gbus = gen[on, GEN_BUS].astype(int)  ## what buses are they at?

        ##-----  run the power flow  -----
        t0 = time()
        if verbose > 0:
            v = ppver('all')
            stdout.write('PYPOWER Version %s, %s' % (v["Version"], v["Date"]))

        if dc:  # DC formulation
            if verbose:
                stdout.write(' -- DC Power Flow\n')

            ## initial state
            Va0 = bus[:, VA] * (pi / 180)

            ## build B matrices and phase shift injections
            B, Bf, Pbusinj, Pfinj = makeBdc(baseMVA, bus, branch)

            ## compute complex bus power injections [generation - load]
            ## adjusted for phase shifters and real shunts
            Pbus = makeSbus(baseMVA, bus, gen).real - Pbusinj - bus[:, GS] / baseMVA

            ## "run" the power flow
            Va = dcpf(B, Pbus, Va0, ref, pv, pq)

            ## update data matrices with solution
            branch[:, [QF, QT]] = zeros((branch.shape[0], 2))
            branch[:, PF] = (Bf * Va + Pfinj) * baseMVA
            branch[:, PT] = -branch[:, PF]
            bus[:, VM] = ones(bus.shape[0])
            bus[:, VA] = Va * (180 / pi)
            ## update Pg for slack generator (1st gen at ref bus)
            ## (note: other gens at ref bus are accounted for in Pbus)
            ##      Pg = Pinj + Pload + Gs
            ##      newPg = oldPg + newPinj - oldPinj
            refgen = zeros(len(ref), dtype=int)
            for k in range(len(ref)):
                temp = find(gbus == ref[k])
                refgen[k] = on[temp[0]]
            gen[refgen, PG] = gen[refgen, PG] + (B[ref, :] * Va - Pbus[ref]) * baseMVA

            success = 1
        else:  ## AC formulation
            alg = ppopt['PF_ALG']
            if verbose > 0:
                if alg == 1:
                    solver = 'Newton'
                elif alg == 2:
                    solver = 'fast-decoupled, XB'
                elif alg == 3:
                    solver = 'fast-decoupled, BX'
                elif alg == 4:
                    solver = 'Gauss-Seidel'
                else:
                    solver = 'unknown'
                print(' -- AC Power Flow (%s)\n' % solver)

            ## initial state
            # V0    = ones(bus.shape[0])            ## flat start
            '''
            To check and compare this part. 
            '''
            V0 = bus[:, VM] * exp(1j * pi / 180 * bus[:, VA])
            V0[gbus] = gen[on, VG] / abs(V0[gbus]) * V0[gbus]

            if qlim:
                ref0 = ref  ## save index and angle of
                Varef0 = bus[ref0, VA]  ##   original reference bus(es)
                limited = []  ## list of indices of gens @ Q lims
                fixedQg = zeros(gen.shape[0])  ## Qg of gens at Q limits

            Ybus, Yf, Yt = makeYbus(baseMVA, bus, branch)
            repeat = True
            while repeat:
                ## build admittance matrices
                '''
                This is changed
                '''
                # Ybus, Yf, Yt = makeYbus(baseMVA, bus, branch)

                ## compute complex bus power injections [generation - load]
                Sbus = makeSbus(baseMVA, bus, gen)

                ## run the power flow
                alg = ppopt["PF_ALG"]
                if alg == 1:
                    V, success, _ = newtonpf(Ybus, Sbus, V0, ref, pv, pq, ppopt)
                elif alg == 2 or alg == 3:
                    Bp, Bpp = makeB(baseMVA, bus, branch, alg)
                    V, success, _ = fdpf(Ybus, Sbus, V0, Bp, Bpp, ref, pv, pq, ppopt)
                elif alg == 4:
                    V, success, _ = gausspf(Ybus, Sbus, V0, ref, pv, pq, ppopt)
                else:
                    stderr.write('Only Newton''s method, fast-decoupled, and '
                                 'Gauss-Seidel power flow algorithms currently '
                                 'implemented.\n')

                ## update data matrices with solution
                bus, gen, branch = pfsoln(baseMVA, bus, gen, branch, Ybus, Yf, Yt, V, ref, pv, pq)

                if qlim:  ## enforce generator Q limits
                    ## find gens with violated Q constraints
                    gen_status = gen[:, GEN_STATUS] > 0
                    qg_max_lim = gen[:, QG] > gen[:, QMAX]
                    qg_min_lim = gen[:, QG] < gen[:, QMIN]

                    mx = find(gen_status & qg_max_lim)
                    mn = find(gen_status & qg_min_lim)

                    if len(mx) > 0 or len(mn) > 0:  ## we have some Q limit violations
                        infeas = r_[mx, mn]
                        temp1 = find(bus[gbus, BUS_TYPE] == PV)
                        temp2 = find(bus[gbus, BUS_TYPE] == REF)
                        temp3 = find(gen[:, GEN_STATUS] > 0)
                        remaining = list((set(temp1) | set(temp2)) & set(temp3))
                        if len(remaining) == len(infeas) and all(infeas == remaining):
                            print('infeasible problem, all PV buses or REF bus exceeds Q limit. ')
                            success = 0
                            break
                        # No PV generators
                        if len(pv) == 0:
                            if verbose:
                                if len(mx) > 0:
                                    print('Gen', (mx + 1),
                                          ' [only one left] exceeds upper Q limit : INFEASIBLE PROBLEM\n')
                                else:
                                    print('Gen ', mn + 1,
                                          '[only one left] exceeds lower Q limit : INFEASIBLE PROBLEM\n')

                            success = 0
                            break

                        ## one at a time?
                        if qlim == 2:  ## fix largest violation, ignore the rest
                            k = argmax(r_[gen[mx, QG] - gen[mx, QMAX],
                                          gen[mn, QMIN] - gen[mn, QG]])
                            if k > len(mx) - 1:
                                mn = mn[k - len(mx)]
                                mx = []
                            else:
                                mx = mx[k]
                                mn = []

                        if verbose and len(mx) > 0:
                            for i in range(len(mx)):
                                print('Gen ' + str(mx[i] + 1) + ' at upper Q limit, converting to PQ bus\n')

                        if verbose and len(mn) > 0:
                            for i in range(len(mn)):
                                print('Gen ' + str(mn[i] + 1) + ' at lower Q limit, converting to PQ bus\n')

                        ## save corresponding limit values
                        fixedQg[mx] = gen[mx, QMAX]
                        fixedQg[mn] = gen[mn, QMIN]
                        mx = r_[mx, mn].astype(int)

                        ## convert to PQ bus
                        gen[mx, QG] = fixedQg[mx]  ## set Qg to binding
                        gen[mx, GEN_STATUS] = 0
                        for i in range(len(mx)):  ## [one at a time, since they may be at same bus]
                            # gen[mx[i], GEN_STATUS] = 0  ## temporarily turn off gen,
                            bi = gen[mx[i], GEN_BUS].astype(int)  ## adjust load accordingly,
                            bus[bi, [PD, QD]] = (bus[bi, [PD, QD]] - gen[mx[i], [PG, QG]])

                        if len(ref) > 1 and any(bus[gen[mx, GEN_BUS], BUS_TYPE] == REF):
                            raise ValueError('Sorry, PYPOWER cannot enforce Q '
                                             'limits for slack buses in systems '
                                             'with multiple slacks.')
                        if 0 in mx:
                            print('Going to change the reference bus status to PV bus.')

                        bus[gen[mx, GEN_BUS].astype(int), BUS_TYPE] = PQ  ## & set bus type to PQ

                        ## update bus index lists of each type of bus
                        ref_temp = ref
                        ref, pv, pq = bustypes(bus, gen)
                        if verbose and ref != ref_temp:
                            print('Bus %d is new slack bus\n' % ref)

                        limited = r_[limited, mx].astype(int)
                    else:
                        repeat = 0  ## no more generator Q limits violated
                else:
                    repeat = 0  ## don't enforce generator Q limits, once is enough

            if qlim and len(limited) > 0:
                ## restore injections from limited gens [those at Q limits]
                gen[limited, QG] = fixedQg[limited]  ## restore Qg value,
                for i in range(len(limited)):  ## [one at a time, since they may be at same bus]
                    bi = gen[limited[i], GEN_BUS].astype(int)  ## re-adjust load,
                    bus[bi, [PD, QD]] = bus[bi, [PD, QD]] + gen[limited[i], [PG, QG]]
                    gen[limited[i], GEN_STATUS] = 1  ## and turn gen back on

                if ref != ref0:
                    ## adjust voltage angles to make original ref bus correct
                    bus[:, VA] = bus[:, VA] - bus[ref0, VA] + Varef0

        ppc["et"] = time() - t0
        ppc["success"] = success

        ##-----  output results  -----
        ## convert back to original bus numbering & print results
        ppc["bus"], ppc["gen"], ppc["branch"] = bus, gen, branch
        results = int2ext(ppc)

        ## zero out result fields of out-of-service gens & branches
        if len(results["order"]["gen"]["status"]["off"]) > 0:
            results["gen"][ix_(results["order"]["gen"]["status"]["off"], [PG, QG])] = 0

        if len(results["order"]["branch"]["status"]["off"]) > 0:
            results["branch"][ix_(results["order"]["branch"]["status"]["off"], [PF, QF, PT, QT])] = 0

        if fname:
            fd = None
            try:
                fd = open(fname, "a")
            except Exception as detail:
                stderr.write("Error opening %s: %s.\n" % (fname, detail))
            finally:
                if fd is not None:
                    printpf(results, fd, ppopt)
                    fd.close()
        else:
            printpf(results, stdout, ppopt)

        ## save solved case
        if solvedcase:
            savecase(solvedcase, results)

        return results, success
