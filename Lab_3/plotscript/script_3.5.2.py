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
#       pandas, matplotlib
#

import pandas as pd  # for storing data
import numpy as np  # for math
import re  # for regex
import matplotlib.pyplot as plt  # for plotting

# read the data as a CSV file, with tabs for separators,
df = pd.read_csv('log-2016-01-14.txt', '\t', header=None)


# Convert GNSS to a continuous number, to avoid 4000 sized jumps at hourly intervals
def convert_gnss(value):
    splits = re.findall('\d\d', str(value))
    return int(splits[0]) * 3600 + int(splits[1]) * 60 + int(splits[2])


df[4] = df[4].apply(lambda l: convert_gnss(l))

x = df[4]  # define x axis
y = df[11]  # define y axis

# plot the data
plt.plot(x, y)
plt.ylabel('Voltage')
plt.xlabel('Time')
plt.savefig('dischargePlot.png')
plt.show()
