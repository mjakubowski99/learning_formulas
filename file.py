import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
import os

def make_train_test_data_files(df, target, train_file="train.txt", test_file="test.txt"):
    classes = df[target].unique()
    classes.sort()

    binarizers = {}

    for column in df.columns:
        if column == target:
            continue
        binarizers[column] = LabelBinarizer()
        binarizers[column].fit(df[column])

    msk = np.random.rand(len(df)) < 0.7
    train = df[msk].groupby(target)
    test = df[~msk].groupby(target)

    os.remove(train_file)
    os.remove(test_file)

    train_file = open(train_file, "a")
    test_file = open(test_file, "a")

    train_classes = len(classes)

    train_file.write(str(train_classes)+'\n')
    test_file.write(str(train_classes)+'\n')

    for c in classes:
        train_group = get_group(train, c)
        write_description_lines(train_file, train_group, binarizers, target)
        write_lines(train_file, binarizers, train_group, target)

        test_group = get_group(test, c)
        write_description_lines(test_file, test_group, binarizers, target)
        write_lines(test_file, binarizers, test_group, target)

    train_file.close()
    test_file.close()

def get_group(df, decision_class):
    if decision_class in df.groups:
        return df.get_group(decision_class)
    else:
        return pd.DataFrame({})

def write_description_lines(file, df, binarizers, target):
    rows_count = len(df)
    if rows_count == 0:
        cols_count = 0
    else:
        cols_count = len(binarize(binarizers, df.iloc[0], df.columns, target).split(' '))
    file.write(str(rows_count)+' '+str(cols_count)+'\n')

def write_lines(file, binarizers, df, target):
    result = None 
    for column in df.columns:
        if column == target:
            continue 
        
        if result is None:
            result = binarizers[column].transform(df[column])
        else:
            result = np.concatenate((result, binarizers[column].transform(df[column])), axis=1)
    np.savetxt(file, result, fmt='%d')
        
def binarize(binarizers, row, columns, target):
    line = ''
    for column in columns:
        if column == target:
            continue
        result = binarizers[column].transform([row[column]])[0]
        line += ' '.join(str(x) for x in result)
        line += ' '
    return line[:-1]

