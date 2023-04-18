
def fill_missing(df, target=None):
    rows_count = len(df)

    for column in df.columns:
        if target is not None and column == target:
            continue

        missing = df[column].isnull().sum()/rows_count
        
        if missing <= 0.1 and df[column].dtype.kind in 'biufc':
            df[column]=df[column].fillna(df[column].mean())
        if missing <= 0.1 and df[column].dtype == "object":
            df[column] = df[column].fillna("Not assigned")
        elif missing <= 0.4:
            df = df.dropna(subset=[column]) 
        else:
            df = df.drop(columns=[column])

    return df
        