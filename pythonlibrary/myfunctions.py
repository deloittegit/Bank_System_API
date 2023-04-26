import pandas as pd 
def readandparse_csv(x):
    df = pd.read_csv(x)
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    df['LastUpdatedTime'] = pd.Timestamp('now')
    listofobjects = []
    for index, rows in df.iterrows():
        listofobjects.append(rows)
    return listofobjects