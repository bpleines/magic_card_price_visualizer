#!/usr/bin/env python
"""
Basic script to create an empty python package containing one module
"""

class MTGCodes:
    """Class to store set codes"""
    def __init__(self):
        self.color_codes = self.get_color_codes()
        self.source_or_target = self.get_set_codes()

    def get_color_codes(self):
        pass

    def get_set_codes(self):
        return ['BRO', 'DMU', 'SNC', 'NEO', 'VOW', 'MID', 'AFR',
                'STX', 'KHM', 'ZNR', 'IKO', 'THB', 'ELD', 'WAR', 'RNA', 'GRN', 'DOM', 'RIX',
                'XLN', 'HOU', 'AKH', 'AER', 'KLD', 'EMN', 'SOI', 'OGW', 'BFZ', 'DTK', 'FRF',
                'KTK', 'JOU', 'BNG', 'THS', 'DGM', 'GTC', 'RTR', 'AVR', 'DKA', 'ISD', 'NPH',
                'MBS', 'SOM', 'ROE', 'WWK', 'ZEN', 'ARB', 'CON', 'ALA', 'EVE', 'SHM', 'MOR',
                'LRW', 'FUT', 'PLC', 'TSP', 'CSP', 'DIS', 'GPT', 'RAV', 'SOK', 'BOK', 'CHK',
                '5DN', 'DST', 'MRD', 'SCG', 'LGN', 'ONS', 'JUD', 'TOR', 'ODY', 'APC', 'PLS',
                'INV', 'PCY', 'NEM', 'MMQ', 'UDS', 'ULG', 'USG', 'EXO', 'STH', 'TMP', 'WTH',
                'VIS', 'MIR', 'ALL', 'HML', 'ICE', 'FEM', 'DRK', 'LEG', 'ATQ', 'ARN']
