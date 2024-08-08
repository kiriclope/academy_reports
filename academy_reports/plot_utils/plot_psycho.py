import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.special import erf

def plot_psychometrics(df):

    # 5 PLOT: PSICOMETRIV ON vs OFF
    df_light_off = df[(df['iti_duration'] >= 6) & (df['opto_bool'] == 0)]
    df_light_on = df[(df['iti_duration'] >= 6) & (df['opto_bool'] == 1)]

    axes = plt.subplot2grid((1600, 50), (1150, 30), rowspan=450, colspan=22)

    # Define the probit function
    def probit(x, beta, alpha):
        return 0.5 * (1 + erf((beta * x + alpha) / np.sqrt(2)))

    # Preparazione dei dati
    df_light_off = df_light_off.copy()  # Evita SettingWithCopyWarning
    df_light_off.loc[:, 'probability_l'] = 1 - df_light_off['probability_r']
    df_light_off.loc[:, 'probability_r'] = df_light_off['probability_r'].astype(float)
    df_light_off.loc[:, 'first_trial_response'] = df_light_off['first_trial_response'].apply(
        lambda x: 1 if x == 'right' else 0)

    df_light_on = df_light_on.copy()  # Evita SettingWithCopyWarning
    df_light_on.loc[:, 'probability_r'] = df_light_on['probability_r'].astype(float)
    df_light_on.loc[:, 'first_trial_response'] = df_light_on['first_trial_response'].apply(
        lambda x: 1 if x == 'right' else 0)

    # Calcolo delle frequenze delle scelte a destra per df_light_off
    probs_off = np.sort(df_light_off['probability_r'].unique())
    right_choice_freq_off = []

    for prob in probs_off:
        indx_blk = df_light_off['probability_r'] == prob
        sum_prob = np.sum(indx_blk)
        if sum_prob > 0:
            indx_blk_r = indx_blk & (df_light_off['first_trial_response'] == 1)
            sum_choice_prob = np.sum(indx_blk_r)
            right_choice_freq_off.append(sum_choice_prob / sum_prob)
        else:
            right_choice_freq_off.append(0)

    # Calcolo delle frequenze delle scelte a destra per df_light_on
    probs_on = np.sort(df_light_on['probability_r'].unique())
    right_choice_freq_on = []

    for prob in probs_on:
        indx_blk = df_light_on['probability_r'] == prob
        sum_prob = np.sum(indx_blk)
        if sum_prob > 0:
            indx_blk_r = indx_blk & (df_light_on['first_trial_response'] == 1)
            sum_choice_prob = np.sum(indx_blk_r)
            right_choice_freq_on.append(sum_choice_prob / sum_prob)
        else:
            right_choice_freq_on.append(0)

    # Adatta le curve probit
    pars_off, _ = curve_fit(probit, df_light_off['probability_r'], df_light_off['first_trial_response'], p0=[0, 1])
    pars_on, _ = curve_fit(probit, df_light_on['probability_r'], df_light_on['first_trial_response'], p0=[0, 1])

    # Impostazioni del grafico

    x = np.linspace(0, 1, 100)

    # Disegna le curve di adattamento probit
    axes.plot(x, probit(x, *pars_off), label='Off' ,color='black', alpha=0.5, linewidth=3)
    axes.plot(x, probit(x, *pars_on), label='On', color='steelblue', alpha=0.5, linewidth=3)

    # Disegna lo scatter plot delle frequenze calcolate per Light Off
    axes.scatter(probs_off, right_choice_freq_off, marker='o', color='black', alpha=0.5, s=10)

    # Disegna lo scatter plot delle frequenze calcolate per Light On
    axes.scatter(probs_on, right_choice_freq_on, marker='o', color='steelblue', alpha=0.5, s=10)

    # Impostazioni aggiuntive del grafico
    axes.set_ylim(0, 1)
    axes.axhline(0.5, color='gray', linestyle='--', alpha=0.3)
    axes.axvline(0.5, color='gray', linestyle='--', alpha=0.3)
    axes.set_xlabel('Probability Type')
    axes.set_ylabel('Right Choice Rate')
    axes.legend()
