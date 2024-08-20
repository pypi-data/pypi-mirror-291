import re

import FM15_transform.metarDecoder.metarDecoders as MD
import FM15_transform.metarDecoder.xmlUtilities as deu
import FM15_transform.bufr2geojson as generic_bufr2geojson

from pywis_xform.opensearch import OpenSearchClient as OSClient

from copy import deepcopy
from typing import Iterator
import csv
from io import StringIO
import logging
import json
import math
import os
from csv2bufr import BUFRMessage
import requests

LOGGER = logging.getLogger(__name__)

FAILED = 0
PASSED = 1

#   Initialize FM15 Metar decoders
fmh = MD.FMH1()
annex3 = MD.Annex3()

re_ID = re.compile(r'(METAR|SPECI)\s+(COR\s+)?(?P<id>\w{4})')

_keys = ['icao_location_identifier', 'product_status', 'station_type',
         'year', 'month', 'day', 'hour', 'minute',
         'wind_direction', 'variable_extreme_ccw', 'variable_extreme_cw',
         'wind_speed_qualifier', 'wind_speed_kn', 'wind_speed_m/s',
         'wind_gust_qualifier', 'gust_speed_kn', 'gust_speed_m/s',
         'air_temp', 'dew_point_temp', 'altimeter', 'general_weather_indicator', 'prevailing_visibility']

metar_template = dict.fromkeys(_keys)

THISDIR = os.path.dirname(os.path.realpath(__file__))
MAPPINGS = f"{THISDIR}{os.sep}resources{os.sep}307051_mapping.json"

# Load template mappings file, this will be updated for each message.
with open(MAPPINGS) as fh:
    _mapping = json.load(fh)

#   Function for updating the bufr template mapping
def update_data_mapping(mapping: list, update: dict):
    match = False
    for idx in range(len(mapping)):
        if mapping[idx]['eccodes_key'] == update['eccodes_key']:
            match = True
            break
    if match:
        mapping[idx] = update
    else:
        mapping.append(update)
    return mapping

#   Function for extracting individual FM15 Metar 
def extract_metar(data: str) -> list:
    format_exp = re.compile(r'MTR([A-Z0-9]{3})')
    if format_exp.match(data):
        data = f"{data}="
        
    if not data.__contains__("="):
        LOGGER.error((
            "Delimiters (=) are not present in the string"))
        LOGGER.debug(data)
        raise ValueError
    
    start_position = data.find("METAR")
    if start_position == -1:
        start_position = data.find("SPECI")
        if start_position == -1:
            raise ValueError("Invalid METAR message. 'METAR' or 'SPECI' could not be found.")
        
    data = re.split('=', data[start_position:])

    for i in range(len(data)):
        data[i] = data[i]+"="

    return data[:len(data)-1]

def parse_metar(message: str, year: int, month: int) -> dict:
    message = message.strip()
    LOGGER.debug(f"Parsing message: {message}")
    icaoID = re_ID.match(message).group('id')
    if deu.isUSIdentifier(icaoID):
        decoded = fmh(message)
    else:
        decoded = annex3(message)

    for key in decoded:
        LOGGER.debug(key, ': ', decoded[key])

    output = deepcopy(metar_template)

    #   ecCodes 001063: ICAO Location Indicator
    if 'ident' in decoded:
        icao = decoded['ident']['str']
        output['icao_location_identifier'] = icao

    #   ecCodes 008079: Aviation Product Status
    #   first get report type which will either be normal (METAR) or special (SPECI)
    report_type = message[0:5]
    #   codes for normal/routine reports
    if report_type == 'METAR':
        #   correction to previously reported product, coded as 1
        if 'cor' in decoded:
            output['product_status'] = 1
        #   normal issue coded as 0
        else:
            output['product_status'] = 0
    #   codes for special reports
    elif report_type == 'SPECI':
        #   corrected special report
        if 'cor' in decoded:
            output['product_status'] = 7
        #   original special report
        else:
            output['product_status'] = 6
    #   TODO: figure out NIL coding

    #   ecCodes 002001: Station Type
    #   metar station type is binary, either AUTOMATIC (0) or MANNED (1)
    if 'auto' in decoded:
        output['station_type'] = 0
    else:
        output['station_type'] = 1

    #   ecCodes 301011: year, month, day / 301012: hour, minute
    output['year'] = year
    output['month'] = month
    if 'itime' in decoded:
        output['day'] = decoded['itime']['tuple'].tm_mday
        output['hour'] = decoded['itime']['tuple'].tm_hour
        output['minute'] = decoded['itime']['tuple'].tm_min

    if 'wind' in decoded:
        #   ecCodes 011001: wind direction
        #   check for missing value
        if decoded['wind']['dd'] != '///':
            output['wind_direction'] = decoded['wind']['dd']

        #   ecCodes 011016: Extreme counterclockwise wind direction of a variable wind
        if 'ccw' in decoded['wind']:
            output['variable_extreme_ccw'] = int(decoded['wind']['ccw'])

        #   ecCodes 011017: Extreme clockwise wind direction of a variable wind
        if 'cw' in decoded['wind']:
            output['variable_extreme_cw'] = int(decoded['wind']['cw'])

        #   ecCodes 008054: qualifier for wind speed
        #   wind speed is greater than what is reported
        if 'ffplus' in decoded['wind']:
            output['wind_speed_qualifier'] = 1
        #   wind speed is as reported
        else:
            output['wind_speed_qualifier'] = 0

        wind_uom = decoded['wind']['uom'] 
        wind_speed = decoded['wind']['ff']

        #   check for missing value
        if wind_speed != '//':
            #   ecCodes 011084: wind speed in knots
            if wind_uom == '[kn_i]':
                output['wind_speed_kn'] = int(wind_speed)

            #   ecCodes 011002: wind speed in m/s
            elif wind_uom == 'm/s':
                output['wind_speed_m/s'] = int(wind_speed)

        #   ecCodes 008054: qualifier for wind gusts
        #   wind gusts are greater than what is reported
        if 'ggplus' in decoded['wind']:
            output['wind_gust_qualifier'] = 1
        #   wind gusts are as reported
        else:
            output['wind_gust_qualifier'] = 0

        if 'gg' in decoded['wind']:
            gust_speed = decoded['wind']['gg']
            #   ecCodes 011086: Maximum wind gust speed reported in knots
            if wind_uom == '[kn_i]':
                output['gust_speed_kn'] = int(gust_speed)
            #   ecCodes 011041: Maximum wind gust speed reported in m/s
            elif wind_uom == 'm/s':
                output['gust_speed_m/s'] = int(gust_speed)

    if 'temps' in decoded:
        if 'air' in decoded['temps']:
            #   check for missing value
            if decoded['temps']['air'] != '//':
                #   ecCodes 012023: Air Temperature in Celsius
                output['air_temp'] = float(decoded['temps']['air'])
        if 'dewpoint' in decoded['temps']:
            #   check for missing value
            if decoded['temps']['dewpoint'] != '//':
                #   ecCodes 012024: Dewpoint temperature in Celsius
                output['dew_point_temp'] = float(decoded['temps']['dewpoint'])

    #   ecCodes 010052: Altimeter setting qnh in Pascals
    if 'altimeter' in decoded:
        altimeter = float(decoded['altimeter']['value'])
        alt_uom = decoded['altimeter']['uom']
        if alt_uom == 'hPa':
            output['altimeter'] = altimeter*100
        elif alt_uom == "[in_i'Hg]":
            # if metar records altimeter in inches of Mercury. need to convert to Pascals for bufr
            output['altimeter'] = round(altimeter*3386.39, 2)

    #   ecCodes 020009: General weather indicator of TAF or METAR
    if 'cavok' in decoded:
        output['general_weather_indicator'] = 2

    #   ecCodes 020060: Prevailing horizontal visibility in meters
    if 'vsby' in decoded:
        #   check for missing value
        if decoded['vsby']['value'] != '////':
            # if recorded in number of statute miles, need to convert value to meters to be bufr compatible
            if decoded['vsby']['uom'] == '[mi_i]':
                vis_miles = float(decoded['vsby']['value'])
                output['prevailing_visibility'] = math.floor(vis_miles * 1609.34)
            elif decoded['vsby']['uom'] == 'm':
                output['prevailing_visibility'] = int(decoded['vsby']['value'])
            #   cap the value at the maximum allowed value (10,230 m) if recorded value is above what ecCodes allows
            output['prevailing_visibility'] = min(10230, output['prevailing_visibility'])

    #   ecCodes 020059: Minimum horizontal visibility in meters
    if 'vvis' in decoded:
        low_vis = float(decoded['vvis']['lo'])
        high_vis = float(decoded['vvis']['hi'])
        #   metar reports variable visibility in statute miles. need to convert to bufr
        output['low_vis'] = math.floor(low_vis * 1609.34)
        output['high_vis'] = math.floor(high_vis * 1609.34)

    num_rvr = 0
    if 'rvr' in decoded:
        num_rvr = len(decoded['rvr']['str'])
        for i in range(num_rvr):
            #   ecCodes 001064: Runway designator
            output[f'rvr_{i+1}_designator'] = decoded['rvr']['rwy'][i]
            qualifier = decoded['rvr']['oper'][i]
            #   ecCodes 008014: Qualifier for runway visual range
            #   encoding: 0 - NORMAL, 1 - ABOVE THE UPPER LIMIT, 2 - BELOW THE LOWER LIMIT
            if qualifier == 'ABOVE':
                output[f'rvr_{i+1}_qualifier'] = 1
            elif qualifier == 'BELOW':
                output[f'rvr_{i+1}_qualifier'] = 2
            elif qualifier == None:
                output[f'rvr_{i+1}_qualifier'] = 0

            #   ecCodes 020061: Runway Visual Range recorded in meters
            mean_vis = float(decoded['rvr']['mean'][i])
            # if distance is reported in meters, we can copy directly to bufr
            if decoded['rvr']['uom'][i] == 'm':
                output[f'rvr_{i+1}_mean'] = int(mean_vis)
            # if distance is reported in ft, have to convert to meters for bufr
            elif decoded['rvr']['uom'][i] == '[ft_i]':
                output[f'rvr_{i+1}_mean'] = math.floor(mean_vis*0.3048)

            #   ecCodes 020018: Tendency of runway visual range
            #   encoding: INCREASING -> 0, DECREASING -> 1, NO DISTINCT CHANGE -> 2
            tendency = decoded['rvr']['tend'][i]
            if tendency == 'UPWARD':
                output[f'rvr_{i+1}_tend'] = 0
            elif tendency == 'DOWNWARD':
                output[f'rvr_{i+1}_tend'] = 1
            elif tendency == 'MISSING_VALUE':
                output[f'rvr_{i+1}_tend'] = 3

    num_vrbrvr = 0
    if 'vrbrvr' in decoded:
        num_vrbrvr = len(decoded['vrbrvr']['str'])
        for i in range(num_vrbrvr):
            #   ecCodes 001064: Runway designator
            output[f'vrbrvr_{i+1}_designator'] = decoded['vrbrvr']['rwy'][i]

            #   ecCodes 008014: Qualifier for runway visual range
            #   encoding: 0 - NORMAL, 1 - ABOVE THE UPPER LIMIT, 2 - BELOW THE LOWER LIMIT
            qualifier = decoded['vrbrvr']['oper'][i]
            if qualifier == 'P':
                output[f'vrbrvr_{i+1}_qualifier'] = 1
            elif qualifier == 'M':
                output[f'vrbrvr_{i+1}_qualifier'] = 2
            elif qualifier == None:
                output[f'vrbrvr_{i+1}_qualifier'] = 0

            low_vis = float(decoded['vrbrvr']['lo'][i])
            high_vis = float(decoded['vrbrvr']['hi'][i])
            
            #   ecCodes 020061: Runway Visual Range recorded in meters
            #   if distance is reported in meters, we can copy directly to bufr
            if decoded['vrbrvr']['uom'][i] == 'm':
                output[f'vrbrvr_{i+1}_low'] = int(low_vis)
                output[f'vrbrvr_{i+1}_high'] = int(high_vis)

            #   if distance is reported in ft, have to convert to meters for bufr
            elif decoded['vrbrvr']['uom'][i] == '[ft_i]':
                output[f'vrbrvr_{i+1}_low'] = math.floor(low_vis*0.3048)
                output[f'vrbrvr_{i+1}_high'] = math.floor(high_vis*0.3048)

    #   ecCodes 020019: Significant weather as either precipitation events or observed phenomena
    num_pcp = 0
    if 'pcp' in decoded:
        num_pcp = len(decoded['pcp']['str'])
        for i in range(num_pcp):
            output[f'precip_{i+1}'] = decoded['pcp']['str'][0]
    num_obv = 0
    if 'obv' in decoded:
        num_obv = len(decoded['obv']['str'])
        for i in range(num_obv):
            output[f'observed_phenom_{i+1}'] = decoded['obv']['str'][i]

    num_sky = 0
    if 'sky' in decoded:
        num_sky = len(decoded['sky']['str'])
        for i in range(num_sky):
            #   special cases where sky cover is recorded as SKC or CLR both with their own meanings. Set flags
            #   for these cases in the output and return zero or one sky groups
            if decoded['sky']['str'][0] == 'SKC':
                output['SKC'] = True
                num_sky = 0
                break
            if decoded['sky']['str'][0] == 'CLR':
                output['CLR'] = True
                num_sky = 1
                break

            #   ecCodes 020091: Vercial visibility reported in ft
            if decoded['sky']['str'][0][:2] == 'VV':
                #   METAR reports vertical visibility in 100s of ft, multiply by 100 to get correct bufr value
                output['vertical_visibility'] = int(decoded['sky']['str'][0][2:]) * 100
                #   also need to reset number of sky groups to zero
                num_sky = 0
                break

            #   ecCodes 020011: Cloud Amount
            #   FEW -> 13, SCT -> 11, BKN -> 12, OVC -> 8*, UNDISCERNABLE OR OBSERVATION NOT MADE -> 15
            #   *FMH1 describes overcast clouds as having full 8 okta cover
            cloud_amount = decoded['sky']['str'][i][:3]
            if cloud_amount == 'FEW':
                output[f'cloud_amount_{i+1}'] = 13
            elif cloud_amount == 'SCT':
                output[f'cloud_amount_{i+1}'] = 11
            elif cloud_amount == 'BKN':
                output[f'cloud_amount_{i+1}'] = 12
            elif cloud_amount == 'OVC':
                output[f'cloud_amount_{i+1}'] = 8
            elif cloud_amount == '///':
                output[f'cloud_amount_{i+1}'] = 15

            #   ecCodes 020092: Height of base cloud reported in ft
            #   check for missing value
            if decoded['sky']['str'][i][3:6] != '///':
                output[f'cloud_height_{i+1}'] = int(decoded['sky']['str'][i][3:6]) * 100

            #   ecCodes 020012: Cloud Type
            #   capture significant convective cloud groups, either cumulonimbus (CB) or towering cumulus (TCU) as reported by METAR
            #   CB -> 8, TCU -> 32
            if len(decoded['sky']['str'][i]) > 6:
                cloud_type = decoded['sky']['str'][i][6:]
                if cloud_type == 'CB':
                    output['sig_convec_'+str(i+1)] = 8
                elif cloud_type == 'TCU':
                    output['sig_convec_'+str(i+1)] = 32


    return output, num_rvr, num_vrbrvr, num_pcp, num_obv, num_sky

def transform(client: OSClient, data: str, year: int, month: int) -> Iterator[dict]:
    # ===================
    # First parse metadata file
    # ===================
    # if isinstance(metadata, str):
    #     fh = StringIO(metadata)
    #     reader = csv.reader(fh, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    #     col_names = next(reader)
    #     metadata_dict = {}
    #     for row in reader:
    #         if len(row) == 0:
    #             continue
    #         single_row = dict(zip(col_names, row))
    #         try:
    #             station_id = single_row['station_identifier']
    #             if station_id in metadata_dict:
    #                 LOGGER.warning(("Duplicate entries found for station"
    #                                 f" {station_id} in station list file"))
    #             metadata_dict[station_id] = deepcopy(single_row)
    #         except Exception as e:
    #             LOGGER.error(e)

    #     fh.close()

    # else:
    #     LOGGER.error("Invalid metadata")
    #     raise ValueError

    try:
        is_bulletin = False
        messages = extract_metar(data)
        if messages[0][:6] == 'METAR\n':
            LOGGER.debug("File is a METAR bulletin")
            is_bulletin = True
            bulletin_type = 'METAR'
        elif messages[0][:6] == 'SPECI\n':
            LOGGER.debug("File is a SPECI bulletin")
            is_bulletin = True
            bulletin_type = 'SPECI'

    except Exception as e:
        LOGGER.error(e)
        return None
     # Count how many conversions were successful using a dictionary
    conversion_success = {}

    for metar in messages[is_bulletin:]:
  
        result = dict()

        mapping = deepcopy(_mapping)

        conversion_success = {}

        try:
            if is_bulletin:
                msg, num_rvr, num_vrbrvr, num_pcp, num_obv, num_sky = parse_metar(f"{bulletin_type} {metar}", year, month)
            else:
                msg, num_rvr, num_vrbrvr, num_pcp, num_obv, num_sky = parse_metar(metar, year, month)
            icao = msg['icao_location_identifier']
        except Exception as e:
            LOGGER.error(f"Error parsing METAR report: {metar}. {str(e)}")
            continue

        try:
            station_info = client.index_feature_field_query('icao', icao, client.srch_list)
            assert(station_info is not None)
        except Exception:
            conversion_success[icao] = False
            LOGGER.warning(f"Station {icao} not found on any station index")
            continue

        # extract station info from metadata dict
        try:
            # get other required metadata
            latitude = station_info['properties']["latitude"]
            longitude = station_info['properties']["longitude"]
            station_height = station_info['properties']["elevation"]
            # add these values to the data dictionary
            msg['_latitude'] = latitude
            msg['_longitude'] = longitude
            msg['_station_height'] = station_height
            conversion_success[icao] = True
        except Exception:
            conversion_success[icao] = False
            if icao == "":
                LOGGER.warning(f"Missing station ID for station {icao}")
            else:
                LOGGER.warning((f"Invalid ICAO ({icao}) found in station list,"
                                " unable to parse"))
            continue

        #   Create mapping for wind speed and gust speed depending on units of measurement
        if 'wind_speed_kn' in msg:
            mapping['data'] = update_data_mapping(mapping['data'], {"eccodes_key": "#2#windSpeed", "value": "data:wind_speed_kn"})
        elif 'wind_speed_m/s' in msg:
            mapping['data'] = update_data_mapping(mapping['data'], {"eccodes_key": "#3#windSpeed", "value": "data:wind_speed_m/s"})
        if 'gust_speed_kn' in msg:
            mapping['data'] = update_data_mapping(mapping['data'], {"eccodes_key": "#2#maximumWindGustSpeed", "value": "data:gust_speed_kn"})
        elif 'gust_speed_m/s' in msg:
            mapping['data'] = update_data_mapping(mapping['data'], {"eccodes_key": "#3#maximumWindGustSpeed", "value": "data:gust_speed_m/s"})
        

        #   Update mappings based on the number of runway visual range and variable runway visual range groups
        for idx in range(num_rvr):
            rvr_mappings = [
                {"eccodes_key": f"#{idx+1}#runwayDesignator", "value": f"data:rvr_{idx+1}_designator"},
                {"eccodes_key": f"#{(idx*2)+1}#qualifierForRunwayVisualRange", "value": f"data:rvr_{idx+1}_qualifier"},
                {"eccodes_key": f"#{(idx*2)+1}#runwayVisualRangeRvr", "value": f"data:rvr_{idx+1}_mean"},
                {"eccodes_key": f"#{idx+1}#tendencyOfRunwayVisualRange", "value": f"data:rvr_{idx+1}_tend"}
            ]

            for m in rvr_mappings:
                mapping['data'] = update_data_mapping(mapping['data'], m)

        for idx in range(num_vrbrvr):
            #   if qualifier is 'P' for above the measuring limit, qualifier will go before the 2nd recorded rvr (max)
            if msg[f'vrbrvr_{idx+1}_qualifier'] == 1:
                vrbrvr_mappings = [
                    {"eccodes_key": f"#{idx+num_rvr+1}#runwayDesignator", "value": f"data:vrbrvr_{idx+1}_designator"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+1}#runwayVisualRangeRvr", "value": f"data:vrbrvr_{idx+1}_low"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+2}#qualifierForRunwayVisualRange", "value": f"data:vrbrvr_{idx+1}_qualifier"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+2}#runwayVisualRangeRvr", "value": f"data:vrbrvr_{idx+1}_high"},
                ]
            #   if qualifer is 'M' for below the measuring limit, qualifier will go before the 1st recorded rvr (min)
            elif msg[f'vrbrvr_{idx+1}_qualifier'] == 2:
                vrbrvr_mappings = [
                    {"eccodes_key": f"#{idx+num_rvr+1}#runwayDesignator", "value": f"data:vrbrvr_{idx+1}_designator"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+1}#qualifierForRunwayVisualRange", "value": f"data:vrbrvr_{idx+1}_qualifier"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+1}#runwayVisualRangeRvr", "value": f"data:vrbrvr_{idx+1}_low"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+2}#runwayVisualRangeRvr", "value": f"data:vrbrvr_{idx+1}_high"},
                ]
            #   if qualifier is not specified, don't include it in this part of the mapping
            elif msg[f'vrbrvr_{idx+1}_qualifier'] == 0:
                vrbrvr_mappings = [
                    {"eccodes_key": f"#{idx+num_rvr+1}#runwayDesignator", "value": f"data:vrbrvr_{idx+1}_designator"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+1}#runwayVisualRangeRvr", "value": f"data:vrbrvr_{idx+1}_low"},
                    {"eccodes_key": f"#{idx+(num_rvr*2)+2}#runwayVisualRangeRvr", "value": f"data:vrbrvr_{idx+1}_high"},
                ]
            for m in vrbrvr_mappings:
                mapping['data'] = update_data_mapping(mapping['data'], m)
        
        #   Update mapping based on number of weather groups, both precipitation and observed phenomena
        for idx in range(num_pcp):
            pcp_mappings = {"eccodes_key": f"#{idx+1}#significantWeather", "value": f"data:precip_{idx+1}"}
            mapping['data'] = update_data_mapping(mapping['data'], pcp_mappings)

        for idx in range(num_obv):
            obv_mappings = {"eccodes_key": f"#{idx+num_pcp+1}#significantWeather", "value": f"data:observed_phenom_{idx+1}"}
            mapping['data'] = update_data_mapping(mapping['data'], obv_mappings)


        #   if SKC reported in cloud/sky group, don't add any additional mappings for clouds and update the general weather indicator
        if 'SKC' in msg:
            msg['general_weather_indicator'] = 3

        #   if CLR reported in cloud/sky group, add only mappings for zero cloud cover based on ecCodes 020011: Cloud Amount and Clear
        #   for ecCodes 020012: Cloud Type
        if 'CLR' in msg:
            cloud_mappings = [
                {"eccodes_key": "#1#cloudAmount", "value": "const:0"},
                {"eccodes_key": "#1#cloudType", "value": "const:43"},
            ]
            for m in cloud_mappings:
                mapping['data'] = update_data_mapping(mapping['data'], m)
        
        #   Otherwise, update mapping based on other reported sky/cloud groups
        else:
            for idx in range(num_sky):
                #   if significant convectivce clouds have been reported, mapping needs to include cloud type
                if f'sig_convec_{idx+1}' in msg:
                    cloud_mappings = [
                        {"eccodes_key": f"#{idx+1}#cloudAmount", "value": f"data:cloud_amount_{idx+1}"},
                        {"eccodes_key": f"#{idx+1}#cloudType", "value": f"data:sig_convec_{idx+1}"},
                        {"eccodes_key": f"#{(idx*2)+2}#heightOfBaseOfCloud", "value": f"data:cloud_height_{idx+1}"}
                    ]
                else:
                    cloud_mappings = [
                        {"eccodes_key": f"#{idx+1}#cloudAmount", "value": f"data:cloud_amount_{idx+1}"},
                        {"eccodes_key": f"#{(idx*2)+2}#heightOfBaseOfCloud", "value": f"data:cloud_height_{idx+1}"}
                    ]
                for m in cloud_mappings:
                    mapping['data'] = update_data_mapping(mapping['data'], m)

        #   Update mapping for vertical visibility if it is recorded instead of a cloud group
        if 'vertical_visibility' in msg:
            vvis_mapping = {"eccodes_key": "#2#verticalVisibility", "value": "data:vertical_visibility"}
            mapping['data'] = update_data_mapping(mapping['data'], vvis_mapping)

        #   set number of replications for each group
        nhvis_307046 = 0
        nrvr_307013 = num_rvr+num_vrbrvr
        nsig_307014 = num_pcp+num_obv
        ncld_307047 = num_sky
        nsig_307016 = 0
        nrwy_307017 = 0
        nsea_307049 = 0     #   short
        nrwy_307050_1 = 0   #   short
        nrwy_307050_2 = 0
        nrwy_307050_3 = 0
        ntrend_307048_1 = 0
        ntrend_307048_2 = 0
        ntrend_307048_3 = 0 #   short
        ntrend_307048_4 = 0 #   short
        ntrend_307048_5 = 0
        ntrend_307048_6 = 0

        unexpanded_descriptors = [307051]
        short_delayed_replications = [
            nsea_307049, nrwy_307050_1, ntrend_307048_3, ntrend_307048_4
        ]
        delayed_replications = [
            nhvis_307046,
            nrvr_307013,
            nsig_307014,
            ncld_307047,
            nsig_307016,
            nrwy_307017,
            nrwy_307050_2,
            nrwy_307050_3,
            ntrend_307048_1,
            ntrend_307048_2,
            ntrend_307048_5,
            ntrend_307048_6
        ]
        extended_delayed_replications = []
        table_version = 37

        try:
            # create new BUFR msg
            message = BUFRMessage(
                unexpanded_descriptors,
                short_delayed_replications,
                delayed_replications,
                extended_delayed_replications,
                table_version)
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error("Error creating BUFRMessage")
            conversion_success[icao] = False
            continue

        # parse
        if conversion_success[icao]:
            try:
                message.parse(msg, mapping)
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error("Error parsing message")
                conversion_success[icao] = False

        # Only convert to BUFR if there's no errors so far
        if conversion_success[icao]:
            try:
                result["bufr4"] = message.as_bufr()  # encode to BUFR
                status = {"code": PASSED}
            except Exception as e:
                LOGGER.error("Error encoding BUFR, null returned")
                LOGGER.error(e)
                result["bufr4"] = None
                status = {
                    "code": FAILED,
                    "message": f"Error encoding, BUFR set to None:\n\t\tError: {e}\n\t\tMessage: {msg}"  # noqa
                }
                conversion_success[icao] = False

            # now identifier based on WSI and observation date as identifier
            isodate = message.get_datetime().strftime('%Y%m%dT%H%M%S')
            rmk = f"ICAO_{icao}_{isodate}"

            # now additional metadata elements
            result["_meta"] = {
                "id": rmk,
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        message.get_element('#1#longitude'),
                        message.get_element('#1#latitude')
                    ]
                },
                "properties": {
                    "md5": message.md5(),
                    "station_identifier": icao,
                    "datetime": message.get_datetime(),
                    "originating_centre":
                    message.get_element("bufrHeaderCentre"),
                    "data_category": message.get_element("dataCategory")
                },
                "result": status
            }

        # now yield result back to caller
        yield result

        # Output conversion status to user
        if conversion_success[icao]:
            LOGGER.info(f"Station {icao} report converted")
        else:
            LOGGER.info(f"Station {icao} report failed to convert")

    # calculate number of successful conversions
    conversion_count = sum(tsi for tsi in conversion_success.values())
    # print number of messages converted
    LOGGER.info((f"{conversion_count} / {len(messages)}"
            " reports converted successfully"))


# def test():
#     with open(f"{THISDIR}{os.sep}resources{os.sep}station_list.csv") as fh:
#         station_metadata = fh.read()

#     result = transform(metar, station_metadata, 2023, 10)

#     for item in result:
#         bufr4 = item['bufr4']

#     geojson_results = generic_bufr2geojson.transform(bufr4, serialize=False)
#     for item in geojson_results:
#         for key in item.keys():
#             print(item[key]['geojson'])

def transform_file(metar_filename, month: int, year: int):
    with open(f"{THISDIR}{os.sep}resources{os.sep}station_list.csv") as fh:
        station_metadata = fh.read()
    with open(metar_filename) as fh:
        metars = fh.read()
    result = transform(metars, station_metadata, year, month)

    for item in result:
        bufr4 = item['bufr4']

        geojson_results = generic_bufr2geojson.transform(bufr4, serialize=False)
        for item in geojson_results:
            for key in item.keys():
                print(item[key]['geojson'])
