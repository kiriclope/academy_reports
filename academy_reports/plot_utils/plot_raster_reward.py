import numpy as np
import matplotlib.pyplot as plt

def plot_raster_reward(df):
    # 2 PLOT: computed probability

    axes = plt.subplot2grid((1600, 50), (600, 1), rowspan=400, colspan=90)
    df['first_response_center'] = df['center_poke_in'].str.split(',').str[0].astype(float)

    #calculate missing and omission per port
    column_names = ['trial', 'side','correct_outcome_int', 'first_response_left', 'first_response_center', 'first_response_right']
    omission_df = df[column_names].copy()
    # replace all nans with 0
    omission_df = omission_df.replace(np.nan, 0)

    #OMISSION
    #general omission: no response in centre and side ports (it's at the same time a central omission).
    omission_df['general_omission'] = (
            (omission_df['first_response_left'] == 0) &
            (omission_df['first_response_right'] == 0) &
            (omission_df['first_response_center'] == 0)
    ).astype(int)
    # left omission: no response in left port when reward it's on side left, and no response in right port too.
    omission_df['left_omission'] = np.where(
        (omission_df['side'] == "left") &
        (omission_df['first_response_left'] == 0) &
        (omission_df['first_response_right'] == 0) &
        (omission_df['first_response_center'] != 0),
        1,  # true
        0  # false
    )
    # right omission: no response in right port when reward it's on side right, and no response in right port too.
    omission_df['right_omission'] = np.where(
        (omission_df['side'] == "right") &
        (omission_df['first_response_left'] == 0) &
        (omission_df['first_response_right'] == 0) &
        (omission_df['first_response_center'] != 0),
        1,  # true
        0  # false
    )



    # Lista per raccogliere le probabilità

    df['rolling_prob'] = df['correct_outcome_int'].rolling(window=5, min_periods=1).mean()


    # Creazione del subplot con dimensioni specifiche nella griglia (1600, 50)

    line_data = df['rolling_prob']
    df['probability_l'] = 1-df['probability_r']

    # Add the new column 'highest_probability' which combines the values
    df['highest_probability'] = df.apply(
        lambda row: row['probability_r'] if row['probability_r'] > 0.5 else row['probability_l'], axis=1
    )

    plt.plot(df['highest_probability'], '-', color='black', linewidth=1, alpha= 0.7)

    # Imposta i limiti dell'asse y con un margine più ampio
    axes.set_ylim(-0.5, 1.5)

    # Imposta i valori delle tacche sull'asse y
    axes.set_yticks([0, 0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 1])
    plt.axhline(y=1, linestyle='solid', color='black', alpha=0.7)
    plt.axhline(y=0.5, linestyle='--', color='lightgray', alpha=0.7)
    plt.axhline(y=0, linestyle= 'solid', color='black', alpha=0.7)

    # Grafico a linee

    axes.plot(df.trial, line_data, linewidth=2, color='orange')

    column = ['trial', 'side', 'correct_outcome_int','first_response_left', 'first_response_right']
    first_lick_df = df[column].copy()

    conditions = [
        (first_lick_df.first_response_left == 0) & (first_lick_df.first_response_right == 0),
        first_lick_df.first_response_left == 0,
        first_lick_df.first_response_right == 0,
        first_lick_df.first_response_left <= first_lick_df.first_response_right,
        first_lick_df.first_response_left > first_lick_df.first_response_right,
    ]

    choices = ["no_response",
               "right",
               "left",
               "left",
               "right"]

    # create a new column in the DF based on the conditions

    first_lick_df["first_trial_response"] = np.select(conditions, choices)

    # Crea la colonna 'first_resp_left'
    first_lick_df["first_resp_left"] = first_lick_df["first_trial_response"].apply(lambda x: 1 if x == "left" else 0)

    # Crea la colonna 'first_resp_right'
    first_lick_df["first_resp_right"] = first_lick_df["first_trial_response"].apply(lambda x: 1 if x == "right" else 0)

    # Trova le posizioni dei tick per 'left' e 'right'
    left_ticks = first_lick_df[first_lick_df["first_resp_left"] == 1].index
    right_ticks = first_lick_df[first_lick_df["first_resp_right"] == 1].index

    # Plotta i tick marks per 'left' e 'right'
    for i, row in first_lick_df.iterrows():
        # Determina la dimensione del marker in base alla corrispondenza
        markersize = 15 if row["first_resp_left"] == row["correct_outcome_int"] else 5
        y_coord = 1.15 if markersize == 15 else -0.15

        # Per 'left'
        if row["first_resp_left"] == 1:
            axes.plot(i, y_coord, marker='|', color='green', markersize=markersize)

    for i, row in first_lick_df.iterrows():
        # Determina la dimensione del marker in base alla corrispondenza
        markersize = 15 if row["first_resp_right"] == row["correct_outcome_int"] else 5
        y_coord = 1.15 if markersize == 15 else -0.15

    # Per 'right'
        if row["first_resp_right"] == 1:
            axes.plot(i, y_coord, marker='|', color='purple', markersize=markersize)

    # Identifica i punti in cui l'indice di blocco cambia
    block_changes = df['Block_index'].diff().fillna(0).abs()
    change_points = df[block_changes > 0].index

    # Itera su ciascun blocco unico
    for block in df['Block_index'].unique():
        block_data = df[df['Block_index'] == block]
        start = block_data['trial'].min()  # Inizio del blocco
        end = block_data['trial'].max()  # Fine del blocco

    # Aggiungi linee tratteggiate per ogni cambio di blocco
    for point in change_points:
        axes.axvline(x=point, color='gray', linestyle='--')

    selected_trials = df.trial[::19]  # 20 trial
    axes.set_xticks(selected_trials)
    axes.set_xticklabels(selected_trials)
    axes.set_xlabel('trial')
    axes.set_ylabel('P(reward)')
    plt.title('Probability Rewarded trials', pad=20)
