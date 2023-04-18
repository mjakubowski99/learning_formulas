import numpy as np
import pandas as pd

def make_train_test_data_files(df, target):
    classes = df[target].unique()

    msk = np.random.rand(len(df)) < 0.7
    train = df[msk].groupby(target)
    test = df[~msk].groupby(target)

    train_file = open("train.txt", "w")
    test_file = open("test.txt", "w")

    train_classes = len(classes)

    train_file.write(str(train_classes)+'\n')
    test_file.write(str(train_classes)+'\n')

    for c in classes:
        train_grouped = train.get_group(c)
        
        rows_count = len(train_grouped)
        cols_count = len(train_grouped.columns)-1

        train_grouped = train_grouped.values.tolist()

        train_file.write(str(rows_count)+' '+str(cols_count)+'\n')
        for x in train_grouped:
            train_file.write(' '.join(str(a) for a in x[:-1])+'\n')

        test_grouped = test.get_group(c)

        rows_count = len(test_grouped)
        cols_count = len(test_grouped.columns)-1

        test_grouped = test_grouped.values.tolist()

        test_file.write(str(rows_count)+' '+str(cols_count)+'\n')
        for x in test_grouped:
            test_file.write(' '.join(str(a) for a in x[:-1])+'\n')