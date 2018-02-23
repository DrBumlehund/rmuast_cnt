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
#       pandas, matplotlib, xlrd
#

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

df = pd.read_excel("MELASTA_Li-Polymer_modifiedNames.xlsx", skiprows=2, skip_footer=3)


# convert string to number
def num(s):
    s = re.search('\d+(\.\d{1,2})?', str(s)).group(0)
    try:
        return int(s)
    except ValueError:
        return float(s)


# clean up various string values in the data set and make them numerical
def clean_data():
    df['Capacity'] = df['Capacity'].apply(lambda x: num(x))
    df['Weight'] = df['Weight'].apply(lambda x: num(x))
    df['Impedance'] = df['Impedance'].apply(lambda x: num(x))
    df['Cell Length'] = df['Cell Length'].apply(lambda x: num(x))
    df['Cell Width'] = df['Cell Width'].apply(lambda x: num(x))
    df['Cell Thickness'] = df['Cell Thickness'].apply(lambda x: num(x))
    df['Distance between tabs'] = df['Distance between tabs'].apply(lambda x: num(x))


clean_data()

df['Voltage'] = 3.7  # set the voltage for the batteries

df['Specific Energy'] = df['Voltage'] * df['Capacity'] / df['Weight']  # Calculate specific energy.

# # uncomment to remove a possible outlier
# print(df[df['Specific Energy'] == numpy.min(df['Specific Energy'])])
# df = df[df['Specific Energy'] != numpy.min(df['Specific Energy'])]

x = df['C']
y = df['Specific Energy']

plt.scatter(x, y)
plt.xlabel('C')
plt.ylabel('Specific Energy')
p = np.poly1d(np.polyfit(x, y, 1))  # calculate trend line
plt.plot(x, p(x), 'r--')
plt.savefig("C:/Users/drbum/git/rmuast_cnt/Lab_3/plotscript/plot.png")
plt.show()

print(np.corrcoef(df['C'], df['Specific Energy']))  # print correlation coefficients.

