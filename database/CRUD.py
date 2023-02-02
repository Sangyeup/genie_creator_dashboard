from database.database import Databases
import pandas as pd
from io import StringIO

class CRUD(Databases):
    def insertDB(self,schema,table,colum,data):
        sql = " INSERT INTO {schema}.{table}({colum}) VALUES ('{data}') ;".format(schema=schema,table=table,colum=colum,data=data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 

    def insertDB_2(self,schema,table,colum_1,colum_2,data_1,data_2):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}) VALUES ('{data_1}', '{data_2}') ;".format(schema=schema,table=table,colum_1=colum_1,colum_2=colum_2,data_1=data_1,data_2=data_2)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 

    def insertDB_3(self,schema,table,colum_1,colum_2,colum_3,data_1,data_2,data_3):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}, {colum_3}) VALUES ('{data_1}', '{data_2}', '{data_3}') ;".format(schema=schema,table=table,colum_1=colum_1,colum_2=colum_2,colum_3=colum_3,data_1=data_1,data_2=data_2,data_3=data_3)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 
    
    def insertDB_4(self,schema,table,colum_1,colum_2,colum_3,colum_4,data_1,data_2,data_3,data_4):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}, {colum_3}, {colum_4}) VALUES ('{data_1}', '{data_2}', '{data_3}', '{data_4}') ;".format(schema=schema,table=table,colum_1=colum_1,colum_2=colum_2,colum_3=colum_3,colum_4=colum_4,data_1=data_1,data_2=data_2,data_3=data_3,data_4=data_4)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 

    def insertDB_5(self,schema,table,colum_1,colum_2,colum_3,colum_4,colum_5,data_1,data_2,data_3,data_4,data_5):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}, {colum_3}, {colum_4}, {colum_5}) VALUES ('{data_1}', '{data_2}', '{data_3}', '{data_4}', '{data_5}') ;".format(schema=schema,table=table,colum_1=colum_1,colum_2=colum_2,colum_3=colum_3,colum_4=colum_4,colum_5=colum_5,data_1=data_1,data_2=data_2,data_3=data_3,data_4=data_4,data_5=data_5)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 

    def insertDB_6(self,schema,table,colum_1,colum_2,colum_3,colum_4,colum_5,colum_6,data_1,data_2,data_3,data_4,data_5,data_6):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}, {colum_3}, {colum_4}, {colum_5}, {colum_6}) VALUES ('{data_1}', '{data_2}', '{data_3}', '{data_4}', '{data_5}', '{data_6}') ;".format(schema=schema,table=table,colum_1=colum_1,colum_2=colum_2,colum_3=colum_3,colum_4=colum_4,colum_5=colum_5,colum_6=colum_6,data_1=data_1,data_2=data_2,data_3=data_3,data_4=data_4,data_5=data_5,data_6=data_6)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 

    def insertDB_7(self,schema,table,colum_1,colum_2,colum_3,colum_4,colum_5,colum_6,colum_7,data_1,data_2,data_3,data_4,data_5,data_6,data_7):
        sql = " INSERT INTO {schema}.{table}({colum_1}, {colum_2}, {colum_3}, {colum_4}, {colum_5}, {colum_6}, {colum_7}) VALUES ('{data_1}', '{data_2}', '{data_3}', '{data_4}', '{data_5}', '{data_6}', '{data_7}') ;".format(schema=schema,table=table,colum_1=colum_1,colum_2=colum_2,colum_3=colum_3,colum_4=colum_4,colum_5=colum_5,colum_6=colum_6,colum_7=colum_7,data_1=data_1,data_2=data_2,data_3=data_3,data_4=data_4,data_5=data_5,data_6=data_6,data_7=data_7)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 
    
    def readDB(self,schema,table,colum):
        sql = " SELECT {colum} from {schema}.{table}".format(colum=colum,schema=schema,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def updateDB(self,schema,table,colum,value,condition):
        sql = " UPDATE {schema}.{table} SET {colum}='{value}' WHERE {colum}='{condition}' ".format(schema=schema
        , table=table , colum=colum ,value=value,condition=condition )
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)

    def deleteDB(self,schema,table,condition):
        sql = " delete from {schema}.{table} where {condition} ; ".format(schema=schema,table=table,
        condition=condition)
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print( "delete DB err", e)

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
            print(result)

        return result

    def get_token_df(self, sql):
        try:
            self.cursor.execute(sql)
            lines = self.cursor.fetchall()
        except Exception as e :
            lines = (" read DB err",e)

        df = 'sender,receiver,token,tx_timestamp\n'

        for line in lines:
            line = str(line)
            line = line.lstrip('(\'(').rstrip(')\',)').replace('"', '')
            df += line + '\n'

        df = StringIO(df)
        df = pd.read_csv(df, sep=",")

        return df

    def get_coin_df(self, sql):
        try:
            self.cursor.execute(sql)
            lines = self.cursor.fetchall()
        except Exception as e :
            lines = (" read DB err",e)

        df = 'sender, receiver, amount, tx_timestamp\n'

        for line in lines:
            line = str(line)
            line = line.lstrip('(\'(').rstrip(')\',)').replace('"', '')
            df += line + '\n'

        df = StringIO(df)
        df = pd.read_csv(df, sep=",")

        return df

if __name__ == "__main__":
    db = CRUD()
    db.insertDB(schema='testschema',table='test_tb',colum='from_address',data='유동적변경')
    print(db.readDB(schema='testschema',table='test_tb',colum='from_address'))
    db.updateDB(schema='testschema',table='test_tb',colum='from_address', value='와우',condition='유동적변경')
    print(db.readDB(schema='testschema',table='test_tb',colum='from_address'))
    db.deleteDB(schema='testschema',table='test_tb',condition ="from_address != 'd'")