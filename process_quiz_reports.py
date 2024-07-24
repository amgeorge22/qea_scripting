import pandas as pd  # pylint: disable=import-error
import os

DIRECTORY_PATH = "."  # just looking in current directory
homework_dict = {
    "Homework 1.csv": ["Homework 1 Quiz.csv", "Homework 1 Survey.csv"],
    "Homework 2.csv": ["Homework 2 Quiz.csv", "Homework 2 Survey.csv"],
    "Homework 3.csv": ["Homework 3 Quiz.csv", "Homework 3 Survey.csv"],
    "Homework 4.csv": ["Homework 4 Quiz.csv", "Homework 4 Survey.csv"],
    "Homework 5.csv": ["Homework 5 Quiz.csv", "Homework 5 Survey.csv"],
    "Homework 6.csv": ["Homework 6 Quiz.csv", "Homework 6 Survey.csv"],
    "Homework 7.csv": ["Homework 7 Quiz.csv", "Homework 7 Survey.csv"],
    "Homework 8.csv": ["Homework 8 Quiz.csv", "Homework 8 Survey.csv"],
    "Homework 9.csv": ["Homework 9 Quiz.csv", "Homework 9 Survey.csv"],
    "Homework 10.csv": ["Homework 10 Quiz.csv", "Homework 10 Survey.csv"],
}


def process_reports_with_quiz(quiz_csv, survey_csv, combined_csv):
    """
    Consolidate survey and quiz reports into one csv, remove unimportant information

    Args:
        quiz_csv: string that represents the file path to a quiz report csv
        survey_csv: string that represents the file path to a survey report csv
        combined_csv: string that represents the name of the consolidated report

        ^^^ All strings must end with .csv
    """
    quiz = pd.read_csv(quiz_csv)
    survey = pd.read_csv(survey_csv)
    extra_question = ["1", "2", "4", "5"]
    found = False
    for report_num in extra_question:
        if report_num in quiz_csv:
            print("Report 1-5")
            dropped_columns = (
                list(range(2, 7)) + (list(range(8, 15, 2))) + list(range(16, 22))
            )
            found = True
            break
        elif "3" in quiz_csv:
            print("Report 3")
            dropped_columns = (
                list(range(2, 7))
                + (list(range(8, 13, 2)))
                + (list(range(13, 14)))
                + (list(range(14, 19, 2)))
                + list(range(19, 24))
            )
            found = True
            break
    if not found:
        print("Report 6-10")
        dropped_columns = (
            list(range(2, 7)) + (list(range(8, 17, 2))) + list(range(17, 20))
        )
    survey = survey.drop(survey.columns[dropped_columns], axis=1)

    #### Remove numbers from headers ########
    rename_columns = list(range(2, 7))
    for col in rename_columns:
        old_content = survey.columns[col]
        # remove ID
        new_content = "".join([i for i in old_content if not i.isdigit()])[2:]
        survey = survey.rename(columns={old_content: new_content})
    print("Reformatted Successfully")

    merged_df = pd.merge(survey, quiz, on="id", how="inner")
    merged_df.to_csv(combined_csv, index=False)
    print(f"{survey_csv} merge complete")


def remove_csv(file):
    """
    Remove input file (if it exists) from directory

    Args:
        file: a String that represents the file to be removed
    """
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        # print("file deleted")
    else:
        print("file not found")


def create_assignment_reports():
    """Create consolidated survey/quiz reports and clean up directory"""
    for homework_path, file_paths in homework_dict.items():
        quiz_path = file_paths[0]
        survey_path = file_paths[1]
        if os.path.exists(quiz_path) and os.path.isfile(quiz_path):
            process_reports_with_quiz(quiz_path, survey_path, homework_path)
            remove_csv(quiz_path)
            remove_csv(survey_path)


def concatenate_csvs(directory_path, final_csv):
    """
    Takes all the assignment reports and consolidates them into one final csv

    Args:
        directory_path: A String representing the directory the assignment reports are in
        final_csv: A String that is the name of the csv for the consolidated reports; must end with .csv
    """
    # List to hold dataframes
    df_list = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            # Read the CSV file
            df = pd.read_csv(file_path)
            # Add a new column with the filename
            assignment_name = filename[:-4]
            df["Assignment"] = assignment_name
            # Append the dataframe to the list
            df_list.append(df)
            remove_csv(filename)

    # Concatenate all dataframes in the list
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv(final_csv, index=False)


def un_dateify(date):
    """Add an apostrophe before a value that would be interpreted as a date by Excel"""
    return "'" + date


def undo_dates(file):
    """
    Edit values in the consolidated report that would be viewed as dates by Excel

    Args:
        file: A string representing the file name of consolidated assignment reports; must end with .csv
    """
    reports = pd.read_csv(file)
    col = 6  # Column that numbers are in
    col_name = reports.columns[col]
    reports[col_name] = reports[col_name].apply(un_dateify)
    reports.to_csv(file, index=False)


def main():
    """Main method"""
    create_assignment_reports()
    report_csv = "Consolidated Reports.csv"
    remove_csv(report_csv)
    concatenate_csvs(DIRECTORY_PATH, report_csv)
    undo_dates(report_csv)


if __name__ == "__main__":
    main()
