#
# Name: EncoderUtilities.py
# Purpose: To share common functions among various MDL decoders and encoders.
#
# Author: Mark Oberfield
# Organization: NOAA/NWS/OSTI/Meteorological Development Laboratory
# Contact Info: Mark.Oberfield@noaa.gov
#
import cmath
import math
import os
import time
import uuid
import xml.etree.ElementTree as ET

import FM15_transform.metarDecoder.xmlConfig as des

CardinalPtsToDegreesS = {'N': '360', 'NNE': '22.5', 'NE': '45', 'ENE': '67.5',
                         'E': '90', 'ESE': '112.5', 'SE': '135', 'SSE': '157.5',
                         'S': '180', 'SSW': '202.5', 'SW': '225', 'WSW': '247.5',
                         'W': '270', 'WNW': '292.5', 'NW': '315', 'NNW': '337.5', }

CardinalPtsToDegreesF = {'N': 360., 'NNE': 22.5, 'NE': 45., 'ENE': 67.5,
                         'E': 90., 'ESE': 112.5, 'SE': 135., 'SSE': 157.5,
                         'S': 180., 'SSW': 202.5, 'SW': 225., 'WSW': 247.5,
                         'W': 270., 'WNW': 292.5, 'NW': 315., 'NNW': 337.5, }


def parseCodeRegistryTables(srcDirectory, neededCodes, preferredLanguage='en'):
    #
    # Nil Reasons are always needed/required
    if 'nil' not in neededCodes:
        neededCodes.append('nil')
    #
    # Get the list of RDF files in the srcDirectory
    neededCodeFiles = [(needed, os.path.join(srcDirectory, rdfFile)) for rdfFile in os.listdir(srcDirectory)
                       for needed in neededCodes if needed in rdfFile]
    #
    events = 'start', 'start-ns'
    codes = {}
    #
    for containerId, fname in neededCodeFiles:

        top = None
        nameSpaces = {'xml': 'http://www.w3.org/XML/1998/namespace'}
        neededNS = ['skos', 'rdf', 'rdfs']

        for event, elem in ET.iterparse(fname, events):
            if event == 'start' and top is None:
                top = elem
            elif neededNS and event == 'start-ns':
                if elem[0] in neededNS:
                    nameSpaces[elem[0]] = elem[1]
                    neededNS.remove(elem[0])
        #
        # Now that we have the required namespaces for searches
        Concept = '{%s}Concept' % nameSpaces.get('skos')
        about = '{%s}about' % nameSpaces.get('rdf')
        label = '{%s}label[@{%s}lang="%s"]' % (nameSpaces.get('rdfs'), nameSpaces.get('xml'), preferredLanguage)
        enlabel = '{%s}label[@{%s}lang="%s"]' % (nameSpaces.get('rdfs'), nameSpaces.get('xml'), 'en')
        nolang = '{%s}label' % nameSpaces.get('rdfs')

        root = ET.ElementTree(top)
        kvp = []
        for concept in root.iter(Concept):
            try:
                uri = concept.get(about)
                key = uri[uri.rfind('/') + 1:]
                text = ''
                try:
                    text = concept.find(label).text
                except AttributeError:
                    if preferredLanguage != 'en':
                        text = concept.find(enlabel).text
                    else:
                        text = concept.find(nolang).text
                finally:
                    kvp.append((key, (uri, text)))

            except AttributeError:
                pass

        codes[containerId] = dict(kvp)
    return codes


def fix_date(tms):
    """Tries to determine month and year from report timestamp.
    tms contains day, hour, min of the report, current year and month"""

    now = time.time()
    t = time.mktime(tuple(tms))

    if t > now + 3 * 86400.0:       # previous month
        if tms[1] > 1:
            tms[1] -= 1
        else:
            tms[1] = 12
            tms[0] -= 1
    elif t < now - 25 * 86400.0:  # next month
        if tms[1] < 12:
            tms[1] += 1
        else:
            tms[1] = 1
            tms[0] += 1


def is_a_number(s):
    return s.replace('-', '', 1).replace('.', '', 1).isdigit()


def getUUID(prefix='uuid.'):
    return '%s%s' % (prefix, uuid.uuid4())


def computeLatLon(lat, lon, bearing, distance, radius=3440.):
    #
    # Assumes flat earth, far from singularities--the poles--and small distances.
    #
    # Fractional errors are O((distance/radius)^2)
    z = cmath.rect(distance, math.radians(bearing)) * 1j 
    nlat = lat + math.degrees(z.imag / radius)
    nlon = lon + math.degrees(-z.real / (radius * math.cos(math.radians(lat))))

    if nlon < -180:
        nlon += 360
    elif nlon > 180:
        nlon -= 360

    return '%.3f %.3f' % (nlat, nlon)


def fixLongitudes(old_pnts):

    new_pnts = []
    for pnt in old_pnts:
        lat, lon = [float(z) for z in pnt.split(' ')]
        if lon > 180:
            lon -= 360
        new_pnts.append(('%.3f %.3f' % (lat, lon)))

    return new_pnts
#
# Returns values (in meters) according to Annex 3 Amd 77
def checkVisibility(value, uom='m'):

    if isinstance(value, str):
        def returnFunction(x):
            return str(x)
        value = float(value)
    else:
        def returnFunction(x):
            return int(x)

    if uom == '[mi_i]':
        value *= 1609.34
    elif uom == '[ft_i]':
        value *= 0.3048

    mod = 1
    value = int(value)
    if value < 800:
        mod = 50
    elif 800 <= value < 5000:
        mod = 100
    elif value < 9999:
        mod = 1000
    else:
        value = 10000

    return returnFunction(value - (value % mod))


def checkRVR(value, uom='m'):

    if isinstance(value, str):
        def returnFunction(x):
            return str(x)
        value = float(value)
    else:
        def returnFunction(x):
            return int(x)

    if uom == '[mi_i]':
        value *= 1609.34
    elif uom == '[ft_i]':
        value *= 0.3048

    value = int(value)
    if value < 400:
        mod = 25
    elif 400 <= value <= 800:
        mod = 50
    else:
        mod = 100

    return returnFunction(value - (value % mod))


def isUSIdentifier(id):
    return des.isUSObservation.match(id) is not None


def computeArea(originalPolygon):
    """Compute 'area' of a polygon as defined with latitude, longitude points"""

    if len(originalPolygon) < 3:
        raise ValueError("Polygon must have 3 or more points")
    #
    # Copy
    polygon = originalPolygon
    #
    # Confirm it's closed
    if polygon[0] != polygon[-1]:
        polygon.append(polygon[0])

    nogylop = []
    #
    # Switch ordering of coordinates from lat/long to long/lat
    # and make x positive for all cases
    for y, x in polygon:
        if x < 0:
            x += 360
        nogylop.append((x, y))
    #
    area = 0
    for p1, p2 in zip(nogylop, nogylop[1:]):
        area += (p2[0] - p1[0]) * (p2[1] + p1[1])

    return area


def isCCW(polygon):
    return computeArea(polygon) < 0
