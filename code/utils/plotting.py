import matplotlib.pyplot as plt
import random as rd
from utils.linear_regression import *
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats
import os
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['figure.figsize'] = (12, 6) # 设置figure_size尺寸


def data_binning(x, y):
    assert len(x) == len(y)
    x_y = {}
    for i in range(len(x)):
        each_x = x[i]
        each_y = y[i]
        if each_x > 8:
            k = math.floor(math.log(each_x, 2))
            a = pow(2,k)
            b = pow(2,k+1)
            each_x = (a+b)/2
        if each_x not in x_y:
            x_y[each_x] = []
        x_y[each_x].append(each_y)
    x_ymean_error = []
    for each_x in x_y:
        _y = np.array(x_y[each_x])
        ymean = _y.mean()
        error = _y.std() / math.sqrt(len(_y))
        x_ymean_error.append([each_x, ymean, error])
    return x_ymean_error


def errorbar_plotting_util(x, y, dy):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    ecolor = 'k'
    rd.shuffle(colors)
    color = rd.sample(colors, 1)[0]
    plt.errorbar(x, y, yerr=dy, fmt='x', ecolor=ecolor, color=color, elinewidth=1, capsize=3)


def errorbar_plotting(x, y):
    data = data_binning(x, y)
    _x = [each[0] for each in data]
    _y = [each[1] for each in data]
    dy = [each[2] for each in data]
    errorbar_plotting_util(_x, _y, dy)


def get_column(matrix, col):
    return [each[col] for each in matrix]


def line_plot(x, y, slope, intercept, r2, xlabel, ylabel, filepath, filename):
    x = np.asarray(x)
    y = np.asarray(y)

    a = math.pow(10, intercept)
    b = slope

    min_x, max_x = min(x), max(x)
    x_pred = np.linspace(min_x, max_x, 1000)
    y_pred = np.asarray([a*math.pow(each_x_pred, b) for each_x_pred in x_pred])

    p_y = [a*math.pow(each_x_pred, b) for each_x_pred in x]
    y_err = y - p_y
    # now calculate the confidence intervals for new test x-series
    x_mean = np.mean(x)
    n = len(x)
    t = 2.31    # appropriate t value (where n=9, two tailed 95%)
    s_err = np.sum(np.power(y_err, 2))
    confs = t * np.sqrt((s_err / (n - 2)) * (1.0 / n + (np.power((x_pred - x_mean), 2) /
                                ((np.sum(np.power(x, 2))) - n * (np.power(x_mean, 2))))))
    upper = y_pred + abs(confs)
    lower = y_pred - abs(confs)

    # colors = ['b', 'g', 'r', 'c', 'm', 'y']
    # while 1:
    #     rd.shuffle(colors)
    #     color1 = rd.sample(colors, 1)[0]
    #     color2 = rd.sample(colors, 1)[0]
    #     if color1 == 'b':
    #         continue
    #     if color1 == 'r':
    #         continue
    #     if color1 != color2:
    #         break

    plt.scatter(x, y, s=15, c='black', alpha=0.4)
    plt.plot(x_pred, y_pred, linewidth=3, c='red')
    plt.fill_between(x_pred, lower, upper, color='blue', alpha=0.4)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    y_axis = max(y)/2
    x_axis = min(x)
    plt.text(x_axis, y_axis, r'$\alpha={},R^2={}$'.format(np.round(slope,3), np.round(r2,3)),
             fontsize=14)
    pdf = PdfPages(os.path.join(filepath, filename+'.pdf'))
    pdf.savefig(bbox_inches='tight')
    pdf.close()
    plt.close()


def curve_plot(x, y, xlabel, ylabel, filepath, filename):
    x = np.asarray(x)
    y = np.asarray(y)
    plt.plot(x, y, marker='o', alpha=0.8)
    # plt.plot(np.arange(x.min(), x.max(), 1), [1] * len(np.arange(x.min(), x.max(), 1)), alpha=0.8)
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    pdf = PdfPages(os.path.join(filepath, filename+'.pdf'))
    pdf.savefig(bbox_inches='tight')
    pdf.close()
    plt.close()


def histogram_plot(x, xlabel, filepath, filename):
    hist, bins = np.histogram(x)
    plt.hist(x, bins=bins, density=True)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel(xlabel, fontsize=18)

    pdf = PdfPages(os.path.join(filepath, filename+'.pdf'))
    pdf.savefig(bbox_inches='tight')
    pdf.close()
    plt.close()
