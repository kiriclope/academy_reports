import numpy as np
import matplotlib.pyplot as plt


def plot_raster_right_choice(df):
    # Lista per raccogliere le probabilità
    df["rolling_prob"] = (
        df["correct_outcome_int"].rolling(window=5, min_periods=1).mean()
    )

    prob_colums = df[["trial", "side", "first_trial_response", "correct_outcome_int"]]
    prob_df = prob_colums.copy()
    # prob_df["right_rewards"] = ((prob_df['side'] == 'right') & (prob_df['correct_outcome_int'] == 1)).astype(int)
    #
    # prob_df['rolling_avg_right_reward'] = prob_df["right_rewards"].rolling(window=5, min_periods=1).mean()

    prob_df["right_rewards"] = (prob_df["first_trial_response"] == "right").astype(int)
    prob_df["rolling_avg_right_reward"] = (
        prob_df["right_rewards"].rolling(window=5, min_periods=1, center=True).mean()
    )

    # Creazione del subplot con dimensioni specifiche nella griglia (1600, 50)
    ax = plt.subplot2grid((1600, 50), (1, 1), rowspan=450, colspan=90)

    plt.plot(df["probability_r"], "-", color="black", linewidth=1, alpha=0.7)

    # Higlight trials in which opto light is ON

    # Condizione specifica
    condition = (df["opto_bool"] == True) & (df["iti_duration"] > 6)

    # Filtraggio dei trial basato sulla condizione
    filtered_trials = df["trial"][condition]

    # Filtra i trial basati sulla condizione 'right' e 'not right'
    filtered_trials_right = filtered_trials[df["first_trial_response"] == "right"]
    filtered_trials_not_right = filtered_trials[df["first_trial_response"] != "right"]

    # Plot per 'right' responses
    plt.plot(
        filtered_trials_right,
        [1] * len(filtered_trials_right),
        "|",
        markersize=7,
        color="blue",
        label="First Trial Response = Right",
    )

    # Plot per non 'right' responses
    plt.plot(
        filtered_trials_not_right,
        [0] * len(filtered_trials_not_right),
        "|",
        markersize=7,
        color="blue",
        label="First Trial Response != Right",
    )

    # Imposta i limiti dell'asse y con un margine più ampio
    ax.set_ylim(-0.5, 1.5)

    # Imposta i valori delle tacche sull'asse y
    ax.set_yticks([0, 0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 1])
    plt.axhline(y=1, linestyle="solid", color="black", alpha=0.7)
    plt.axhline(y=0.5, linestyle="--", color="lightgray", alpha=0.7)
    plt.axhline(y=0, linestyle="solid", color="black", alpha=0.7)

    # Grafico a linee

    line_data = prob_df["rolling_avg_right_reward"]
    ax.plot(df.trial, line_data, linewidth=2, color="mediumturquoise")

    column = [
        "trial",
        "side",
        "correct_outcome_int",
        "first_response_left",
        "first_response_right",
    ]
    first_lick_df = df[column].copy()

    conditions = [
        (first_lick_df.first_response_left == 0)
        & (first_lick_df.first_response_right == 0),
        first_lick_df.first_response_left == 0,
        first_lick_df.first_response_right == 0,
        first_lick_df.first_response_left <= first_lick_df.first_response_right,
        first_lick_df.first_response_left > first_lick_df.first_response_right,
    ]

    choices = ["no_response", "right", "left", "left", "right"]
    # create a new column in the DF based on the conditions

    first_lick_df["first_trial_response"] = np.select(conditions, choices)

    # Crea la colonna 'first_resp_left'
    first_lick_df["first_resp_left"] = first_lick_df["first_trial_response"].apply(
        lambda x: 1 if x == "left" else 0
    )

    # Crea la colonna 'first_resp_right'
    first_lick_df["first_resp_right"] = first_lick_df["first_trial_response"].apply(
        lambda x: 1 if x == "right" else 0
    )

    # Trova le posizioni dei tick per 'left' e 'right'
    left_ticks = first_lick_df[first_lick_df["first_resp_left"] == 1].index
    right_ticks = first_lick_df[first_lick_df["first_resp_right"] == 1].index

    # Plotta i tick marks per 'left' e 'right'
    for i, row in first_lick_df.iterrows():
        # Determina la dimensione del marker in base alla corrispondenza
        markersize = 15 if row["first_resp_left"] == row["correct_outcome_int"] else 5
        y_coord = -0.35 if markersize == 5 else -0.15
        # Per 'left'
        if row["first_resp_left"] == 1:
            ax.plot(i, y_coord, marker="|", color="green", markersize=markersize)

    for i, row in first_lick_df.iterrows():
        # Determina la dimensione del marker in base alla corrispondenza
        markersize = 15 if row["first_resp_right"] == row["correct_outcome_int"] else 5
        y_coord = 1.35 if markersize == 5 else 1.15

        # Per 'right'
        if row["first_resp_right"] == 1:
            ax.plot(i, y_coord, marker="|", color="purple", markersize=markersize)

    # Identifica i punti in cui l'indice di blocco cambia
    block_changes = df["Block_index"].diff().fillna(0).abs()
    change_points = df[block_changes > 0].index

    # Itera su ciascun blocco unico
    for block in df["Block_index"].unique():
        block_data = df[df["Block_index"] == block]
        start = block_data["trial"].min()  # Inizio del blocco
        end = block_data["trial"].max()  # Fine del blocco
        block_center = (start + end) / 2  # Calcola il punto centrale del blocco
        block_prob = block_data["probability_r"].iloc[0]  # Probabilità del blocco

        # Scegli il colore in base alla probabilità
        if block_prob > 0.5:
            color = "purple"
        elif block_prob == 0.5:
            color = "grey"
        else:
            color = "green"

        # Disegna una linea orizzontale per il blocco e la probabilità
        ax.hlines(
            y=1.5, xmin=start, xmax=end, colors=color, linestyles="solid", linewidth=10
        )
        ax.text(
            block_center,
            1.6,
            f"{block_prob:.2f}",
            ha="center",
            va="center",
            backgroundcolor="white",
            fontsize=5,
        )

    # Aggiungi linee tratteggiate per ogni cambio di blocco
    for point in change_points:
        ax.axvline(x=point, color="gray", linestyle="--")

    ax.text(
        1.02,
        0.1,
        "L",
        ha="left",
        va="top",
        color="green",
        transform=ax.transAxes,
        fontsize=10,
    )

    # Posiziona la lettera 'R' appena fuori dal bordo destro del grafico
    ax.text(
        1.02,
        0.9,
        "R",
        ha="left",
        va="bottom",
        color="purple",
        transform=ax.transAxes,
        fontsize=10,
    )

    # Posiziona la lettera 'Light on' appena fuori dal bordo destro del grafico
    ax.text(
        1.02,
        0.74,
        "R ON",
        ha="left",
        va="bottom",
        color="blue",
        transform=ax.transAxes,
        fontsize=8,
    )

    # Posiziona la lettera 'Light on' appena fuori dal bordo destro del grafico
    ax.text(
        1.02,
        0.24,
        "L ON",
        ha="left",
        va="bottom",
        color="blue",
        transform=ax.transAxes,
        fontsize=8,
    )

    # Posiziona la lettera 'C' appena fuori dal bordo destro del grafico
    ax.text(
        1.02,
        0.45557,
        "C",
        ha="left",
        va="bottom",
        color="black",
        transform=ax.transAxes,
        fontsize=10,
    )

    selected_trials = df.trial[::19]  # 20 trial
    ax.set_xticks(selected_trials)
    ax.set_xticklabels(selected_trials)
    ax.set_xlabel("trial")
    ax.set_ylabel("P(right)")
    plt.title("Probability right reward", pad=20)
