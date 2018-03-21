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

from exercise_nmea_data.exportkml import kmlclass
import pandas as pd  # for storing data
from datetime import datetime
import numpy as np  # for math
import re  # for regex
import matplotlib.pyplot as plt  # for plotting
import matplotlib.dates as dt


# http://www.trimble.com/oem_receiverhelp/v4.44/en/nmea-0183messages_gga.html
# http://www.gpsinformation.org/dale/nmea.htm#GGA
class NMEA:

    def __init__(self):
        self.df = {}

    def import_file(self, file_name):
        self.df = pd.read_csv(file_name, header=None, skipfooter=1, engine='python', dtype={4: str, 2: str})
        self.df[1] = self.df[1].apply(lambda x: self.convert_dates(x))
        self.df[2] = self.df[2].apply(lambda x: self.convert_degrees(2, x))
        self.df[4] = self.df[4].apply(lambda x: self.convert_degrees(3, x))
        self.df[6] = self.df[6].apply(lambda x: self.convert_quality(x))

    @staticmethod
    def convert_dates(value):
        t = datetime.strptime(str(value), '%H%M%S.%f')
        return t

    @staticmethod
    def convert_degrees(deg_length, value):
        deg = float(value[:deg_length])
        minutes = float(value[deg_length:])
        return float(deg + minutes / 60)

    @staticmethod
    def convert_quality(value):
        quality = {0: 'invalid', 1: 'GPS fix (SPS)', 2: 'DGPS fix', 3: 'PPS fix', 4: 'RTK', 5: 'RTK float',
                   6: 'estimated', 7: 'Manual input', 8: 'Simulation Mode'}
        val = quality[value]
        return val

    def print_data(self):
        print(self.df)

    def plot_height_over_time(self):
        fig, ax = plt.subplots()
        dates = dt.date2num(self.df[1])
        plt.plot(dates, self.df[9])
        plt.xlabel('Time [utc]')
        plt.ylabel('Height [m]')
        ax.xaxis.set_major_formatter(dt.DateFormatter('%H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.savefig('height_time_plot.png')
        plt.show()

    def plot_number_of_satellites_over_time(self):
        fig, ax = plt.subplots()
        dates = dt.date2num(self.df[1])
        plt.plot(dates, self.df[7])
        plt.xlabel('Time [utc]')
        plt.ylabel('Satellites [#]')
        ax.xaxis.set_major_formatter(dt.DateFormatter('%H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.savefig('number_of_satellites_plot.png')
        plt.show()

    def plot_quality_of_signal_over_time(self):
        fig, ax = plt.subplots()
        dates = dt.date2num(self.df[1])
        plt.plot(dates, self.df[6])
        plt.xlabel('Time [utc]')
        plt.ylabel('Fix quality')
        ax.xaxis.set_major_formatter(dt.DateFormatter('%H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.savefig('quality_of_signal_plot.png')
        plt.show()

    def plot_track(self):
        fig, ax = plt.subplots()
        plt.plot(self.df[4], self.df[2])
        ax.ticklabel_format(useOffset=False)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig('track_plot.png')
        plt.show()

    def export_kml(self):
        print('Creating the file testfile.kml as an example on how tu use kmlclass')
        # width: defines the line width, use e.g. 0.1 - 1.0
        kml = kmlclass()
        kml.begin('export.kml', 'Example', 'Example on the use of kmlclass', 0.1)
        # color: use 'red' or 'green' or 'blue' or 'cyan' or 'yellow' or 'grey'
        # altitude: use 'absolute' or 'relativeToGround'
        kml.trksegbegin('', '', 'red', 'absolute')

        for i, x in self.df.iterrows():
            kml.trkpt(x[2], x[4], x[9])

        kml.trksegend()
        kml.end()


if __name__ == '__main__':
    print('importing file')
    nmea = NMEA()
    nmea.import_file('nmea_trimble_gnss_eduquad_flight.txt')
    nmea.print_data()
    nmea.plot_height_over_time()
    nmea.plot_number_of_satellites_over_time()
    nmea.plot_track()
    nmea.export_kml()
    nmea = NMEA()
    nmea.import_file('nmea_ublox_neo_24h_static.txt')
    nmea.print_data()
    nmea.plot_quality_of_signal_over_time()
