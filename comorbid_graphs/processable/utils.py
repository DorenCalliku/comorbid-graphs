import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import groupby

def intersect_series(series):
    cleaned = [i for i in series if i is not None]
    if cleaned == []:
        return []
    return set.intersection(*cleaned)


def union_series(series):
    cleaned = [i for i in series if i is not None]
    if cleaned == []:
        return []
    return set.union(*cleaned)


def pivot_group(data_list, pivot="ancestor", attribute="name"):
    return {
        i: set([j[attribute] for j in gr])
        for i, gr in groupby(data_list, lambda x: x[pivot])
    }

def get_shared_annotations(df):
    # per node shared labels
    df["all"] = df.apply(union_series, axis=1)
    df["common"] = df.iloc[:, :-1].apply(intersect_series, axis=1)

    # per analysis category
    all = {}
    for name, values in df.iteritems():
        all[name] = union_series(values)
    all["node"] = "all"
    shared = {}
    for name, values in df.iteritems():
        shared[name] = intersect_series(values)
    shared["node"] = "common"
    df = df.append(pd.DataFrame([all,shared]).set_index("node"))
    return df

def heatmap_plot_df(numerical_df):
    # optional: resize images from now on
    plt.rcParams["figure.figsize"] = (16, 12)

    # numerical data only
    sns.heatmap(numerical_df)
    plt.show()
