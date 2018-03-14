#!/usr/bin/env python
# *****************************************************************************
# UTM projection conversion test
# Copyright (c) 2013-2016, Kjeld Jensen <kjeld@frobomind.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# *****************************************************************************
"""
This file contains a simple Python script to test the UTM conversion class.

Revision
2013-04-05 KJ First version
2015-03-09 KJ Minor update of the license text.
2016-01-16 KJ Corrected a minor problem with the library location reference.
"""
# import utmconv class
from exercise_utm.utm import utmconv
from math import pi, cos, sqrt, sin, asin

# instantiate utmconv class
uc = utmconv()

# define test position
test_lat1 = 55.47
test_lon1 = 010.33
test_lat2 = 55.46809039111672
test_lon2 = 010.345481691709665

test_lat = test_lat2
test_lon = test_lon2
print('Test position [deg]:')
print('  latitude:  %.10f' % test_lat)
print('  longitude: %.10f' % test_lon)


def great_circle_distance(lat1, lon1, lat2, lon2):
    return asin(sqrt((sin((lat1 - lat2) / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin((lon1 - lon2) / 2)) ** 2))


(hemisphere1, zone1, letter1, easting1, northing1) = uc.geodetic_to_utm(test_lat1, test_lon1)
(hemisphere2, zone2, letter2, easting2, northing2) = uc.geodetic_to_utm(test_lat2, test_lon2)
d = great_circle_distance(easting1, northing1, easting2, northing2)
print('\nTest Distance [km]:')
print('  distance: %.4f km' % d)
print('  error:    %.3f %%' % (d / 1 * 100 - 100))

# convert from geodetic to UTM
(hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm(test_lat, test_lon)
print('\nConverted from geodetic to UTM [m]')
print('  %d %c %.5fe %.5fn' % (zone, letter, easting, northing))

# convert back from UTM to geodetic
(lat, lon) = uc.utm_to_geodetic(hemisphere, zone, easting, northing)
print('\nConverted back from UTM to geodetic [deg]:')
print('  latitude:  %.10f' % lat)
print('  longitude: %.10f' % lon)

# determine conversion position error [m]
lat_err = abs(lat - test_lat)
lon_err = abs(lon - test_lon)
earth_radius = 6378137.0  # [m]
lat_pos_err = lat_err / 360.0 * 2 * pi * earth_radius
lon_pos_err = lon_err / 360.0 * 2 * pi * (cos(lat) * earth_radius)
print('\nPositional error from the two conversions [m]:')
print('  latitude:  %.10f' % lat_pos_err)
print('  longitude: %.10f' % lon_pos_err)
