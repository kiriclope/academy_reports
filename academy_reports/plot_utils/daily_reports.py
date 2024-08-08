import traceback

from academy_reports.plot_utils.preprocess import preprocess_df
from academy_reports.plot_utils.plot_raster_choice import plot_raster_right_choice
from academy_reports.plot_utils.plot_raster_reward import plot_raster_reward
from academy_reports.plot_utils.plot_latency import plot_latency_first_correct
from academy_reports.plot_utils.plot_psycho import plot_psychometrics


def generate_daily_reports(df):
    try:
        df = preprocess_df(df)
    except Exception as exc:
        print("### ERROR PREPROCESSING DATAFRAME ###")
        print(traceback.format_exc())

    try:
        plot_raster_right_choice(df)
    except Exception as exc:
        print("### ERROR PLOTTING RASTER RIGHT CHOICE ###")
        print(traceback.format_exc())

    try:
        plot_raster_reward(df)
    except Exception as exc:
        print("### ERROR PLOTTING RASTER REWARD ###")
        print(traceback.format_exc())

    try:
        plot_latency_first_correct(df)
    except Exception as exc:
        print("### ERROR PLOTTING LATENCY ###")
        print(traceback.format_exc())

    try:
        plot_psychometrics(df)
    except Exception as exc:
        print("### ERROR PLOTTING PSYCHO CURVES ###")
        print(traceback.format_exc())
