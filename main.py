from turtle import color
import streamlit as st
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network

import plotly.graph_objects as go
import datetime as dt
import requests
import time

from data import get_send_coin_data, get_send_token_data, get_date_range, transaction_analysis, get_dummy_discord_chat
from visualization import discord_transactions, tokenGraph, genie_registration, coinGraph, temp_sankey, discord_member, APT_transactions, discord_transaction_bar, discord_chat_bar
from ui_utils import add_bg_from_local, set_page_container_style

TICKER = 'Bruh Bear' # ['Bruh Bear', 'MAVERIC', 'AptosMonkeys']
SERVER = 'Bruh Bears'
isToken = True
SCHEMA = 'dummy_2'

st.set_page_config(layout="wide", page_title="Genie Creator Dashboard")
set_page_container_style()
#add_bg_from_local('home.png') 

TICKER = st.selectbox('',
               options=('Bruh Bear', 'MAVERIK', 'AptosMonkeys'),
               index=0)

if TICKER == 'Bruh Bear':
    SERVER = 'Bruh Bears'
elif TICKER == 'MAVERIK':
    SERVER = 'MAVERIK'
elif TICKER == 'AptosMonkeys':
    SERVER = 'Aptos Monkeys'

st.title('Genie Creator Dashboard')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.plotly_chart(genie_registration(SERVER))

with col2:
    st.plotly_chart(discord_member(SERVER))

with col3:
    st.plotly_chart(APT_transactions(SERVER))

with col4:
    st.plotly_chart(discord_transactions(SERVER))


bar_col1, bar_col2 = st.columns(2)

with bar_col1:
    st.plotly_chart(discord_transaction_bar(transaction_analysis(ticker=TICKER, schema=SCHEMA), TICKER))

with bar_col2:
    st.plotly_chart(discord_chat_bar(get_dummy_discord_chat()))




if 'start_time' in st.session_state:        
    del st.session_state['start_time']
if 'end_time' in st.session_state:
    del st.session_state['end_time']
st.session_state['token'] = TICKER
st.session_state['isToken'] = isToken


min_date, max_date = get_date_range(TICKER, SCHEMA, isToken=st.session_state['isToken'])

st.header('On-chain Network Visualization')

with st.form("Choose Date range"):
    # Select date range
    st.write('Select date range (Time Zone: UTC)')
    
    user_start_date = st.date_input(f'Start date: available from {min_date}', min_date, disabled=False, min_value=dt.date(1960, 1, 1))
    user_end_date = st.date_input(f'End date: available until {max_date}', min_date + dt.timedelta(days=2), disabled=False, max_value=dt.date(2023, 12, 31))
    date_submitted = st.form_submit_button("Submit")

    if date_submitted:
        if user_end_date < user_start_date:
            st.warning('End date must fall after start date.')
        elif user_start_date < min_date:
            st.warning(f'Start date must be after {min_date}.')
        elif user_end_date > max_date:
            st.warning(f'End date must be before {max_date}.')

        st.session_state['start_time'] = user_start_date
        st.session_state['end_time'] = user_end_date


if 'start_time' in st.session_state and st.session_state['start_time'] != None:
    token = st.session_state['token']
    user_start_time = st.session_state['start_time']
    user_end_time = st.session_state['end_time']

    st.text(f"On-chain Network of {token} from {user_start_time} to {user_end_time} (UTC)")

    min_value = 0
    max_value = 0
    
    if 'isToken' in st.session_state and st.session_state['isToken']==True:
        df = get_send_token_data(TICKER, SCHEMA, str(user_start_time), str(user_end_time), 60)
        tokenGraph(df, TICKER)

    elif 'isToken' in st.session_state and st.session_state['isToken']==False:
        df = get_send_coin_data(TICKER, SCHEMA, str(user_start_time), str(user_end_time), 60)
        coinGraph(df, TICKER)


# st.header('Related Projects')

# st.plotly_chart(temp_sankey())
    

