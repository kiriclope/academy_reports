# import warnings
# warnings.filterwarnings("ignore")

import os
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages

from academy_reports import settings, utils
from academy_reports.helpers import (
    generate_water_calibration_plot,
    get_intersessions,
    get_save_path,
)
from academy_reports.plot_utils.daily_reports import generate_daily_reports


def daily_reports_to_pdf(verbose=0):
    raw_paths = utils.path_generator(settings.data_directory, ".csv")

    if verbose:
        print(raw_paths)

    # dfs = []

    for path in raw_paths:
        if verbose:
            print("path", path)

        # sort, only analyze general csvs
        subject = os.path.basename(path)
        # remove .csv
        subject, ext = os.path.splitext(subject)

        if verbose:
            print("subject", subject)

        if verbose:
            print("saving to", save_directory)

        df = pd.read_csv(path, sep=";")

        # if verbose:
        #     print('df', df.keys())
        # dfs.append(df)

        save_directory = settings.save_directory + "/" + subject
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        if verbose:
            print("settings", settings.save_directory)

        if "water" in path:
            generate_water_calibration_plot()
        elif "B10" in path:
            get_intersessions(df, subject, save_directory)
        else:
            save_path = get_save_path(df, save_directory, verbose=verbose)

            if verbose:
                print("save_path", save_path)

            generate_daily_reports(df)

            pdf_pages = PdfPages(save_path)
            pdf_pages.savefig()
            pdf_pages.close()


if __name__ == "__main__":
    daily_reports_to_pdf()
