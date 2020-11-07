import _py_abc as pyabc

'''
P - proliferative tissue, tumor tissue
Q - non-proliferative tissue
C - drug concentration
QP - DNA-damaged Q tissue by the drug impact
KDE - constant rate of the decay of the PCV concentration

lambda_P - growth rate of P
gamma_P - damages in P tissue caused by the drug
gamma_Q - damages in Q tissue caused by the drug
k_QP_P - constant rate of transfer from QP to P tissue
delta_QP - constant rate of elimination of QP tissue
k_P_Q - constant rate of transfer from P to Q tissue
K - maximal tumor size

dCdt = -KDE * C
dPdt = lambda_P * P*(1 - P'/K) + k_QP_P * QP - k_P_Q * P - gamma_P * C * KDE * P
dQdt = k_PQ * P - gamma_Q * C * KDE * Q
dQPdt = gamma_Q * C * KDE * Q - k_QP_P * QP - delta_QP * Q_P
P' = P + Q + QP
 

'''



class TumorGrowthModel:

    def __init__(self, ):

