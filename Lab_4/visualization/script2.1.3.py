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
# Packages to install: (pip install)
#       pandas, matplotlib, xlrd, numpy
#

import pandas as pd  # for storing data
import numpy as np  # for math
import matplotlib.pyplot as plt  # for plotting
import matplotlib.patches as pch  # for legends on the plots

trends = dict()
x = []


def plot(path, inches):
    global trends, x
    df = pd.read_csv(path)

    # Set x and y values
    x = df['Power']
    y1 = df['Thrust CW AVG']
    y2 = df['Thrust CCW AVG']

    # define labels for the legend
    cw = pch.Patch(color='orange', label='CW')
    ccw = pch.Patch(color='teal', label='CCW')
    reg_cw = pch.Patch(color='red', label='CW trend')
    reg_ccw = pch.Patch(color='blue', label='CCW trend')
    plt.legend(handles=[cw, ccw, reg_cw, reg_ccw])

    # add lines to the plot
    plt.scatter(x, y1, color='orange')
    plt.scatter(x, y2, color='teal')

    # regression for CW
    p = np.polyfit(x, y1, 3)
    f_cw = np.poly1d(p)
    plt.plot(x, f_cw(x), color='red')

    # regression for CCW
    p = np.polyfit(x, y2, 3)  # calculate third degree polynomial trend line
    f_ccw = np.poly1d(p)
    plt.plot(x, f_ccw(x), color='blue')

    # set plot axis labels
    plt.xlabel('Power')
    plt.ylabel('Thrust')

    # save plot
    plt.savefig(str(inches) + '.png')
    # show plot
    plt.show()

    trends[str(inches) + '\" CW'] = f_cw
    trends[str(inches) + '\" CCW'] = f_ccw


plot('Thrust curve - 8 inch.csv', 8)

# define possible colors for trend plot
colors = ['red', 'blue', 'green', 'yellow']
# create list for legend
legend = []
# loop through the trends
for name, f in trends.items():
    print('name=' + str(name) + ' f=' + str(f))
    col = colors.pop()  # get color
    legend.append(pch.Patch(color=col, label=name))  # create legend entry
    plt.plot(x, f(x), color=col)  # add line to plot

# add legend and axis labels to plot
plt.legend(handles=legend)
plt.xlabel('Power')
plt.ylabel('thrust')

# save plot
plt.savefig('trends.png')
# show the plot
plt.show()
