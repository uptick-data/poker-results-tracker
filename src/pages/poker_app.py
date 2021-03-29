"""This page is for input of results"""
import datetime
import logging

import pandas as pd
import settings
import streamlit as st
from aggregate_functions.dropbox_functions import (
    backup_csv_file,
    read_csv_file,
    write_csv_file,
)
from aggregate_functions.sum_check_results import sum_checker

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def write():
    """Writes content to the app"""
    st.title("Write poker session results")

    # user input date
    user_input_date = st.text_input(
        "Date of game:", value=datetime.datetime.now().strftime("%Y-%m-%d"), key="1"
    )

    # user input venue
    user_input_venue = st.text_input("Location of game:", value="Loon", key="2")

    # user input venue
    input_num_hands = st.number_input("Number of hands played:", min_value=0, value=50, key="16")

    # ben
    input_result_ben = st.number_input(
        "Input Ben's result", min_value=-5000.0, value=0.0, key="3"
    )

    # liang
    input_result_liang = st.number_input(
        "Input Liang's result", min_value=-5000.0, value=0.0, key="4"
    )

    # loon
    input_result_loon = st.number_input(
        "Input Loon's result", min_value=-5000.0, value=0.0, key="5"
    )

    # seb
    input_result_seb = st.number_input(
        "Input Seb's result", min_value=-5000.0, value=0.0, key="6"
    )

    # shuming
    input_result_shuming = st.number_input(
        "Input Shuming's result", min_value=-5000.0, value=0.0, key="7"
    )

    # yopo
    input_result_yopo = st.number_input(
        "Input Yopo's result", min_value=-5000.0, value=0.0, key="8"
    )

    # yuheng
    input_result_yuheng = st.number_input(
        "Input Yuheng's result", min_value=-5000.0, value=0.0, key="8"
    )

    # KA
    input_result_ka = st.number_input(
        "Input Uncle KA's result", min_value=-5000.0, value=0.0, key="9"
    )

    # russell
    input_result_russ = st.number_input(
        "Input Russ's result", min_value=-5000.0, value=0.0, key="10"
    )

    # yj
    input_result_yj = st.number_input(
        "Input Uncle YJ's result", min_value=-5000.0, value=0.0, key="11"
    )

    # leo
    input_result_leo = st.number_input(
        "Input Leo's result", min_value=-5000.0, value=0.0, key="12"
    )

    # kc
    input_result_kc = st.number_input(
        "Input Uncle KC's result", min_value=-5000.0, value=0.0, key="13"
    )

    # francis
    input_result_francis = st.number_input(
        "Input Uncle Francis's result", min_value=-5000.0, value=0.0, key="14"
    )

    # tushit
    input_result_tushit = st.number_input(
        "Input Tushit's result", min_value=-5000.0, value=0.0, key="15"
    )

    results, results_string, list_results = sum_checker(
        input_result_ben,
        input_result_liang,
        input_result_loon,
        input_result_seb,
        input_result_shuming,
        input_result_yopo,
        input_result_yuheng,
        input_result_ka,
        input_result_yj,
        input_result_leo,
        input_result_kc,
        input_result_francis,
        input_result_tushit,
        input_result_russ,
    )

    st.write("net balance of wins and losses: ", results)
    st.write("need a recount: ", results_string)

    # get dataframe
    current_session_df = (
        pd.DataFrame({"user_name": settings.list_user_names, "result": list_results})
        .pipe(lambda x: x.assign(date=pd.to_datetime(user_input_date)))
        .pipe(lambda x: x.assign(place=user_input_venue))
        .pipe(lambda x: x.assign(year=x.date.dt.year))
        .pipe(lambda x:x.assign(num_hands=input_num_hands))[
            ["date", "year", "place", "user_name", "result", "num_hands"]
        ]
    )

    # backup master file to today's session date
    session_date = pd.to_datetime(user_input_date).strftime("%Y%m%d")
    backup_csv_file(settings.master_file_directory, settings.master_file, session_date)

    # append to master file, read from dropbox
    new_master_df = (
        read_csv_file(settings.master_file_directory, settings.master_file)
        .append(current_session_df)
        .sort_values(["date", "user_name"])
        .drop_duplicates()
        .groupby(["date", "year", "place", "user_name"])
        .agg({"result": "sum", "num_hands":"max"})
        .reset_index()
    )

    # write final file to dropbox
    write_csv_file(settings.master_file_directory, settings.master_file, new_master_df)

    # revert back to previous version

    st.write(new_master_df)


if __name__ == "__main__":
    write()
