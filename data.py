import dis
import re
from database.CRUD import CRUD
import datetime as dt
import pandas as pd
import numpy as np
import random

crud = CRUD()

def get_send_token_data(ticker, schema, user_start, user_end, n):
    sql = " SELECT (sender, receiver, token, tx_timestamp) FROM {schema}.{table} JOIN {schema}.token ON {table}.token=token.name JOIN {schema}.collection ON token.collection=collection.id WHERE collection.collection_name='{ticker}' AND tx_timestamp>='{user_start}' AND tx_timestamp<='{user_end}' LIMIT {n}".format(schema=schema,table='send_token', ticker=ticker, user_start=user_start, user_end=user_end, n=n)
    return crud.get_token_df(sql)

def get_send_coin_data(ticker, schema, user_start, user_end, n):
    sql = " SELECT (sender, receiver, amount, tx_timestamp) FROM {schema}.{table} WHERE coin='{ticker}' AND tx_timestamp>='{user_start}' AND tx_timestamp<='{user_end}' ORDER BY amount DESC LIMIT {n}".format(schema=schema,table='send_coin', ticker=ticker, user_start=user_start, user_end=user_end, n=n)
    return crud.get_coin_df(sql)

def get_date_range(ticker, schema, isToken=True):
    if isToken:
        minsql = "SELECT MIN(tx_timestamp) FROM {schema}.{table} JOIN {schema}.token ON {table}.token=token.name JOIN {schema}.collection ON token.collection=collection.id WHERE collection.collection_name='{ticker}'".format(schema=schema, table="send_token", ticker=ticker)
        maxsql = "SELECT MAX(tx_timestamp) FROM {schema}.{table} JOIN {schema}.token ON {table}.token=token.name JOIN {schema}.collection ON token.collection=collection.id WHERE collection.collection_name='{ticker}'".format(schema=schema, table="send_token", ticker=ticker)
    
    else:
        minsql = "SELECT MIN(tx_timestamp) from {schema}.{table} WHERE coin='{ticker}'".format(schema=schema, table="send_coin", ticker=ticker)
        maxsql = "SELECT MAX(tx_timestamp) from {schema}.{table} WHERE coin='{ticker}'".format(schema=schema, table="send_coin", ticker=ticker)

    min_date = crud.execute_sql(minsql)[0][0].date()
    max_date = crud.execute_sql(maxsql)[0][0].date()

    return min_date, max_date

def transaction_analysis(ticker, schema):
    token_sql = "SELECT (tx_timestamp) FROM {schema}.{table} JOIN {schema}.token ON {table}.token=token.name JOIN {schema}.collection ON token.collection=collection.id WHERE collection.collection_name='{ticker}'".format(schema=schema, table='send_token', ticker=ticker)
    coin_sql = "SELECT (tx_timestamp) FROM {schema}.{table} JOIN {schema}.coin ON {table}.coin=coin.coin_type WHERE coin.coin_type='{ticker}'".format(schema=schema, table='send_coin', ticker='APT') 

    token_data = crud.execute_sql(token_sql)
    coin_data = crud.execute_sql(coin_sql)
    dict_temp = {}

    for i in token_data:
        if str(i[0])[:10] in dict_temp.keys():
            dict_temp[str(i[0])[:10]][ticker] += 1
        else:
            dict_temp[str(i[0])[:10]] = {}
            dict_temp[str(i[0])[:10]][ticker] = 1
            dict_temp[str(i[0])[:10]]['$APT'] = 0

    for i in coin_data:
        if str(i[0])[:10] in dict_temp.keys():
            dict_temp[str(i[0])[:10]]['$APT'] += 1
        else:
            dict_temp[str(i[0])[:10]] = {}
            dict_temp[str(i[0])[:10]]['$APT'] = 1
            if ticker not in dict_temp[str(i[0])[:10]].keys():
                dict_temp[str(i[0])[:10]][ticker] = 0
    
    dict_new = {
            'day': [],
            'transaction': [],
            'type': []
            }

    # REVISED NEEDED
    int_list = range(0, 15)
    for key in dict_temp.keys():
        dict_new['day'].append(key)
        dict_new['transaction'].append(dict_temp[key][ticker])
        dict_new['type'].append(ticker)
        dict_new['day'].append(key)
        dict_new['transaction'].append(dict_temp[key]['$APT'])
        dict_new['type'].append('$APT')
        dict_new['day'].append(key)
        dict_new['transaction'].append(random.choice(int_list))
        dict_new['type'].append('Other NFTs')
    
    df = pd.DataFrame(dict_new)

    return df

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)

def get_dummy_discord_chat():
    d1 = dt.datetime.strptime('10/14/2022', '%m/%d/%Y')
    d2 = dt.datetime.strptime('2/2/2023', '%m/%d/%Y')
    dict_new = {
            'day': [],
            'chat': [],
            'type': []
            }
    for i in daterange(d1, d2):
        dict_new['day'].append(i)
        dict_new['chat'].append(random.uniform(300,600))
        dict_new['type'].append('Genies')
        dict_new['day'].append(i)
        dict_new['chat'].append(random.uniform(200,500))
        dict_new['type'].append('Others')
        
    
    df = pd.DataFrame(dict_new)

    return df

def get_common_users(ticker, schema):
    discord_server_list = ['Aptos Monkeys', 'MAVERIK', 'Aptomingos', 'Pontem Dark Ages', 'The Things', 'Spooks', 'Kreaches']
    discord_server_list = list(set(discord_server_list) - set([ticker]))
    sql = "select member from {schema}.server_member where server='{server}'".format(schema=schema,server=ticker)
    member_list = crud.execute_sql(sql)

    common_dict = {
        'server': [],
        'percent': []
    }

    for server in discord_server_list:
        # sql = "select member from {schema}.server_member where server='{server}'".format(schema=schema,server=server)
        # other_member_list = crud.execute_sql(sql)
        # percent = ((len(set(other_member_list)) - len(set(other_member_list) - set(member_list)))/len(set(other_member_list))) * 100
        percent = random.uniform(30, 100) 
        common_dict['server'].append(server)
        common_dict['percent'].append(percent)
    
    df = pd.DataFrame(common_dict) 

    return df

