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
import pandas as pd  # for storing data
import numpy as np  # for math
from bokeh.plotting import figure, show, output_file

df = pd.read_csv('Thrust curve - all.csv')

output_file('thrust_curve.html')
p = figure(title='Thrust Curve', x_axis_label='Power [% duty cycle]', y_axis_label='Thrust [G]', x_range=[0, 100],
           y_range=(0, 850))

x = df['Power']

p.scatter(x, df['8 Thrust CW 1'], legend='8\" run 1', size=3, color='teal')
p.scatter(x, df['8 Thrust CW 2'], legend='8\" run 2', size=3, color='orange')
p.scatter(x, df['8 Thrust CW 3'], legend='8\" run 3', size=3, color='green')
p.scatter(x, df['8 Thrust CW'], legend='8\" avg', size=5, color='red')

p.scatter(x, df['10 Thrust CW'], legend='10\" cw', size=5, color='blue')
p.scatter(x, df['10 Thrust CCW'], legend='10\" ccw', size=5, color='brown')

f = np.poly1d(np.polyfit(x, df['8 Thrust CW'], 3))
p.line(x, f(x), legend="8\" trend", color='pink', line_dash='4 4')

f = np.poly1d(np.polyfit(x, df['10 Thrust CW'], 3))
p.line(x, f(x), legend="10\" cw trend", color='cyan', line_dash='4 4')

f = np.poly1d(np.polyfit(x, df['10 Thrust CCW'], 3))
p.line(x, f(x), legend="10\" ccw trend", color='purple', line_dash='4 4')
show(p)
