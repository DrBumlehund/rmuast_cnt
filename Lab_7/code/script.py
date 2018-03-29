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

    def pdis(a, b, c):
        t = b[0] - a[0], b[1] - a[1]  # Vector ab
        dd = sqrt(t[0] ** 2 + t[1] ** 2)  # Length of ab
        t = t[0] / dd, t[1] / dd  # unit vector of ab
        n = -t[1], t[0]  # normal unit vector to ab
        ac = c[0] - a[0], c[1] - a[1]  # vector ac
        return fabs(ac[0] * n[0] + ac[1] * n[1])  # Projection of ac to n (the minimum distance)


    def rdp_algorithm(self, epsilon, indexx, endd): #Ramer-Douglas-Peucker Algorithm.
        # todo: Chris implement dp algoritm
        print('not yet implemented')

        # Find the point with the maximum distance
        dmax = 0
        index = indexx
        end = self.df.size - 1
        count = 0
        for index, row in self.df.iterrows():
            if count == 0:#We skip first row
                count += 1
            else:
                fRow = self.df.iloc[0]
                eRow = self.df.iloc[end]
                sPoint = (fRow['lat'],fRow['long'])
                ePoint = (eRow['lat'],fRow['long'])
                cPoint = (row['lat'],row['long'])
                #Get the perpendicular distance, from cPoint to a line between sPoint and ePoint
                d = self.pdis(sPoint, ePoint, cPoint)
                #if d > dmax:






        
      
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
    d.mean_filter(k=100)
    d.median_filter(k=100)

    d.plot_track()
    d.export_kml('close_mean_median_100.kml', 'close_mean_median_100',
                 'mean and median filtered close data, window 100', 'cyan')
    d.calculate_angles()
    d.plot_angles()
    d.print_data()
