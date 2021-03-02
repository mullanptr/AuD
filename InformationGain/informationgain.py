import math
import pandas as pd
import numpy as np
from collections import defaultdict

def single_ent(p):
    """
    Entropy of a single probability, i.e. a float \in [0|1].

    Remarks:
    - Uses log2 -> Thus units is [bits].
    - Probability of 0 returns an entropy of 0 bit.
    """
    assert 0 <= p <= 1, f'Probability must be \in [0|1] but is {p}.'
    if p == 0:
        return 0
    return p * math.log2(p)

def entropy(probs):
    """
    Entropy over a list of probabilites.
    For instance, can be used to calculate the entropy over a source.
    """
    e = np.sum([single_ent(p) for p in probs])
    return -1 * e

def get_priors(df, gt_col):
    """
    Calculates prior probabilites of classes in df,
    where column `gt_col` addresses the class column.
    """
    probs = df[gt_col].value_counts()/len(df)
    return probs

def _helper_infogain(df, gt_col, orig_len):

    weight = len(df)/orig_len
    priors = get_priors(df=df, gt_col=gt_col)
    ent = entropy(probs=priors)
    return weight * ent

def _infogain(dfs, gt_col):

    assert len(dfs) == 3
    assert len(dfs[0]) == len(dfs[1]) + len(dfs[2])

    orig_ent = _helper_infogain(df=dfs[0], gt_col=gt_col, orig_len=len(dfs[0]))
    low_ent = _helper_infogain(df=dfs[1], gt_col=gt_col, orig_len=len(dfs[0]))
    high_ent = _helper_infogain(df=dfs[2], gt_col=gt_col, orig_len=len(dfs[0]))

    return orig_ent - (low_ent + high_ent)

def _define_mumber_of_samples(method, max_samples):

    if isinstance(method, str):
        if method=='all':
            samples = max_samples
        if method=='sqrt':
            samples = int(np.sqrt(max_samples))

    assert isinstance(samples, int), f'method needs to be of type str ("all","sqrt") or a int, but is type {type(method)}'

    samples = min(samples, max_samples)
    return samples

def split(df, splitcol, splitval):
    """
    Splits a df into two dfs: (df_low, df_high).

    df_low: all rows where values in column `splitcol` are less or equal `splitval`.
    df_high: all rows where values in column `splitcol` are larger than `splitval`.
    """

    df_low = df.loc[df[splitcol] <= splitval]
    df_high = df.loc[df[splitcol] > splitval]
    return df_low, df_high

def find_split(df, gt_col, samplecols='sqrt', samplevals='sqrt', verbose=False):
    """
    Randomly searches for the best split of df on a feature column.
    Both different columns and different values within the columns are searched over,
    thus the proposed column, the propsed value and the calculated information gain
    are returned as a triplet.

    Input:
    df: pd.DataFrame
    gt_col: str
        class column; Not searched over, but required to asses split quality
    samplecols: Union(str,int,list)
        if str or int:
            Number of columns to search over.
            If `sqrt`, then sqrt of number of columns are randomly tested,
            If `all`, then all columns are tested,
            Else: Int, defining number of searchable columns
        if list:
            user-defined list of columns to test for
    samplevals: Union(str,int)
        Number of values within a colum to search over.
        If `sqrt`, then sqrt of number of values per column are randomly tested,
        If `all`, then all values in the selected columns are tested,
        Else: Int, defining number of searchable values per column.

    Return:
    (best_col, best_val, igs)
    best_col: str
        The best colum that was found to yield the best split
    best_col: str
        The best value for `best_col` that was found to yield the best split
    info_gain: dict
        dictionary with all tested columns as key and their best information gain as tuple (value_to_split_on, ig)
    """

    cols = set(df.keys()) - set((gt_col,))
    assert len(cols) == len(df.keys()) - 1
    cols = list(cols)

    if not isinstance(samplecols,list):
        # if no list of columns to test for was provided, randomly select columns to test for
        num_samplecols = _define_mumber_of_samples(method=samplecols, max_samples=len(cols))
        assert 0 < num_samplecols <= len(cols)

        samplecols = np.random.choice(cols,num_samplecols,replace=False)

    if verbose:
        print(f' Sample from cols {samplecols}')

    igs = {}

    best_col = None
    best_val = np.nan
    best_ig = -1 * np.inf

    for c in samplecols:

        # uniq vals in column df[c]
        vals = sorted(df[c].unique())[:-1]
        if len(vals) == 0:
            if verbose:
                print('      No variance for this col')
            continue

        v = _define_mumber_of_samples(method=samplevals, max_samples=len(vals))
        assert 0 < v <= len(vals)

        vals = np.random.choice(vals,v,replace=False)
        if verbose:
            print(f'     With vals: {vals}')

        for v in vals:

            df_low, df_high = split(df=df, splitcol=c, splitval=v)
            ig = _infogain([df, df_low, df_high], gt_col=gt_col)

            if c not in igs:
                # no score yet
                igs[c] = (v, ig)
            else:
                if igs[c][1] < ig:
                    #update score if a better was found
                    igs[c] = (v, ig)

            if ig > best_ig:
                best_col = c
                best_val = v
                best_ig = ig

    if verbose:
        print('Found IGS:')
        print(igs)

    return best_col, best_val, igs

if __name__ == '__main__':

    df = pd.DataFrame(
        [
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 0],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        ],
        columns=['gt','x1'])

    best_col, best_val, feature_scores = find_split(df, gt_col='gt', samplecols='sqrt', samplevals='sqrt', verbose=True)
    print(best_col, best_val)
    print(feature_scores)

