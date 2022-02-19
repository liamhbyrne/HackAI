
met_codes = {'BKK': ['BKK', 'DMK'], 'BJS': ['PEK', 'PKX', 'NAY'], 'OSA': ['KIX', 'ITM', 'UKB'], 'SPK': ['CTS', 'OKD'], 'SEL': ['ICN', 'GMP'], 'SHA': ['SHA', 'PVG'], 'TYO': ['NRT', 'HND'], 'JKT': ['CGK', 'HLP'], 'MEL': ['MEL', 'AVV', 'MEB'], 'BER': ['BER', 'TXL', 'SXF'], 'BUH': ['OTP', 'BBU'], 'BRU': ['BRU', 'CRL'], 'LON': ['BQH', 'LCY', 'LGW', 'LTN', 'LHR', 'SEN', 'STN'], 'MIL': ['BGY', 'MXP', 'LIN', 'PMF'], 'MOW': ['SVO', 'DME', 'VKO', 'BKA'], 'OSL': ['OSL', 'TRF', 'RYG'], 'PAR': ['CDG', 'ORY', 'LBG'], 'REK': ['KEF', 'RKV'], 'ROM': ['FCO', 'CIA'], 'STO': ['ARN', 'NYO', 'BMA', 'VST', 'GOT'], 'TCI': ['TFN', 'TFS'], 'CHI': ['ORD', 'MDW', 'RFD'], 'QDF': ['DAL', 'DFW'], 'DTT': ['DTW', 'DET', 'YIP'], 'YEA': ['YEG'], 'QHO': ['IAH', 'HOU'], 'LAX': ['LAX', 'ONT', 'SNA', 'BUR'], 'QMI': ['MIA', 'FLL', 'PBI'], 'YMQ': ['YUL', 'YMY'], 'NYC': ['JFK', 'EWR', 'LGA', 'HPN'], 'YTO': ['YYZ', 'YTZ', 'YKF'], 'WAS': ['IAD', 'DCA', 'BWI'], 'BHZ': ['CNF', 'PLU'], 'BUE': ['EZE', 'AEP'], 'RIO': ['GIG', 'SDU'], 'SAO': ['GRU', 'CGH', 'VCP']}

def met_to_airports(met_code):
    return met_codes[met_code]

def airport_to_met(airport_code):
    for met, airports in met_codes.items():
        if airport_code in airports:
            return met
        else:
            return airport_code
