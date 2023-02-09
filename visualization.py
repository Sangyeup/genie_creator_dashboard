import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from database.CRUD import CRUD
import plotly.graph_objects as go
import urllib, json
import plotly.express as px
from ui_utils import revise_pyvis_html
import random
import streamlit as st

SCHEMA = 'dummy_2'

crud = CRUD()
    
def genie_registration(ticker):
    genie_member_count = crud.execute_sql("SELECT COUNT(*) FROM {schema}.server_member WHERE server='{ticker}'".format(schema=SCHEMA,ticker=ticker))
    discord_member_count = crud.execute_sql("SELECT MEMBERS FROM {schema}.discord_server WHERE server='{ticker}'".format(schema=SCHEMA,ticker=ticker))
    fig = go.Figure()
    value = (genie_member_count[0][0] / int(discord_member_count[0][0])) * 100
    fig.add_trace(go.Indicator(
        value = value,
        gauge = {'axis': {'range': [0, 100], 'visible': False}, 
                'bar': {'color': '#66FCF1'},
                'bordercolor': "lavender",
                    },
        domain = {'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Genie Registration (%)", 'font': {'size': 22}},
            'mode' : "number+gauge"}]
                             }},
        height=300, width=300)

    return fig

def discord_member(ticker):
    fig = go.Figure()
    discord_member_count = crud.execute_sql("SELECT MEMBERS FROM {schema}.discord_server WHERE server='{ticker}'".format(schema=SCHEMA,ticker=ticker))
    fig.add_trace(go.Indicator(
        value = discord_member_count[0][0],
        gauge = {'axis': {'range': [0, 50000], 'visible': False}, 
                'bar': {'color': "#5200ff"},
                'bordercolor': "lavender"
                    },
        domain = {'x': [0, 1], 'y': [0, 1]}))            

    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Discord Members", 'font': {'size': 22}},
            'mode' : "number+gauge"}]
                             }},
        height=300, width=300)

    return fig

def discord_transactions(ticker):
    fig = go.Figure()
    transaction_count = crud.execute_sql("select count(*) from {schema}.send_token where discord='{ticker}'".format(schema=SCHEMA,ticker=ticker))
    fig.add_trace(go.Indicator(
        value = transaction_count[0][0],
        gauge = {'axis': {'range': [0, 3000], 'visible': False}, 
                'bar': {'color': "#5200ff"},
                'bordercolor': "lavender"
                    },
        domain = {'x': [0, 1], 'y': [0, 1]}))             

    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Discord Transactions", 'font': {'size': 22}},
            'mode' : "number+gauge"}]
                             }},
        height=300, width=300)

    return fig

# REVISE NEEDED
def APT_transactions(ticker):
    fig = go.Figure()
    volume = random.uniform(1000, 3000)
    fig.add_trace(go.Indicator(
        value = volume,
        gauge = {'axis': {'range': [0, 5000], 'visible': False}, 
                'bar': {'color': '#66FCF1'},
                'bordercolor': "lavender"
                    },
        domain = {'x': [0, 1], 'y': [0, 1]})) 

    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': "Aptos Volume ($APT)", 'font': {'size': 22}},
            'mode' : "number+gauge"}]
                             }},
        height=300, width=300)

    return fig



def discord_chat_bar(df):
    color = {
        'Genies': '#66FCF1',
        'Others': '#5200ff',
        }
    fig = px.bar(df, x='day', y ='chat',
                 color_discrete_map=color,
                color='type', height=350, width=600,
                labels={'day':'', 'chat':''})
    fig.update_layout(title='Discord Chat Activity')
    return fig


def discord_transaction_bar(df, ticker):
    color = {
        'Other NFTs': 'pink',
        ticker: '#66FCF1',
        '$APT': '#5200ff'
        }
    fig = px.bar(df, x='day', y ='transaction',
                 color_discrete_map=color,
                color='type', height=350, width=600,
                labels={'day':'', 'transaction':''})
    fig.update_layout(title='Daily Transaction Count')
    return fig

def common_user_bar(df):
    fig = px.bar(df, x='server', y='percent',
            height=350, width=600,
            color_discrete_sequence=['#66FCF1'],
            labels={'server': '', 'percent': 'Percent (%)'})
    fig.update_layout(title='Common Users',uniformtext_minsize=4, uniformtext_mode='hide', xaxis={'categoryorder':'total descending'})
    
    return fig

def discord_chat_ranking():
    chat = []
    for i in range(10):
        chat.append(int(random.uniform(300, 1000)))
    chat.sort()

    fig = go.Figure(go.Bar(
            x=chat,
            y=['LYVBWQ#5788', 'JCSVYJ#1294', 'ZUGGOL#4281', 'DNMUS#5755', 'FHKUXJ#9924', 'DTHBIT#7173', 'PKLRRD#3544', 'JWGMJO#1145', 'VHASKA#0827', 'AXJKSC#7009'],
            orientation='h',
            marker = {'color':'#5200ff'}
            ))
    fig.update_layout(title='Discord Chat Ranking',height=350, width=600)
    return fig

def tokenGraph(df, ticker):
    with st.spinner("Generating graph, please wait..."):
        G = nx.from_pandas_edgelist(df, source='sender', target='receiver', edge_attr='token', create_using=nx.MultiDiGraph())
        edge_info=nx.get_edge_attributes(G,'token')

        # Make Discord_id dict (Need optimization)
        discord_id = {}
        for wallet in G.nodes().keys():
            sql = " SELECT {colum} FROM {schema}.{table} WHERE address='{address}'".format(schema=SCHEMA,table='wallet',colum='discord_id',address=wallet)
            discord_id[wallet] = crud.execute_sql(sql)[0][0]


        # Normlization for node size
        node_size = {key: value ** 2 for key, value in dict(G.degree()).items()}


        # Color variation
        flow_dict = {}
        for i in G.nodes():
            flow_dict[i] = 0
        for edge in G.edges():
            flow_dict[edge[0]] += 1
            flow_dict[edge[1]] -= 1

        color_dict = {}
        for i in G.nodes():
            if flow_dict[i] > 2:
                color_dict[i] = '#66FCF1'
            elif flow_dict[i] >= 0:
                color_dict[i] = '#96AAE3' 
            elif flow_dict[i] > -2:
                color_dict[i] = '#C657D5'
            else:
                color_dict[i] = '#f705c7'

        #Setting up size attribute
        nx.set_node_attributes(G, node_size, 'size')
        nx.set_node_attributes(G, discord_id, 'title')
        nx.set_edge_attributes(G, dict(edge_info), 'title')
        # nx.set_edge_attributes(G, 0, 'weight')
        nx.set_node_attributes(G, color_dict, 'color')
        nx.set_edge_attributes(G, 'white', 'color')
        # nx.set_edge_attributes(G,'gray','color')

        # Initiate PyVis network object
        token_net = Network(height='700px', width=1270, bgcolor='#111111', font_color='#10000000', directed=True, neighborhood_highlight=True)
        # Take Networkx graph and translate it to a PyVis graph format
        token_net.from_nx(G)

        # Generate network with specific layout settings
        token_net.repulsion(node_distance=500, central_gravity=0.2, spring_length=100, spring_strength=0.01, damping=0.95)

        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            token_net.save_graph(f'token/{ticker}/pyvis_graph.html')
            revise_pyvis_html(f'token/{ticker}/pyvis_graph.html')
            HtmlFile = open(f'token/{ticker}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
        except:
            path = '/html_files'
            token_net.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=600)

def coinGraph(df, ticker):
    with st.spinner("Generating graph, please wait..."):
        spinner = st.spinner("Generating graph, please wait...")
        G = nx.from_pandas_edgelist(df, source='sender', target=' receiver', edge_attr=' amount', create_using=nx.MultiDiGraph())
        edge_info=nx.get_edge_attributes(G, ' amount')

        # Make Discord_id dict (Need optimization)
        discord_id = {}
        for wallet in G.nodes().keys():
            sql = " SELECT {colum} FROM {schema}.{table} WHERE address='{address}'".format(schema=SCHEMA,table='wallet',colum='discord_id',address=wallet)
            discord_id[wallet] = crud.execute_sql(sql)[0][0]


        # Normlization for node size
        node_size = {key: value *10 for key, value in dict(G.degree()).items()}

        # Color variation
        flow_dict = {}
        for i in G.nodes():
            flow_dict[i] = 0
        for edge in G.edges():
            e=list(edge)
            e.append(0)
            e=tuple(e)
            flow_dict[edge[0]] += edge_info[e]
            flow_dict[edge[1]] -= edge_info[e]

        color_dict = {}
        for i in G.nodes():
            if flow_dict[i] > 20000:
                color_dict[i] = '#66FCF1'
            elif flow_dict[i] >= 0:
                color_dict[i] = '#96AAE3' 
            elif flow_dict[i] > -20000:
                color_dict[i] = '#C657D5'
            else:
                color_dict[i] = '#f705c7'

        #Setting up size attribute
        nx.set_node_attributes(G, node_size, 'size')
        nx.set_node_attributes(G, discord_id, 'title')
        nx.set_edge_attributes(G, dict(edge_info), 'title')
        #nx.set_edge_attributes(G, dict(edge_info), 'weight')
        nx.set_node_attributes(G, color_dict, 'color')
        nx.set_edge_attributes(G, 'white', 'color')
        # nx.set_edge_attributes(G,'gray','color')

        # Initiate PyVis network object
        token_net = Network(height='700px', width=1270, bgcolor='#111111', font_color='#10000000', directed=True, neighborhood_highlight=True)

        # Take Networkx graph and translate it to a PyVis graph format
        token_net.from_nx(G)

        # Generate network with specific layout settings
        token_net.repulsion(node_distance=500, central_gravity=0.2, spring_length=100, spring_strength=0.01, damping=0.95)

        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            token_net.save_graph(f'coin/{ticker}/pyvis_graph.html')
            revise_pyvis_html(f'coin/{ticker}/pyvis_graph.html')
            HtmlFile = open(f'coin/{ticker}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
        except:
            path = '/html_files'
            token_net.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=700)

def temp_sankey():
    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    fig = go.Figure(data=[go.Sankey(
        valueformat = ".0f",
        valuesuffix = "TWh",
        node = dict(
        pad = 15,
        thickness = 15,
        line = dict(color = "black", width = 0.5),
        label =  data['data'][0]['node']['label'],
        color =  data['data'][0]['node']['color']
        ),
        link = dict(
        source =  data['data'][0]['link']['source'],
        target =  data['data'][0]['link']['target'],
        value =  data['data'][0]['link']['value'],
          label =  data['data'][0]['link']['label']
      ))])

    fig.update_layout(
        hovermode = 'x',
        width=1270,
        font=dict(size = 10, color = 'white'),
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    return fig
