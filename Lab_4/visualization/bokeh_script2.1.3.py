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
#       pandas, numpy, Bokeh
#

import pandas as pd  # for storing data
import numpy as np  # for math
from bokeh.plotting import figure, output_file, show  # for plotting data

df = pd.read_csv('Thrust curve - all.csv')
df_volt = pd.read_csv("Thrust curve - voltage.csv")
x = df['Power']

# thrust curve 8 inch
p = figure(title='Thrust Curve', x_axis_label='Power [% duty cycle]', y_axis_label='Thrust [G]')

p.scatter(x, df['8 Thrust CW 1'], legend='8\" run 1', size=3, color='grey')
p.scatter(x, df['8 Thrust CW 2'], legend='8\" run 2', size=3, color='lightgrey')
p.scatter(x, df['8 Thrust CW 3'], legend='8\" run 3', size=3, color='darkgrey')
p.scatter(x, df['8 Thrust CW'], legend='8\" avg', size=5, color='orange')
p.legend.location = 'top_left'

# thrust curve 10 inch
q = figure(title='Thrust Curve', x_axis_label='Power [% duty cycle]', y_axis_label='Thrust [G]')

q.scatter(x, df['10 Thrust CW'], legend='10\" cw', size=5, color='orange')
q.scatter(x, df['10 Thrust CCW'], legend='10\" ccw', size=5, color='teal')
q.legend.location = 'top_left'

# trend comparison
b = figure(title='Thrust Curve', x_axis_label='Power [% duty cycle]', y_axis_label='Thrust [G]')

f = np.poly1d(np.polyfit(x, df['8 Thrust CW'], 3))
b.line(x, f(x), legend="8\" trend", color='orange')

f = np.poly1d(np.polyfit(x, df['10 Thrust CW'], 3))
b.line(x, f(x), legend="10\" cw trend", color='teal')

f = np.poly1d(np.polyfit(x, df['10 Thrust CCW'], 3))
b.line(x, f(x), legend="10\" ccw trend", color='green')

b.legend.location = 'top_left'

# volt vs max thrust
d = figure(title='Thrust Curve', x_axis_label='Voltage [V]', y_axis_label='Thrust [G]')

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

d.scatter(x_volts, y_volts, size=5, color='orange', legend='max thrust')
d.legend.location = 'top_left'

show(p)
show(q)
show(b)
show(d)
