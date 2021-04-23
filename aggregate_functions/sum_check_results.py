import pandas as pd
import numpy as np

def sum_checker(
    input_result_ben, input_result_liang,  input_result_loon,
    input_result_seb, input_result_shuming, input_result_yopo,
    input_result_yuheng, input_result_weisheng, input_result_ka, input_result_yj,
    input_result_leo, input_result_kc, input_result_francis,
    input_result_tushit, input_result_russ, input_result_pinshun,
):
    return_sum = (
        input_result_ben + input_result_liang + input_result_loon +
        input_result_seb + input_result_shuming +input_result_yopo +
        input_result_yuheng + input_result_weisheng + input_result_ka + input_result_yj +
        input_result_leo + input_result_kc + input_result_francis +
        input_result_tushit + input_result_russ + input_result_pinshun,
    )

    return_string = "nothing wrong, no need for recount"

    if abs(return_sum) >= 50:
        return_string = "sum dont add up, all players check count again"

    list_results = [
        input_result_ben, input_result_liang,  input_result_loon,
        input_result_seb, input_result_shuming, input_result_yopo,
        input_result_yuheng, input_result_weisheng, input_result_ka, input_result_russ,
        input_result_yj, input_result_leo, input_result_kc,
        input_result_francis, input_result_tushit, input_result_pinshun
    ]

    return return_sum, return_string, list_results
