from database.CRUD import CRUD
import pandas as pd
from io import StringIO

class CRUD_genie(CRUD):
    def insertDB_wallet(self,schema,table,colum,wallet):
        sql = " INSERT INTO {schema}.{table}({colum}) VALUES ('{wallet}') ;".format(schema=schema,table=table,colum=colum,wallet=wallet)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 

    def insertDB_users(self,schema,table,colum,wallet, discord_id):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}) VALUES ('{discord_id}, {wallet}') ;".format(schema=schema,table=table,colum_1=colum,wallet=wallet)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 
    
