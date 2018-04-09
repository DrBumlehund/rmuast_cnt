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
#       pandas, matplotlib, numpy
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as ln

a = 2400000000  # 2.4 GHz
b = 433000000  # 433 MHz
c = 5800000000  # 5.8 GHz
freqs = {'a': a, 'b': b, 'c': c}
d1 = list(range(0, 101))
d2 = d1.copy()
d2.reverse()
df = pd.DataFrame({'d1': d1, 'd2': d2})

for l in ['a', 'b', 'c']:
    f = freqs[l]
    for n in [1, 2, 3]:
        key = "F%i %s" % (n, l)
        df[key] = np.sqrt((n * f * (df['d1'] * df['d2'])) / (df['d1'] + df['d2']))
        key_neg = '-' + key
        df[key_neg] = -1 * df[key]

print(df)

plt.plot(df['d1'], df['F1 a'], c='teal', linestyle=':')
plt.plot(df['d1'], df['F2 a'], c='teal', linestyle=':')
plt.plot(df['d1'], df['F3 a'], c='teal', linestyle=':')
plt.plot(df['d1'], df['-F1 a'], c='teal', linestyle=':')
plt.plot(df['d1'], df['-F2 a'], c='teal', linestyle=':')
plt.plot(df['d1'], df['-F3 a'], c='teal', linestyle=':')

plt.plot(df['d1'], df['F1 b'], c='orange', linestyle='-.')
plt.plot(df['d1'], df['F2 b'], c='orange', linestyle='-.')
plt.plot(df['d1'], df['F3 b'], c='orange', linestyle='-.')
plt.plot(df['d1'], df['-F1 b'], c='orange', linestyle='-.')
plt.plot(df['d1'], df['-F2 b'], c='orange', linestyle='-.')
plt.plot(df['d1'], df['-F3 b'], c='orange', linestyle='-.')

plt.plot(df['d1'], df['F1 c'], c='lime', linestyle='--')
plt.plot(df['d1'], df['F2 c'], c='lime', linestyle='--')
plt.plot(df['d1'], df['F3 c'], c='lime', linestyle='--')
plt.plot(df['d1'], df['-F1 c'], c='lime', linestyle='--')
plt.plot(df['d1'], df['-F2 c'], c='lime', linestyle='--')
plt.plot(df['d1'], df['-F3 c'], c='lime', linestyle='--')

plt.legend(handles=[
    ln.Line2D([], [], color='teal', label='2.4 GHz', linestyle=':'),
    ln.Line2D([], [], color='orange', label='433 MHz', linestyle='-.'),
    ln.Line2D([], [], color='lime', label='5.8 GHz', linestyle='--'),
])
plt.xlabel('Distance [m]')
plt.ylabel('Radius [m]')
plt.savefig('freznel.png')
plt.show()
