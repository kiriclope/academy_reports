import matplotlib.pyplot as plt
from matplotlib import ticker


def plot_latency_first_correct(df):
    # 3 PLOT: latency to the first correct poke & PC
    # LATENCY
    ax1 = plt.subplot2grid((1600, 50), (1150, 1), rowspan=450, colspan=25)

    plt.plot(df.trial, df.side_response_latency, color="mediumvioletred", label="Side")
    plt.plot(df.trial, df.centre_response_latency, color="black", label="Centre")

    # Personalizzazione dei ticks sull'asse y

    custom_yticks = [
        0,
        1,
        10,
        20,
        50,
        100,
        200,
        250,
        300,
    ]  # I valori che desideri mostrare sull'asse y
    ax1.set_yscale("log")
    ax1.set_yscale("log")
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: "{:g}".format(y)))

    for y in custom_yticks:
        plt.axhline(y=y, linestyle="--", color="lightgray", alpha=0.7)

    # Aggiungi titoli e etichette
    plt.legend()
    plt.title("Latency to fist correct poke")
    plt.xlabel("Trial")
    plt.ylabel("Latency (s)")

    plt.legend(loc="upper right", bbox_to_anchor=(1, -0.2))
