from informationgain import find_split, split
import pandas as pd

class random_tree():
    """
    Grows a single, fully-gown decision tree on data in df.
    Splits are performed on information gain.
    """

    def __init__(self, samplecols='sqrt', verbose=False):

        self.samplecols=samplecols
        self.verbose = verbose

        self.left = None
        self.right = None
        self.split_col = None
        self.istrained = False

    def __str__(self):
        s = f'id: {id(self)},\n'
        if self.istrained:
            s += f'mode_class: {self.mode_class[0]}, with prior {self.mode_prior:.2f},\n'
        s += f'has left: {self.left is not None}, has right: {self.right is not None}.\n'
        return s

    def train(self, df, gt_col):

        self.istrained=True
        self.mode_class = df[gt_col].mode()
        self.mode_prior = df[gt_col].value_counts()[0]/len(df)

        #import pudb; pudb.set_trace()

        if df[gt_col].nunique() == 1: return # pure leaf, i.e., all samples of the same class

        self.split_col, self.split_val, _ = find_split(df, gt_col=gt_col, samplecols=self.samplecols, samplevals='all', verbose=self.verbose)
        if self.split_col is None:
            if self.verbose:
                # this is opposed to the sklearn implementation;
                # there it says, if no split within selected cols is found, search continues
                # over remaining columns. See documentaion: `max_features`
                print(f'Could not find a split; although leaf is not pure: {df[gt_col].value_counts()}')

            self.mode_class = df[gt_col].mode()
            return

        df_low, df_high = split(df, self.split_col, self.split_val)
        assert len(df_low) > 0, f'low of len 0'
        assert len(df_high) > 0, f'high of len 0'

        self.left = random_tree().train(df=df_low, gt_col=gt_col)
        self.right = random_tree().train(df=df_high, gt_col=gt_col)

    def predict(self, sample: pd.Series):

        assert self.istrained, f'Tree not trained, thus can not make a prediction'

        if self.left is None: # already in a leaf
            return self.mode_class[0]
        if sample[self.split_col] <= self.split_val:
            return self.left.predict(sample)
        return self.right.predict(sample)

if __name__ == '__main__':

    df = pd.DataFrame(
        [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        ],
        columns=['gt', 'x1', 'x2'])


    r_tree = random_tree()
    r_tree.train(df, gt_col='gt')
    print(r_tree)
