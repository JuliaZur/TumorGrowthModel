import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

'''
MTD to Sphere = 2*pi/9*MTD^2 
'''


def load_data(sphere=True):
    PCV1 = pd.read_csv('./data/PCV1.csv', header=1)
    PCV2 = pd.read_csv('./data/PCV2.csv', header=1)
    PCV3 = pd.read_csv('./data/PCV3.csv', header=1)

    RT1 = pd.read_csv('./data/RT1.csv', header=1)
    RT2 = pd.read_csv('./data/RT2.csv', header=1)
    RT3 = pd.read_csv('./data/RT3.csv', header=1)

    TMZ1 = pd.read_csv('./data/TMZ1.csv', header=1)
    TMZ2 = pd.read_csv('./data/TMZ2.csv', header=1)
    TMZ3 = pd.read_csv('./data/TMZ3.csv', header=1)

    loaded_data = [PCV1, PCV2, PCV3, TMZ1, TMZ2, TMZ3, RT1, RT2, RT3]

    patients_data = []

    for group in loaded_data:
        headers = list(group.columns)
        group_data = []
        for i in range(0, len(headers) - 1, 2):
            data = sorted(zip(group[headers[i]], group[headers[i + 1]]))
            x = [k for k, v in list(data)]
            if sphere:
                y = [mtd2sphere(v) for k, v in list(data)]
            else:
                y = [v for k, v in list(data)]
            group_data.append(x)
            group_data.append(y)
        patients_data.append(DataFrame(group_data).transpose())

    return patients_data


def make_plot(patients_data, sphere=True):
    fig = make_subplots(rows=3, cols=3,
                        subplot_titles=("PCV1", "PCV2", "PCV3", "TMZ1", "TMZ2", "TMZ3",
                                        "RT1", "RT2", "RT3"))
    row = 1
    col = 1

    for key in patients_data:

        headers = list(key.columns)

        for i in range(0, len(headers) - 1, 2):

            x = list(key[headers[i]])
            y = list(key[headers[i + 1]])

            if sphere:
                y_title = 'Volume [mm^3]'
                y_range = [0, 6000]
            else:
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

    return fig


def mtd2sphere(mtd):
    return 2 * math.pi / 9 * (mtd ** 2)


if __name__ == '__main__':
    patients_data = load_data()
    fig = make_plot(patients_data)
    fig.show()
