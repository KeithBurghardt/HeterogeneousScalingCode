from scipy import stats
import numpy as np
import math


def linear_regression(data):
    x = [math.log10(each[0]) for each in data]
    y = [math.log10(each[1]) for each in data]

    x = np.asarray(x)
    y = np.asarray(y)

    if len(x) < 6:
        slope = intercept = r_value = p_value = std_err = np.nan
    else:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        if p_value >= 0.05:
            slope = intercept = r_value = p_value = std_err = np.nan

    return float(slope), float(r_value**2), float(p_value), float(intercept), float(std_err)
