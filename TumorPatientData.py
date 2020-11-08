import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

'''
MTD to Sphere = 2*pi/9*MTD^2 
'''

PCV1 = pd.read_csv('./data/PCV1.csv', header=1)
PCV2 = pd.read_csv('./data/PCV2.csv', header=1)
PCV3 = pd.read_csv('./data/PCV3.csv', header=1)

RT1 = pd.read_csv('./data/RT1.csv', header=1)
RT2 = pd.read_csv('./data/RT2.csv', header=1)
RT3 = pd.read_csv('./data/RT3.csv', header=1)

TMZ1 = pd.read_csv('./data/TMZ1.csv', header=1)
TMZ2 = pd.read_csv('./data/TMZ2.csv', header=1)
TMZ3 = pd.read_csv('./data/TMZ3.csv', header=1)

patients_data = [PCV1, PCV2, PCV3, TMZ1, TMZ2, TMZ3, RT1, RT2, RT3]

fig = make_subplots(rows=3, cols=3,
                    subplot_titles=("PCV1", "PCV2", "PCV3", "TMZ1", "TMZ2", "TMZ3",
                                    "RT1", "RT2", "RT3"))
row = 1
col = 1

print(RT2)

MTD2SPEHERE = True


def mtd2sphere(mtd):
    return 2 * math.pi / 9 * (mtd ** 2)


for key in patients_data:

    headers = list(key.columns)

    for i in range(0, len(headers) - 1, 2):

        data = sorted(zip(key[headers[i]], key[headers[i + 1]]))
        x = [k for k, v in list(data)]

        if MTD2SPEHERE:
            y = [mtd2sphere(v) for k, v in list(data)]
            y_title = 'Volume [mm^3]'
            y_range = [0, 6000]
        else:
            y = [v for k, v in list(data)]
            y_title = 'MTD [mm]'
            y_range = [0, 100]

        fig.add_trace(
            go.Scatter(x=x, y=y, mode='lines+markers'),
            row=row, col=col
        )
        fig.update_yaxes(title_text=y_title, row=row, col=col, range=y_range)
        fig.update_xaxes(title_text="Time [month]", row=row, col=col, range=[-100, 100], zerolinewidth=1,
                         zerolinecolor='Black')

    col += 1
    if col > 3:
        row += 1
        col = 1

fig.show()
