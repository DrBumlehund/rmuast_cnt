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
import matplotlib.lines as ln  # for legends on the plots

df = pd.read_csv("Thrust curve - all.csv")
df_volt = pd.read_csv("Thrust curve - voltage.csv")

# Set x and y values
x = df['Power']
y8_1 = df['8 Thrust CW 1']
y8_2 = df['8 Thrust CW 2']
y8_3 = df['8 Thrust CW 3']

y8_avg = df['8 Thrust CW']

y10_cv = df['10 Thrust CW']
y10_ccv = df['10 Thrust CCW']

# plot dots for all tests on 8 inch propeller
plt.scatter(x, y8_1, color='grey')
plt.scatter(x, y8_2, color='grey')
plt.scatter(x, y8_3, color='grey')
plt.scatter(x, y8_avg, color='teal')

p_8 = np.poly1d(np.polyfit(x, y8_avg, 3))
plt.plot(x, p_8(x), color='orange')
print('8\"\n' + str(p_8))
legend = [
    ln.Line2D([], [], color='grey', label='Observation', marker="o", linewidth=0),
    ln.Line2D([], [], color='teal', label='Average', marker="o", linewidth=0),
    ln.Line2D([], [], color='orange', label='Trend')
]

plt.legend(handles=legend)
plt.xlabel('Power [% duty cycle]')
plt.ylabel('Thrust [g]')
plt.title('8 inch propeller thrust curve Test')
plt.savefig('8 inch test.png')
plt.show()

# plot for 10 inch propellers

plt.plot(x, y10_cv, linestyle='dashed', label='average', color='teal')
plt.plot(x, y10_ccv, linestyle='dashed', label='average', color='green')

p_10_cv = np.poly1d(np.polyfit(x, y10_cv, 3))
plt.plot(x, p_10_cv(x), color='orange')
print('10\" cw\n' + str(p_10_cv))

p_10_ccv = np.poly1d(np.polyfit(x, y10_ccv, 3))
plt.plot(x, p_10_ccv(x), color='red')
print('10\" ccw\n' + str(p_10_ccv))

plt.legend(handles=[
    ln.Line2D([], [], color='teal', label='Average cw', linestyle='dashed'),
    ln.Line2D([], [], color='green', label='Average ccw', linestyle='dashed'),
    ln.Line2D([], [], color='orange', label='Trend cw'),
    ln.Line2D([], [], color='red', label='Trend ccw')
])
plt.xlabel('Power [% duty cycle]')
plt.ylabel('Thrust [g]')
plt.title('10 inch propeller thrust curve Test')
plt.savefig('10 inch test.png')
plt.show()

# trend line comparison
plt.plot(x, p_8(x), color='teal')
plt.plot(x, p_10_cv(x), color='orange')
plt.plot(x, p_10_ccv(x), color='green')
plt.legend(handles=[
    ln.Line2D([], [], color='teal', label='Trend 8\" cw'),
    ln.Line2D([], [], color='orange', label='Trend 10\" cw'),
    ln.Line2D([], [], color='green', label='Trend 10\" ccw'),
])
plt.xlabel('Power [% duty cycle]')
plt.ylabel('Thrust [g]')
plt.title('Thrust curve trend comparison')
plt.savefig('trend comparison.png')
plt.show()

# max over voltage plot
x_volts = [
    np.max(df_volt['8 Thrust CW 1']),
    np.max(df_volt['8 Thrust CW 2']),
    np.max(df_volt['8 Thrust CW 3'])
]
y_volts = [
    np.max(df['8 Thrust CW 1']),
    np.max(df['8 Thrust CW 2']),
    np.max(df['8 Thrust CW 3'])
]

plt.plot(x_volts, y_volts)
plt.xlabel('Battery voltage [V]')
plt.ylabel('Thrust [g]')
plt.title('Max thrust vs. Battery Voltage')
plt.savefig('voltage plot.png')
plt.show()
