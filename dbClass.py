from time import sleep

import pandas as pd
import json
import os
import sys
import pymysql
from pymysql import Error

'''
for remote access - add HOSTNAME=localhost to env  
ssh -L 8676:127.0.0.1:3306 ialerner@cse191.ucsd.edu
'''
class dbClass:

    def __init__(self, type="JSON"):
        self.outType = type
        # AMAZON CLOUD - AWS DB Cluster
        print("connect to main DB")
        self.servername = "127.0.0.1"
        self.username = "root"
        self.password = "iotiot"
        self.dbname = "cse191"
        self.port = 3306

        if os.getenv('HOSTNAME') == "localpc":
            print("connect local ssh tunnel")
            self.port = 8676

        self.reconnect()

    def check_conn(self):

        # test connection
        try:
            if self.db.cursor().execute("SELECT now()") == 0:
                return self.reconnect()
            else:
                print("DB connection OK\n")
                return True
        except:
            print("Unexpected exception occurred: ", sys.exc_info())
            return self.reconnect()

    def reconnect(self):

        # try to connect 5 times
        retry = 5
        while retry > 0:
            try:
                print("connecting to DB...")
                self.db = pymysql.connect(
                    host=self.servername,
                    user=self.username,
                    password=self.password,
                    database=self.dbname,
                    port=self.port
                )
                retry = 0
                return True
            except:
                print("Unexpected exception occurred: ", sys.exc_info())
                retry -= 1
                if retry > 0:
                    print("retry\n")
                    sleep(2)
                else:
                    exit(-1)

        print("Success\n")

    def loadStudents(self):
        if self.check_conn():
            stu_df = pd.DataFrame
            sqlStr = "SELECT * FROM cse191.students ORDER BY groupnumber"
            print(sqlStr)
            cursor = self.db.cursor()
            result = None
            try:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                print(result)
                stu_df = pd.DataFrame.from_dict(result) 
                stu_df.columns=["id","name","email","groupnumber","groupname"]
                print(stu_df)
            except Error as e:
                print(f"The error '{e}' occurred")

            return stu_df