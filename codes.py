#!/usr/bin/env python
"""
Simple class to manage codes used by scripts uniformly
"""

class MTGCodes:
    """Class to store set and color codes"""
    def __init__(self):
        self.color_codes = self.get_color_codes()
        self.source_or_target = self.get_set_codes()

    def encode_color(self, color):
        # Handle colorless case
        if len(color) == 0:
            return '#8c8d8b'
        # Handle multicolored case
        elif len(color) >= 2:
            return '#d78f42'
        else:
            color_map = {
                "R": "#ff1a1a",
                "W": "#ffffff",
                "U": "#341aff",
                "B": "#000000",
                "G": "#087500"
            }
            return color_map[color[0]]

    def get_color_codes(self):
        return ['W', 'U', 'B', 'R', 'G']

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
