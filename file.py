import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
import os

def make_train_test_data_files(df, target, train_file="train.txt", test_file="test.txt"):
    if os.path.isfile(train_file):
        os.remove(train_file)
    if os.path.isfile(test_file):
        os.remove(test_file)

    train_file = open(train_file, "a")
    test_file = open(test_file, "a")

    msk = np.random.rand(len(df)) < 0.7
    
    train_len = len(df[msk])
    test_len = len(df[~msk])

    train = df[msk].groupby(target)
    test = df[~msk].groupby(target)

    all_bin = True
    for column in df.columns:
        if column == target:
            continue
        if df[column].min() != 0 or df[column].max() not in [0,1]:
            all_bin = False
            break 

    classes = df[target].unique()
    classes.sort()

    if all_bin:

        train_file.write(str(len(classes))+'\n')
        test_file.write(str(len(classes))+'\n')

        for c in classes:
            train_group = get_group(train, c)
            test_group = get_group(test,c)

            line = str(len(train_group))+" "+str(len(train_group.iloc[0])-1)+'\n'
            train_file.write(line)
            np.savetxt(train_file, train_group.loc[:, train_group.columns != target].values, fmt='%d')

            line = str(len(test_group))+" "+str(len(test_group.iloc[0])-1)+'\n'
            test_file.write(line)
            np.savetxt(test_file, test_group.loc[:, test_group.columns != target].values, fmt='%d')

        return
    
    binarizers = {}

    for column in df.columns:
        if column == target:
            continue
        binarizers[column] = LabelBinarizer()
        binarizers[column].fit(df[column])

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
    all_bin = True
    for column in df.columns:
        if column == target:
            continue
        if df[column].min() != 0 or df[column].max() != 1:
            all_bin = False

    if all_bin:
        np.savetxt(file, df.values, fmt='%d')
        return
            
    result = None 
    for column in df.columns:
        if column == target:
            continue

        if result is None:
            result = binarizers[column].transform(df[column])
            continue

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

