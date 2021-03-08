"""This page is for input of results"""
import datetime
import logging

import numpy as np
import pandas as pd
import plotly.express as px
import settings
import streamlit as st
from aggregate_functions.dropbox_functions import read_csv_file

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def write():
    """Writes content to the app"""
    st.title("Poker result charts and table")

    # read csv
    df = read_csv_file(settings.master_file_directory, settings.master_file)

    # filter out sessions that are all zeros
    df_non_zero = (
        df
        .groupby(["date", "result"])
        .agg({"place":"count","user_name":"nunique"})
        .reset_index()
        .pipe(lambda x:x.assign(percentage_zeros = x.place/x.user_name))
        .pipe(lambda x:x.assign(is_exclude_date = np.where(
            (x.percentage_zeros >= 0.75) & (x.result == 0), 1, 0
        )))
        .query("is_exclude_date != 1")
        [["date"]]
        .drop_duplicates()
    )

    df = (
        df
        .merge(df_non_zero, how="inner", on=['date'])
        .pipe(lambda x:x.assign(is_win = np.where(x.result >= 0.02, 1, 0)))
    )

    # cumulative results overtime
    df_cumulative = df.sort_values(["user_name", "date"])
    df_cumulative["cumsum_result"] = df_cumulative.groupby(
        "user_name"
    ).result.transform(np.cumsum)

    # top results as of today
    df_top = (
        df
        .query("result != 0")
        .groupby(["user_name"])
        .agg({"result": "sum", "date": "nunique", "is_win": "sum"})
        .reset_index()
        .pipe(lambda x: x.assign(avg_per_session=x.result / x.date))
        .rename(columns={"date": "num_sessions"})
        .sort_values(["result", "avg_per_session"], ascending=False)
        .reset_index(drop=True)
        .pipe(lambda x:x.assign(win_rate = x.is_win/x.num_sessions))
        .drop(['is_win'], 1)
        [['user_name', 'result', 'num_sessions', 'win_rate', 'avg_per_session']]
    )

    # get total number of sessions
    total_num_sessions = range(df_top.num_sessions.max()+1)[1:]

    st.text("Top 8 results as of today, " + str(datetime.datetime.now()))
    is_remove_few = st.selectbox("Select players with >= number of sessions?", tuple(total_num_sessions))

    df_top_filter = (
        df_top
        # .query(f"num_sessions >= '{is_remove_few}'")
        .query("num_sessions >= " + str(is_remove_few))
        .reset_index(drop=True)
    )
    st.write(df_top_filter.head(8))

    # get all dates
    list_of_dates = ["All"]
    for i in df.date.unique():
        temp_date = pd.to_datetime(i).strftime("%Y-%m-%d")
        list_of_dates.append(temp_date)

    # get specific week session
    option = st.selectbox("Which week would you like to see?", tuple(list_of_dates))

    if option == "All":
        result_df = pd.pivot_table(
            df,
            index="user_name",
            columns=["date"],
            values="result",
            aggfunc="sum",
            fill_value=0,
        ).reset_index()

        result_df["total_sum"] = result_df.sum(axis=1)
        result_df.sort_values(["total_sum"], ascending=False, inplace=True)
    else:
        result_df = pd.pivot_table(
            df.query(f"date == '{option}'"),
            index="user_name",
            columns=["date"],
            values="result",
            aggfunc="sum",
            fill_value=0,
        ).reset_index()

        result_df["total_sum"] = result_df.sum(axis=1)
        result_df.sort_values(["total_sum"], ascending=False, inplace=True)

    st.write(result_df)

    # plot chart of results overtime
    fig = px.line(
        df, x="date", y="result", color="user_name", title="Results for each Session"
    )
    st.plotly_chart(fig)

    # plot chart of results overtime
    fig_cumsum = px.line(
        df_cumulative,
        x="date",
        y="cumsum_result",
        color="user_name",
        title="Cumulative results overtime",
    )
    st.plotly_chart(fig_cumsum)


if __name__ == "__main__":
    write()
