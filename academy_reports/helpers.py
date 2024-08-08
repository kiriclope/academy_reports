import os
import traceback
import pandas as pd
from datetime import datetime

from academy_reports import settings
from report_tasks.water_calibration import report_water_calibration
from report_tasks.intersession import intersession
from report_tasks.temperature_reports import temperature_reports


def generate_water_calibration_plot():
    print("################################")
    print("Starting water calibration plot")

    try:
        calibration_path = (
            settings.calibration_path
        )  # the path is on the "setting" file

        df = pd.read_csv(calibration_path, sep=";")
        save_path = calibration_path[:-3] + "pdf"

        report_water_calibration(df, save_path)

        print("Water calibration plot succesfully done")

    except Exception as error:
        print(traceback.format_exc())
        print("Error in water calibration plot")


def get_intersessions(df, subject, save_directory):
    print("########################################")
    print("Starting intersession report " + str(subject))

    # file_name_intersession = subject + '_intersession.pdf'
    # save_path_intersession = os.path.join(save_directory, file_name_intersession)
    # intersession(df.copy(), save_path_intersession)
    # print('intersession correct for subject: ', str(subject))

    try:
        file_name_intersession = subject + "_intersession.pdf"
        save_path_intersession = os.path.join(save_directory, file_name_intersession)
        intersession(df.copy(), save_path_intersession)
        print("intersession correct for subject: ", str(subject))
    except:
        print(
            "Error performing the intersession for the subject: ",
            str(subject),
        )
        pass


def get_save_path(df, save_directory, verbose=0):
    print("########################################")
    print("Generating Daily Reports ...")

    subject = df.subject.iloc[0]
    task = df.task.iloc[0]
    stage = df.stage.iloc[0]

    if verbose:
        print("subject", subject, "task", task, "stage", stage)

    try:
        date = datetime.fromtimestamp(df.TRIAL_START.iloc[0]).strftime("%Y%m%d-%H%M%S")
    except:
        date = df.TRIAL_START.iloc[0]

    if verbose:
        print("date", date)

    file_name = subject + "_" + task + "-" + str(stage) + "_" + date + ".pdf"

    print("checking file: ", file_name)
    save_path = os.path.join(save_directory, file_name)

    return save_path
