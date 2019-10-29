import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def get_commenters(html, pers, ordr) :
    names = list()
    soup = BeautifulSoup(open(html), 'html.parser')
    tags = soup.find_all('a', class_ = 'UFICommentActorName')
    for item in tags :
        name = item.text
        names.append(name)
    person = [pers] * len(names)
    order = [ordr] * len(names)
    df = pd.DataFrame({'From': person, 'To': names, 'Order': order})
    df = df.drop_duplicates('To', keep = 'first')
    return df

def get_likers(html, pers, ordr) :
    names = list()
    soup = BeautifulSoup(open(html), 'html.parser')
    tags = soup.find_all('a')
    for item in tags :
        name = item.text
        names.append(name)
    person = [pers] * len(names)
    order = [ordr] * len(names)
    df = pd.DataFrame({'From': person, 'To': names, 'Order': order})
    df = df.drop_duplicates('To', keep = 'first')
    df = df[~df['To'].str.isnumeric()]
    df = df.replace('', float('nan'))
    x = np.where(pd.isnull(df))
    df = df.iloc[(int(x[0]) + 1):, :]
    return df

def get_sharers(html, pers, ordr) :
    names = list()
    soup = BeautifulSoup(open(html), 'html.parser')
    tags = soup.find_all('a', {'data-ft':'{"tn":"l"}'})
    for item in tags :
        name = item.text
        names.append(name)
    person = [pers] * len(names)
    order = [ordr] * len(names)
    df = pd.DataFrame({'From': person, 'To': names, 'Order': order})
    df = df.drop_duplicates('To', keep = 'first')
    return df

def is_in(df1, df2, link) :
    connectors = df1[df1['To'].isin(df2['To'])]
    connectors['Link'] = [link] * len(connectors)
    return connectors

def give_rank(df1, df2) :
    vals = {'Share': 3, 'Comment': 2, 'Like': 1}
    merged = df1.merge(df2, on = 'To')
    merged['Value'] = merged['Order_y'].map(vals)
    merged = merged.sort_values(by = 'Value', ascending = False)
    if len(merged[merged['Value'] > 1]) > 10 :
        merged = merged[merged['Value'] > 1]
    return merged

def survey_to_nx(df) :
    df_surveys = pd.read_csv(df).rename(columns = {'Name (FB)': 'To'})
    df_surveys['From'] = ['Messenger'] * len(df_surveys)
    df_surveys['Order'] = ['Survey'] * len(df_surveys)
    df_surveys = df_surveys[['From', 'To', 'Order', 'Date']]
    return df_surveys
