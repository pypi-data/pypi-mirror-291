import numpy as np
import pandas as pd

from .pi_hat import pi_hat_sreg, pi_hat_creg
from .lin_adj import lin_adj_sreg, lin_adj_creg
#-------------------------------------------------------------------
# %#     Function that implements \hat{\tau} --
# %#     i.e. the ATE estimator
#-------------------------------------------------------------------

def tau_hat_sreg(Y, S, D, X=None, model=None):
    tau_hat = np.zeros(np.max(D))
    for d in range(1, np.max(D) + 1):
        if X is not None:
            data = pd.DataFrame({'Y': Y, 'S': S, 'D': D})
            X_df = pd.DataFrame(X)
            data = pd.concat([data, X_df], axis=1)
            data['pi'] = pi_hat_sreg(S, D)[:, d-1]
            data['pi_0'] = pi_hat_sreg(S, D, inverse=True)[:, 0]
            data['A'] = np.where(D == d, 1, np.where(D == 0, 0, -999999))
            data['I'] = (data['A'] != -999999).astype(int)
            mu_hat_d = lin_adj_sreg(d, data['S'], data.iloc[:, 3:(3+X.shape[1])], model)
            mu_hat_0 = lin_adj_sreg(0, data['S'], data.iloc[:, 3:(3+X.shape[1])], model)
            Ksi_vec = data['I'] * (((data['A'] * (data['Y'] - mu_hat_d)) / data['pi']) -
                                   (((1 - data['A']) * (data['Y'] - mu_hat_0)) / data['pi_0'])) + \
                                   (mu_hat_d - mu_hat_0)
            tau_hat[d-1] = np.mean(Ksi_vec)
        else:
            data = pd.DataFrame({'Y': Y, 'S': S, 'D': D})
            data['pi'] = pi_hat_sreg(S, D)[:, d-1]
            data['pi_0'] = pi_hat_sreg(S, D, inverse=True)[:, 0]
            data['A'] = np.where(D == d, 1, np.where(D == 0, 0, -999999))
            data['I'] = (data['A'] != -999999).astype(int)
            mu_hat_d = 0
            mu_hat_0 = 0
            Ksi_vec = data['I'] * (((data['A'] * (data['Y'] - mu_hat_d)) / data['pi']) -
                                   (((1 - data['A']) * (data['Y'] - mu_hat_0)) / data['pi_0'])) + \
                                   (mu_hat_d - mu_hat_0)
            tau_hat[d-1] = np.mean(Ksi_vec)
    return tau_hat


def tau_hat_creg(Y, S, D, G_id, Ng, X=None, model=None):
    tau_hat_vec = np.zeros(np.max(D))
    Y_bar_g_list = [None] * np.max(D)
    mu_hat_list = [None] * np.max(D)
    pi_hat_list = [None] * np.max(D)
    data_list = [None] * np.max(D)
    
    if X is not None:
        cl_lvl_data = model['cl_lvl_data'].copy() 
        data = cl_lvl_data.copy()
        Ng_full = data['Ng']
        Y_bar_full = data['Y_bar']
        for d in range(1, np.max(D) + 1):
            data['pi'] = pi_hat_creg(data['S'], data['D'])[:, d-1]
            data['pi_0'] = pi_hat_creg(data['S'], data['D'], inverse=True)[:, 0]
            data['A'] = np.where(data['D'] == d, 1, np.where(data['D'] == 0, 0, -999999))
            data['I'] = (data['A'] != -999999).astype(int)
            data_list[d-1] = data.copy()
            pi_hat_list[d-1] = data['pi'].copy()

            mu_hat_d = lin_adj_creg(d, model['cl_lvl_data'], model)
            mu_hat_0 = lin_adj_creg(0, model['cl_lvl_data'], model)

            Xi_g = data['I'] * (((data['A'] * (Y_bar_full * data['Ng'] - mu_hat_d)) / data['pi']) -
                                (((1 - data['A']) * (Y_bar_full * data['Ng'] - mu_hat_0)) / data['pi_0'])) + \
                                (mu_hat_d - mu_hat_0)

            mu_hat_list[d-1] = np.column_stack((mu_hat_0, mu_hat_d))

            tau_hat = np.mean(Xi_g) / np.mean(Ng_full)
            tau_hat_vec[d-1] = tau_hat

        rtrn_list = {
            "tau_hat": tau_hat_vec,
            "mu_hat": mu_hat_list,
            "pi_hat": pi_hat_list,
            "pi_hat_0": data['pi_0'],
            "data_list": data_list,
            "Y_bar_g": Y_bar_full,
            "Ng": Ng_full
        }
    else:
        working_df = pd.DataFrame({'Y': Y, 'S': S, 'D': D, 'G_id': G_id})
        if Ng is None:
            working_df['Ng'] = working_df.groupby('G_id')['G_id'].transform('size')
        else:
            working_df['Ng'] = Ng
        Y_bar_full = working_df.groupby('G_id')['Y'].mean().values
        cl_lvl_data = working_df.drop_duplicates(subset=['G_id', 'D', 'S', 'Ng'])
        Ng_full = cl_lvl_data['Ng'].values

        for d in range(1, np.max(D) + 1):
            data = cl_lvl_data.copy()
            data['pi'] = pi_hat_creg(data['S'].values, data['D'].values)[:, d-1]
            data['pi_0'] = pi_hat_creg(data['S'].values, data['D'].values, inverse=True)[:, 0]
            data['A'] = np.where(data['D'] == d, 1, np.where(data['D'] == 0, 0, -999999))
            data['I'] = (data['A'] != -999999).astype(int)
            data_list[d-1] = data
            pi_hat_list[d-1] = data['pi']

            mu_hat_d = 0
            mu_hat_0 = 0

            Xi_g = data['I'] * (((data['A'] * (Y_bar_full * data['Ng'] - mu_hat_d)) / data['pi']) -
                                (((1 - data['A']) * (Y_bar_full * data['Ng'] - mu_hat_0)) / data['pi_0'])) + \
                                (mu_hat_d - mu_hat_0)

            mu_hat_list[d-1] = np.column_stack((mu_hat_0, mu_hat_d))

            tau_hat = np.mean(Xi_g) / np.mean(Ng_full)
            tau_hat_vec[d-1] = tau_hat

        rtrn_list = {
            "tau_hat": tau_hat_vec,
            "mu_hat": mu_hat_list,
            "pi_hat": pi_hat_list,
            "pi_hat_0": data['pi_0'],
            "data_list": data_list,
            "Y_bar_g": Y_bar_full,
            "Ng": Ng_full
        }
    
    return rtrn_list
