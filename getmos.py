"""
Created on Tue Aug  6 10:50:49 2019

@author: mariofire

Refactor starting Wed Oct 2 19:51:00 2019
@author: ClariNerd617
"""
##############################################################################
# This script takes the input for a MOS station in the United States and grabs
# the data and puts it into a pandas dataframe.
#
# import NAMMOS or GFSMOS
#
# function call:
# df = NAMMOS(stationcode) ex: 'KLWM', 'KBOX' (USE ICAO CODE)
#
#
# This only is for the short term MOS. The values for Q06, P06, P12, Q12, X/N
# are not properly spaced out to match with their appropriate times at this 
# point so adjustments need to be made when using said data. This will be added
# in a future update
##############################################################################

import re
import string

import pandas as pd
import requests
from urllib3 import exceptions, disable_warnings

disable_warnings(exceptions.InsecureRequestWarning)


def switch_month(month: string):
    months = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
        }
    return 1 if month == "DEC" else months.get(month) + 1


def get_mos(model: string, **kwargs):
    try:
        if model.lower() is "nam":
            r = requests.get(url="https://www.nws.noaa.gov/mdl/forecast/text/nammet.txt", verify=False)
            r.raise_for_status()
        elif model.lower() is "gfs":
            r = requests.get(url="https://www.nws.noaa.gov/mdl/forecast/test/avnmav.txt", verify=False)
            r.raise_for_status()
    except requests.HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)
    return r if kwargs.get("test") else r.text.split("/n")


def mos_data_transform(station: string, model: string, **kwargs):
    data = get_mos(model=model)
    x = re.sub("\s+", ",", data.get(0)).split(',')
    ind = x.index(station)
    new_list = x[ind:]
    ind_2 = new_list.index("OBV") + 22
    datalist = new_list[0:ind_2]
    try:
        ind_xn = datalist.index('X/N')
    except ValueError:
        ind_xn = datalist.index('N/X')
    ind_hr = datalist.index('HR')
    ind_tmp = datalist.index('TMP')
    ind_dpt = datalist.index('DPT')
    ind_cld = datalist.index('CLD')
    ind_wdr = datalist.index('WDR')
    ind_wsp = datalist.index('WSP')
    ind_p06 = datalist.index('P06')
    ind_p12 = datalist.index('P12')
    ind_q06 = datalist.index('Q06')
    ind_q12 = datalist.index('Q12')
    ind_t06 = datalist.index('T06')
    ind_t12 = datalist.index('T12')
    ind_cig = datalist.index('CIG')
    ind_vis = datalist.index('VIS')
    ind_obv = datalist.index('OBV')
    ind_dt = datalist.index('DT')
    hour = datalist.get[ind_hr + 1]
    if hour == 18:
        month = datalist[ind_dt + 4][1:]
        last_day = int(datalist[ind_dt + 5])
    else:
        month = datalist[ind_dt + 3][1:]
        last_day = int(datalist[ind_dt + 6])
    if last_day + 1 is 31:
        [month, last_day] = [switch_month(month), "01"]
    elif last_day + 1 is 32:
        [month, last_day] = [switch_month(month), "01"]
    elif last_day + 1 in [29, 30]:
        [month, last_day] = [switch_month(month), "01"]
    else:
        [month, last_day] = [month, str(last_day + 1)]
    # TODO: Refactor the rest of the script below
    mos = None
    mos_df = None
    return mos if kwargs.get("api") else mos_df


def NAMMOS(station):
    # Open the data file
    # response = requests.get('https://www.nws.noaa.gov/mdl/forecast/text/nammet.txt')
    # Put data into list
    # data = response.text
    # data = data.split("/n")

    # Remove all white spaces and replace with commas then split by comma
    # x = re.sub("\s+", ",", data[0]).split(',')

    # Get the index of the place that we want
    # string = station
    # ind = x.index(string)

    # Make new list starting from our list
    # new_string = x[ind:]

    # Get index of 'OBV' string and add 21 to get to last value
    # ind2 = new_string.index('OBV')
    # ind2 = ind2 + 22

    # Put data into new list
    # datalist = new_string[0:ind2]

    # Get index of each of the main values to make dictionary
    # ind_hr = datalist.index('HR')
    # try:
    #     ind_xn = datalist.index('X/N')
    # except:
    #     ind_xn = datalist.index('N/X')
    # ind_tmp = datalist.index('TMP')
    # ind_dpt = datalist.index('DPT')
    # ind_cld = datalist.index('CLD')
    # ind_wdr = datalist.index('WDR')
    # ind_wsp = datalist.index('WSP')
    # ind_p06 = datalist.index('P06')
    # ind_p12 = datalist.index('P12')
    # ind_q06 = datalist.index('Q06')
    # ind_q12 = datalist.index('Q12')
    # ind_t06 = datalist.index('T06')
    # ind_t12 = datalist.index('T12')
    # ind_cig = datalist.index('CIG')
    # ind_vis = datalist.index('VIS')
    # ind_obv = datalist.index('OBV')
    # ind_dt = datalist.index('DT')

    # Get the first hour and then put the dates for each hour in.
    # hour = int(datalist[ind_hr + 1])

    # Now check to make sure the last date and month are correct for longer times



    if hour == 18:
        days = [datalist[ind_dt + 2], datalist[ind_dt + 2], datalist[ind_dt + 3] + datalist[ind_dt + 4],
                datalist[ind_dt + 3] + datalist[ind_dt + 4], datalist[ind_dt + 3] + datalist[ind_dt + 4],
                datalist[ind_dt + 3] + datalist[ind_dt + 4], datalist[ind_dt + 3] + datalist[ind_dt + 4],
                datalist[ind_dt + 3] + datalist[ind_dt + 4], datalist[ind_dt + 3] + datalist[ind_dt + 4],
                datalist[ind_dt + 3] + datalist[ind_dt + 4], datalist[ind_dt + 5] + datalist[ind_dt + 6],
                datalist[ind_dt + 5] + datalist[ind_dt + 6], datalist[ind_dt + 5] + datalist[ind_dt + 6],
                datalist[ind_dt + 5] + datalist[ind_dt + 6], datalist[ind_dt + 5] + datalist[ind_dt + 6],
                datalist[ind_dt + 5] + datalist[ind_dt + 6], datalist[ind_dt + 5] + datalist[ind_dt + 6],
                datalist[ind_dt + 5] + datalist[ind_dt + 6], last_day + '/' + month, last_day + '/' + month,
                last_day + '/' + month]
    elif hour == 12:
        days = [datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                last_day + '/' + month, last_day + '/' + month, last_day + '/' + month]
    elif hour == 6:
        days = [datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], last_day + '/' + month, last_day + '/' + month]
    else:
        days = [datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 2] + datalist[ind_dt + 3], datalist[ind_dt + 2] + datalist[ind_dt + 3],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 4] + datalist[ind_dt + 5], datalist[ind_dt + 4] + datalist[ind_dt + 5],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                datalist[ind_dt + 6] + datalist[ind_dt + 1], datalist[ind_dt + 6] + datalist[ind_dt + 1],
                last_day + '/' + month]

    # Put everything into a dictionary
    dictionary = {
        'HR': datalist[ind_hr + 1:ind_xn],
        'X/N': datalist[ind_xn + 1:ind_tmp],
        'TMP': datalist[ind_tmp + 1:ind_dpt],
        'DPT': datalist[ind_dpt + 1:ind_cld],
        'CLD': datalist[ind_cld + 1:ind_wdr],
        'WDR': datalist[ind_wdr + 1:ind_wsp],
        'WSP': datalist[ind_wsp + 1:ind_p06],
        'P06': datalist[ind_p06 + 1:ind_p12],
        'P12': datalist[ind_p12 + 1:ind_q06],
        'Q06': datalist[ind_q06 + 1:ind_q12],
        'Q12': datalist[ind_q12 + 1:ind_t06],
        'T06': datalist[ind_t06 + 1:ind_t12],
        'T12': datalist[ind_t12 + 1:ind_cig],
        'CIG': datalist[ind_cig + 1:ind_vis],
        'VIS': datalist[ind_vis + 1:ind_obv],
        'OBV': datalist[ind_obv + 1:],
    }

    # Make a pandas dataframe from the dictionary and append the
    df = pd.DataFrame.from_dict(dictionary, orient='index')
    temp = df[0]['X/N']
    temp2 = df[1]['X/N']
    temp3 = df[2]['X/N']
    temp4 = df[3]['X/N']
    temp5 = df[4]['X/N']
    df[6]['X/N'] = temp
    df[10]['X/N'] = temp2
    df[14]['X/N'] = temp3
    df[18]['X/N'] = temp4
    df[20]['X/N'] = temp5
    df[0]['X/N'] = None
    df[1]['X/N'] = None
    df[2]['X/N'] = None
    df[3]['X/N'] = None
    df[4]['X/N'] = None

    temp = df[0]['P06']
    temp2 = df[1]['P06']
    temp3 = df[2]['P06']
    temp4 = df[3]['P06']
    temp5 = df[4]['P06']
    temp6 = df[5]['P06']
    temp7 = df[6]['P06']
    temp8 = df[7]['P06']
    temp9 = df[8]['P06']
    temp10 = df[9]['P06']
    temp11 = df[10]['P06']
    df[2]['P06'] = temp
    df[4]['P06'] = temp2
    df[6]['P06'] = temp3
    df[8]['P06'] = temp4
    df[10]['P06'] = temp5
    df[12]['P06'] = temp6
    df[14]['P06'] = temp7
    df[16]['P06'] = temp8
    df[18]['P06'] = temp9
    df[19]['P06'] = temp10
    df[20]['P06'] = temp11
    df[0]['P06'] = None
    df[1]['P06'] = None
    df[3]['P06'] = None
    df[5]['P06'] = None
    df[7]['P06'] = None
    df[9]['P06'] = None
    df[11]['P06'] = None

    temp = df[0]['Q06']
    temp2 = df[1]['Q06']
    temp3 = df[2]['Q06']
    temp4 = df[3]['Q06']
    temp5 = df[4]['Q06']
    temp6 = df[5]['Q06']
    temp7 = df[6]['Q06']
    temp8 = df[7]['Q06']
    temp9 = df[8]['Q06']
    temp10 = df[9]['Q06']
    temp11 = df[10]['Q06']
    df[2]['Q06'] = temp
    df[4]['Q06'] = temp2
    df[6]['Q06'] = temp3
    df[8]['Q06'] = temp4
    df[10]['Q06'] = temp5
    df[12]['Q06'] = temp6
    df[14]['Q06'] = temp7
    df[16]['Q06'] = temp8
    df[18]['Q06'] = temp9
    df[19]['Q06'] = temp10
    df[20]['Q06'] = temp11
    df[0]['Q06'] = None
    df[1]['Q06'] = None
    df[3]['Q06'] = None
    df[5]['Q06'] = None
    df[7]['Q06'] = None
    df[9]['Q06'] = None
    df[11]['Q06'] = None

    temp = df[0]['P12']
    temp2 = df[1]['P12']
    temp3 = df[2]['P12']
    temp4 = df[3]['P12']
    temp5 = df[4]['P12']
    df[6]['P12'] = temp
    df[10]['P12'] = temp2
    df[14]['P12'] = temp3
    df[18]['P12'] = temp4
    df[20]['P12'] = temp5
    df[0]['P12'] = None
    df[1]['P12'] = None
    df[2]['P12'] = None
    df[3]['P12'] = None
    df[4]['P12'] = None

    temp = df[0]['Q12']
    temp2 = df[1]['Q12']
    temp3 = df[2]['Q12']
    temp4 = df[3]['Q12']
    temp5 = df[4]['Q12']
    df[6]['Q12'] = temp
    df[10]['Q12'] = temp2
    df[14]['Q12'] = temp3
    df[18]['Q12'] = temp4
    df[20]['Q12'] = temp5
    df[0]['Q12'] = None
    df[1]['Q12'] = None
    df[2]['Q12'] = None
    df[3]['Q12'] = None
    df[4]['Q12'] = None

    df.columns = days

    # Swap the order of the rows to better match MOS output
    df = df.reindex(['HR', 'X/N', 'TMP', 'DPT', 'CLD', 'WDR', 'WSP', 'P06', 'P12', 'Q06', 'Q12', 'CIG', 'VIS', 'OBV'])
    return df


def GFSMOS(station):
    # Open the data file
    response = requests.get('https://www.nws.noaa.gov/mdl/forecast/text/avnmav.txt')

    # Put data into list
    data = response.text
    data = data.split("/n")

    # Remove all white spaces and replace with commas then split by comma
    x = re.sub("\s+", ",", data[0]).split(',')

    # Get the index of the place that we want
    string = station
    ind = x.index(string)

    # Make new list starting from our list
    newstring = x[ind:]

    # Get index of 'OBV' string and add 21 to get to last value
    ind2 = newstring.index('OBV')
    ind2 = ind2 + 22

    # Put data into new list
    datalist = newstring[0:ind2]

    # Get index of each of the main values to make dictionary
    indhr = datalist.index('HR')
    try:
        indxn = datalist.index('X/N')
    except:
        indxn = datalist.index('N/X')
    indtmp = datalist.index('TMP')
    inddpt = datalist.index('DPT')
    indcld = datalist.index('CLD')
    indwdr = datalist.index('WDR')
    indwsp = datalist.index('WSP')
    indp06 = datalist.index('P06')
    indp12 = datalist.index('P12')
    indq06 = datalist.index('Q06')
    indq12 = datalist.index('Q12')
    indt06 = datalist.index('T06')
    indt12 = datalist.index('T12')
    indcig = datalist.index('CIG')
    indvis = datalist.index('VIS')
    indobv = datalist.index('OBV')
    inddt = datalist.index('DT')

    # Get the first hour and then put the dates for each hour in. We will be putting any dates beyond day 3 under the header for day 3
    hour = int(datalist[indhr + 1])

    # Now check to make sure the last date and month are correct for longer times
    if (hour == 18):
        month = datalist[inddt + 4]
        month = month[1:]
        lastday = datalist[inddt + 5]
        lastday = int(lastday)
    else:
        month = datalist[inddt + 3]
        month = month[1:]
        lastday = datalist[inddt + 6]
        lastday = int(lastday)
    if (month == 'JAN' and (lastday + 1) == 32):
        month = 'FEB'
        lastday = '01'
    elif (month == 'FEB' and (lastday + 1) == 29):
        month = 'MAR'
        lastday = '01'
    elif (month == 'MAR' and (lastday + 1) == 32):
        month = 'APR'
        lastday = '01'
    elif (month == 'APR' and (lastday + 1) == 31):
        month = 'MAY'
        lastday = '01'
    elif (month == 'MAY' and (lastday + 1) == 32):
        month = 'JUN'
        lastday = '01'
    elif (month == 'JUN' and (lastday + 1) == 31):
        month = 'JUL'
        lastday = '01'
    elif (month == 'JUL' and (lastday + 1) == 32):
        month = 'AUG'
        lastday = '01'
    elif (month == 'AUG' and (lastday + 1) == 32):
        month = 'SEP'
        lastday = '01'
    elif (month == 'SEP' and (lastday + 1) == 31):
        month = 'OCT'
        lastday = '01'
    elif (month == 'OCT' and (lastday + 1) == 32):
        month = 'NOV'
        lastday = '01'
    elif (month == 'NOV' and (lastday + 1) == 31):
        month = 'DEC'
        lastday = '01'
    elif (month == 'DEC' and (lastday + 1) == 32):
        month = 'JAN'
        lastday = '01'
    else:
        month = month
        lastday = str(lastday + 1)

    if (hour == 18):
        days = [datalist[inddt + 2], datalist[inddt + 2], datalist[inddt + 3] + datalist[inddt + 4],
                datalist[inddt + 3] + datalist[inddt + 4], datalist[inddt + 3] + datalist[inddt + 4],
                datalist[inddt + 3] + datalist[inddt + 4], datalist[inddt + 3] + datalist[inddt + 4],
                datalist[inddt + 3] + datalist[inddt + 4], datalist[inddt + 3] + datalist[inddt + 4],
                datalist[inddt + 3] + datalist[inddt + 4], datalist[inddt + 5] + datalist[inddt + 6],
                datalist[inddt + 5] + datalist[inddt + 6], datalist[inddt + 5] + datalist[inddt + 6],
                datalist[inddt + 5] + datalist[inddt + 6], datalist[inddt + 5] + datalist[inddt + 6],
                datalist[inddt + 5] + datalist[inddt + 6], datalist[inddt + 5] + datalist[inddt + 6],
                datalist[inddt + 5] + datalist[inddt + 6], lastday + '/' + month, lastday + '/' + month,
                lastday + '/' + month]
    elif (hour == 12):
        days = [datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                lastday + '/' + month, lastday + '/' + month, lastday + '/' + month]
    elif (hour == 6):
        days = [datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                datalist[inddt + 6] + datalist[inddt + 1], lastday + '/' + month, lastday + '/' + month]
    else:
        days = [datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 2] + datalist[inddt + 3], datalist[inddt + 2] + datalist[inddt + 3],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 4] + datalist[inddt + 5], datalist[inddt + 4] + datalist[inddt + 5],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                datalist[inddt + 6] + datalist[inddt + 1], datalist[inddt + 6] + datalist[inddt + 1],
                lastday + '/' + month]

    # Put everything into a     return dfdictionary
    dictionary = {
        'HR': datalist[indhr + 1:indxn],
        'X/N': datalist[indxn + 1:indtmp],
        'TMP': datalist[indtmp + 1:inddpt],
        'DPT': datalist[inddpt + 1:indcld],
        'CLD': datalist[indcld + 1:indwdr],
        'WDR': datalist[indwdr + 1:indwsp],
        'WSP': datalist[indwsp + 1:indp06],
        'P06': datalist[indp06 + 1:indp12],
        'P12': datalist[indp12 + 1:indq06],
        'Q06': datalist[indq06 + 1:indq12],
        'Q12': datalist[indq12 + 1:indt06],
        'T06': datalist[indt06 + 1:indt12],
        'T12': datalist[indt12 + 1:indcig],
        'CIG': datalist[indcig + 1:indvis],
        'VIS': datalist[indvis + 1:indobv],
        'OBV': datalist[indobv + 1:],
    }

    # Make a pandas dataframe from the dictionary and append the
    df = pd.DataFrame.from_dict(dictionary, orient='index')
    temp = df[0]['X/N']
    temp2 = df[1]['X/N']
    temp3 = df[2]['X/N']
    temp4 = df[3]['X/N']
    temp5 = df[4]['X/N']
    df[6]['X/N'] = temp
    df[10]['X/N'] = temp2
    df[14]['X/N'] = temp3
    df[18]['X/N'] = temp4
    df[20]['X/N'] = temp5
    df[0]['X/N'] = None
    df[1]['X/N'] = None
    df[2]['X/N'] = None
    df[3]['X/N'] = None
    df[4]['X/N'] = None

    temp = df[0]['P06']
    temp2 = df[1]['P06']
    temp3 = df[2]['P06']
    temp4 = df[3]['P06']
    temp5 = df[4]['P06']
    temp6 = df[5]['P06']
    temp7 = df[6]['P06']
    temp8 = df[7]['P06']
    temp9 = df[8]['P06']
    temp10 = df[9]['P06']
    temp11 = df[10]['P06']
    df[2]['P06'] = temp
    df[4]['P06'] = temp2
    df[6]['P06'] = temp3
    df[8]['P06'] = temp4
    df[10]['P06'] = temp5
    df[12]['P06'] = temp6
    df[14]['P06'] = temp7
    df[16]['P06'] = temp8
    df[18]['P06'] = temp9
    df[19]['P06'] = temp10
    df[20]['P06'] = temp11
    df[0]['P06'] = None
    df[1]['P06'] = None
    df[3]['P06'] = None
    df[5]['P06'] = None
    df[7]['P06'] = None
    df[9]['P06'] = None
    df[11]['P06'] = None

    temp = df[0]['Q06']
    temp2 = df[1]['Q06']
    temp3 = df[2]['Q06']
    temp4 = df[3]['Q06']
    temp5 = df[4]['Q06']
    temp6 = df[5]['Q06']
    temp7 = df[6]['Q06']
    temp8 = df[7]['Q06']
    temp9 = df[8]['Q06']
    temp10 = df[9]['Q06']
    temp11 = df[10]['Q06']
    df[2]['Q06'] = temp
    df[4]['Q06'] = temp2
    df[6]['Q06'] = temp3
    df[8]['Q06'] = temp4
    df[10]['Q06'] = temp5
    df[12]['Q06'] = temp6
    df[14]['Q06'] = temp7
    df[16]['Q06'] = temp8
    df[18]['Q06'] = temp9
    df[19]['Q06'] = temp10
    df[20]['Q06'] = temp11
    df[0]['Q06'] = None
    df[1]['Q06'] = None
    df[3]['Q06'] = None
    df[5]['Q06'] = None
    df[7]['Q06'] = None
    df[9]['Q06'] = None
    df[11]['Q06'] = None

    temp = df[0]['P12']
    temp2 = df[1]['P12']
    temp3 = df[2]['P12']
    temp4 = df[3]['P12']
    temp5 = df[4]['P12']
    df[6]['P12'] = temp
    df[10]['P12'] = temp2
    df[14]['P12'] = temp3
    df[18]['P12'] = temp4
    df[20]['P12'] = temp5
    df[0]['P12'] = None
    df[1]['P12'] = None
    df[2]['P12'] = None
    df[3]['P12'] = None
    df[4]['P12'] = None

    temp = df[0]['Q12']
    temp2 = df[1]['Q12']
    temp3 = df[2]['Q12']
    temp4 = df[3]['Q12']
    temp5 = df[4]['Q12']
    df[6]['Q12'] = temp
    df[10]['Q12'] = temp2
    df[14]['Q12'] = temp3
    df[18]['Q12'] = temp4
    df[20]['Q12'] = temp5
    df[0]['Q12'] = None
    df[1]['Q12'] = None
    df[2]['Q12'] = None
    df[3]['Q12'] = None
    df[4]['Q12'] = None

    df.columns = days

    # Swap the order of the rows to better match MOS output
    df = df.reindex(['HR', 'X/N', 'TMP', 'DPT', 'CLD', 'WDR', 'WSP', 'P06', 'P12', 'Q06', 'Q12', 'CIG', 'VIS', 'OBV'])
    return df
