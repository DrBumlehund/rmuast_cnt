#
#  Copyright 2018 Chris Bang Sørensen, Niels Hvid, Thomas Lemqvist
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#  of the Software, and to permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
# Packages to install: (pip install)
#       pandas, matplotlib, xlrd, numpy
#

from kml.exportkml import kmlclass
from utm.utm import utmconv
import pandas as pd  # for storing data
import numpy as np  # for math
from datetime import datetime as time
import datetime
import matplotlib.pyplot as plt  # for plotting
import matplotlib.dates as dt
import matplotlib.lines as ln
from math import pi, cos, sqrt, sin, asin, fabs


class TrackSimplifier:
    def __init__(self):
        self.df = pd.DataFrame()
        self.time = 0
        self.c = 1

    def import_data(self, file_name):
        self.df = pd.read_csv(file_name)

    def print_data(self):
        print(self.df)

    def plot_track(self, utm=False):
        print('plotting track')
        fig, ax = plt.subplots()
        if utm:
            plt.plot(self.df['utm_easting'], self.df['utm_northing'])
        else:
            plt.plot(self.df['lon'], self.df['lat'])
        ax.ticklabel_format(useOffset=False)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig('track_plot.png')
        plt.show()

    def convert_to_utm(self):
        u = utmconv()
        # (hemisphere, zone, letter, easting, northing)
        hemispheres, zones, letters, eastings, northings = [], [], [], [], []
        for index, row in self.df.iterrows():
            (hemisphere, zone, letter, easting, northing) = u.geodetic_to_utm(row['lat'], row['lon'])
            hemispheres.append(hemisphere)
            zones.append(zone)
            letters.append(letter)
            eastings.append(easting)
            northings.append(northing)
        self.df['utm_hemisphere'] = hemispheres
        self.df['utm_zone'] = zones
        self.df['utm_letter'] = letters
        self.df['utm_easting'] = eastings
        self.df['utm_northing'] = northings

    def export_kml(self, file_name, title, description, color):
        print('Creating the file export.kml')
        # width: defines the line width, use e.g. 0.1 - 1.0
        kml = kmlclass()
        kml.begin(file_name, title, description, 0.1)
        # color: use 'red' or 'green' or 'blue' or 'cyan' or 'yellow' or 'grey'
        kml.trksegbegin('', '', color, 'absolute')
        for i, x in self.df.iterrows():
            kml.trkpt(x['lat'], x['lon'], x['alt'])
        kml.trksegend()
        kml.end()

    def mean_filter(self, k=30, utm=False):
        label_lat, label_lon = 'lat', 'lon'
        if utm:
            label_lat, label_lon = 'utm_northing', 'utm_easting'
        means_lat, means_lon = [], []
        for index, row in self.df.iterrows():
            lower = int(np.max([index - np.floor(k / 2), 0]))
            upper = int(np.min([index + np.floor(k / 2), self.df.shape[0] - 1]))
            means_lat.append(np.mean(self.df.iloc[lower:upper][label_lat]))
            means_lon.append(np.mean(self.df.iloc[lower:upper][label_lon]))
        self.df[label_lat] = means_lat
        self.df[label_lon] = means_lon

    def median_filter(self, k=30, utm=False):
        label_lat, label_lon = 'lat', 'lon'
        if utm:
            label_lat, label_lon = 'utm_northing', 'utm_easting'
        medians_lat, medians_lon = [], []
        for index, row in self.df.iterrows():
            lower = int(np.max([index - np.floor(k / 2), 0]))
            upper = int(np.min([index + np.floor(k / 2), self.df.shape[0] - 1]))
            medians_lat.append(np.median(self.df.iloc[lower:upper][label_lat]))
            medians_lon.append(np.median(self.df.iloc[lower:upper][label_lon]))
        self.df[label_lat] = medians_lat
        self.df[label_lon] = medians_lon

    def calculate_angles(self):
        min_t = np.min(self.df['#time_boot'])
        times, angle_x, angle_y, angle_z = [], [], [], []
        x, y, z = 0, 0, 0
        for index, row in self.df.iterrows():
            t = row['#time_boot'] - min_t
            delta_t = t - self.time
            times.append(delta_t)
            if not np.isnan(row['vx']):
                x += float((row['vx'] * delta_t) * 180 / np.pi)
                y += float((row['vy'] * delta_t) * 180 / np.pi)
                z += float((row['vz'] * delta_t) * 180 / np.pi)
                angle_x.append(x)
                angle_y.append(y)
                angle_z.append(z)
            else:
                angle_x.append(np.nan)
                angle_y.append(np.nan)
                angle_z.append(np.nan)
            self.time = t
        self.df['delta_t'] = times
        self.df['angle_x'] = angle_x
        self.df['angle_y'] = angle_y
        self.df['angle_z'] = angle_z

    def plot_angles(self):
        plt.plot(self.df['#time_boot'], self.df['angle_x'])
        plt.show()

    @staticmethod
    # distance function (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line)
    def perpendicular_distance(start, end, p):
        lat, lon = p[0], p[1]
        lat_1, lon_1 = start[0], start[1]
        lat_2, lon_2 = end[0], end[1]
        dist = np.absolute((lat_2 - lat_1) * lon - (lon_2 - lon_1) * lat + lon_2 * lat_1 - lat_2 * lon_1) / np.sqrt(
            (lat_2 - lat_1) ** 2 + (lon_2 - lon_1) ** 2)
        return dist

    # todo: Chris implement dp algoritm
    def rdp_algorithm(self, epsilon, utm, point_list=None):  # Ramer-Douglas-Peucker Algorithm.
        label_lat, label_lon = 'lat', 'lon'
        if utm:
            label_lat, label_lon = 'utm_northing', 'utm_easting'
        # Find the point with the maximum distance
        df = point_list
        if point_list is None:
            df = self.df
        d_max = 0
        index = 0
        end = df.shape[0] - 1
        result_list = pd.DataFrame()
        count = 0
        for i, row in df.iterrows():
            if 0 < count < end:
                first_row = df.iloc[0]
                end_row = df.iloc[end]
                start_point = (first_row[label_lat], first_row[label_lon])
                end_point = (end_row[label_lat], end_row[label_lon])
                current_point = (row[label_lat], row[label_lon])
                # Get the perpendicular distance, from current_point to a line between start_point and end_point
                distance = self.perpendicular_distance(start_point, end_point, current_point)
                if distance > d_max:
                    index = count
                    d_max = distance
            count += 1

        if d_max > epsilon:
            print('%i) d_max = %.3f, index = %i' % (self.c, d_max, index))
            self.c += 1
            rec_result_1 = self.rdp_algorithm(epsilon, utm, df.iloc[0:(index + 1)])
            rec_result_2 = self.rdp_algorithm(epsilon, utm, df.iloc[index:(end + 1)])

            # build the result list
            rec_result_1.drop(rec_result_1.tail(1).index, inplace=True)
            result_list = pd.concat([rec_result_1, rec_result_2])
        else:
            result_list = df.iloc[[0, end]]
           # q print(result_list)

        return result_list

    def ramer_douglas_peucker(self, epsilon, utm=False):
        self.df = self.rdp_algorithm(epsilon, utm=utm)

    def print_length(self):
        print('df has %i rows' % self.df.shape[0])

    def angle_algorithm(self):
        # todo: Niels ?
        print('not yet implemented')

    def velocity_algorithm(self):
        # todo: Thomas
        print('not yet implemented')


if __name__ == '__main__':
    d = TrackSimplifier()
    d.import_data('position_close_space.txt')
    d.convert_to_utm()
    d.mean_filter(utm=True)
    d.median_filter(utm=True)
    #
    #
    # d.export_kml('close_mean_median_100.kml', 'close_mean_median_100',
    #              'mean and median filtered close data, window 100', 'cyan')
    # d.calculate_angles()
    # d.plot_angles()
    # d.print_data()

    d.print_length()
    d.ramer_douglas_peucker(0.2, True)
    d.print_length()
    # d.print_data()
    d.export_kml('rdp_close.kml', 'rdp_close',
                 'green', 'cyan')
    d.plot_track(utm=True)
