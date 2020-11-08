import pyabc
from enum import Enum
import plotly as plt
import os
import tempfile

'''
P - proliferative tissue, tumor tissue
Q - non-proliferative tissue
C - drug concentration
QP - DNA-damaged Q tissue by the drug impact
KDE - constant rate of the decay of the PCV concentration

lambda_P - growth rate of P
gamma_P - damages in P tissue caused by the drug
gamma_Q - damages in Q tissue caused by the drug    >  gamma_P = gamma_Q
k_QP_P - constant rate of transfer from QP to P tissue 
delta_QP - constant rate of elimination of QP tissue
k_PQ - constant rate of transfer from P to Q tissue
K - maximal tumor size

Parameters to estimate: (lambda_P, k_PQ, k_QP_P,delta_QP,gamma,KDE)

Starting values:
P0 = P(t=0)
Q0 = Q(t=0)     > t=0 - first available data
QP0 = QP(t=0) = 0 
C0 = 1
K = 100 mm

dCdt = -KDE * C
dPdt = lambda_P * P*(1 - P'/K) + k_QP_P * QP - k_PQ * P - gamma_P * C * KDE * P
dQdt = k_PQ * P - gamma_Q * C * KDE * Q
dQPdt = gamma_Q * C * KDE * Q - k_QP_P * QP - delta_QP * QP
P_Q_QP = P + Q + QP
'''


class Therapy(Enum):
    TMZ = "temozolomide chemotherapy"
    PCV = "1-(2-chloroethyl)-3-cyclohexyl-l-nitrosourea, and vincristine chemotherapy"
    RT = "radiotherapy"


class TumorGrowthModel:
    def __init__(self, C0, P0, Q0, QP0, K0, lambda_P, k_PQ, k_QP_P, delta_QP, gamma, KDE):
        self.K0 = K0
        self.C0 = C0
        self.P0 = P0
        self.Q0 = Q0
        self.QP0 = QP0
        self.K0 = K0
        self.lambda_P = lambda_P
        self.k_PQ = k_PQ
        self.k_QP_P = k_QP_P
        self.delta_QP = delta_QP
        self.gamma = gamma
        self.KDE = KDE

        self.C = self.C0
        self.Q = self.Q0
        self.P = self.P0
        self.QP = self.QP0
        self.K = self.K0

        self.P_Q_QP = self.P + self.Q + self.QP

        self.parameter_priors = [
            pyabc.Distribution(dCdt=pyabc.RV("norm", 0, 100))
        ]

        self.parameters = {'lambda_P': self.lambda_P, 'k_PQ': self.k_PQ, 'k_QP_P': self.k_QP_P,
                           'delta_QP': self.delta_QP, 'gamma': self.gamma, 'KDE': self.KDE}

    def model(self, parameters):
        data = {}
        data['dCdt'] = -parameters['KDE'] * self.C
        data['dPdt'] = parameters['lambda_P'] * self.P * (1 - self.P_Q_QP / self.K) + parameters['k_QP_P'] * self.QP - \
                       parameters['k_PQ'] * self.P - parameters['gamma'] * self.C * parameters['KDE'] * self.P
        data['dQdt'] = parameters['k_PQ'] * self.P - parameters['gamma'] * self.C * parameters['KDE'] * self.Q
        data['dQPdt'] = parameters['gamma'] * self.C * parameters['KDE'] * self.Q - parameters['k_QP_P'] * self.QP - \
                        parameters['delta_QP'] * self.QP

        self.C = data['dCdt']
        self.P = data['dPdt']
        self.QP = data['dQPdt']
        self.Q = data['dQdt']
        self.P_Q_QP = self.P + self.Q + self.QP

        return data

    def distance(self, x, y):
        return abs(x["data"] - y["data"])

    def parameters_inference(self):
        abc = pyabc.ABCSMC(self.model, self.parameter_priors, self.distance)

        db_path = ("sqlite:///" +
                   os.path.join(tempfile.gettempdir(), "test.db"))
        data = {'data': [1, 7, 41, 0]}
        abc.new(db_path, data)

        history = abc.run(minimum_epsilon=.1, max_nr_populations=10)

        fig, ax = plt.subplots()
        for t in range(history.max_t + 1):
            df, w = history.get_distribution(m=0, t=t)
            pyabc.visualization.plot_kde_1d(
                df, w,
                xmin=0, xmax=5,
                x="mean", ax=ax,
                label="PDF t={}".format(t))
        ax.axvline(data['dCdt'], color="k", linestyle="dashed")
        ax.legend()


if __name__ == '__main__':
    tumorGrowthModel = TumorGrowthModel(1, 20, 80, 0, 100, 0.1, 0.1, 0.05, 0.1, 0.3, 0.1)
    tumorGrowthModel.parameters_inference()
