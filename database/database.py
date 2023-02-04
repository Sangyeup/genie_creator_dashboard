import psycopg2
import streamlit as st

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(**st.secrets["postgres"])
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()

